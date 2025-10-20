#!/usr/bin/env python3
"""UdaPlay AI Research Agent - Main Application

This is the main entry point for the UdaPlay AI Research Agent,
a system designed to answer questions about video games using
both local knowledge and web search capabilities.
"""

import sys
from pathlib import Path

from src.utils.logger import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from agent.udaplay_agent import UdaPlayAgent
from config.settings import Settings
from database.vector_store import GameVectorStore


def initialize_vector_store() -> GameVectorStore:
    """Initialize and populate the vector store with game data."""
    logger.info("Initializing vector store...")

    vector_store = GameVectorStore(
        collection_name=Settings.COLLECTION_NAME,
        persist_directory=Settings.get_database_path()
    )

    # Check if collection is empty and load games if needed
    stats = vector_store.get_collection_stats()
    if stats.get("total_games", 0) == 0:
        logger.info("Loading games from directory...")
        games_loaded = vector_store.load_games_from_directory(Settings.GAMES_DIRECTORY)
        logger.info(f"Loaded {games_loaded} games into vector store")
    else:
        logger.info(f"Vector store already contains {stats['total_games']} games")

    return vector_store


def create_agent() -> UdaPlayAgent:
    """Create and initialize the UdaPlay agent."""
    logger.info("Creating UdaPlay agent...")

    # Initialize vector store
    vector_store = initialize_vector_store()

    # Create agent
    agent = UdaPlayAgent(
        vector_store=vector_store,
        openai_api_key=Settings.OPENAI_API_KEY,
        tavily_api_key=Settings.TAVILY_API_KEY
    )

    logger.info("UdaPlay agent initialized successfully!")
    return agent


def main():
    """Main application entry point."""
    logger.info("=" * 60)
    logger.info("🎮 UdaPlay AI Research Agent")
    logger.info("=" * 60)
    # Show basic usage/instruction messages immediately so the user knows how to interact
    logger.info("\n" + "=" * 60)
    logger.info("Ask me anything about video games!")
    logger.info("Type 'quit', 'exit', or 'q' to stop")
    logger.info("Type 'history' to see conversation history")
    logger.info("Type 'clear' to clear conversation history")
    logger.info("=" * 60)

    try:
        # Validate required settings (API keys) before runtime
        Settings.validate(require_keys=True)

        # Create agent
        agent = create_agent()

        # Display agent info
        info = agent.get_agent_info()
        logger.info(f"\n{info['name']} v{info['version']}")
        logger.info(f"Description: {info['description']}")
        logger.info(f"Capabilities: {', '.join(info['capabilities'])}")

        # Interactive loop
        logger.info("\n" + "=" * 60)
        logger.info("Ask me anything about video games!")
        logger.info("Type 'quit', 'exit', or 'q' to stop")
        logger.info("Type 'history' to see conversation history")
        logger.info("Type 'clear' to clear conversation history")
        logger.info("=" * 60)

        while True:
            try:
                user_input = input("\n🎮 Your question: ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    logger.info("👋 Goodbye! Thanks for using UdaPlay!")
                    break

                if user_input.lower() == "history":
                    history = agent.get_conversation_history()
                    if history:
                        logger.info("\n📜 Conversation History:")
                        for i, entry in enumerate(history, 1):
                            logger.info(f"{i}. Q: {entry['user']}")
                            logger.info(f"   A: {entry['assistant'][:100]}...")
                    else:
                        logger.info("No conversation history yet.")
                    continue

                if user_input.lower() == "clear":
                    agent.clear_conversation()
                    logger.info("Conversation history cleared.")
                    continue

                if not user_input:
                    continue

                # Process the query
                logger.info("\n🤔 Thinking...")
                response = agent.process_query(user_input)

                # Display response
                logger.info(f"\n🎯 Answer (Confidence: {response.confidence:.2f}):")
                logger.info(f"{response.answer}")

                if response.sources:
                    logger.info(f"\n📚 Sources: {', '.join(response.sources)}")
                logger.info(f"🔍 Search Method: {response.search_method}")

            except KeyboardInterrupt:
                logger.info("\n\n👋 Goodbye! Thanks for using UdaPlay!")
                break
            except Exception as e:
                logger.error(f"\n❌ Error: {e}")
                logger.info("Please try again or type 'quit' to exit.")
            except EOFError:
                # Handles non-interactive environments or closed stdin gracefully
                logger.info("\n👋 Exiting: no more input available (EOF). Goodbye!")
                break

    except Exception as e:
        logger.error(f"❌ Failed to initialize UdaPlay: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
