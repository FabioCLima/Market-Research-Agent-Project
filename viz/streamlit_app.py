"""Streamlit dashboard to visualize UdaPlay retrievals and knowledge base.

Run with:

    pip install streamlit
    streamlit run viz/streamlit_app.py

This dashboard intentionally avoids calling embedding APIs. It reads the ChromaDB `documents/` backup files
and the `state.json` persisted by the state machine so it works without OpenAI keys for most features.
"""
import json
from pathlib import Path

import streamlit as st

# Try importing the GameVectorStore type for type hints only
try:
    from src.database.vector_store import GameVectorStore
except Exception:
    GameVectorStore = None


st.set_page_config(page_title="UdaPlay - Retrieval Dashboard", layout="wide")

st.title("UdaPlay — Retrieval / Knowledge Base Dashboard")

st.sidebar.header("Settings")
persist_dir = st.sidebar.text_input("ChromaDB persist directory", value="./chromadb")
show_raw_state = st.sidebar.checkbox("Show raw state.json", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("Note: this dashboard reads backup JSON files in the ChromaDB `documents/` folder and the `state.json` file. It does not call OpenAI/Tavily APIs.")

persist_path = Path(persist_dir)

col1, col2 = st.columns([2, 3])

with col1:
    st.header("Collection stats")
    stats = {}
    try:
        if GameVectorStore is not None:
            # create a lightweight store object only for stats (may attempt to initialize chroma)
            try:
                vs = GameVectorStore(persist_directory=str(persist_path))
                stats = vs.get_collection_stats()
            except Exception as e:
                stats = {"error": str(e)}
        else:
            stats = {"error": "GameVectorStore not importable (check PYTHONPATH)"}
    except Exception as e:
        stats = {"error": str(e)}

    st.json(stats)

    st.markdown("---")
    st.header("State machine")
    state_file = persist_path / "state.json"
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text(encoding="utf-8"))
            if show_raw_state:
                st.json(data)
            else:
                st.write(f"State: {data.get('state')}")
                st.write(f"Last transition: {data.get('last_transition_time')}")
        except Exception as e:
            st.error(f"Failed to read state.json: {e}")
    else:
        st.info("No state.json found in persist directory")

    st.markdown("---")
    st.header("Documents backup (chromadb/documents)")
    docs_dir = persist_path / "documents"
    if docs_dir.exists() and docs_dir.is_dir():
        files = sorted(docs_dir.glob("*.json"))
        st.write(f"Found {len(files)} backup documents")
        doc_choice = st.selectbox("Choose a document to preview", options=[f.name for f in files])
        if doc_choice:
            try:
                doc_path = docs_dir / doc_choice
                content = json.loads(doc_path.read_text(encoding="utf-8"))
                st.json(content)
            except Exception as e:
                st.error(f"Failed to load document: {e}")
    else:
        st.info("No documents/ folder found inside persist directory")

with col2:
    st.header("Simple keyword search (no embeddings)")
    st.write("This performs lightweight substring search over the backup documents' content and metadata.")
    query = st.text_input("Query (keyword)")
    max_results = st.slider("Max results", min_value=1, max_value=50, value=10)

    results = []
    if query:
        if docs_dir.exists() and docs_dir.is_dir():
            for f in files:
                try:
                    doc = json.loads(f.read_text(encoding="utf-8"))
                    # doc may be {'content':..., 'metadata':...} or a raw metadata JSON
                    text = json.dumps(doc)
                    if query.lower() in text.lower():
                        results.append({"file": f.name, "preview": text[:500], "full": doc})
                except Exception:
                    continue

    st.write(f"Results: {len(results)}")
    for r in results[:max_results]:
        st.subheader(r["file"])
        st.write(r["preview"])
        if st.button(f"Show full {r['file']}"):
            st.json(r["full"])

    st.markdown("---")
    st.header("Manual collection query (experimental)")
    st.write("If your environment has valid embedding configuration, you can try running the vector store query. This may require OPENAI_API_KEY.")

    exp_query = st.text_input("Vector query (experimental)")
    if st.button("Run vector query"):
        if GameVectorStore is None:
            st.error("GameVectorStore import failed; ensure project root is on PYTHONPATH")
        else:
            try:
                vs2 = GameVectorStore(persist_directory=str(persist_path))
                # Try to call search_games; it may return an empty list or raise if embeddings not configured
                hits = vs2.search_games(exp_query, n_results=10)
                st.write(f"Found {len(hits)} hits")
                for h in hits:
                    st.write(h)
            except Exception as e:
                st.error(f"Vector search failed: {e}")

st.sidebar.markdown("---")
st.sidebar.header("Quick links")
st.sidebar.markdown("- [Open README](../README.md)")
st.sidebar.markdown("- [Submission notes](../submission_notes.md)")
