"""Game Recommendation Engine Tool.

This tool provides personalized game recommendations based on user preferences,
game characteristics, and collaborative filtering techniques.
"""

import json
from typing import Any

from src.database.vector_store import GameVectorStore
from src.utils.logger import logger


class GameRecommendationTool:
    """Tool for providing personalized game recommendations.
    
    This tool analyzes user preferences and game characteristics to provide
    personalized recommendations using various algorithms:
    - Content-based filtering
    - Collaborative filtering
    - Hybrid approaches
    """

    def __init__(self, vector_store: GameVectorStore):
        """Initialize the recommendation engine.
        
        Args:
            vector_store: Initialized GameVectorStore instance
        """
        self.vector_store = vector_store

    def __call__(self, user_preferences: str, recommendation_type: str = "content_based", limit: int = 5) -> str:
        """Generate game recommendations based on user preferences.
        
        Args:
            user_preferences: User's preferences (e.g., "I like RPG games with fantasy themes")
            recommendation_type: Type of recommendation algorithm
            limit: Maximum number of recommendations
            
        Returns:
            JSON string containing personalized recommendations
        """
        try:
            recommendations = []
            
            if recommendation_type == "content_based":
                recommendations = self._content_based_recommendations(user_preferences, limit)
            elif recommendation_type == "collaborative":
                recommendations = self._collaborative_recommendations(user_preferences, limit)
            elif recommendation_type == "hybrid":
                recommendations = self._hybrid_recommendations(user_preferences, limit)
            elif recommendation_type == "similar_games":
                recommendations = self._similar_games_recommendations(user_preferences, limit)
            else:
                recommendations = self._content_based_recommendations(user_preferences, limit)

            return json.dumps({
                "recommendations": recommendations,
                "recommendation_type": recommendation_type,
                "user_preferences": user_preferences,
                "total_recommendations": len(recommendations),
                "algorithm_description": self._get_algorithm_description(recommendation_type)
            }, indent=2)

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return json.dumps({
                "error": f"Recommendation generation failed: {e!s}",
                "recommendations": [],
                "total_recommendations": 0
            })

    def _content_based_recommendations(self, preferences: str, limit: int) -> list[dict[str, Any]]:
        """Generate recommendations based on game content similarity."""
        try:
            # Search for games matching user preferences
            results = self.vector_store.search_games(preferences, n_results=limit * 2)
            
            recommendations = []
            for result in results:
                game = result["game"]
                similarity_score = result["similarity_score"]
                
                # Calculate recommendation score based on similarity and additional factors
                recommendation_score = self._calculate_recommendation_score(game, similarity_score, preferences)
                
                recommendations.append({
                    "game": game.model_dump(),
                    "recommendation_score": recommendation_score,
                    "similarity_score": similarity_score,
                    "reason": f"Matches your preferences: {preferences[:50]}...",
                    "recommendation_type": "content_based"
                })
            
            # Sort by recommendation score and return top results
            recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error in content-based recommendations: {e}")
            return []

    def _collaborative_recommendations(self, preferences: str, limit: int) -> list[dict[str, Any]]:
        """Generate recommendations based on similar users' preferences."""
        try:
            # Simulate collaborative filtering by finding games with high popularity
            # In a real implementation, this would use user interaction data
            
            # Search for popular games in similar genres
            genre_keywords = self._extract_genre_keywords(preferences)
            recommendations = []
            
            for genre in genre_keywords:
                results = self.vector_store.search_games(f"popular {genre} games", n_results=3)
                for result in results:
                    game = result["game"]
                    recommendation_score = self._calculate_collaborative_score(game, preferences)
                    
                    recommendations.append({
                        "game": game.model_dump(),
                        "recommendation_score": recommendation_score,
                        "similarity_score": result["similarity_score"],
                        "reason": f"Popular among users who like {genre} games",
                        "recommendation_type": "collaborative"
                    })
            
            # Remove duplicates and sort by score
            unique_games = {}
            for rec in recommendations:
                game_id = rec["game"]["name"]
                if game_id not in unique_games or rec["recommendation_score"] > unique_games[game_id]["recommendation_score"]:
                    unique_games[game_id] = rec
            
            sorted_recommendations = sorted(unique_games.values(), key=lambda x: x["recommendation_score"], reverse=True)
            return sorted_recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error in collaborative recommendations: {e}")
            return []

    def _hybrid_recommendations(self, preferences: str, limit: int) -> list[dict[str, Any]]:
        """Generate recommendations using hybrid approach."""
        try:
            # Combine content-based and collaborative filtering
            content_recs = self._content_based_recommendations(preferences, limit // 2)
            collab_recs = self._collaborative_recommendations(preferences, limit // 2)
            
            # Combine and re-rank
            all_recommendations = content_recs + collab_recs
            
            # Remove duplicates based on game name
            unique_games = {}
            for rec in all_recommendations:
                game_id = rec["game"]["name"]
                if game_id not in unique_games:
                    unique_games[game_id] = rec
                else:
                    # Boost score for games found by both methods
                    unique_games[game_id]["recommendation_score"] *= 1.2
                    unique_games[game_id]["reason"] += " (found by multiple methods)"
            
            # Sort by recommendation score
            sorted_recommendations = sorted(unique_games.values(), key=lambda x: x["recommendation_score"], reverse=True)
            return sorted_recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error in hybrid recommendations: {e}")
            return []

    def _similar_games_recommendations(self, game_name: str, limit: int) -> list[dict[str, Any]]:
        """Find games similar to a specific game."""
        try:
            # Search for the specific game first
            game_results = self.vector_store.search_games(game_name, n_results=1)
            if not game_results:
                return []
            
            target_game = game_results[0]["game"]
            
            # Find similar games based on genre, platform, and publisher
            similar_queries = [
                f"{target_game.genre} games",
                f"games on {target_game.platform}",
                f"games by {target_game.publisher}"
            ]
            
            recommendations = []
            for query in similar_queries:
                results = self.vector_store.search_games(query, n_results=3)
                for result in results:
                    game = result["game"]
                    # Skip the target game itself
                    if game.name.lower() != target_game.name.lower():
                        recommendation_score = self._calculate_similarity_score(target_game, game)
                        
                        recommendations.append({
                            "game": game.model_dump(),
                            "recommendation_score": recommendation_score,
                            "similarity_score": result["similarity_score"],
                            "reason": f"Similar to {target_game.name} (same {query.split()[0]})",
                            "recommendation_type": "similar_games"
                        })
            
            # Remove duplicates and sort
            unique_games = {}
            for rec in recommendations:
                game_id = rec["game"]["name"]
                if game_id not in unique_games or rec["recommendation_score"] > unique_games[game_id]["recommendation_score"]:
                    unique_games[game_id] = rec
            
            sorted_recommendations = sorted(unique_games.values(), key=lambda x: x["recommendation_score"], reverse=True)
            return sorted_recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error in similar games recommendations: {e}")
            return []

    def _calculate_recommendation_score(self, game: Any, similarity_score: float, preferences: str) -> float:
        """Calculate recommendation score for a game."""
        base_score = similarity_score
        
        # Boost score for recent games
        try:
            current_year = 2024
            if game.year_of_release and int(game.year_of_release) >= current_year - 2:
                base_score += 0.1
        except (ValueError, TypeError):
            pass
        
        # Boost score for popular platforms
        popular_platforms = ["PlayStation", "Nintendo", "Xbox", "PC"]
        if any(platform in game.platform for platform in popular_platforms):
            base_score += 0.05
        
        # Boost score for popular genres
        popular_genres = ["Action", "RPG", "Adventure", "Racing"]
        if game.genre in popular_genres:
            base_score += 0.05
        
        return min(1.0, base_score)

    def _calculate_collaborative_score(self, game: Any, preferences: str) -> float:
        """Calculate collaborative filtering score."""
        base_score = 0.6  # Base score for collaborative filtering
        
        # Adjust based on game characteristics
        if game.genre in ["Action", "RPG", "Adventure"]:
            base_score += 0.2
        
        if "PlayStation" in game.platform or "Nintendo" in game.platform:
            base_score += 0.1
        
        return min(1.0, base_score)

    def _calculate_similarity_score(self, target_game: Any, candidate_game: Any) -> float:
        """Calculate similarity score between two games."""
        score = 0.0
        
        # Genre similarity
        if target_game.genre == candidate_game.genre:
            score += 0.4
        
        # Platform similarity
        if target_game.platform == candidate_game.platform:
            score += 0.3
        
        # Publisher similarity
        if target_game.publisher == candidate_game.publisher:
            score += 0.2
        
        # Year similarity (prefer games from similar era)
        try:
            if target_game.year_of_release and candidate_game.year_of_release:
                year_diff = abs(int(target_game.year_of_release) - int(candidate_game.year_of_release))
                if year_diff <= 2:
                    score += 0.1
        except (ValueError, TypeError):
            pass
        
        return min(1.0, score)

    def _extract_genre_keywords(self, preferences: str) -> list[str]:
        """Extract genre keywords from user preferences."""
        genres = ["Action", "RPG", "Adventure", "Racing", "Sports", "Fighting", "Puzzle", "Strategy"]
        found_genres = []
        
        preferences_lower = preferences.lower()
        for genre in genres:
            if genre.lower() in preferences_lower:
                found_genres.append(genre)
        
        return found_genres if found_genres else ["Action", "Adventure"]  # Default genres

    def _get_algorithm_description(self, algorithm: str) -> str:
        """Get description of the recommendation algorithm."""
        descriptions = {
            "content_based": "Recommends games based on similarity to your preferences and game characteristics",
            "collaborative": "Recommends games popular among users with similar tastes",
            "hybrid": "Combines content-based and collaborative filtering for better recommendations",
            "similar_games": "Finds games similar to a specific game you like"
        }
        return descriptions.get(algorithm, "Custom recommendation algorithm")

    def get_tool_definition(self) -> dict[str, Any]:
        """Get the tool definition for the agent.
        
        Returns:
            Dictionary containing tool metadata and schema
        """
        return {
            "type": "function",
            "function": {
                "name": "get_game_recommendations",
                "description": (
                    "Provides personalized game recommendations based on user preferences. "
                    "Uses various algorithms including content-based filtering, collaborative filtering, "
                    "and hybrid approaches to suggest games the user might enjoy."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_preferences": {
                            "type": "string",
                            "description": "User's gaming preferences (e.g., 'I like RPG games with fantasy themes', 'action games on PlayStation')"
                        },
                        "recommendation_type": {
                            "type": "string",
                            "description": "Type of recommendation algorithm to use",
                            "default": "content_based",
                            "enum": ["content_based", "collaborative", "hybrid", "similar_games"]
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of recommendations to return",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 10
                        }
                    },
                    "required": ["user_preferences"]
                }
            }
        }
