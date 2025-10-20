#!/usr/bin/env python3
"""UdaPlay AI Research Agent - Demo Script

This script demonstrates the key features and capabilities of the UdaPlay agent
without requiring interactive input. Perfect for showcasing the system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import create_agent


def run_demo():
    """Run a demonstration of the UdaPlay agent."""
    print("🎮 UdaPlay AI Research Agent - Demo")
    print("=" * 60)

    try:
        # Create agent
        print("Initializing UdaPlay agent...")
        agent = create_agent()

        # Display agent capabilities
        info = agent.get_agent_info()
        print(f"\n✅ {info['name']} v{info['version']} is ready!")
        print(f"📝 {info['description']}")

        # Demo queries
        demo_queries = [
            {
                "question": "When were Pokémon Gold and Silver released?",
                "description": "Testing knowledge about classic Pokémon games"
            },
            {
                "question": "Which was the first 3D platformer Mario game?",
                "description": "Testing knowledge about Mario game history"
            },
            {
                "question": "What racing games are available on PlayStation?",
                "description": "Testing genre and platform-based search"
            }
        ]

        print(f"\n🧪 Running {len(demo_queries)} demo queries...")
        print("=" * 60)

        for i, demo in enumerate(demo_queries, 1):
            print(f"\n🔍 Demo Query {i}: {demo['description']}")
            print(f"❓ Question: {demo['question']}")
            print("-" * 40)

            try:
                response = agent.process_query(demo["question"])

                print("✅ Answer:")
                print(f"   {response.answer}")
                print(f"\n📊 Confidence: {response.confidence:.2f}")
                print(f"🔍 Search Method: {response.search_method}")
                print(f"📚 Sources: {', '.join(response.sources)}")

            except Exception as e:
                print(f"❌ Error processing query: {e}")

            print("-" * 40)

        print("\n🎉 Demo completed successfully!")
        print("=" * 60)
        print("UdaPlay is ready to answer your gaming questions!")
        print("Run 'python run_udaplay.py' for interactive mode.")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check that your .env file contains valid API keys")
        print("2. Ensure all dependencies are installed")
        print("3. Verify the games directory exists")
        sys.exit(1)


if __name__ == "__main__":
    run_demo()
