import pytest
from loguru import logger

from src.database.vector_store import GameVectorStore


@pytest.fixture(scope="module")
def vector_store(tmp_path_factory, dummy_embedding):
    logger.info("Inicializando GameVectorStore para testes (tmp dir module)...")
    db_dir = tmp_path_factory.mktemp("chromadb_test_module")
    store = GameVectorStore(persist_directory=str(db_dir), embedding_function=dummy_embedding)
    return store


def test_load_games(vector_store):
    logger.info("Testando carregamento de jogos...")
    count = vector_store.load_games_from_directory("./starter/games")
    logger.info(f"Jogos carregados: {count}")
    assert count > 0


def test_search_game_by_name(vector_store):
    logger.info("Testando busca por nome de jogo...")
    results = vector_store.search_games("Pokémon Gold")
    logger.info(f"Resultados encontrados: {len(results)}")
    assert any("Pokémon Gold" in r["Name"] for r in results)


def test_search_game_by_platform(vector_store):
    logger.info("Testando busca por plataforma...")
    results = vector_store.search_games("PlayStation")
    logger.info(f"Resultados encontrados: {len(results)}")
    assert any("PlayStation" in r["Platform"] for r in results)
