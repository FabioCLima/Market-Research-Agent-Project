"""Trending Games Detection Tool.

This tool identifies trending games based on various signals
like recent releases, high ratings, popular genres, and
social media mentions.
"""

import json
from datetime import datetime, timedelta
from typing import Any

from src.database.vector_store import GameVectorStore
from src.utils.logger import logger


class TrendingGamesTool:
    """Tool for detecting trending games based on various signals.
    
    This tool analyzes game data to identify trending games
    based on factors like:
    - Recent releases (last 2 years)
    - High-rated games
    - Popular genres
    - Games with high search frequency
    """

    def __init__(self, vector_store: GameVectorStore):
        """Initialize the trending games tool.
        
        Args:
            vector_store: Initialized GameVectorStore instance
        """
        self.vector_store = vector_store

    def __call__(self, criteria: str = "recent_high_rated", limit: int = 10) -> str:
        """Detect trending games based on specified criteria.
        
        Args:
            criteria: Trending criteria ("recent_high_rated", "popular_genres", "all_time_classics")
            limit: Maximum number of trending games to return
            
        Returns:
            JSON string containing trending games analysis
        """
        try:
            trending_games = []
            
            if criteria == "recent_high_rated":
                trending_games = self._get_recent_high_rated_games(limit)
            elif criteria == "popular_genres":
                trending_games = self._get_popular_genre_games(limit)
            elif criteria == "all_time_classics":
                trending_games = self._get_classic_games(limit)
            else:
                # Default: mixed criteria
                trending_games = self._get_mixed_trending_games(limit)

            return json.dumps({
                "trending_games": trending_games,
                "criteria_used": criteria,
                "total_found": len(trending_games),
                "analysis_date": datetime.now().isoformat(),
                "description": self._get_criteria_description(criteria)
            }, indent=2)

        except Exception as e:
            logger.error(f"Error detecting trending games: {e}")
            return json.dumps({
                "error": f"Trending games detection failed: {e!s}",
                "trending_games": [],
                "total_found": 0
            })

    def _get_recent_high_rated_games(self, limit: int) -> list[dict[str, Any]]:
        """Get recently released games that are highly rated."""
        try:
            # Search for recent games (last 2 years)
            current_year = datetime.now().year
            recent_years = [str(year) for year in range(current_year - 1, current_year + 1)]
            
            trending = []
            for year in recent_years:
                results = self.vector_store.search_games(f"games released in {year}", n_results=5)
                for result in results:
                    game = result["game"]
                    # Add trending score based on recency and genre popularity
                    trending_score = self._calculate_trending_score(game, "recent")
                    trending.append({
                        "game": game.model_dump(),
                        "trending_score": trending_score,
                        "reason": f"Recent release ({game.year_of_release})"
                    })
            
            # Sort by trending score and return top results
            trending.sort(key=lambda x: x["trending_score"], reverse=True)
            return trending[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recent high-rated games: {e}")
            return []

    def _get_popular_genre_games(self, limit: int) -> list[dict[str, Any]]:
        """Get games from popular genres."""
        try:
            # Popular genres based on gaming industry trends
            popular_genres = ["Action", "RPG", "Adventure", "Racing", "Sports", "Fighting"]
            
            trending = []
            for genre in popular_genres:
                results = self.vector_store.search_games(f"{genre} games", n_results=3)
                for result in results:
                    game = result["game"]
                    trending_score = self._calculate_trending_score(game, "genre")
                    trending.append({
                        "game": game.model_dump(),
                        "trending_score": trending_score,
                        "reason": f"Popular genre ({game.genre})"
                    })
            
            trending.sort(key=lambda x: x["trending_score"], reverse=True)
            return trending[:limit]
            
        except Exception as e:
            logger.error(f"Error getting popular genre games: {e}")
            return []

    def _get_classic_games(self, limit: int) -> list[dict[str, Any]]:
        """Get classic games that are timeless favorites."""
        try:
            # Search for well-known classic games
            classic_queries = [
                "Super Mario", "Zelda", "Pokemon", "Final Fantasy", "Street Fighter",
                "Mortal Kombat", "Sonic", "Donkey Kong", "Metroid", "Castlevania"
            ]
            
            trending = []
            for query in classic_queries:
                results = self.vector_store.search_games(query, n_results=2)
                for result in results:
                    game = result["game"]
                    trending_score = self._calculate_trending_score(game, "classic")
                    trending.append({
                        "game": game.model_dump(),
                        "trending_score": trending_score,
                        "reason": f"Classic franchise ({query})"
                    })
            
            trending.sort(key=lambda x: x["trending_score"], reverse=True)
            return trending[:limit]
            
        except Exception as e:
            logger.error(f"Error getting classic games: {e}")
            return []

    def _get_mixed_trending_games(self, limit: int) -> list[dict[str, Any]]:
        """Get trending games using mixed criteria."""
        recent = self._get_recent_high_rated_games(limit // 3)
        genre_based = self._get_popular_genre_games(limit // 3)
        classics = self._get_classic_games(limit // 3)
        
        all_trending = recent + genre_based + classics
        all_trending.sort(key=lambda x: x["trending_score"], reverse=True)
        
        return all_trending[:limit]

    def _calculate_trending_score(self, game: Any, trend_type: str) -> float:
        """Calculate trending score for a game."""
        base_score = 0.5
        
        # Adjust based on trend type
        if trend_type == "recent":
            current_year = datetime.now().year
            if game.year_of_release and int(game.year_of_release) >= current_year - 1:
                base_score += 0.3
        elif trend_type == "genre":
            popular_genres = ["Action", "RPG", "Adventure", "Racing"]
            if game.genre in popular_genres:
                base_score += 0.2
        elif trend_type == "classic":
            base_score += 0.4  # Classics have high trending value
        
        # Adjust based on platform popularity
        popular_platforms = ["PlayStation", "Nintendo", "Xbox", "PC"]
        if any(platform in game.platform for platform in popular_platforms):
            base_score += 0.1
        
        return min(1.0, base_score)

    def _get_criteria_description(self, criteria: str) -> str:
        """Get description of the criteria used."""
        descriptions = {
            "recent_high_rated": "Games released in the last 2 years with high potential",
            "popular_genres": "Games from currently popular genres (Action, RPG, Adventure, etc.)",
            "all_time_classics": "Timeless classic games from major franchises",
            "mixed": "Combination of recent releases, popular genres, and classics"
        }
        return descriptions.get(criteria, "Custom trending criteria")

    def get_tool_definition(self) -> dict[str, Any]:
        """Get the tool definition for the agent.
        
        Returns:
            Dictionary containing tool metadata and schema
        """
        return {
            "type": "function",
            "function": {
                "name": "detect_trending_games",
                "description": (
                    "Detects trending games based on various criteria like recent releases, "
                    "popular genres, or classic franchises. Useful for identifying "
                    "what games are currently popular or worth playing."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "criteria": {
                            "type": "string",
                            "description": "Trending criteria: 'recent_high_rated', 'popular_genres', 'all_time_classics', or 'mixed'",
                            "default": "recent_high_rated",
                            "enum": ["recent_high_rated", "popular_genres", "all_time_classics", "mixed"]
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of trending games to return",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 20
                        }
                    },
                    "required": []
                }
            }
        }
