import json

from src.database.vector_store import GameVectorStore


def test_add_document_backup_and_dedup(tmp_path):
    # Prepare a temporary persist directory
    persist_dir = tmp_path / "chromadb"
    persist_dir.mkdir()

    gv = GameVectorStore(persist_directory=str(persist_dir))

    content = "This is a test web document about a Mock Game."
    metadata = {"title": "Mock Game Page", "url": "https://example.com/mock-game"}

    # First add should return True
    added = gv.add_document(content, metadata)
    assert added is True

    # Check that backup file and index exist
    docs_dir = persist_dir / "documents"
    assert docs_dir.exists()

    ingested_index = persist_dir / "ingested_index.json"
    assert ingested_index.exists()

    with open(ingested_index, encoding="utf-8") as f:
        seen = json.load(f)

    assert len(seen) == 1

    # Second add (same content/url/title) should be deduped and return False
    added2 = gv.add_document(content, metadata)
    assert added2 is False
