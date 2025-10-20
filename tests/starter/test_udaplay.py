#!/usr/bin/env python3
"""UdaPlay AI Research Agent - Test Script

Test script to verify the UdaPlay agent functionality with sample queries.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import create_agent


def test_sample_queries():
    """Test the agent with sample queries."""
    print("🧪 Testing UdaPlay Agent with Sample Queries")
    print("=" * 50)

    try:
        # Create agent
        agent = create_agent()

        # Sample test queries
        test_queries = [
            "When were Pokémon Gold and Silver released?",
            "Which was the first 3D platformer Mario game?",
            "Was Mortal Kombat X released for PlayStation 5?",
            "What racing games are available on PlayStation?",
            "Tell me about games by Nintendo"
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 40)

            try:
                response = agent.process_query(query)

                print(f"✅ Answer: {response.answer[:200]}...")
                print(f"📊 Confidence: {response.confidence:.2f}")
                print(f"🔍 Search Method: {response.search_method}")
                print(f"📚 Sources: {', '.join(response.sources)}")

            except Exception as e:
                print(f"❌ Error: {e}")

        print("\n" + "=" * 50)
        print("✅ Testing completed!")

    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_sample_queries()
