# ResearchPilot — AI Research & Intelligence Assistant

ResearchPilot is an intelligent agentic workflow application designed to assist with deep research, information retrieval, and synthesis. It uses RAG (Retrieval-Augmented Generation) and LangChain to provide insightful answers grounded in retrieved documents.

## Current Capabilities
* Basic project structure established.
* FastAPI setup for health monitoring and simple API entrypoints.
* Environment configuration management using Pydantic Settings.
* Base dependencies configured for future integration.

## Planned Architecture
* **Vector Storage**: ChromaDB for document embeddings.
* **LLM Orchestration**: LangChain for chaining, RAG, and agentic workflows.
* **API Layer**: FastAPI for serving the application.
* **Frontend**: A simple UI (planned) for interacting with the AI.

## Tech Stack
* Python 3
* FastAPI & Uvicorn
* LangChain
* Pydantic
* Pytest

## Project Structure
```
researchpilot/
├── app/             # Main application code (FastAPI, config, logic)
├── data/            # Data storage (documents, chroma DB)
├── docs/            # Documentation (Walkthroughs, etc.)
├── scripts/         # Utility scripts
├── tests/           # Pytest unit and integration tests
├── .env.example     # Template for environment variables
├── requirements.txt # Python dependencies
└── run.py           # Entry point for running the application
```

## Installation Instructions

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   * Windows: `.venv\Scripts\activate`
   * Unix/macOS: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
Copy `.env.example` to `.env` and fill in your values.
```bash
cp .env.example .env
```
Key variables:
* `LLM_API_KEY`: Your LLM provider API key
* `MODEL_NAME`: The model to use (e.g., gpt-4o)

## How to Run
```bash
python run.py
```
Or via uvicorn directly:
```bash
uvicorn app.main:app --reload
```

## How to Run Tests
```bash
pytest
```

## Development Roadmap
- [x] Initial project setup (V0)
- [ ] Implement document ingestion and vectorization (V1)
- [ ] Build basic RAG pipeline and query endpoint (V1)
- [ ] Add agentic workflows with tool calling (V2)
- [ ] Build simple frontend UI (V2)
