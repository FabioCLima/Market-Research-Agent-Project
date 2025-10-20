"""Trend Analysis Tool for Gaming Industry.

This tool analyzes gaming trends, market patterns, and industry insights
based on game data and temporal analysis.
"""

import json
from datetime import datetime, timedelta
from typing import Any

from src.database.vector_store import GameVectorStore
from src.utils.logger import logger


class TrendAnalysisTool:
    """Tool for analyzing gaming industry trends and patterns.
    
    This tool provides insights into:
    - Release patterns over time
    - Genre popularity trends
    - Platform market share
    - Publisher performance
    - Seasonal trends
    """

    def __init__(self, vector_store: GameVectorStore):
        """Initialize the trend analysis tool.
        
        Args:
            vector_store: Initialized GameVectorStore instance
        """
        self.vector_store = vector_store

    def __call__(self, analysis_type: str = "comprehensive", time_period: str = "all_time") -> str:
        """Analyze gaming trends based on specified criteria.
        
        Args:
            analysis_type: Type of analysis ("comprehensive", "genre_trends", "platform_trends", "publisher_trends")
            time_period: Time period for analysis ("all_time", "recent", "decade", "year")
            
        Returns:
            JSON string containing trend analysis results
        """
        try:
            analysis_results = {}
            
            if analysis_type == "comprehensive":
                analysis_results = self._comprehensive_analysis(time_period)
            elif analysis_type == "genre_trends":
                analysis_results = self._analyze_genre_trends(time_period)
            elif analysis_type == "platform_trends":
                analysis_results = self._analyze_platform_trends(time_period)
            elif analysis_type == "publisher_trends":
                analysis_results = self._analyze_publisher_trends(time_period)
            elif analysis_type == "release_patterns":
                analysis_results = self._analyze_release_patterns(time_period)
            else:
                analysis_results = self._comprehensive_analysis(time_period)

            return json.dumps({
                "trend_analysis": analysis_results,
                "analysis_type": analysis_type,
                "time_period": time_period,
                "analysis_date": datetime.now().isoformat(),
                "data_points": self._get_data_points_count(time_period)
            }, indent=2)

        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return json.dumps({
                "error": f"Trend analysis failed: {e!s}",
                "trend_analysis": {},
                "data_points": 0
            })

    def _comprehensive_analysis(self, time_period: str) -> dict[str, Any]:
        """Perform comprehensive trend analysis."""
        try:
            # Get all games for analysis
            all_games = self._get_games_for_period(time_period)
            
            analysis = {
                "genre_trends": self._analyze_genre_trends(time_period),
                "platform_trends": self._analyze_platform_trends(time_period),
                "publisher_trends": self._analyze_publisher_trends(time_period),
                "release_patterns": self._analyze_release_patterns(time_period),
                "market_insights": self._generate_market_insights(all_games),
                "key_findings": self._generate_key_findings(all_games)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return {}

    def _analyze_genre_trends(self, time_period: str) -> dict[str, Any]:
        """Analyze genre popularity trends."""
        try:
            games = self._get_games_for_period(time_period)
            
            genre_counts = {}
            genre_years = {}
            
            for game in games:
                genre = game.get("genre", "Unknown")
                year = game.get("year_of_release", "Unknown")
                
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
                
                if genre not in genre_years:
                    genre_years[genre] = []
                genre_years[genre].append(year)
            
            # Calculate trends
            genre_trends = {}
            for genre, years in genre_years.items():
                recent_years = [y for y in years if y != "Unknown" and int(y) >= 2020]
                total_games = len(years)
                recent_games = len(recent_years)
                
                trend_direction = "stable"
                if recent_games > total_games * 0.3:
                    trend_direction = "growing"
                elif recent_games < total_games * 0.1:
                    trend_direction = "declining"
                
                genre_trends[genre] = {
                    "total_games": total_games,
                    "recent_games": recent_games,
                    "trend_direction": trend_direction,
                    "popularity_score": total_games / len(games) if games else 0
                }
            
            # Sort by popularity
            sorted_genres = sorted(genre_trends.items(), key=lambda x: x[1]["popularity_score"], reverse=True)
            
            return {
                "genre_distribution": dict(sorted_genres),
                "top_genres": [genre for genre, _ in sorted_genres[:5]],
                "trending_genres": [genre for genre, data in sorted_genres if data["trend_direction"] == "growing"],
                "declining_genres": [genre for genre, data in sorted_genres if data["trend_direction"] == "declining"]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing genre trends: {e}")
            return {}

    def _analyze_platform_trends(self, time_period: str) -> dict[str, Any]:
        """Analyze platform market trends."""
        try:
            games = self._get_games_for_period(time_period)
            
            platform_counts = {}
            platform_years = {}
            
            for game in games:
                platform = game.get("platform", "Unknown")
                year = game.get("year_of_release", "Unknown")
                
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
                
                if platform not in platform_years:
                    platform_years[platform] = []
                platform_years[platform].append(year)
            
            # Analyze platform evolution
            platform_analysis = {}
            for platform, years in platform_years.items():
                recent_years = [y for y in years if y != "Unknown" and int(y) >= 2020]
                total_games = len(years)
                recent_games = len(recent_years)
                
                market_share = total_games / len(games) if games else 0
                
                platform_analysis[platform] = {
                    "total_games": total_games,
                    "recent_games": recent_games,
                    "market_share": market_share,
                    "activity_level": "high" if recent_games > 2 else "medium" if recent_games > 0 else "low"
                }
            
            # Sort by market share
            sorted_platforms = sorted(platform_analysis.items(), key=lambda x: x[1]["market_share"], reverse=True)
            
            return {
                "platform_distribution": dict(sorted_platforms),
                "market_leaders": [platform for platform, _ in sorted_platforms[:3]],
                "emerging_platforms": [platform for platform, data in sorted_platforms if data["activity_level"] == "high" and data["recent_games"] > data["total_games"] * 0.5],
                "total_platforms": len(platform_counts)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing platform trends: {e}")
            return {}

    def _analyze_publisher_trends(self, time_period: str) -> dict[str, Any]:
        """Analyze publisher performance and trends."""
        try:
            games = self._get_games_for_period(time_period)
            
            publisher_counts = {}
            publisher_years = {}
            
            for game in games:
                publisher = game.get("publisher", "Unknown")
                year = game.get("year_of_release", "Unknown")
                
                publisher_counts[publisher] = publisher_counts.get(publisher, 0) + 1
                
                if publisher not in publisher_years:
                    publisher_years[publisher] = []
                publisher_years[publisher].append(year)
            
            # Analyze publisher performance
            publisher_analysis = {}
            for publisher, years in publisher_years.items():
                recent_years = [y for y in years if y != "Unknown" and int(y) >= 2020]
                total_games = len(years)
                recent_games = len(recent_years)
                
                productivity_score = total_games / len(games) if games else 0
                
                publisher_analysis[publisher] = {
                    "total_games": total_games,
                    "recent_games": recent_games,
                    "productivity_score": productivity_score,
                    "activity_level": "high" if recent_games > 1 else "medium" if recent_games > 0 else "low"
                }
            
            # Sort by productivity
            sorted_publishers = sorted(publisher_analysis.items(), key=lambda x: x[1]["productivity_score"], reverse=True)
            
            return {
                "publisher_distribution": dict(sorted_publishers),
                "top_publishers": [publisher for publisher, _ in sorted_publishers[:5]],
                "most_active_publishers": [publisher for publisher, data in sorted_publishers if data["activity_level"] == "high"],
                "total_publishers": len(publisher_counts)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing publisher trends: {e}")
            return {}

    def _analyze_release_patterns(self, time_period: str) -> dict[str, Any]:
        """Analyze release patterns and timing trends."""
        try:
            games = self._get_games_for_period(time_period)
            
            year_counts = {}
            month_patterns = {}
            
            for game in games:
                year = game.get("year_of_release", "Unknown")
                if year != "Unknown":
                    year_counts[year] = year_counts.get(year, 0) + 1
                    
                    # Simulate month analysis (in real implementation, you'd have month data)
                    month = "Q4"  # Most games release in Q4
                    month_patterns[month] = month_patterns.get(month, 0) + 1
            
            # Find peak years
            peak_years = sorted(year_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
            return {
                "yearly_releases": dict(sorted(year_counts.items())),
                "peak_release_years": [year for year, _ in peak_years],
                "release_patterns": month_patterns,
                "total_games_analyzed": len(games),
                "release_trend": "increasing" if len(peak_years) > 0 and peak_years[0][0] >= "2020" else "stable"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing release patterns: {e}")
            return {}

    def _generate_market_insights(self, games: list[dict[str, Any]]) -> dict[str, Any]:
        """Generate market insights and predictions."""
        try:
            if not games:
                return {"insights": [], "predictions": []}
            
            insights = []
            predictions = []
            
            # Analyze genre diversity
            genres = set(game.get("genre", "Unknown") for game in games)
            if len(genres) > 5:
                insights.append("High genre diversity indicates a healthy, varied gaming market")
            
            # Analyze platform distribution
            platforms = set(game.get("platform", "Unknown") for game in games)
            if len(platforms) > 3:
                insights.append("Multi-platform presence suggests strong market competition")
            
            # Predict trends
            recent_games = [game for game in games if game.get("year_of_release", "0") >= "2020"]
            if len(recent_games) > len(games) * 0.3:
                predictions.append("Gaming industry shows strong growth momentum")
            
            return {
                "insights": insights,
                "predictions": predictions,
                "market_health_score": min(1.0, len(genres) / 10 + len(platforms) / 5)
            }
            
        except Exception as e:
            logger.error(f"Error generating market insights: {e}")
            return {"insights": [], "predictions": []}

    def _generate_key_findings(self, games: list[dict[str, Any]]) -> list[str]:
        """Generate key findings from the analysis."""
        try:
            findings = []
            
            if not games:
                return ["No games data available for analysis"]
            
            # Most popular genre
            genres = [game.get("genre", "Unknown") for game in games]
            genre_counts = {}
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            
            most_popular_genre = max(genre_counts.items(), key=lambda x: x[1])
            findings.append(f"Most popular genre: {most_popular_genre[0]} ({most_popular_genre[1]} games)")
            
            # Most active platform
            platforms = [game.get("platform", "Unknown") for game in games]
            platform_counts = {}
            for platform in platforms:
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
            
            most_active_platform = max(platform_counts.items(), key=lambda x: x[1])
            findings.append(f"Most active platform: {most_active_platform[0]} ({most_active_platform[1]} games)")
            
            # Recent activity
            recent_games = [game for game in games if game.get("year_of_release", "0") >= "2020"]
            if recent_games:
                findings.append(f"Recent activity: {len(recent_games)} games released since 2020")
            
            return findings
            
        except Exception as e:
            logger.error(f"Error generating key findings: {e}")
            return ["Error generating key findings"]

    def _get_games_for_period(self, time_period: str) -> list[dict[str, Any]]:
        """Get games data for the specified time period."""
        try:
            # This is a simplified implementation
            # In a real system, you'd query the database with time filters
            
            # For now, get all games and filter by time period
            all_games = []
            
            # Search for games from different eras
            search_queries = [
                "games from 1990s",
                "games from 2000s", 
                "games from 2010s",
                "games from 2020s"
            ]
            
            for query in search_queries:
                results = self.vector_store.search_games(query, n_results=10)
                for result in results:
                    game_data = result["game"].model_dump()
                    all_games.append(game_data)
            
            # Filter by time period if needed
            if time_period == "recent":
                current_year = datetime.now().year
                all_games = [game for game in all_games if game.get("year_of_release", "0") >= str(current_year - 2)]
            elif time_period == "decade":
                all_games = [game for game in all_games if game.get("year_of_release", "0") >= "2010"]
            
            return all_games
            
        except Exception as e:
            logger.error(f"Error getting games for period: {e}")
            return []

    def _get_data_points_count(self, time_period: str) -> int:
        """Get count of data points used in analysis."""
        try:
            games = self._get_games_for_period(time_period)
            return len(games)
        except Exception:
            return 0

    def get_tool_definition(self) -> dict[str, Any]:
        """Get the tool definition for the agent.
        
        Returns:
            Dictionary containing tool metadata and schema
        """
        return {
            "type": "function",
            "function": {
                "name": "analyze_gaming_trends",
                "description": (
                    "Analyzes gaming industry trends, market patterns, and insights. "
                    "Provides comprehensive analysis of genre trends, platform market share, "
                    "publisher performance, release patterns, and market predictions."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_type": {
                            "type": "string",
                            "description": "Type of trend analysis to perform",
                            "default": "comprehensive",
                            "enum": ["comprehensive", "genre_trends", "platform_trends", "publisher_trends", "release_patterns"]
                        },
                        "time_period": {
                            "type": "string",
                            "description": "Time period for analysis",
                            "default": "all_time",
                            "enum": ["all_time", "recent", "decade", "year"]
                        }
                    },
                    "required": []
                }
            }
        }
