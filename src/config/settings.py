import os

from dotenv import load_dotenv

from src.utils.logger import logger

# Load environment variables from .env file (if present)
load_dotenv()


class Settings:
    """Application settings and configuration.

    Note: Validation of required API keys is done at runtime (initialization)
    to allow importing modules for testing without real credentials.
    """

    # API Keys (read at runtime)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Database settings
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chromadb")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "udaplay_games")

    # Games data
    GAMES_DIRECTORY: str = os.getenv("GAMES_DIRECTORY", "./starter/games")

    # Agent settings
    DEFAULT_SEARCH_RESULTS: int = int(os.getenv("DEFAULT_SEARCH_RESULTS", "5"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))

    # OpenAI settings
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

    @classmethod
    def validate(cls, require_keys: bool = True) -> bool:
        """Validate that required settings are present.

        If require_keys is False, only ensures directories exist and basic types.
        """
        # Ensure database path exists
        os.makedirs(cls.CHROMA_DB_PATH, exist_ok=True)

        if not require_keys:
            logger.debug("Skipping API keys validation (require_keys=False)")
            return True

        required_vars = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
        missing_vars = []

        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        return True

    @classmethod
    def get_database_path(cls) -> str:
        """Get the database path, creating it if it doesn't exist."""
        os.makedirs(cls.CHROMA_DB_PATH, exist_ok=True)
        return cls.CHROMA_DB_PATH


# Note: do not validate keys on import to allow tests to import modules without keys
logger.debug("Settings loaded (no validation performed on import). Call Settings.validate() at runtime if needed.")
