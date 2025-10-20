# UdaPlay AI Research Agent

> 🎮 An AI-powered research agent specialized in video game industry questions

UdaPlay is an AI-powered research agent specialized in answering questions about
the video game industry. It combines local knowledge from a curated game
database with web search capabilities to provide comprehensive, accurate, and
well-cited responses.

## Features

- **Two-Tier Information Retrieval**: Primary RAG system with vector database +
  Secondary web search fallback
- **Semantic Game Search**: Advanced vector similarity search for game
  information
- **Quality Evaluation**: LLM-based assessment of retrieval quality
- **Structured Responses**: Well-formatted answers with confidence scores and
  source citations
- **Conversation Memory**: Maintains context across interactions
- **Modular Architecture**: Clean, extensible codebase with Pydantic models
- **🎮 Game Recommendation Engine**: Personalized recommendations using content-based and collaborative filtering
- **📊 Trend Analysis**: Comprehensive gaming industry trend analysis and market insights
- **😊 Sentiment Analysis**: Analysis of game reviews and user feedback
- **🔥 Trending Games Detection**: Real-time identification of popular and trending games
- **🧠 Advanced Memory System**: Persistent learning from interactions and web searches
- **📋 Structured Output**: Multiple output formats (JSON, API, Webhook) for easy integration
- **📈 Advanced Analytics Dashboard**: Real-time monitoring and comprehensive analytics

## Architecture

```text
UdaPlay AI Research Agent
├── Data Layer
│   ├── Vector Database (ChromaDB)
│   ├── Game Data (JSON files)
│   └── Embeddings (OpenAI)
├── RAG Pipeline
│   ├── Document Processing
│   ├── Vector Search
│   └── Context Augmentation
├── Agent Core
│   ├── State Machine
│   ├── Tool Orchestration
│   └── Memory Management
├── Tools
│   ├── retrieve_game (Vector DB search)
│   ├── evaluate_retrieval (Quality assessment)
│   └── game_web_search (Tavily API)
└── Output Layer
    ├── Structured Responses
    ├── Confidence Scoring
    └── Source Citation

```

```text
UdaPlay AI Research Agent
# UdaPlay AI Research Agent

> 🎮 An AI-powered research agent specialized in video game industry questions

UdaPlay is an AI-powered research agent specialized in answering questions about the video game industry.
 It combines local knowledge from a curated game database with web search capabilities to provide comprehensive,
  accurate, and well-cited responses.

## Features

- **Two-Tier Information Retrieval**: Primary RAG system with vector database + Secondary web search fallback
- **Semantic Game Search**: Advanced vector similarity search for game information
- **Quality Evaluation**: LLM-based assessment of retrieval quality
- **Structured Responses**: Well-formatted answers with confidence scores and source citations
- **Conversation Memory**: Maintains context across interactions
- **Modular Architecture**: Clean, extensible codebase with Pydantic models

## Architecture

```text
UdaPlay AI Research Agent ├── Data Layer │   ├── Vector Database (ChromaDB) │
├── Game Data (JSON files) │   └── Embeddings (OpenAI) ├── RAG Pipeline │   ├──
Document Processing │   ├── Vector Search │   └── Context Augmentation ├── Agent
Core │   ├── State Machine │   ├── Tool Orchestration │   └── Memory Management
├── Tools │   ├── retrieve_game (Vector DB search) │   ├── evaluate_retrieval
(Quality assessment) │   └── game_web_search (Tavily API) └── Output Layer
├── Structured Responses     ├── Confidence Scoring     └── Source Citation

```

## Installation

### Step 1: Clone the repository

```bash
git clone <repository-url> cd udaplay-project

```

### Step 2: Create and activate virtual environment

```bash
python -m venv .venv source .venv/bin/activate  # On Windows:
.venv\Scripts\activate

```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt

```

### Step 4: Set up environment variables

```bash
cp .env.example .env # Edit .env with your API keys

```

## Usage

### Interactive Mode

Run the agent in interactive mode:

```bash
python run_udaplay.py

```

### Test Mode

Run the test suite with sample queries:

```bash
python test_udaplay.py

```

### Programmatic Usage

```python
from src.main import create_agent

# Create agent agent = create_agent()

# Ask a question response = agent.process_query("When was Pokémon Gold and
Silver released?")

print(f"Answer: {response.answer}") print(f"Confidence: {response.confidence}")
print(f"Sources: {response.sources}")

```

## Configuration

The agent can be configured through environment variables:

```bash
# Database settings CHROMA_DB_PATH="./chromadb" COLLECTION_NAME="udaplay_games"

# Games data GAMES_DIRECTORY="./starter/games"

# Agent settings DEFAULT_SEARCH_RESULTS=5 CONFIDENCE_THRESHOLD=0.7

# OpenAI settings OPENAI_MODEL="gpt-4o-mini" OPENAI_TEMPERATURE=0.3

```

## Sample Queries

The agent can handle various types of questions:

- **Release Information**: "When was Pokémon Gold and Silver released?"
- **Platform Queries**: "Which was the first 3D platformer Mario game?"
- **Publisher Information**: "What games did Rockstar Games develop?"
- **Genre Searches**: "What racing games are available on PlayStation?"
- **Technical Questions**: "Was Mortal Kombat X released for PlayStation 5?"

