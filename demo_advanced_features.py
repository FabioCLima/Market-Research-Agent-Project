#!/usr/bin/env python3
"""UdaPlay Advanced Features Demo Script

This script demonstrates the new advanced features implemented in UdaPlay:
- Game Recommendation Engine
- Trend Analysis
- Advanced Memory System
- Structured Output
- Analytics Dashboard
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import create_agent


def demo_game_recommendations(agent):
    """Demonstrate game recommendation engine."""
    print("\n🎮 === GAME RECOMMENDATION ENGINE ===")
    print("=" * 50)
    
    # Test different recommendation types
    test_preferences = [
        "I like RPG games with fantasy themes",
        "I enjoy action games on PlayStation",
        "I want racing games with realistic graphics"
    ]
    
    for i, preferences in enumerate(test_preferences, 1):
        print(f"\n🔍 Test {i}: {preferences}")
        print("-" * 40)
        
        try:
            recommendations = agent.get_game_recommendations(preferences, "content_based", 3)
            print(f"✅ Recommendations generated successfully")
            print(f"📊 Response length: {len(recommendations)} characters")
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_trend_analysis(agent):
    """Demonstrate trend analysis capabilities."""
    print("\n📊 === TREND ANALYSIS ===")
    print("=" * 50)
    
    # Test different analysis types
    analysis_types = [
        ("comprehensive", "all_time"),
        ("genre_trends", "recent"),
        ("platform_trends", "decade")
    ]
    
    for analysis_type, time_period in analysis_types:
        print(f"\n🔍 Analysis: {analysis_type} ({time_period})")
        print("-" * 40)
        
        try:
            trends = agent.analyze_gaming_trends(analysis_type, time_period)
            print(f"✅ Trend analysis completed")
            print(f"📊 Response length: {len(trends)} characters")
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_sentiment_analysis(agent):
    """Demonstrate sentiment analysis capabilities."""
    print("\n😊 === SENTIMENT ANALYSIS ===")
    print("=" * 50)
    
    # Test sentiment analysis on game reviews
    test_reviews = [
        ("This game is absolutely amazing! The graphics are stunning and the gameplay is incredible.", "Cyberpunk 2077"),
        ("The game has some bugs but overall it's quite enjoyable. Worth playing.", "Fallout 76"),
        ("Terrible game, waste of money. Don't buy it.", "Generic Game")
    ]
    
    for i, (review, game_title) in enumerate(test_reviews, 1):
        print(f"\n🔍 Review {i}: {review[:50]}...")
        print(f"Game: {game_title}")
        print("-" * 40)
        
        try:
            sentiment = agent.analyze_sentiment(review, game_title)
            print(f"✅ Sentiment analysis completed")
            print(f"📊 Response length: {len(sentiment)} characters")
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_trending_games(agent):
    """Demonstrate trending games detection."""
    print("\n🔥 === TRENDING GAMES DETECTION ===")
    print("=" * 50)
    
    # Test different trending criteria
    criteria_tests = [
        ("recent_high_rated", 5),
        ("popular_genres", 3),
        ("all_time_classics", 4)
    ]
    
    for criteria, limit in criteria_tests:
        print(f"\n🔍 Criteria: {criteria} (limit: {limit})")
        print("-" * 40)
        
        try:
            trending = agent.detect_trending_games(criteria, limit)
            print(f"✅ Trending games detected")
            print(f"📊 Response length: {len(trending)} characters")
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_advanced_memory(agent):
    """Demonstrate advanced memory system."""
    print("\n🧠 === ADVANCED MEMORY SYSTEM ===")
    print("=" * 50)
    
    # Test memory system features
    print("\n🔍 Memory Statistics:")
    print("-" * 40)
    
    try:
        memory_stats = agent.get_memory_stats()
        print(f"✅ Memory stats retrieved")
        print(f"📊 Stats: {memory_stats}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🔍 Learned Facts:")
    print("-" * 40)
    
    try:
        facts = agent.get_learned_facts("Pokémon")
        print(f"✅ Learned facts retrieved")
        print(f"📊 Found {len(facts)} facts about Pokémon")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🔍 Personalized Recommendations:")
    print("-" * 40)
    
    try:
        personalized = agent.get_personalized_recommendations("demo_user")
        print(f"✅ Personalized recommendations retrieved")
        print(f"📊 Recommendations: {personalized}")
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_structured_output(agent):
    """Demonstrate structured output system."""
    print("\n📋 === STRUCTURED OUTPUT SYSTEM ===")
    print("=" * 50)
    
    # Test structured output with a sample query
    test_query = "When was Pokémon Gold and Silver released?"
    
    print(f"\n🔍 Test Query: {test_query}")
    print("-" * 40)
    
    try:
        # Get regular response
        response = agent.process_query(test_query)
        print(f"✅ Regular response generated")
        
        # Generate structured output
        structured = agent.generate_structured_response(response, "detailed")
        print(f"✅ Structured output generated")
        print(f"📊 Output format: {structured.get('format', 'unknown')}")
        print(f"📊 Metadata included: {bool(structured.get('metadata'))}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_agent_info(agent):
    """Demonstrate enhanced agent information."""
    print("\nℹ️ === ENHANCED AGENT INFO ===")
    print("=" * 50)
    
    try:
        info = agent.get_agent_info()
        print(f"✅ Agent info retrieved")
        print(f"📊 Name: {info['name']}")
        print(f"📊 Version: {info['version']}")
        print(f"📊 Description: {info['description']}")
        print(f"📊 Capabilities: {len(info['capabilities'])}")
        print(f"📊 Tools: {len(info['tools'])}")
        print(f"📊 Advanced Features: {len(info.get('advanced_features', []))}")
        
        print(f"\n🔧 Available Tools:")
        for tool in info['tools']:
            print(f"  - {tool}")
        
        print(f"\n🚀 Advanced Features:")
        for feature in info.get('advanced_features', []):
            print(f"  - {feature}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main demo function."""
    print("🎮 UdaPlay Advanced Features Demo")
    print("=" * 60)
    print("This demo showcases the new advanced features implemented in UdaPlay:")
    print("• Game Recommendation Engine")
    print("• Trend Analysis")
    print("• Sentiment Analysis")
    print("• Advanced Memory System")
    print("• Structured Output")
    print("• Enhanced Analytics")
    print("=" * 60)
    
    try:
        # Create agent
        print("\n🤖 Creating UdaPlay agent...")
        agent = create_agent()
        print("✅ Agent created successfully!")
        
        # Run demos
        demo_agent_info(agent)
        demo_game_recommendations(agent)
        demo_trend_analysis(agent)
        demo_sentiment_analysis(agent)
        demo_trending_games(agent)
        demo_advanced_memory(agent)
        demo_structured_output(agent)
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed successfully!")
        print("=" * 60)
        
        print("\n📊 Summary of Advanced Features:")
        print("✅ Game Recommendation Engine - Personalized game suggestions")
        print("✅ Trend Analysis - Industry insights and patterns")
        print("✅ Sentiment Analysis - Review and feedback analysis")
        print("✅ Advanced Memory - Persistent learning system")
        print("✅ Structured Output - Multiple format support")
        print("✅ Enhanced Analytics - Comprehensive dashboard")
        
        print("\n🚀 Next Steps:")
        print("• Run 'streamlit run viz/advanced_analytics.py' for analytics dashboard")
        print("• Use 'python run_udaplay.py' for interactive mode")
        print("• Explore the new tools and capabilities")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
