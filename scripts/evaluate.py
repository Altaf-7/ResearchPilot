import sys
import os
import json
import logging
from typing import List, Dict, Any

sys.path.insert(0, os.getcwd())

from app.services.report import ReportService
from app.services.agent import AgentService
from scripts.metrics import recall_at_k, precision_at_k, evaluate_groundedness, evaluate_relevance

logging.basicConfig(level=logging.WARNING)

def run_evaluation(dataset_path: str, k: int = 3):
    print(f"Loading dataset from {dataset_path}...")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    print(f"Loaded {len(dataset)} evaluation cases.\n")
    
    report_service = ReportService()
    agent_service = AgentService()
    
    metrics_summary = {
        "retrieval_recall": [],
        "retrieval_precision": [],
        "generation_groundedness": [],
        "generation_relevance": []
    }
    
    # We will test the full dataset for an intense retest
    eval_subset = dataset
    print(f"Running full evaluation on {len(eval_subset)} cases...\n")
    
    for case in eval_subset:
        print(f"=== Evaluating: [{case['category']}] {case['question']} ===")
        
        # 1. Evaluate Retrieval (only for document_search where we expect specific internal files)
        if case["category"] == "document_search" and case.get("expected_sources"):
            # Manually run the retrieval tool to isolate retrieval performance
            # AgentService invokes tools under the hood, but for pure IR evaluation, we want to see what is retrieved.
            # We can run agent_service.research and intercept the retrieved sources.
            _, tools_used, messages = agent_service.research(case["question"])
            
            # Normalize sources using the existing ReportService logic
            normalized_sources = report_service._normalize_sources(messages)
            retrieved_ids = [s.url_or_id for s in normalized_sources]
            
            recall = recall_at_k(retrieved_ids, case["expected_sources"], k)
            precision = precision_at_k(retrieved_ids, case["expected_sources"], k)
            
            metrics_summary["retrieval_recall"].append(recall)
            metrics_summary["retrieval_precision"].append(precision)
            print(f"[Retrieval] Recall@{k}: {recall:.2f}, Precision@{k}: {precision:.2f}")
            
        # 2. Evaluate Generation Quality (End-to-End)
        try:
            # Generate the report
            report = report_service.generate_report(case["question"])
            
            # Prepare evidence string for the judge
            evidence_str = ""
            for i, source in enumerate(report.sources, 1):
                evidence_str += f"[{i}] ID: {source.url_or_id}\nSnippet: {source.metadata.get('snippet', '')}\n\n"
            
            if not evidence_str:
                evidence_str = "No evidence retrieved."
            
            # Evaluate Groundedness
            groundedness_result = evaluate_groundedness(case["question"], report.detailed_analysis, evidence_str)
            metrics_summary["generation_groundedness"].append(groundedness_result.score)
            print(f"[Generation] Groundedness: {groundedness_result.score}/5 (Reason: {groundedness_result.reasoning})")
            
            # Evaluate Relevance
            relevance_result = evaluate_relevance(case["question"], report.detailed_analysis, case["expected_answer_concepts"])
            metrics_summary["generation_relevance"].append(relevance_result.score)
            print(f"[Generation] Relevance: {relevance_result.score}/5 (Reason: {relevance_result.reasoning})")
            
        except Exception as e:
            print(f"[Generation] FAILED: {str(e)}")
            
        print("")

    # Output Summary
    print("==========================================")
    print("           EVALUATION SUMMARY             ")
    print("==========================================")
    
    def avg(lst):
        return sum(lst)/len(lst) if lst else 0.0
        
    print(f"Average Retrieval Recall@{k}:    {avg(metrics_summary['retrieval_recall']):.2f}")
    print(f"Average Retrieval Precision@{k}: {avg(metrics_summary['retrieval_precision']):.2f}")
    print(f"Average Answer Groundedness:   {avg(metrics_summary['generation_groundedness']):.2f} / 5.0")
    print(f"Average Answer Relevance:      {avg(metrics_summary['generation_relevance']):.2f} / 5.0")
    print("==========================================")

if __name__ == "__main__":
    dataset_file = os.path.join("data", "evaluation", "dataset.json")
    run_evaluation(dataset_file, k=3)
