# Market Research Agent Project - UdaPlay

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-ready%20for%20submission-brightgreen.svg)

## 🎮 About

UdaPlay is an advanced AI-powered research agent specialized in answering questions about the video game industry. This project implements a comprehensive RAG (Retrieval Augmented Generation) system with multiple advanced features.

## 🚀 Key Features

- **Two-Tier RAG System**: Vector database + Web search fallback
- **Game Recommendation Engine**: Personalized content-based recommendations
- **Trend Analysis**: Comprehensive gaming industry insights
- **Sentiment Analysis**: Game review and feedback analysis
- **Advanced Memory System**: Persistent learning from interactions
- **Analytics Dashboard**: Real-time monitoring with Streamlit
- **Structured Output**: Multiple formats (JSON, API, Webhook)

## 🛠️ Technology Stack

- **Python 3.13+** with modern packaging (`uv` + `pyproject.toml`)
- **ChromaDB** for vector database and semantic search
- **OpenAI GPT** for LLM interactions
- **Tavily API** for web search capabilities
- **Streamlit** for analytics dashboards
- **Pydantic** for data validation and models

## 📊 Project Statistics

- **53 Python files** with modular architecture
- **10 comprehensive test files** with mock support
- **9 agent tools** integrated
- **4 Streamlit dashboards** for visualization
- **6 advanced features** beyond basic requirements

## 🎯 Quick Start

```bash
# Install dependencies
uv sync

# Run tests
uv run python -m pytest tests/ -v

# Start interactive agent
uv run python run_udaplay.py

# Launch analytics dashboard
streamlit run viz/simple_analytics.py
```

## 📋 Udacity Submission Ready

This project meets all Udacity AI Engineering requirements:
- ✅ Entry point: `python run_udaplay.py`
- ✅ Tests run without external secrets
- ✅ Complete documentation and examples
- ✅ Modular, well-documented codebase
- ✅ Advanced features demonstrating technical excellence

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Fabio Carvalho Lima**  
Email: lima.fisico@gmail.com  
GitHub: [@FabioCLima](https://github.com/FabioCLima)

---

*Built for Udacity AI Engineering Program*
