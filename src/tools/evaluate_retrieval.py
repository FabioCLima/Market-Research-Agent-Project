import json
from typing import Any

from openai import OpenAI

from src.models.game import EvaluationReport
from src.utils.logger import logger


class EvaluateRetrievalTool:
    """Tool for evaluating the quality and usefulness of retrieved game information.
    
    This tool uses an LLM as a judge to assess whether the retrieved documents
    are sufficient to answer the user's question, providing confidence scores
    and recommendations for next actions.
    """

    def __init__(self, api_key: str = None):
        """Initialize the evaluation tool.
        
        Args:
            api_key: OpenAI API key (if None, uses environment variable)

        """
        self.client = OpenAI(api_key=api_key)

    def __call__(self, question: str, retrieved_docs: str) -> str:
        """Evaluate the usefulness of retrieved documents for answering a question.
        
        Args:
            question: Original question from user
            retrieved_docs: Retrieved documents (JSON string from retrieve_game tool)
            
        Returns:
            JSON string containing evaluation report

        """
        try:
            # Parse retrieved documents
            docs_data = json.loads(retrieved_docs)
            games = docs_data.get("games", [])

            if not games:
                logger.debug("No games retrieved; recommending web search")
                return self._create_evaluation_report(
                    useful=False,
                    description="No games were retrieved from the database",
                    confidence=0.0,
                    recommendation="search_web"
                )

            # Create context for evaluation
            context = self._create_evaluation_context(question, games)

            # Use LLM as judge
            evaluation_prompt = self._create_evaluation_prompt(question, context)

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert evaluator for a video game research system. "
                            "Your task is to evaluate if the retrieved game documents are "
                            "sufficient to answer the user's question. Give a detailed "
                            "explanation so it's possible to take appropriate action."
                        )
                    },
                    {
                        "role": "user",
                        "content": evaluation_prompt
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            # Parse LLM response
            evaluation_data = json.loads(response.choices[0].message.content)

            return self._create_evaluation_report(
                useful=evaluation_data.get("useful", False),
                description=evaluation_data.get("description", ""),
                confidence=evaluation_data.get("confidence", 0.0),
                recommendation=evaluation_data.get("recommendation", "search_web")
            )

        except Exception as e:
            logger.error(f"Error during evaluation: {e}")
            return self._create_evaluation_report(
                useful=False,
                description=f"Error during evaluation: {e!s}",
                confidence=0.0,
                recommendation="search_web"
            )

    def _create_evaluation_context(self, question: str, games: list[dict[str, Any]]) -> str:
        """Create context string from retrieved games."""
        context_parts = [f"User Question: {question}\n\nRetrieved Games:"]

        for i, game in enumerate(games, 1):
            context_parts.append(
                f"{i}. {game['name']} ({game['platform']}, {game['year_of_release']})\n"
                f"   Genre: {game['genre']}\n"
                f"   Publisher: {game['publisher']}\n"
                f"   Description: {game['description']}"
            )

        return "\n\n".join(context_parts)

    def _create_evaluation_prompt(self, question: str, context: str) -> str:
        """Create the evaluation prompt for the LLM judge."""
        return f"""
{context}

Please evaluate whether the retrieved game information is sufficient to answer the user's question. Consider:

1. **Relevance**: Do the retrieved games directly relate to what the user is asking?
2. **Completeness**: Is there enough information to provide a comprehensive answer?
3. **Accuracy**: Are the game details accurate and up-to-date?
4. **Specificity**: Does the information match the specific aspects of the question?

IMPORTANT: If the retrieved games contain relevant information that can answer the user's question (even partially), mark as useful. Only recommend web search if:
- No games match the query at all
- The question is about very recent games not in the database
- The question requires current/real-time information (sales, reviews, etc.)
- The question is about technical details not covered in descriptions

Respond with a JSON object containing:
- "useful": boolean - whether the documents are sufficient to answer the question
- "description": string - detailed explanation of your evaluation
- "confidence": float (0.0-1.0) - your confidence in this evaluation
- "recommendation": string - next action ("proceed_with_answer" or "search_web")

Examples of when to recommend "proceed_with_answer":
- Question about game release dates, platforms, genres, publishers
- Question about game descriptions and characteristics
- Question about games that are in the database
- Question about game series or franchises

Examples of when to recommend "search_web":
- Question about very recent games (2024+)
- Question about game sales numbers or current reviews
- Question about technical specifications not in descriptions
- Question about games from publishers not in the database
"""

    def _create_evaluation_report(self, useful: bool, description: str,
                                confidence: float, recommendation: str) -> str:
        """Create a standardized evaluation report."""
        report = EvaluationReport(
            useful=useful,
            description=description,
            confidence=confidence,
            recommendation=recommendation
        )
        return report.model_dump_json(indent=2)

    def get_tool_definition(self) -> dict[str, Any]:
        """Get the tool definition for the agent.
        
        Returns:
            Dictionary containing tool metadata and schema

        """
        return {
            "type": "function",
            "function": {
                "name": "evaluate_retrieval",
                "description": (
                    "Evaluates the quality and usefulness of retrieved game documents "
                    "to determine if they are sufficient to answer the user's question. "
                    "Uses an LLM judge to assess relevance, completeness, and accuracy. "
                    "Provides confidence scores and recommendations for next actions."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The original question from the user"
                        },
                        "retrieved_docs": {
                            "type": "string",
                            "description": "The retrieved documents from the vector database (JSON string)"
                        }
                    },
                    "required": ["question", "retrieved_docs"]
                }
            }
        }
