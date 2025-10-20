"""Sentiment Analysis Tool for Game Reviews.

This tool analyzes the sentiment of game reviews and user feedback
to provide insights about game reception and player satisfaction.
"""

import json
from typing import Any

from src.utils.logger import logger


class SentimentAnalysisTool:
    """Tool for analyzing sentiment of game reviews and user feedback.
    
    This tool uses OpenAI's language model to analyze sentiment
    of game reviews, user comments, and feedback to provide
    insights about game reception and player satisfaction.
    """

    def __init__(self, openai_api_key: str | None = None):
        """Initialize the sentiment analysis tool.
        
        Args:
            openai_api_key: OpenAI API key (if None, uses environment variable)
        """
        try:
            from openai import OpenAI  # type: ignore
            from src.config.settings import Settings
            
            self.openai_client = OpenAI(api_key=openai_api_key or Settings.OPENAI_API_KEY)
        except ImportError:
            logger.warning("OpenAI not available for sentiment analysis")
            self.openai_client = None

    def __call__(self, text: str, game_title: str | None = None) -> str:
        """Analyze sentiment of game-related text.
        
        Args:
            text: Text to analyze (review, comment, feedback)
            game_title: Optional game title for context
            
        Returns:
            JSON string containing sentiment analysis results
        """
        if not self.openai_client:
            return json.dumps({
                "error": "OpenAI client not available",
                "sentiment": "unknown",
                "confidence": 0.0
            })

        try:
            # Create prompt for sentiment analysis
            context = f" for {game_title}" if game_title else ""
            prompt = f"""Analyze the sentiment of this game review{context}:

Text: "{text}"

Provide:
1. Overall sentiment (positive, negative, neutral)
2. Confidence score (0.0 to 1.0)
3. Key positive aspects mentioned
4. Key negative aspects mentioned
5. Overall rating suggestion (1-10 scale)

Format as JSON with keys: sentiment, confidence, positive_aspects, negative_aspects, suggested_rating"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing game review sentiment. Be objective and thorough."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            result_text = response.choices[0].message.content or "{}"
            
            # Try to parse as JSON, fallback to structured response
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Fallback structured response
                result = {
                    "sentiment": "neutral",
                    "confidence": 0.5,
                    "positive_aspects": [],
                    "negative_aspects": [],
                    "suggested_rating": 5,
                    "raw_analysis": result_text
                }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return json.dumps({
                "error": f"Sentiment analysis failed: {e!s}",
                "sentiment": "unknown",
                "confidence": 0.0
            })

    def get_tool_definition(self) -> dict[str, Any]:
        """Get the tool definition for the agent.
        
        Returns:
            Dictionary containing tool metadata and schema
        """
        return {
            "type": "function",
            "function": {
                "name": "analyze_sentiment",
                "description": (
                    "Analyzes sentiment of game reviews, user feedback, or comments. "
                    "Provides sentiment classification (positive/negative/neutral), "
                    "confidence score, key aspects mentioned, and suggested rating. "
                    "Useful for understanding player reception and satisfaction."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The review text, comment, or feedback to analyze"
                        },
                        "game_title": {
                            "type": "string",
                            "description": "Optional game title for better context analysis",
                            "default": None
                        }
                    },
                    "required": ["text"]
                }
            }
        }
