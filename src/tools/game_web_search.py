import json
from typing import Any

from tavily import TavilyClient

from src.models.game import WebSearchResult
from src.utils.logger import logger


class GameWebSearchTool:
    """Tool for searching the web for additional game information.
    
    This tool uses the Tavily API to perform web searches when the local
    vector database doesn't contain sufficient information to answer
    user questions about games.
    """

    def __init__(self, api_key: str = None):
        """Initialize the web search tool.
        
        Args:
            api_key: Tavily API key (if None, uses environment variable)

        """
        # Use provided API key or environment variable
        key = api_key
        if key is None:
            import os

            key = os.getenv("TAVILY_API_KEY")

        self.client = TavilyClient(api_key=key)

    def __call__(self, question: str, max_results: int = 5) -> str:
        """Search the web for game-related information.
        
        Args:
            question: Question about games to search for
            max_results: Maximum number of search results to return
            
        Returns:
            JSON string containing search results

        """
        try:
            # Enhance query for better game-related results
            enhanced_query = self._enhance_query(question)

            # Perform web search
            search_results = self.client.search(
                query=enhanced_query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=True,
                include_raw_content=False
            )

            # Process results
            web_results = []

            if search_results.get("results"):
                for result in search_results["results"]:
                    web_result = WebSearchResult(
                        title=result.get("title", ""),
                        url=result.get("url", ""),
                        content=result.get("content", ""),
                        relevance_score=result.get("score", 0.0)
                    )
                    web_results.append(web_result.model_dump())

            # Include answer if available
            answer_content = search_results.get("answer", "")

            return json.dumps({
                "question": question,
                "enhanced_query": enhanced_query,
                "results": web_results,
                "answer": answer_content,
                "total_results": len(web_results),
                "search_method": "web_search"
            }, indent=2)

        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return json.dumps({
                "error": f"Error performing web search: {e!s}",
                "question": question,
                "results": [],
                "total_results": 0,
                "search_method": "web_search"
            })

    def _enhance_query(self, question: str) -> str:
        """Enhance the query for better game-related search results.
        
        Args:
            question: Original user question
            
        Returns:
            Enhanced query string

        """
        # Add game-related context to improve search relevance
        enhanced_query = question

        # Add video game context if not already present
        game_keywords = ["game", "video game", "gaming", "gamer", "console", "platform"]
        if not any(keyword in question.lower() for keyword in game_keywords):
            enhanced_query = f"{question} video game"

        # Add specific gaming sites for better results
        enhanced_query += " site:ign.com OR site:gamespot.com OR site:metacritic.com OR site:wikipedia.org"

        return enhanced_query

    def get_tool_definition(self) -> dict[str, Any]:
        """Get the tool definition for the agent.
        
        Returns:
            Dictionary containing tool metadata and schema

        """
        return {
            "type": "function",
            "function": {
                "name": "game_web_search",
                "description": (
                    "Searches the web for current and additional game information "
                    "when local knowledge is insufficient. Use this tool when "
                    "the vector database doesn't contain enough information to "
                    "answer the user's question about games, publishers, platforms, "
                    "or gaming industry topics."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The question about games that needs web search"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of search results to return (default: 5, max: 10)",
                            "default": 5,
                            "minimum": 1,
                            "maximum": 10
                        }
                    },
                    "required": ["question"]
                }
            }
        }
