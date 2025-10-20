import json
import os

from src.agent.state_machine import AgentState
from src.agent.udaplay_agent import UdaPlayAgent
from src.database.vector_store import GameVectorStore


def test_state_persistence(tmp_path, monkeypatch, dummy_embedding):
    # Create temporary chroma persist directory
    db_dir = tmp_path / "chromadb_state_test"
    db_dir.mkdir()

    # Initialize GameVectorStore pointing to tmp dir
    vs = GameVectorStore(persist_directory=str(db_dir), embedding_function=dummy_embedding)

    # Create agent which will set up state_machine._persist_file
    agent = UdaPlayAgent(vector_store=vs, openai_api_key="sk-test", tavily_api_key="tv-test")

    # Ensure initial state is idle
    assert agent.state_machine.get_state() == AgentState.IDLE.value

    # Perform a valid transition and persist
    transitioned = agent.state_machine.transition(AgentState.RETRIEVING)
    assert transitioned is True
    # explicit persist called by transition, but call again to test public persist()
    agent.state_machine.persist()

    # Verify state.json file exists and contains the expected state
    state_file = os.path.join(str(db_dir), "state.json")
    assert os.path.exists(state_file)
    with open(state_file, encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("state") == AgentState.RETRIEVING.value

    # Create a new vector store instance pointing to same dir and agent to load persisted state
    vs2 = GameVectorStore(persist_directory=str(db_dir), embedding_function=dummy_embedding)
    agent2 = UdaPlayAgent(vector_store=vs2, openai_api_key="sk-test", tavily_api_key="tv-test")

    # New agent should load persisted state
    assert agent2.state_machine.get_state() == AgentState.RETRIEVING.value
