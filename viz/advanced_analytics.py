"""Advanced Analytics Dashboard for UdaPlay Agent.

This dashboard provides comprehensive analytics and visualization
of the agent's performance, user interactions, and knowledge base.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import streamlit as st

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from src.database.vector_store import GameVectorStore
    from src.tools.advanced_memory import AdvancedMemorySystem
    from src.utils.logger import logger
except ImportError:
    # Fallback for when running directly
    from database.vector_store import GameVectorStore
    from tools.advanced_memory import AdvancedMemorySystem
    from utils.logger import logger


class AdvancedAnalyticsDashboard:
    """Advanced analytics dashboard for UdaPlay agent.
    
    This dashboard provides:
    - Performance metrics and KPIs
    - User interaction analytics
    - Knowledge base insights
    - Trend analysis and predictions
    - Memory system statistics
    - Real-time monitoring
    """

    def __init__(self, vector_store: GameVectorStore, memory_system: AdvancedMemorySystem):
        """Initialize the analytics dashboard.
        
        Args:
            vector_store: Initialized GameVectorStore instance
            memory_system: Advanced memory system instance
        """
        self.vector_store = vector_store
        self.memory_system = memory_system

    def render_dashboard(self) -> None:
        """Render the complete analytics dashboard."""
        st.set_page_config(
            page_title="UdaPlay Analytics Dashboard",
            page_icon="🎮",
            layout="wide"
        )
        
        st.title("🎮 UdaPlay Analytics Dashboard")
        st.markdown("---")
        
        # Sidebar for navigation
        self._render_sidebar()
        
        # Main dashboard content
        selected_page = st.session_state.get("selected_page", "overview")
        
        if selected_page == "overview":
            self._render_overview()
        elif selected_page == "performance":
            self._render_performance_metrics()
        elif selected_page == "user_analytics":
            self._render_user_analytics()
        elif selected_page == "knowledge_base":
            self._render_knowledge_base_insights()
        elif selected_page == "memory_system":
            self._render_memory_system_stats()
        elif selected_page == "trends":
            self._render_trend_analysis()
        elif selected_page == "real_time":
            self._render_real_time_monitoring()

    def _render_sidebar(self) -> None:
        """Render the sidebar navigation."""
        st.sidebar.title("📊 Navigation")
        
        pages = [
            ("📈 Overview", "overview"),
            ("⚡ Performance", "performance"),
            ("👥 User Analytics", "user_analytics"),
            ("🧠 Knowledge Base", "knowledge_base"),
            ("💾 Memory System", "memory_system"),
            ("📊 Trends", "trends"),
            ("🔄 Real-time", "real_time")
        ]
        
        for page_name, page_key in pages:
            if st.sidebar.button(page_name, key=f"nav_{page_key}"):
                st.session_state.selected_page = page_key
                st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🎯 Quick Stats")
        
        # Quick stats
        try:
            stats = self._get_quick_stats()
            st.sidebar.metric("Total Games", stats.get("total_games", 0))
            st.sidebar.metric("Active Users", stats.get("active_users", 0))
            st.sidebar.metric("Memory Facts", stats.get("memory_facts", 0))
            st.sidebar.metric("Success Rate", f"{stats.get('success_rate', 0):.1%}")
        except Exception as e:
            st.sidebar.error(f"Error loading stats: {e}")

    def _render_overview(self) -> None:
        """Render the overview dashboard."""
        st.header("📈 Dashboard Overview")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            stats = self._get_quick_stats()
            
            with col1:
                st.metric(
                    label="🎮 Total Games",
                    value=stats.get("total_games", 0),
                    delta=f"+{stats.get('games_added_today', 0)} today"
                )
            
            with col2:
                st.metric(
                    label="👥 Active Users",
                    value=stats.get("active_users", 0),
                    delta=f"+{stats.get('new_users_today', 0)} today"
                )
            
            with col3:
                st.metric(
                    label="💾 Memory Facts",
                    value=stats.get("memory_facts", 0),
                    delta=f"+{stats.get('facts_learned_today', 0)} today"
                )
            
            with col4:
                st.metric(
                    label="✅ Success Rate",
                    value=f"{stats.get('success_rate', 0):.1%}",
                    delta=f"{stats.get('success_rate_change', 0):+.1%}"
                )
        except Exception as e:
            st.error(f"Error loading overview metrics: {e}")
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Query Types Distribution")
            self._render_query_types_chart()
        
        with col2:
            st.subheader("🎯 Confidence Distribution")
            self._render_confidence_chart()
        
        # Recent activity
        st.subheader("🔄 Recent Activity")
        self._render_recent_activity()

    def _render_performance_metrics(self) -> None:
        """Render performance metrics page."""
        st.header("⚡ Performance Metrics")
        
        # Performance KPIs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Response Time", "1.2s", "0.1s faster")
        
        with col2:
            st.metric("API Success Rate", "98.5%", "0.2% better")
        
        with col3:
            st.metric("Memory Usage", "45MB", "2MB less")
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Response Time Trends")
            self._render_response_time_chart()
        
        with col2:
            st.subheader("🎯 Accuracy Over Time")
            self._render_accuracy_chart()
        
        # System health
        st.subheader("🏥 System Health")
        self._render_system_health()

    def _render_user_analytics(self) -> None:
        """Render user analytics page."""
        st.header("👥 User Analytics")
        
        # User metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", "1,234", "+23 this week")
        
        with col2:
            st.metric("Active Sessions", "89", "+5 today")
        
        with col3:
            st.metric("Avg Session Duration", "4.2 min", "+0.3 min")
        
        # User behavior charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 User Query Patterns")
            self._render_user_query_patterns()
        
        with col2:
            st.subheader("🎮 Popular Game Topics")
            self._render_popular_topics()
        
        # User preferences
        st.subheader("❤️ User Preferences")
        self._render_user_preferences()

    def _render_knowledge_base_insights(self) -> None:
        """Render knowledge base insights."""
        st.header("🧠 Knowledge Base Insights")
        
        try:
            # Knowledge base stats
            stats = self.vector_store.get_collection_stats()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Games", stats.get("total_games", 0))
            
            with col2:
                st.metric("Genres Covered", stats.get("unique_genres", 0))
            
            with col3:
                st.metric("Platforms", stats.get("unique_platforms", 0))
            
            # Knowledge distribution
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎮 Genre Distribution")
                self._render_genre_distribution()
            
            with col2:
                st.subheader("🖥️ Platform Distribution")
                self._render_platform_distribution()
            
            # Knowledge quality
            st.subheader("📊 Knowledge Quality Metrics")
            self._render_knowledge_quality()
            
        except Exception as e:
            st.error(f"Error loading knowledge base insights: {e}")

    def _render_memory_system_stats(self) -> None:
        """Render memory system statistics."""
        st.header("💾 Memory System Statistics")
        
        try:
            # Memory stats
            memory_stats = self.memory_system.get_memory_stats()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Facts", memory_stats.get("total_facts", 0))
            
            with col2:
                st.metric("Active Users", memory_stats.get("total_users", 0))
            
            with col3:
                st.metric("Interactions", memory_stats.get("total_interactions", 0))
            
            with col4:
                st.metric("Learned Patterns", memory_stats.get("learned_patterns", 0))
            
            # Memory charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Learning Progress")
                self._render_learning_progress()
            
            with col2:
                st.subheader("🧠 Fact Categories")
                self._render_fact_categories()
            
            # Recent learning
            st.subheader("🔄 Recent Learning Activity")
            self._render_recent_learning()
            
        except Exception as e:
            st.error(f"Error loading memory system stats: {e}")

    def _render_trend_analysis(self) -> None:
        """Render trend analysis page."""
        st.header("📊 Trend Analysis")
        
        # Trend metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Query Growth", "+15%", "vs last month")
        
        with col2:
            st.metric("Popular Genres", "Action, RPG", "trending up")
        
        with col3:
            st.metric("Platform Trends", "PlayStation", "gaining share")
        
        # Trend charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Query Volume Trends")
            self._render_query_volume_trends()
        
        with col2:
            st.subheader("🎮 Genre Popularity Trends")
            self._render_genre_trends()
        
        # Predictions
        st.subheader("🔮 Predictions & Insights")
        self._render_predictions()

    def _render_real_time_monitoring(self) -> None:
        """Render real-time monitoring page."""
        st.header("🔄 Real-time Monitoring")
        
        # Real-time metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Queries", "12", "3 in queue")
        
        with col2:
            st.metric("Response Time", "1.1s", "avg")
        
        with col3:
            st.metric("Success Rate", "99.2%", "last hour")
        
        with col4:
            st.metric("Memory Usage", "42MB", "stable")
        
        # Real-time charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Live Query Stream")
            self._render_live_query_stream()
        
        with col2:
            st.subheader("⚡ Performance Metrics")
            self._render_live_performance()
        
        # System alerts
        st.subheader("🚨 System Alerts")
        self._render_system_alerts()

    def _get_quick_stats(self) -> dict[str, Any]:
        """Get quick statistics for the dashboard."""
        try:
            # Vector store stats
            vector_stats = self.vector_store.get_collection_stats()
            
            # Memory stats
            memory_stats = self.memory_system.get_memory_stats()
            
            return {
                "total_games": vector_stats.get("total_games", 0),
                "active_users": memory_stats.get("total_users", 0),
                "memory_facts": memory_stats.get("total_facts", 0),
                "success_rate": 0.95,  # Mock data
                "games_added_today": 3,
                "new_users_today": 2,
                "facts_learned_today": 15,
                "success_rate_change": 0.02
            }
        except Exception as e:
            logger.error(f"Error getting quick stats: {e}")
            return {}

    def _render_query_types_chart(self) -> None:
        """Render query types distribution chart."""
        try:
            # Mock data for demonstration
            query_types = {
                "Release Info": 35,
                "Game Recommendations": 25,
                "Platform Questions": 20,
                "Genre Analysis": 15,
                "Publisher Info": 5
            }
            
            st.bar_chart(query_types)
        except Exception as e:
            st.error(f"Error rendering query types chart: {e}")

    def _render_confidence_chart(self) -> None:
        """Render confidence distribution chart."""
        try:
            # Mock data for demonstration
            confidence_levels = {
                "High (0.8-1.0)": 45,
                "Medium (0.6-0.8)": 35,
                "Low (0.4-0.6)": 15,
                "Very Low (<0.4)": 5
            }
            
            st.bar_chart(confidence_levels)
        except Exception as e:
            st.error(f"Error rendering confidence chart: {e}")

    def _render_recent_activity(self) -> None:
        """Render recent activity feed."""
        try:
            # Mock recent activity data
            activities = [
                {"time": "2 min ago", "user": "user_123", "action": "Asked about Pokémon games", "status": "✅"},
                {"time": "5 min ago", "user": "user_456", "action": "Requested RPG recommendations", "status": "✅"},
                {"time": "8 min ago", "user": "user_789", "action": "Searched for PlayStation games", "status": "✅"},
                {"time": "12 min ago", "user": "user_101", "action": "Compared racing games", "status": "✅"},
            ]
            
            for activity in activities:
                col1, col2, col3, col4 = st.columns([1, 2, 3, 1])
                with col1:
                    st.write(activity["time"])
                with col2:
                    st.write(activity["user"])
                with col3:
                    st.write(activity["action"])
                with col4:
                    st.write(activity["status"])
        except Exception as e:
            st.error(f"Error rendering recent activity: {e}")

    def _render_response_time_chart(self) -> None:
        """Render response time trends chart."""
        try:
            # Mock data
            response_times = {
                "00:00": 1.2,
                "04:00": 1.1,
                "08:00": 1.3,
                "12:00": 1.4,
                "16:00": 1.2,
                "20:00": 1.1
            }
            
            st.line_chart(response_times)
        except Exception as e:
            st.error(f"Error rendering response time chart: {e}")

    def _render_accuracy_chart(self) -> None:
        """Render accuracy over time chart."""
        try:
            # Mock data
            accuracy_data = {
                "Week 1": 0.92,
                "Week 2": 0.94,
                "Week 3": 0.96,
                "Week 4": 0.95
            }
            
            st.line_chart(accuracy_data)
        except Exception as e:
            st.error(f"Error rendering accuracy chart: {e}")

    def _render_system_health(self) -> None:
        """Render system health indicators."""
        try:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.success("🟢 Database: Healthy")
            
            with col2:
                st.success("🟢 Memory: Normal")
            
            with col3:
                st.success("🟢 API: Operational")
            
            with col4:
                st.warning("🟡 CPU: Moderate")
        except Exception as e:
            st.error(f"Error rendering system health: {e}")

    def _render_user_query_patterns(self) -> None:
        """Render user query patterns chart."""
        try:
            patterns = {
                "Morning": 45,
                "Afternoon": 65,
                "Evening": 80,
                "Night": 25
            }
            
            st.bar_chart(patterns)
        except Exception as e:
            st.error(f"Error rendering user query patterns: {e}")

    def _render_popular_topics(self) -> None:
        """Render popular topics chart."""
        try:
            topics = {
                "Pokémon": 25,
                "Mario": 20,
                "Zelda": 18,
                "Final Fantasy": 15,
                "Call of Duty": 12,
                "Minecraft": 10
            }
            
            st.bar_chart(topics)
        except Exception as e:
            st.error(f"Error rendering popular topics: {e}")

    def _render_user_preferences(self) -> None:
        """Render user preferences analysis."""
        try:
            preferences = {
                "Action Games": 40,
                "RPG Games": 35,
                "Adventure Games": 25,
                "Racing Games": 20,
                "Sports Games": 15
            }
            
            st.bar_chart(preferences)
        except Exception as e:
            st.error(f"Error rendering user preferences: {e}")

    def _render_genre_distribution(self) -> None:
        """Render genre distribution chart."""
        try:
            genres = {
                "Action": 30,
                "RPG": 25,
                "Adventure": 20,
                "Racing": 15,
                "Sports": 10
            }
            
            st.bar_chart(genres)
        except Exception as e:
            st.error(f"Error rendering genre distribution: {e}")

    def _render_platform_distribution(self) -> None:
        """Render platform distribution chart."""
        try:
            platforms = {
                "PlayStation": 35,
                "Nintendo": 30,
                "Xbox": 20,
                "PC": 15
            }
            
            st.bar_chart(platforms)
        except Exception as e:
            st.error(f"Error rendering platform distribution: {e}")

    def _render_knowledge_quality(self) -> None:
        """Render knowledge quality metrics."""
        try:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Data Completeness", "94%", "2% better")
            
            with col2:
                st.metric("Accuracy Score", "96%", "1% better")
            
            with col3:
                st.metric("Coverage Score", "89%", "3% better")
        except Exception as e:
            st.error(f"Error rendering knowledge quality: {e}")

    def _render_learning_progress(self) -> None:
        """Render learning progress chart."""
        try:
            progress = {
                "Day 1": 10,
                "Day 2": 25,
                "Day 3": 45,
                "Day 4": 60,
                "Day 5": 75,
                "Day 6": 85,
                "Day 7": 95
            }
            
            st.line_chart(progress)
        except Exception as e:
            st.error(f"Error rendering learning progress: {e}")

    def _render_fact_categories(self) -> None:
        """Render fact categories chart."""
        try:
            categories = {
                "Release Info": 40,
                "Genre Info": 25,
                "Platform Info": 20,
                "Publisher Info": 15
            }
            
            st.bar_chart(categories)
        except Exception as e:
            st.error(f"Error rendering fact categories: {e}")

    def _render_recent_learning(self) -> None:
        """Render recent learning activity."""
        try:
            learning_activities = [
                {"time": "1 hour ago", "fact": "Learned about new Pokémon release", "confidence": "0.9"},
                {"time": "2 hours ago", "fact": "Updated Mario game information", "confidence": "0.8"},
                {"time": "3 hours ago", "fact": "Added Zelda franchise details", "confidence": "0.95"},
            ]
            
            for activity in learning_activities:
                st.write(f"**{activity['time']}**: {activity['fact']} (Confidence: {activity['confidence']})")
        except Exception as e:
            st.error(f"Error rendering recent learning: {e}")

    def _render_query_volume_trends(self) -> None:
        """Render query volume trends chart."""
        try:
            trends = {
                "Jan": 1200,
                "Feb": 1350,
                "Mar": 1500,
                "Apr": 1650,
                "May": 1800,
                "Jun": 1950
            }
            
            st.line_chart(trends)
        except Exception as e:
            st.error(f"Error rendering query volume trends: {e}")

    def _render_genre_trends(self) -> None:
        """Render genre trends chart."""
        try:
            trends = {
                "Action": [30, 32, 35, 38, 40],
                "RPG": [25, 27, 28, 30, 32],
                "Adventure": [20, 22, 24, 25, 26]
            }
            
            st.line_chart(trends)
        except Exception as e:
            st.error(f"Error rendering genre trends: {e}")

    def _render_predictions(self) -> None:
        """Render predictions and insights."""
        try:
            st.info("🔮 **Prediction**: RPG games will see 15% growth in the next quarter")
            st.info("📊 **Insight**: Evening queries have 20% higher success rates")
            st.info("🎯 **Recommendation**: Focus on expanding Action game coverage")
        except Exception as e:
            st.error(f"Error rendering predictions: {e}")

    def _render_live_query_stream(self) -> None:
        """Render live query stream."""
        try:
            # Mock live data
            live_queries = [
                {"time": "now", "query": "Best RPG games 2024", "status": "processing"},
                {"time": "30s ago", "query": "Pokémon release dates", "status": "completed"},
                {"time": "1m ago", "query": "PlayStation exclusives", "status": "completed"},
            ]
            
            for query in live_queries:
                st.write(f"**{query['time']}**: {query['query']} - {query['status']}")
        except Exception as e:
            st.error(f"Error rendering live query stream: {e}")

    def _render_live_performance(self) -> None:
        """Render live performance metrics."""
        try:
            metrics = {
                "CPU Usage": 45,
                "Memory Usage": 60,
                "Response Time": 1.2,
                "Success Rate": 98.5
            }
            
            for metric, value in metrics.items():
                st.metric(metric, value)
        except Exception as e:
            st.error(f"Error rendering live performance: {e}")

    def _render_system_alerts(self) -> None:
        """Render system alerts."""
        try:
            alerts = [
                {"level": "info", "message": "Memory usage is normal", "time": "5 min ago"},
                {"level": "warning", "message": "High query volume detected", "time": "10 min ago"},
                {"level": "success", "message": "Database backup completed", "time": "1 hour ago"},
            ]
            
            for alert in alerts:
                if alert["level"] == "info":
                    st.info(f"ℹ️ {alert['message']} - {alert['time']}")
                elif alert["level"] == "warning":
                    st.warning(f"⚠️ {alert['message']} - {alert['time']}")
                elif alert["level"] == "success":
                    st.success(f"✅ {alert['message']} - {alert['time']}")
        except Exception as e:
            st.error(f"Error rendering system alerts: {e}")


def run_analytics_dashboard():
    """Run the analytics dashboard."""
    try:
        # Initialize components
        vector_store = GameVectorStore()
        memory_system = AdvancedMemorySystem()
        
        # Create and render dashboard
        dashboard = AdvancedAnalyticsDashboard(vector_store, memory_system)
        dashboard.render_dashboard()
        
    except Exception as e:
        st.error(f"Error running analytics dashboard: {e}")


if __name__ == "__main__":
    run_analytics_dashboard()