## Development

### Project Structure

```text
udaplay-project/ ├── src/ │   ├── agent/           # Agent implementation │
├── config/          # Configuration management │   ├── database/        #
Vector database management │   ├── models/          # Pydantic data models │
├── tools/           # Agent tools │   └── main.py          # Main application
├── starter/             # Original starter files │   └── games/           #
Game data (JSON files) ├── run_udaplay.py       # CLI runner ├── test_udaplay.py
# Test script └── README.md

```

### Adding New Tools

1. Create a new tool class in `src/tools/`
2. Implement the `__call__` method and `get_tool_definition` method
3. Add the tool to the agent in `src/agent/udaplay_agent.py`

### Extending Data Models

1. Add new Pydantic models in `src/models/`
2. Update the `__init__.py` file to export new models
3. Use the models throughout the application

## Testing

Run the test suite:

```bash
python test_udaplay.py

```

The test suite includes:

## Performance

The agent is optimized for:

- **Fast Retrieval**: ChromaDB vector search with OpenAI embeddings
- **Efficient Evaluation**: LLM-based quality assessment
- **Smart Fallback**: Web search only when local knowledge is insufficient
- **Memory Management**: Conversation state tracking

## Security

- API keys are loaded from environment variables
- No sensitive data is logged or stored
- Vector database is stored locally
- Web search results are processed securely

## Contributing

## Visualization Dashboards

There are multiple Streamlit dashboards available:

### 1. Simple Analytics Dashboard (Recommended)
A lightweight dashboard with mock data that works without API keys:

```bash
streamlit run viz/simple_analytics.py
```

### 2. Enhanced Analytics Dashboard (With Plotly Charts)
A dashboard with advanced Plotly charts including pie charts:

```bash
# Install Plotly first
uv add plotly

# Run the enhanced dashboard
streamlit run viz/enhanced_analytics.py
```

### 3. Advanced Analytics Dashboard
A comprehensive dashboard with real data integration:

```bash
# Option 1: Direct execution
streamlit run viz/advanced_analytics.py

# Option 2: Using the wrapper script
uv run python run_analytics_dashboard.py
```

### 4. Original Knowledge Base Dashboard
The original dashboard for inspecting the knowledge base:

```bash
streamlit run viz/streamlit_app.py
```

The dashboards provide:
- Real-time performance metrics
- User analytics and behavior patterns
- Knowledge base insights
- Memory system statistics
- Trend analysis and predictions
- System health monitoring
- Advanced chart types (pie charts, interactive plots)

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for Udacity AI Engineering program
- Uses OpenAI GPT models for language understanding
- ChromaDB for vector storage and retrieval
- Tavily API for web search capabilities

## Support

For questions or issues:

1. Check the documentation
2. Run the test suite to verify setup
3. Check environment variable configuration
4. Open an issue on GitHub

---

## Submission (Udacity)

This section helps you prepare the project for submission to the Udacity evaluator. Follow the checklist below to ensure
 your project satisfies the typical submission rules used in the Udacity AI Engineering projects.

### Checklist

- [ ] Project runs from the top-level entry point: `python run_udaplay.py` and starts an interactive session
- [ ] Tests run locally with no external secrets required (see Testing section below). Use `python run_tests.py` or `pytest`
- [ ] Include a sample `.env.example` with required environment variable names and placeholder values
- [ ] No hardcoded API keys or credentials in the repo
- [ ] Vector DB persistence files (folder `chromadb/`) are ignored in `.gitignore` or minimal for size limits
- [ ] Project contains a clear README with run instructions, expected outputs, and design notes

### Recommended Submission Steps

#### Step 1: Confirm your virtual environment is active and dependencies installed

```bash
python -m venv .venv source .venv/bin/activate pip install -r requirements.txt

```

#### Step 2: Copy the sample environment file

```bash
cp .env.example .env # Edit .env and set OPENAI_API_KEY and TAVILY_API_KEY only
if you intend to run live queries

```

#### Step 3: Run the tests

The repository includes mocked tests so they should pass without keys:

```bash
python run_tests.py # or, if you prefer: pytest -q

```

#### Step 4: Start the interactive agent

```bash
python run_udaplay.py

```

### What the Evaluator Checks

- The project launches from the provided entry point
- The project contains automated tests and they pass in a clean environment
- Environment-sensitive validation does not break imports or unit-tests (validation at runtime is acceptable)
- The code is modular and well-documented (README and docstrings)

### Tips for Packaging and Submission

Create a zip/tar of the project root excluding virtual environments and large DB artifacts:

```bash
git archive --format=tar.gz -o udaplay-submission.tar.gz HEAD

```

Add a short "Submission Notes" text file (`submission_notes.md`) listing any known limitations, test commands, and exact
Python version used.

---

### State persistence note

The agent persists its internal state machine to `state.json` inside the ChromaDB `persist_directory`
 (by default `./chromadb/state.json`). On startup the agent will attempt to restore state from this file (if present).
  To reduce data-loss risk the agent also explicitly saves the state after processing every query — this improves crash
   guarantees more predictable conversation resumption.

If you want to validate the behaviour locally, see the unit test that covers save/reload semantics: `tests/test_state_persistence.py`.

**UdaPlay** - Your AI Research Assistant for the Gaming Industry!
