import json
from typing import Any

from src.database.vector_store import GameVectorStore
from src.models.game import GameSearchResult
from src.utils.logger import logger


class RetrieveGameTool:
    """Tool for retrieving game information from the vector database.
    
    This tool performs semantic search on the game database to find
    relevant games based on user queries about titles, platforms,
    genres, publishers, or other game characteristics.
    """

    def __init__(self, vector_store: GameVectorStore):
        """Initialize the retrieve game tool.
        
        Args:
            vector_store: Initialized GameVectorStore instance

        """
        self.vector_store = vector_store

    def __call__(self, query: str, n_results: int = 5) -> str:
        """Search for games using semantic similarity.
        
        Args:
            query: Question about game industry (e.g., "racing games on PlayStation")
            n_results: Maximum number of results to return
            
        Returns:
            JSON string containing search results

        """
        try:
            # Perform semantic search
            search_results = self.vector_store.search_games(query, n_results)

            if not search_results:
                logger.debug("No search results returned from vector store")
                return json.dumps({
                    "games": [],
                    "query": query,
                    "total_results": 0,
                    "confidence_score": 0.0,
                    "search_method": "vector_db",
                    "message": "No games found matching the query"
                })

            # Convert results to Game objects
            games = [result["game"] for result in search_results]

            # Calculate average confidence score
            avg_confidence = sum(result["similarity_score"] for result in search_results) / len(search_results)
            # Ensure confidence is between 0 and 1
            avg_confidence = max(0.0, min(1.0, avg_confidence))

            # Create search result object
            game_search_result = GameSearchResult(
                games=games,
                query=query,
                total_results=len(games),
                confidence_score=avg_confidence,
                search_method="vector_db"
            )

            return game_search_result.model_dump_json(indent=2)

        except Exception as e:
            logger.error(f"Error searching games: {e}")
            return json.dumps({
                "error": f"Error searching games: {e!s}",
                "query": query,
                "total_results": 0,
                "confidence_score": 0.0,
                "search_method": "vector_db"
            })

    def get_tool_definition(self) -> dict[str, Any]:
        """Get the tool definition for the agent.
        
        Returns:
            Dictionary containing tool metadata and schema

        """
        return {
            "type": "function",
            "function": {
                "name": "retrieve_game",
                "description": (
                    "Semantic search: Finds most relevant games in the vector database. "
                    "Use this tool to search for games by title, platform, genre, publisher, "
                    "release year, or any other game-related characteristics. "
                    "Returns detailed information about matching games including platform, "
                    "genre, publisher, description, and release year."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "A question or search query about games (e.g., 'racing games on PlayStation', 'Pokémon games', 'games by Nintendo')"
                        },
                        "n_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 5, max: 10)",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 10
                        }
                    },
                    "required": ["query"]
                }
            }
        }
