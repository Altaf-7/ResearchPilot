import sys
import os

# Ensure the root project directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.ingestion import DocumentIngestor

def main():
    print("Starting document ingestion...")
    ingestor = DocumentIngestor()
    ingestor.process_and_store()
    print("Done!")

if __name__ == "__main__":
    main()
