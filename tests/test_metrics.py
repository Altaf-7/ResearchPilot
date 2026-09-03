import pytest
from scripts.metrics import precision_at_k, recall_at_k

def test_precision_at_k_perfect():
    retrieved = ["doc1", "doc2", "doc3"]
    expected = ["doc1", "doc2", "doc3"]
    assert precision_at_k(retrieved, expected, k=3) == 1.0

def test_precision_at_k_partial():
    retrieved = ["doc1", "doc2", "doc3"]
    expected = ["doc1", "doc4"]
    # Top 3 retrieved: doc1, doc2, doc3
    # Relevant in top 3: doc1 (1 item)
    # Precision@3 = 1 / 3 = 0.333...
    assert abs(precision_at_k(retrieved, expected, k=3) - 0.3333) < 0.001

def test_precision_at_k_none():
    retrieved = ["doc1", "doc2"]
    expected = ["doc3", "doc4"]
    assert precision_at_k(retrieved, expected, k=2) == 0.0

def test_recall_at_k_perfect():
    retrieved = ["doc1", "doc2", "doc3"]
    expected = ["doc1", "doc2", "doc3"]
    assert recall_at_k(retrieved, expected, k=3) == 1.0

def test_recall_at_k_partial():
    retrieved = ["doc1", "doc2", "doc3"]
    expected = ["doc1", "doc4"]
    # Top 3 retrieved: doc1, doc2, doc3
    # Relevant in top 3: doc1 (1 item)
    # Total expected relevant: doc1, doc4 (2 items)
    # Recall@3 = 1 / 2 = 0.5
    assert recall_at_k(retrieved, expected, k=3) == 0.5

def test_recall_at_k_larger_k():
    retrieved = ["doc1", "doc2", "doc3", "doc4"]
    expected = ["doc1", "doc4"]
    # Top 2 retrieved: doc1, doc2
    # Relevant in top 2: doc1 (1 item)
    # Total expected: 2
    # Recall@2 = 1 / 2 = 0.5
    assert recall_at_k(retrieved, expected, k=2) == 0.5
