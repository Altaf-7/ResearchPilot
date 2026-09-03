import logging
import json
from typing import List, Dict, Any, Tuple
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from app.api.models import ReportSource, ResearchReport
from app.core.llm import get_llm
from app.services.agent import AgentService

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self):
        self.agent_service = AgentService()
        self.llm = get_llm()
        # Ensure the LLM supports structured output
        try:
            self.structured_llm = self.llm.with_structured_output(ResearchReport)
        except Exception as e:
            logger.error(f"Failed to bind structured output to LLM: {str(e)}")
            # Fallback or re-raise
            raise RuntimeError(f"LLM does not support structured output: {str(e)}")
            
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert research analyst. Your task is to generate a comprehensive, structured research report based on the provided evidence.

CRITICAL INSTRUCTIONS:
1. Use ONLY the provided evidence. Do not hallucinate or use outside knowledge.
2. Every claim in your detailed analysis MUST be cited using the format [ID] where ID corresponds to the source number in the evidence list.
3. The 'sources' field must contain exactly the sources you cited, mapping the ID correctly.
4. For the 'limitations' field, strictly list limitations based on missing evidence in the provided sources. Do not mention general topic ambiguity.
5. Distinguish clearly between concrete evidence and assumptions. Mention uncertainty if the evidence is weak."""),
            ("human", """Research Question: {question}

Evidence Provided:
{evidence}

Generate the structured report now.""")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def _normalize_sources(self, messages: List[BaseMessage]) -> List[ReportSource]:
        """Extracts and deduplicates sources from raw ToolMessages."""
        sources: List[ReportSource] = []
        seen_urls = set()
        
        for msg in messages:
            if isinstance(msg, ToolMessage):
                if msg.name == "web_search":
                    try:
                        results = json.loads(msg.content)
                        if isinstance(results, list):
                            for r in results:
                                url = r.get("url", "")
                                if url and url not in seen_urls:
                                    seen_urls.add(url)
                                    sources.append(ReportSource(
                                        title=r.get("title", "Web Page"),
                                        url_or_id=url,
                                        source_type="web",
                                        metadata={"snippet": r.get("snippet", "")}
                                    ))
                    except json.JSONDecodeError:
                        pass # Handle cases where DDG fails and returns raw text
                elif msg.name == "document_search":
                    # Parse the custom format: "Source: {source} | Content: {content}"
                    # Split by double newline first to separate distinct chunks
                    chunks = msg.content.split("\n\n")
                    for chunk in chunks:
                        if chunk.startswith("Source:"):
                            try:
                                source_part, content_part = chunk.split(" | Content: ", 1)
                                source_id = source_part.replace("Source: ", "").strip()
                                if source_id and source_id not in seen_urls:
                                    seen_urls.add(source_id)
                                    sources.append(ReportSource(
                                        title=source_id.split("/")[-1], # Rough title estimation
                                        url_or_id=source_id,
                                        source_type="document",
                                        metadata={"snippet": content_part[:200]} # Just save a short snippet
                                    ))
                            except ValueError:
                                continue
        return sources

    def generate_report(self, question: str) -> ResearchReport:
        logger.info(f"Report generation started for: {question}")
        
        # 1. Gather Evidence using the Agent
        _, _, messages = self.agent_service.research(question)
        
        # 2. Normalize and deduplicate sources
        normalized_sources = self._normalize_sources(messages)
        
        # 3. Format evidence for the prompt
        evidence_text = ""
        for i, source in enumerate(normalized_sources, 1):
            evidence_text += f"[{i}] Title: {source.title}\nID/URL: {source.url_or_id}\nContent Snippet: {source.metadata.get('snippet', '')}\n\n"
            
        if not evidence_text:
            evidence_text = "No evidence could be retrieved."
            
        # 4. Generate the structured report
        logger.info("Invoking LLM for structured report generation...")
        try:
            report: ResearchReport = self.chain.invoke({
                "question": question,
                "evidence": evidence_text
            })
            
            # Post-process: ensure the sources in the report match our normalized ones
            # The LLM might hallucinate the source structure, so we could override it
            # or just trust the LLM. We will trust the LLM's selection of sources, 
            # but ideally we cross-reference.
            
            return report
        except Exception as e:
            logger.error(f"Failed to generate structured report: {str(e)}")
            raise RuntimeError(f"Report generation failed: {str(e)}")
