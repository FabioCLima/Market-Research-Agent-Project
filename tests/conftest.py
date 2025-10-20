import warnings

import pytest

# Reduce noisy DeprecationWarning emitted by chromadb about legacy embedding
# config during tests. This is a test-time suppression only.
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*legacy embedding function config.*",
)


class DummyEmbedding:
    def __init__(self, *args, **kwargs):
        self.is_legacy = False

    def __call__(self, input):
        try:
            return [[0.0] for _ in input]
        except TypeError:
            return [[0.0]]

    def embed_query(self, input):
        # alias used by chroma for single-query embeddings
        return self.__call__(input)

    def name(self):
        # return a stable name expected by Chroma config validation
        return "default"


@pytest.fixture(scope="module")
def dummy_embedding():
    return DummyEmbedding()
