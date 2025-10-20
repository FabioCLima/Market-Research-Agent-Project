import hashlib
import json
import os
from datetime import UTC, datetime
from typing import Any

from chromadb.api.models.Collection import Collection as ChromaCollection
from chromadb.utils import embedding_functions

import chromadb
from src.models.game import Game
from src.utils.logger import logger


class GameVectorStore:
    """Vector database manager for game data using ChromaDB.
    
    This class handles the creation and management of a ChromaDB collection
    specifically for game data, providing methods for indexing and searching
    game information using semantic similarity.
    """

    def __init__(self, collection_name: str = "udaplay_games", persist_directory: str = "./chromadb", embedding_function: Any | None = None):
        """Initialize the game vector store.

        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database

        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_directory)

        # Create embedding function using OpenAI by default, but allow tests to inject a stub.
        if embedding_function is not None:
            self.embedding_function = embedding_function
        else:
            # Prefer using environment variable for persistent configuration per ChromaDB guidance
            api_env_var = "OPENAI_API_KEY"
            if not os.getenv(api_env_var):
                logger.warning(f"{api_env_var} not set; embedding operations may warn or fail until provided")
            # Use api_key_env_var to persist configuration via environment variables (recommended by chromadb)
            self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key_env_var=api_env_var,
                model_name="text-embedding-3-small"
            )

        # Get or create collection
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self) -> ChromaCollection:
        """Get existing collection or create a new one."""
        try:
            collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Loaded existing collection: {self.collection_name}")
            return collection
        except Exception:
            try:
                collection = self.client.create_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function
                )
                logger.info(f"Created new collection: {self.collection_name}")
                return collection
            except Exception as e:
                # Some Chroma backends may report a race where the collection was
                # created between the get_collection and create_collection calls.
                # Try to fetch the collection again before failing.
                try:
                    collection = self.client.get_collection(
                        name=self.collection_name,
                        embedding_function=self.embedding_function
                    )
                    logger.info(f"Loaded existing collection after race: {self.collection_name}")
                    return collection
                except Exception:
                    raise e

    def _ensure_documents_dir(self) -> str:
        docs_dir = os.path.join(self.persist_directory, "documents")
        try:
            os.makedirs(docs_dir, exist_ok=True)
        except Exception:
            pass
        return docs_dir

    def load_games_from_directory(self, games_directory: str) -> int:
        """Load all game JSON files from a directory into the vector store.

        Args:
            games_directory: Path to directory containing game JSON files

        Returns:
            Number of games loaded

        """
        if not os.path.exists(games_directory):
            raise FileNotFoundError(f"Games directory not found: {games_directory}")

        games_loaded = 0

        for file_name in sorted(os.listdir(games_directory)):
            if not file_name.endswith(".json"):
                continue

            file_path = os.path.join(games_directory, file_name)

            try:
                with open(file_path, encoding="utf-8") as f:
                    game_data = json.load(f)

                # Create Game object for validation
                game = Game(**game_data)

                # Create searchable content
                content = self._create_searchable_content(game)

                # Use file name (without extension) as ID
                doc_id = os.path.splitext(file_name)[0]

                # Add to collection
                self.collection.add(
                    ids=[doc_id],
                    documents=[content],
                    metadatas=[game.model_dump()]
                )

                # Backup original JSON for traceability
                try:
                    docs_dir = self._ensure_documents_dir()
                    backup_path = os.path.join(docs_dir, f"{doc_id}.json")
                    with open(backup_path, "w", encoding="utf-8") as bf:
                        json.dump(game_data, bf, ensure_ascii=False, indent=2)
                except Exception:
                    logger.debug("Failed to backup original game JSON")

                games_loaded += 1
                logger.info(f"Loaded game: {game.name} ({game.platform})")

            except Exception as e:
                logger.error(f"Error loading {file_name}: {e}")
                continue

        logger.info(f"Total games loaded: {games_loaded}")
        return games_loaded

    def _create_searchable_content(self, game: Game) -> str:
        """Create searchable text content from game data.

        Args:
            game: Game object to convert to searchable text

        Returns:
            Formatted text content for embedding

        """
        return (
            f"[{game.platform}] {game.name} ({game.year_of_release}) - "
            f"Genre: {game.genre}, Publisher: {game.publisher}. "
            f"{game.description}"
        )

    def search_games(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Search for games using semantic similarity.

        Args:
            query: Search query string
            n_results: Number of results to return

        Returns:
            List of search results with games and metadata

        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "distances", "metadatas"]
            )

            search_results = []

            if results["documents"] and results["documents"][0]:
                for i, (doc, distance, metadata) in enumerate(zip(
                    results["documents"][0],
                    results["distances"][0],
                    results["metadatas"][0], strict=False
                )):
                    # Convert metadata back to Game object
                    try:
                        game = Game(**metadata)
                        # return metadata with aliases (Name, Platform, etc.) for compatibility with tests
                        metadata_out = game.model_dump(by_alias=True)
                    except Exception:
                        # fallback: use raw metadata dict
                        metadata_out = metadata

                    search_results.append({
                        "Name": metadata_out.get("Name") or metadata_out.get("name") or "",
                        "Platform": metadata_out.get("Platform") or metadata_out.get("platform") or "",
                        "Genre": metadata_out.get("Genre") or metadata_out.get("genre") or "",
                        "Publisher": metadata_out.get("Publisher") or metadata_out.get("publisher") or "",
                        "Description": metadata_out.get("Description") or metadata_out.get("description") or "",
                        "YearOfRelease": metadata_out.get("YearOfRelease") or metadata_out.get("year_of_release") or None,
                        "content": doc,
                        "distance": distance,
                        "similarity_score": 1 - distance,  # Convert distance to similarity
                        "rank": i + 1
                    })

            return search_results

        except Exception as e:
            logger.error(f"Error searching games: {e}")
            return []

    def get_collection_stats(self) -> dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_games": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {"error": str(e)}

    def clear_collection(self):
        """Clear all data from the collection."""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self._get_or_create_collection()
            logger.info(f"Collection {self.collection_name} cleared")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")

    def add_game(self, game: Game, doc_id: str | None = None) -> bool:
        """Add a Game object to the collection and persist it.

        Args:
            game: Game object to add
            doc_id: Optional ID to use (defaults to timestamp-based id)

        Returns:
            True if added successfully, False otherwise

        """
        try:
            if doc_id is None:
                # simple id generation
                import time

                doc_id = f"game_{int(time.time() * 1000)}"

            content = self._create_searchable_content(game)
            self.collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[game.model_dump()]
            )
            logger.info(f"Added game to collection: {game.name} (id={doc_id})")

            # Backup game JSON
            try:
                docs_dir = self._ensure_documents_dir()
                backup_path = os.path.join(docs_dir, f"{doc_id}.game.json")
                with open(backup_path, "w", encoding="utf-8") as bf:
                    json.dump(game.model_dump(), bf, ensure_ascii=False, indent=2)
            except Exception:
                logger.debug("Failed to backup added game JSON")
            return True
        except Exception as e:
            logger.error(f"Failed to add game to collection: {e}")
            return False

    def add_document(self, content: str, metadata: dict[str, Any], doc_id: str | None = None) -> bool:
        """Add an arbitrary document to the collection (useful for web results).

        Args:
            content: Text content to embed
            metadata: Metadata dictionary (will be stored)
            doc_id: Optional ID

        Returns:
            True if added successfully

        """
        try:
            # enrich metadata
            import time

            timestamp = datetime.now(UTC).isoformat()
            metadata_enriched = dict(metadata)
            metadata_enriched.setdefault("ingested_at", timestamp)
            metadata_enriched.setdefault("snippet", content[:500])

            # Stronger dedup: create a stable key from url + title
            url = (metadata_enriched.get("url") or "").strip()
            title = (metadata_enriched.get("title") or "").strip()
            dup_raw = f"{url}|{title}" if (url or title) else content[:200]
            dup_key = hashlib.sha256(dup_raw.encode("utf-8")).hexdigest()

            dedup_file = os.path.join(self.persist_directory, "ingested_index.json")
            seen = {}
            if os.path.exists(dedup_file):
                try:
                    with open(dedup_file, encoding="utf-8") as f:
                        seen = json.load(f)
                except Exception:
                    seen = {}

            if dup_key in seen:
                logger.debug(f"Document already ingested (dedup): {dup_key}")
                return False

            if doc_id is None:
                doc_id = f"doc_{int(time.time() * 1000)}"

            self.collection.add(ids=[doc_id], documents=[content], metadatas=[metadata_enriched])

            # update seen index with key and backup file
            seen[dup_key] = {"id": doc_id, "ingested_at": timestamp, "title": title, "url": url}
            try:
                with open(dedup_file, "w", encoding="utf-8") as f:
                    json.dump(seen, f, ensure_ascii=False, indent=2)
            except Exception:
                logger.warning("Failed to update ingested index file")

            # Backup raw document to documents/ for traceability
            try:
                docs_dir = self._ensure_documents_dir()
                backup_path = os.path.join(docs_dir, f"{doc_id}.json")
                with open(backup_path, "w", encoding="utf-8") as bf:
                    json.dump({"content": content, "metadata": metadata_enriched}, bf, ensure_ascii=False, indent=2)
            except Exception:
                logger.debug("Failed to backup ingested document")

            logger.info(f"Added document to collection: id={doc_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add document to collection: {e}")
            return False
