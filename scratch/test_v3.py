import os
import sys

# Ensure the root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.agent import AgentService

def run_tests():
    print("=============================================")
    print("   V3 LANGCHAIN AGENT TEST SUITE             ")
    print("=============================================\n")

    try:
        agent = AgentService()
        print("[+] AgentService initialized successfully.\n")
    except Exception as e:
        print(f"[-] Failed to initialize AgentService: {e}")
        sys.exit(1)

    tests = [
        {
            "name": "Test 1. General Knowledge (No Tool)",
            "query": "What is the capital of France?"
        },
        {
            "name": "Test 2. Real-Time Query (Web Search)",
            "query": "What is the weather in New York today?"
        },
        {
            "name": "Test 3. Proprietary Knowledge (Document Search)",
            "query": "What are the core components of the RAG system described in the uploaded documents?"
        }
    ]

    for test in tests:
        print(f"--- Running {test['name']} ---")
        print(f"Query: {test['query']}")
        try:
            answer, tools_used = agent.research(test["query"])
            print(f"Tools Used: {len(tools_used)}")
            for tool in tools_used:
                print(f" - {tool['tool']} (query: {tool['query_used']})")
                
            # Safely print preview ignoring charmap errors
            safe_answer = answer.encode('ascii', errors='ignore').decode('ascii')
            print(f"Answer Preview: {safe_answer[:150]}...")
            print("[PASS]\n")
        except Exception as e:
            print(f"[FAIL] Error: {e}\n")

    print("=============================================")
    print("            TEST SUITE COMPLETE              ")
    print("=============================================\n")

if __name__ == "__main__":
    run_tests()
