import logging
from typing import Tuple, List, Dict, Any
from langchain.agents import create_agent
from app.core.llm import get_llm
from app.tools.web_search import web_search_tool
from app.tools.rag_search import document_search_tool
from app.prompts import AGENT_SYSTEM_PROMPT
from langchain_core.messages import ToolMessage

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        self.tools = [web_search_tool, document_search_tool]
        self.llm = get_llm()
        
        # Create the agent using current LangChain API
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=AGENT_SYSTEM_PROMPT
        )

    def research(self, question: str) -> Tuple[str, List[Dict[str, Any]]]:
        logger.info(f"Agent received question: {question}")
        
        try:
            inputs = {"messages": [{"role": "user", "content": question}]}
            final_state = self.agent.invoke(inputs, config={"recursion_limit": 5})
            
            messages = final_state.get("messages", [])
            answer = messages[-1].content if messages else ""
            
            tools_used = []
            for msg in messages:
                if isinstance(msg, ToolMessage):
                    tools_used.append({
                        "tool": msg.name,
                        "query_used": "..." # In newer versions ToolMessage doesn't store the exact input string directly in an easy format, but we can extract it if needed.
                    })
                    logger.info(f"Agent used tool '{msg.name}'")
                    
            return answer, tools_used
            
        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            raise RuntimeError(f"Agent error: {str(e)}")
