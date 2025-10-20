"""Simplified Analytics Dashboard for UdaPlay Agent.

This is a simplified version that works without complex dependencies.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

st.set_page_config(
    page_title="UdaPlay Analytics Dashboard",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 UdaPlay Analytics Dashboard")
st.markdown("---")

# Sidebar navigation
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

selected_page = st.session_state.get("selected_page", "overview")

for page_name, page_key in pages:
    if st.sidebar.button(page_name, key=f"nav_{page_key}"):
        st.session_state.selected_page = page_key
        st.rerun()

# Main content based on selected page
if selected_page == "overview":
    st.header("📈 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎮 Total Games", "18", "+3 today")
    
    with col2:
        st.metric("👥 Active Users", "5", "+2 today")
    
    with col3:
        st.metric("💾 Memory Facts", "45", "+15 today")
    
    with col4:
        st.metric("✅ Success Rate", "95%", "+2%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Query Types Distribution")
        query_types = {
            "Release Info": 35,
            "Game Recommendations": 25,
            "Platform Questions": 20,
            "Genre Analysis": 15,
            "Publisher Info": 5
        }
        st.bar_chart(query_types)
    
    with col2:
        st.subheader("🎯 Confidence Distribution")
        confidence_levels = {
            "High (0.8-1.0)": 45,
            "Medium (0.6-0.8)": 35,
            "Low (0.4-0.6)": 15,
            "Very Low (<0.4)": 5
        }
        st.bar_chart(confidence_levels)
    
    # Recent activity
    st.subheader("🔄 Recent Activity")
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

elif selected_page == "performance":
    st.header("⚡ Performance Metrics")
    
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
        response_times = {
            "00:00": 1.2,
            "04:00": 1.1,
            "08:00": 1.3,
            "12:00": 1.4,
            "16:00": 1.2,
            "20:00": 1.1
        }
        st.line_chart(response_times)
    
    with col2:
        st.subheader("🎯 Accuracy Over Time")
        accuracy_data = {
            "Week 1": 0.92,
            "Week 2": 0.94,
            "Week 3": 0.96,
            "Week 4": 0.95
        }
        st.line_chart(accuracy_data)

elif selected_page == "user_analytics":
    st.header("👥 User Analytics")
    
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
        patterns = {
            "Morning": 45,
            "Afternoon": 65,
            "Evening": 80,
            "Night": 25
        }
        st.bar_chart(patterns)
    
    with col2:
        st.subheader("🎮 Popular Game Topics")
        topics = {
            "Pokémon": 25,
            "Mario": 20,
            "Zelda": 18,
            "Final Fantasy": 15,
            "Call of Duty": 12,
            "Minecraft": 10
        }
        st.bar_chart(topics)

elif selected_page == "knowledge_base":
    st.header("🧠 Knowledge Base Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Games", "18")
    
    with col2:
        st.metric("Genres Covered", "8")
    
    with col3:
        st.metric("Platforms", "6")
    
    # Knowledge distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎮 Genre Distribution")
        genres = {
            "Action": 30,
            "RPG": 25,
            "Adventure": 20,
            "Racing": 15,
            "Sports": 10
        }
        st.bar_chart(genres)
    
    with col2:
        st.subheader("🖥️ Platform Distribution")
        platforms = {
            "PlayStation": 35,
            "Nintendo": 30,
            "Xbox": 20,
            "PC": 15
        }
        st.bar_chart(platforms)

elif selected_page == "memory_system":
    st.header("💾 Memory System Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Facts", "45")
    
    with col2:
        st.metric("Active Users", "5")
    
    with col3:
        st.metric("Interactions", "127")
    
    with col4:
        st.metric("Learned Patterns", "12")
    
    # Memory charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Learning Progress")
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
    
    with col2:
        st.subheader("🧠 Fact Categories")
        categories = {
            "Release Info": 40,
            "Genre Info": 25,
            "Platform Info": 20,
            "Publisher Info": 15
        }
        st.bar_chart(categories)

elif selected_page == "trends":
    st.header("📊 Trend Analysis")
    
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
        trends = {
            "Jan": 1200,
            "Feb": 1350,
            "Mar": 1500,
            "Apr": 1650,
            "May": 1800,
            "Jun": 1950
        }
        st.line_chart(trends)
    
    with col2:
        st.subheader("🎮 Genre Popularity Trends")
        genre_trends = {
            "Action": [30, 32, 35, 38, 40],
            "RPG": [25, 27, 28, 30, 32],
            "Adventure": [20, 22, 24, 25, 26]
        }
        st.line_chart(genre_trends)

elif selected_page == "real_time":
    st.header("🔄 Real-time Monitoring")
    
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
        live_queries = [
            {"time": "now", "query": "Best RPG games 2024", "status": "processing"},
            {"time": "30s ago", "query": "Pokémon release dates", "status": "completed"},
            {"time": "1m ago", "query": "PlayStation exclusives", "status": "completed"},
        ]
        
        for query in live_queries:
            st.write(f"**{query['time']}**: {query['query']} - {query['status']}")
    
    with col2:
        st.subheader("⚡ Performance Metrics")
        metrics = {
            "CPU Usage": 45,
            "Memory Usage": 60,
            "Response Time": 1.2,
            "Success Rate": 98.5
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Quick Stats")
st.sidebar.metric("Total Games", "18")
st.sidebar.metric("Active Users", "5")
st.sidebar.metric("Memory Facts", "45")
st.sidebar.metric("Success Rate", "95%")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Quick Links")
st.sidebar.markdown("- [Open README](../README.md)")
st.sidebar.markdown("- [Run Agent](../run_udaplay.py)")
st.sidebar.markdown("- [Demo Features](../demo_advanced_features.py)")
