from datetime import UTC, datetime

from pydantic import (  # pyright: ignore[reportMissingImports]
    BaseModel,
    ConfigDict,
    Field,
)


class Game(BaseModel):
    """Game data model representing a video game entry."""

    name: str = Field(..., description="Name of the game", alias="Name")
    platform: str = Field(..., description="Platform the game was released on", alias="Platform")
    genre: str = Field(..., description="Genre of the game", alias="Genre")
    publisher: str = Field(..., description="Publisher of the game", alias="Publisher")
    description: str = Field(..., description="Description of the game", alias="Description")
    year_of_release: int = Field(..., description="Year the game was released", alias="YearOfRelease")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "Name": "Gran Turismo",
                "Platform": "PlayStation 1",
                "Genre": "Racing",
                "Publisher": "Sony Computer Entertainment",
                "Description": "A realistic racing simulator featuring a wide array of cars and tracks, setting a new standard for the genre.",
                "YearOfRelease": 1997
            }
        }
    )


class GameSearchResult(BaseModel):
    """Result from game search operations."""

    games: list[Game] = Field(..., description="List of matching games")
    query: str = Field(..., description="Original search query")
    total_results: int = Field(..., description="Total number of results found")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the results")
    search_method: str = Field(..., description="Method used for search (vector_db, web_search)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "games": [
                    {
                        "name": "Gran Turismo",
                        "platform": "PlayStation 1",
                        "genre": "Racing",
                        "publisher": "Sony Computer Entertainment",
                        "description": "A realistic racing simulator...",
                        "year_of_release": 1997
                    }
                ],
                "query": "racing games on PlayStation",
                "total_results": 1,
                "confidence_score": 0.95,
                "search_method": "vector_db"
            }
        }
    )


class EvaluationReport(BaseModel):
    """Report from retrieval evaluation."""

    useful: bool = Field(..., description="Whether the retrieved documents are useful")
    description: str = Field(..., description="Detailed explanation of the evaluation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the evaluation")
    recommendation: str = Field(..., description="Recommended next action")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "useful": True,
                "description": "The retrieved documents contain relevant information about the requested game.",
                "confidence": 0.85,
                "recommendation": "proceed_with_answer"
            }
        }
    )


class WebSearchResult(BaseModel):
    """Result from web search operations."""

    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    content: str = Field(..., description="Content snippet from the search result")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Pokémon Gold and Silver - Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Pokémon_Gold_and_Silver",
                "content": "Pokémon Gold and Silver are 1999 role-playing video games...",
                "relevance_score": 0.92
            }
        }
    )


class AgentResponse(BaseModel):
    """Final response from the UdaPlay agent."""

    answer: str = Field(..., description="The agent's answer to the user's question")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the answer")
    sources: list[str] = Field(..., description="List of sources used")
    search_method: str = Field(..., description="Primary method used (vector_db, web_search, combined)")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), description="When the response was generated")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "answer": "Pokémon Gold and Silver were released in 1999 for the Game Boy Color.",
                "confidence": 0.95,
                "sources": ["vector_db", "game_data_006.json"],
                "search_method": "vector_db",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
    )
