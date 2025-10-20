"""Enhanced Analytics Dashboard with Plotly Charts

This version uses Plotly for more advanced chart types including pie charts.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

st.set_page_config(
    page_title="UdaPlay Analytics Dashboard",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 UdaPlay Analytics Dashboard (Enhanced)")
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
        st.subheader("🧠 Fact Categories (Pie Chart)")
        categories = {
            "Release Info": 40,
            "Genre Info": 25,
            "Platform Info": 20,
            "Publisher Info": 15
        }
        
        # Create pie chart with Plotly
        fig = px.pie(
            values=list(categories.values()),
            names=list(categories.keys()),
            title="Fact Categories Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

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
        st.subheader("🖥️ Platform Distribution (Pie Chart)")
        platforms = {
            "PlayStation": 35,
            "Nintendo": 30,
            "Xbox": 20,
            "PC": 15
        }
        
        # Create pie chart with Plotly
        fig = px.pie(
            values=list(platforms.values()),
            names=list(platforms.keys()),
            title="Platform Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

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

else:
    st.header(f"📊 {selected_page.title()} Page")
    st.info("This page is under development. More features coming soon!")

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

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Chart Types")
st.sidebar.info("This dashboard uses Plotly for enhanced chart visualization including pie charts!")
