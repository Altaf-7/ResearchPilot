import logging
from typing import List
from pydantic import BaseModel, Field
from app.core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

def precision_at_k(retrieved_ids: List[str], expected_ids: List[str], k: int) -> float:
    """
    Precision@K measures the proportion of retrieved items in the top-K that are relevant.
    precision = (relevant items retrieved in top-K) / K
    """
    if k <= 0:
        return 0.0
    
    top_k_retrieved = retrieved_ids[:k]
    if not top_k_retrieved:
        return 0.0
        
    relevant_retrieved = [doc_id for doc_id in top_k_retrieved if doc_id in expected_ids]
    return len(relevant_retrieved) / k

def recall_at_k(retrieved_ids: List[str], expected_ids: List[str], k: int) -> float:
    """
    Recall@K measures the proportion of all relevant items that were retrieved in the top-K.
    recall = (relevant items retrieved in top-K) / (total relevant items)
    """
    if k <= 0 or not expected_ids:
        return 0.0
        
    top_k_retrieved = retrieved_ids[:k]
    relevant_retrieved = [doc_id for doc_id in top_k_retrieved if doc_id in expected_ids]
    return len(relevant_retrieved) / len(expected_ids)

class EvaluationScore(BaseModel):
    score: int = Field(description="An integer score from 1 to 5")
    reasoning: str = Field(description="A brief explanation for the score")

def evaluate_groundedness(question: str, report: str, evidence: str) -> EvaluationScore:
    """
    Uses an LLM-as-judge to evaluate if the report is grounded in the provided evidence.
    Score 5: Fully grounded, no hallucinations.
    Score 1: Completely hallucinates or contradicts evidence.
    """
    llm = get_llm()
    try:
        structured_llm = llm.with_structured_output(EvaluationScore)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an impartial evaluator assessing the groundedness of an AI research report.
Your task is to determine if the report's claims are fully supported by the provided evidence.
Score from 1 to 5:
5 - All claims are strictly supported by evidence. If no evidence was provided, the report correctly states it cannot answer.
4 - Mostly supported, but minor unstated assumptions exist.
3 - Some claims are supported, but others are hallucinated.
2 - Mostly hallucinated or uses external knowledge heavily.
1 - Completely contradicts evidence or hallucinated the entire answer."""),
            ("human", """Question: {question}
Evidence: {evidence}
Report: {report}""")
        ])
        chain = prompt | structured_llm
        return chain.invoke({
            "question": question,
            "evidence": evidence,
            "report": report
        })
    except Exception as e:
        logger.error(f"Groundedness evaluation failed: {e}")
        return EvaluationScore(score=0, reasoning=f"Error evaluating: {e}")

def evaluate_relevance(question: str, report: str, expected_concepts: List[str]) -> EvaluationScore:
    """
    Uses an LLM-as-judge to evaluate if the report is relevant and addresses expected concepts.
    Score 5: Highly relevant, covers key concepts.
    Score 1: Irrelevant or misses all key concepts.
    """
    llm = get_llm()
    try:
        structured_llm = llm.with_structured_output(EvaluationScore)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an impartial evaluator assessing the relevance of an AI research report.
Does the report answer the user's question and cover the expected concepts?
Score from 1 to 5:
5 - Perfectly relevant, covers expected concepts.
3 - Somewhat relevant, misses some concepts.
1 - Completely irrelevant."""),
            ("human", """Question: {question}
Expected Concepts: {expected}
Report: {report}""")
        ])
        chain = prompt | structured_llm
        return chain.invoke({
            "question": question,
            "expected": ", ".join(expected_concepts),
            "report": report
        })
    except Exception as e:
        logger.error(f"Relevance evaluation failed: {e}")
        return EvaluationScore(score=0, reasoning=f"Error evaluating: {e}")
