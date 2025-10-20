import json
import os
from datetime import datetime
from typing import Any

from openai import OpenAI  # type: ignore
from openai.types.chat import ChatCompletion  # type: ignore

from src.agent.state_machine import AgentStateMachine
from src.config.settings import Settings
from src.database.vector_store import GameVectorStore
from src.models.game import AgentResponse
from src.tools.evaluate_retrieval import EvaluateRetrievalTool
from src.tools.game_web_search import GameWebSearchTool
from src.tools.retrieve_game import RetrieveGameTool
from src.tools.sentiment_analysis import SentimentAnalysisTool
from src.tools.trending_games import TrendingGamesTool
from src.tools.game_recommendation import GameRecommendationTool
from src.tools.trend_analysis import TrendAnalysisTool
from src.tools.advanced_memory import AdvancedMemorySystem
from src.tools.structured_output import StructuredOutputSystem
from src.utils.logger import logger


class UdaPlayAgent:
    """UdaPlay AI Research Agent for video game industry questions.

    This agent implements a two-tier information retrieval system:
    1. Primary: RAG over local game database using vector search
    2. Secondary: Web search using Tavily API when local knowledge is insufficient

    The agent maintains conversation state and provides structured, 
    well-cited responses with confidence scores.
    """

    def __init__(self, vector_store: GameVectorStore, openai_api_key: str | None = None, tavily_api_key: str | None = None):
        """Initialize the UdaPlay agent.

        Args:
            vector_store: Initialized GameVectorStore instance
            openai_api_key: OpenAI API key (if None, uses environment variable)
            tavily_api_key: Tavily API key (if None, uses environment variable)

        """
        # Validate settings (non-blocking by default)
        Settings.validate(require_keys=False)

        # Initialize OpenAI client (allow override via parameter)
        self.openai_client: OpenAI = OpenAI(api_key=openai_api_key or Settings.OPENAI_API_KEY)

        # Initialize tools
        self.retrieve_game_tool: RetrieveGameTool = RetrieveGameTool(vector_store)
        self.evaluate_retrieval_tool: EvaluateRetrievalTool = EvaluateRetrievalTool(openai_api_key or Settings.OPENAI_API_KEY)
        self.game_web_search_tool: GameWebSearchTool = GameWebSearchTool(tavily_api_key or Settings.TAVILY_API_KEY)
        self.sentiment_analysis_tool: SentimentAnalysisTool = SentimentAnalysisTool(openai_api_key or Settings.OPENAI_API_KEY)
        self.trending_games_tool: TrendingGamesTool = TrendingGamesTool(vector_store)
        self.game_recommendation_tool: GameRecommendationTool = GameRecommendationTool(vector_store)
        self.trend_analysis_tool: TrendAnalysisTool = TrendAnalysisTool(vector_store)
        self.advanced_memory_system: AdvancedMemorySystem = AdvancedMemorySystem()
        self.structured_output_system: StructuredOutputSystem = StructuredOutputSystem()

        # Agent instructions
        self.system_instructions: str = self._create_system_instructions()

        # Conversation history
        self.conversation_history: list[dict[str, str]] = []

        # State machine
        self.state_machine = AgentStateMachine()
        # Attempt to load persisted state if available in the vector store persist directory
        try:
            persist_dir = getattr(vector_store, "persist_directory", None)
            if persist_dir:
                state_file = os.path.join(persist_dir, "state.json")
                if os.path.exists(state_file):
                    self.state_machine.load_from_file(state_file)
                else:
                    # ensure state machine knows the intended persist file so
                    # subsequent calls to persist() will write to the correct location
                    # even if the file does not yet exist.
                    self.state_machine._persist_file = state_file
        except Exception:
            # non-fatal if loading fails
            logger.debug("No persisted state loaded for state machine")

    def _create_system_instructions(self) -> str:
        """Create system instructions for the agent."""
        return """You are UdaPlay, an AI Research Agent specializing in the video game industry. 

Your capabilities:
1. Answer questions about games using internal knowledge (vector database)
2. Search the web when internal knowledge is insufficient
3. Provide structured, well-cited responses
4. Maintain conversation context and state

Available tools:
- retrieve_game: Search the local game database for relevant games
- evaluate_retrieval: Assess if retrieved information is sufficient to answer the question
- game_web_search: Search the web for additional information when needed
- analyze_sentiment: Analyze sentiment of game reviews and user feedback
- detect_trending_games: Identify trending games based on various criteria
- get_game_recommendations: Provide personalized game recommendations
- analyze_gaming_trends: Analyze gaming industry trends and patterns
- learn_from_interaction: Learn from user interactions and web searches
- generate_structured_output: Generate responses in multiple formats

Workflow:
1. First, try to retrieve relevant games from the local database
2. Evaluate if the retrieved information is sufficient to answer the question
3. If not sufficient, search the web for additional information
4. Provide a comprehensive answer with proper citations and confidence scores

Always be helpful, accurate, and provide detailed information about games including:
- Game titles, platforms, genres, publishers
- Release dates and years
- Game descriptions and characteristics
- Any relevant gaming industry context

When you don't have enough information, clearly state this and explain what additional information would be helpful."""

    def process_query(self, user_question: str) -> AgentResponse:
        """Process a user query and return a structured response.

        Args:
            user_question: The user's question about games

        Returns:
            AgentResponse with answer, confidence, sources, and metadata

        """
        try:
            # Step 1: Retrieve games from local database
            print(f"[UdaPlay] Processing query: {user_question}")

            # Use retrieve_game tool
            retrieval_result = self.retrieve_game_tool(user_question, n_results=5)
            retrieval_data = json.loads(retrieval_result)

            print(f"[UdaPlay] Retrieved {retrieval_data.get('total_results', 0)} games from database")

            # Step 2: Evaluate retrieval quality
            evaluation_result = self.evaluate_retrieval_tool(user_question, retrieval_result)
            evaluation_data = json.loads(evaluation_result)

            print(f"[UdaPlay] Evaluation: {evaluation_data.get('useful', False)} (confidence: {evaluation_data.get('confidence', 0.0)})")

            # Step 3: Determine if web search is needed
            use_web_search = not evaluation_data.get("useful", False) or evaluation_data.get("confidence", 0.0) < 0.7

            web_results = None
            if use_web_search:
                print("[UdaPlay] Local knowledge insufficient, searching web...")
                web_search_result = self.game_web_search_tool(user_question, max_results=3)
                web_results = json.loads(web_search_result)
                print(f"[UdaPlay] Found {web_results.get('total_results', 0)} web results")

            # Step 4: Generate final answer using LLM
            final_answer = self._generate_final_answer(
                user_question,
                retrieval_data,
                evaluation_data,
                web_results
            )

            # Step 5: Create response object
            response = AgentResponse(
                answer=final_answer["answer"],
                confidence=final_answer["confidence"],
                sources=final_answer["sources"],
                search_method=final_answer["search_method"]
            )

            # Persist web results into vector store if available (with richer metadata)
            try:
                if web_results and web_results.get("results"):
                    for r in web_results["results"]:
                        metadata = {
                            "title": r.get("title", ""),
                            "url": r.get("url", ""),
                            "source": "web_search",
                            "relevance_score": r.get("relevance_score", r.get("score", None))
                        }
                        added = self.retrieve_game_tool.vector_store.add_document(r.get("content", ""), metadata)
                        if not added:
                            logger.debug("Skipped adding duplicate web document")
                    
                    # Learn from web search results
                    self.advanced_memory_system.learn_from_web_search(user_question, web_results)
            except Exception as e:
                logger.error(f"Failed to persist web results: {e}")
            
            # Learn from conversation interaction
            try:
                self.advanced_memory_system.learn_from_conversation(user_question, final_answer["answer"])
            except Exception as e:
                logger.error(f"Failed to learn from conversation: {e}")

            # Update conversation history
            self.conversation_history.append({
                "user": user_question,
                "assistant": final_answer["answer"],
                "timestamp": datetime.now().isoformat()
            })

            # Persist state machine after processing the query so that state.json
            # is kept up-to-date (explicit save in addition to automatic saves on transitions)
            try:
                self.state_machine.persist()
            except Exception:
                logger.debug("Failed to explicitly persist state machine after process_query")

            return response

        except Exception as e:
            error_response = AgentResponse(
                answer=f"I encountered an error while processing your question: {e!s}",
                confidence=0.0,
                sources=[],
                search_method="error"
            )
            return error_response

    def _generate_final_answer(self, question: str, retrieval_data: dict[str, Any],
                             evaluation_data: dict[str, Any], web_results: dict[str, Any] | None) -> dict[str, Any]:
        """Generate the final answer using LLM with all available information."""
        # Prepare context for LLM
        context_parts: list[str] = []
        sources: list[str] = []
        search_method: str = "vector_db"

        # Add local database results
        if retrieval_data.get("games"):
            context_parts.append("LOCAL GAME DATABASE RESULTS:")
            for game in retrieval_data["games"]:
                context_parts.append(
                    f"- {game['name']} ({game['platform']}, {game['year_of_release']})\n"
                    f"  Genre: {game['genre']}, Publisher: {game['publisher']}\n"
                    f"  Description: {game['description']}"
                )
            sources.append("vector_db")

        # Add web search results
        if web_results and web_results.get("results"):
            context_parts.append("\nWEB SEARCH RESULTS:")
            for result in web_results["results"][:3]:  # Top 3 results
                context_parts.append(
                    f"- {result['title']}\n"
                    f"  URL: {result['url']}\n"
                    f"  Content: {result['content'][:200]}..."
                )
            sources.append("web_search")
            search_method = "combined" if sources else "web_search"

        # Add evaluation information
        context_parts.append(f"\nEVALUATION: {evaluation_data.get('description', '')}")

        context = "\n".join(context_parts)

        # Create prompt for final answer generation
        prompt = f"""Based on the following information, provide a comprehensive and accurate answer to the user's question about games.

USER QUESTION: {question}

AVAILABLE INFORMATION:
{context}

INSTRUCTIONS:
1. Provide a clear, detailed answer based on the available information
2. Include specific game details (titles, platforms, years, genres, publishers)
3. Cite your sources (local database, web search, etc.)
4. If information is limited, acknowledge this and suggest what additional information might be helpful
5. Be conversational but informative
6. End with a confidence level (0.0 to 1.0) for your answer

ANSWER:"""

        # Generate answer using LLM
        response: ChatCompletion = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are UdaPlay, a knowledgeable gaming industry expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        answer_text: str | None = response.choices[0].message.content

        # Extract confidence from answer (look for confidence score at the end)
        confidence: float = 0.8  # Default confidence
        if answer_text and "confidence:" in answer_text.lower():
            try:
                confidence_part = answer_text.lower().split("confidence:")[-1].strip()
                confidence = float(confidence_part.split()[0])
            except (ValueError, IndexError):
                pass

        return {
            "answer": answer_text or "No response generated",
            "confidence": confidence,
            "sources": sources,
            "search_method": search_method
        }

    def get_conversation_history(self) -> list[dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history.copy()

    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history.clear()

    def get_game_recommendations(self, user_preferences: str, recommendation_type: str = "content_based", limit: int = 5) -> str:
        """Get personalized game recommendations."""
        return self.game_recommendation_tool(user_preferences, recommendation_type, limit)

    def analyze_gaming_trends(self, analysis_type: str = "comprehensive", time_period: str = "all_time") -> str:
        """Analyze gaming industry trends."""
        return self.trend_analysis_tool(analysis_type, time_period)

    def analyze_sentiment(self, text: str, game_title: str | None = None) -> str:
        """Analyze sentiment of game reviews or feedback."""
        return self.sentiment_analysis_tool(text, game_title)

    def detect_trending_games(self, criteria: str = "recent_high_rated", limit: int = 10) -> str:
        """Detect trending games based on various criteria."""
        return self.trending_games_tool(criteria, limit)

    def generate_structured_response(self, response: AgentResponse, output_format: str = "standard") -> dict[str, Any]:
        """Generate structured response in multiple formats."""
        return self.structured_output_system.generate_structured_response(response, output_format)

    def get_memory_stats(self) -> dict[str, Any]:
        """Get memory system statistics."""
        return self.advanced_memory_system.get_memory_stats()

    def get_learned_facts(self, topic: str = None) -> list[dict[str, Any]]:
        """Get learned facts from memory system."""
        return self.advanced_memory_system.get_learned_facts(topic)

    def get_personalized_recommendations(self, user_id: str = "default") -> dict[str, Any]:
        """Get personalized recommendations based on learned preferences."""
        return self.advanced_memory_system.get_personalized_recommendations(user_id)

    def get_agent_info(self) -> dict[str, Any]:
        """Get information about the agent."""
        return {
            "name": "UdaPlay",
            "version": "2.0.0",
            "description": "Advanced AI Research Agent for video game industry questions",
            "capabilities": [
                "Local game database search",
                "Web search for additional information",
                "Structured response generation",
                "Conversation state management",
                "Personalized recommendations",
                "Trend analysis",
                "Sentiment analysis",
                "Advanced memory and learning",
                "Multi-format output generation"
            ],
            "tools": [
                "retrieve_game",
                "evaluate_retrieval",
                "game_web_search",
                "analyze_sentiment",
                "detect_trending_games",
                "get_game_recommendations",
                "analyze_gaming_trends",
                "learn_from_interaction",
                "generate_structured_output"
            ],
            "advanced_features": [
                "Persistent learning from interactions",
                "User preference profiling",
                "Trend analysis and predictions",
                "Multi-format output (JSON, API, Webhook)",
                "Real-time analytics dashboard",
                "Memory-based recommendations"
            ]
        }
