"""Small script to initialize GameVectorStore and add a document to reproduce warnings/logs.
Run with: PYTHONPATH=. python scripts/collect_warnings.py
"""
import os
import tempfile

from src.database.vector_store import GameVectorStore

if __name__ == "__main__":
    tmp = tempfile.TemporaryDirectory()
    print("Using tmpdir:", tmp.name)
    # set test env var to avoid raising
    os.environ.setdefault("OPENAI_API_KEY", "test")
    vs = GameVectorStore(persist_directory=tmp.name)
    added = vs.add_document("Hello world test", {"title": "test", "url": ""})
    print("Added:", added)
    print("Ingested index exists:", os.path.exists(os.path.join(tmp.name, "ingested_index.json")))
