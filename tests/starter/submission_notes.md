Submission notes for Udacity evaluator

Project: UdaPlay AI Research Agent

Python version used: 3.13 (development environment .venv)

How to run (minimal):

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. (Optional) Copy the example environment and provide API keys for live runs:

```bash
cp .env.example .env
# Edit .env to set OPENAI_API_KEY and TAVILY_API_KEY only if you want live calls
```

1. Run tests (the repository includes mocked tests so they pass without API keys):

```bash
python run_tests.py
# or: pytest -q
```

1. Run interactive agent:

```bash
python run_udaplay.py
```

Notes / Known limitations:


- External APIs (OpenAI/Tavily) are required for live web search and embedding operations. Tests mock these in CI.
- Some deprecation warnings appear (Pydantic class-based config; chromadb embedding config; naive datetime usage updated in state machine) — they do not break execution but should be addressed in a follow-up.
- The project creates a local ChromaDB persist directory (`chromadb/`) which can be large; ensure it is excluded from submission archives if size-limited.

Changes made since starter project:


- Added public `persist()` wrapper to `src/agent/state_machine.py` and ensured the agent sets the `state.json` path inside the vector store `persist_directory`.
- `UdaPlayAgent` now calls `state_machine.persist()` after each `process_query` to improve crash recovery and ensure state is saved frequently.
- Added unit test `tests/test_state_persistence.py` to validate save/reload behaviour of the state machine.
- Added tests for `add_document` edge cases: missing url/title, duplicate detection by content, and simulated disk write failures (`tests/test_vector_store_add_document_extra.py`).
- Made `GameVectorStore` accept an optional `embedding_function` for easier testing without network calls and added small robustness when creating/obtaining ChromaDB collections.

Test summary (local):


- All tests pass locally in the development environment: `9 passed, 7 warnings` (see README for recommended test commands).

Contact / support: See README.md for detailed developer notes and usage.
Submission notes for Udacity evaluator

Project: UdaPlay AI Research Agent

Python version used: 3.13 (development environment .venv)

How to run (minimal):

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Copy the example environment and provide API keys for live runs:

```bash
cp .env.example .env
# Edit .env to set OPENAI_API_KEY and TAVILY_API_KEY only if you want live calls
```

4. Run tests (the repository includes mocked tests so they pass without API keys):

```bash
python run_tests.py
# or: pytest -q
```

5. Run interactive agent:

```bash
python run_udaplay.py
```

Notes / Known limitations:
- External APIs (OpenAI/Tavily) are required for live web search and embedding operations. Tests mock these in CI.
- Some deprecation warnings appear (Pydantic class-based config; chromadb embedding config; naive datetime usage updated in state machine) — they do not break execution but should be addressed in a follow-up.
- The project creates a local ChromaDB persist directory (`chromadb/`) which can be large; ensure it is excluded from submission archives if size-limited.

Changes made since starter project:
- Added public `persist()` wrapper to `src/agent/state_machine.py` and ensured the agent sets the `state.json` path inside the vector store `persist_directory`.
- `UdaPlayAgent` now calls `state_machine.persist()` after each `process_query` to improve crash recovery and ensure state is saved frequently.
- Added unit test `tests/test_state_persistence.py` to validate save/reload behaviour of the state machine.
- Added tests for `add_document` edge cases: missing url/title, duplicate detection by content, and simulated disk write failures (`tests/test_vector_store_add_document_extra.py`).
- Made `GameVectorStore` accept an optional `embedding_function` for easier testing without network calls and added small robustness when creating/obtaining ChromaDB collections.

Test summary (local):
- All tests pass locally in the development environment: `9 passed, 7 warnings` (see README for recommended test commands).


Contact / support: See README.md for detailed developer notes and usage.
