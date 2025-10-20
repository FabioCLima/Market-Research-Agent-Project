import json

import pytest

from src.agent.udaplay_agent import UdaPlayAgent
from src.database.vector_store import GameVectorStore
from src.models.game import Game


class DummyOpenAIClient:
    class Chat:
        @staticmethod
        def completions_create(*args, **kwargs):
            # basic mock response shape
            class Choice:
                class Message:
                    content = json.dumps({
                        "useful": True,
                        "description": "Mock evaluation: useful",
                        "confidence": 0.9,
                        "recommendation": "proceed_with_answer"
                    })

                message = Message()

            class Response:
                choices = [Choice()]

            return Response()


class DummyTavilyClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def search(self, query, **kwargs):
        return {
            "results": [
                {"title": "Mock Result", "url": "https://example.com", "content": "Mock content about Pokemon", "score": 0.9}
            ],
            "answer": "Mock answer",
        }


@pytest.fixture
def temp_vector_store(tmp_path, monkeypatch, dummy_embedding):
    # create temporary chroma path
    db_dir = tmp_path / "chromadb_test"
    db_dir.mkdir()

    vs = GameVectorStore(persist_directory=str(db_dir), embedding_function=dummy_embedding)

    # add a small game to the store
    g = Game(Name="Mock Game", Platform="MockPlatform", Genre="Adventure", Publisher="MockPub", Description="A mock game used for tests", YearOfRelease=2000)
    vs.add_game(g, doc_id="mock_game_1")

    return vs


def test_agent_flow_with_mocks(monkeypatch, temp_vector_store):
    # Monkeypatch OpenAI and Tavily clients used inside tools
    from src.tools.evaluate_retrieval import EvaluateRetrievalTool

    # Mock the EvaluateRetrievalTool.__call__ to return a valid evaluation JSON directly
    def fake_evaluate_call(self, question, retrieved_docs):
        return json.dumps({
            "useful": True,
            "description": "Mock evaluation: useful",
            "confidence": 0.9,
            "recommendation": "proceed_with_answer"
        })

    monkeypatch.setattr(EvaluateRetrievalTool, "__call__", fake_evaluate_call)

    # Mock the Tavily client used by GameWebSearchTool
    monkeypatch.setattr("src.tools.game_web_search.TavilyClient", lambda api_key=None: DummyTavilyClient(api_key))

    # Create agent with the temp vector store
    agent = UdaPlayAgent(vector_store=temp_vector_store, openai_api_key="sk-test", tavily_api_key="tv-test")

    response = agent.process_query("When was Mock Game released?")
    assert response is not None
    assert hasattr(response, "answer")
    assert response.confidence >= 0.0
