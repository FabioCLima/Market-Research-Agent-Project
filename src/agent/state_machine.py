import json
import os
from datetime import UTC, datetime
from enum import Enum

from src.utils.logger import logger


class AgentState(Enum):
    IDLE = "idle"
    RETRIEVING = "retrieving"
    EVALUATING = "evaluating"
    WEB_SEARCH = "web_search"
    ANSWERING = "answering"


class AgentStateMachine:
    """State machine with guarded transitions and logging.

    Allowed transitions:
      idle -> retrieving
      retrieving -> evaluating
      evaluating -> web_search | answering
      web_search -> answering
      answering -> idle
    """

    _allowed = {
        AgentState.IDLE: [AgentState.RETRIEVING],
        AgentState.RETRIEVING: [AgentState.EVALUATING],
        AgentState.EVALUATING: [AgentState.WEB_SEARCH, AgentState.ANSWERING],
        AgentState.WEB_SEARCH: [AgentState.ANSWERING],
        AgentState.ANSWERING: [AgentState.IDLE],
    }

    def __init__(self):
        # Optional persistence file path can be provided later via `load_from_file` / constructor variant.
        self.state = AgentState.IDLE
        # Use timezone-aware UTC timestamps
        self.last_transition_time = datetime.now(UTC)
        self._persist_file: str | None = None

    def load_from_file(self, persist_file: str) -> None:
        """Load state from a JSON persistence file if it exists.

        The file will contain: {"state": "idle", "last_transition_time": "..."}
        """
        self._persist_file = persist_file
        try:
            if os.path.exists(persist_file):
                with open(persist_file, encoding="utf-8") as f:
                    data = json.load(f)
                state_str = data.get("state")
                if state_str:
                    self.state = AgentState(state_str)
                ts = data.get("last_transition_time")
                if ts:
                    try:
                        self.last_transition_time = datetime.fromisoformat(ts)
                    except Exception:
                        self.last_transition_time = datetime.now(UTC)
                logger.debug(f"Loaded state machine from {persist_file}: {self.state.value}")
        except Exception as e:
            logger.warning(f"Failed to load state machine from {persist_file}: {e}")

    def _persist(self) -> None:
        if not self._persist_file:
            return
        try:
            data = {
                "state": self.state.value,
                "last_transition_time": self.last_transition_time.isoformat()
            }
            with open(self._persist_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Failed to persist state machine to {self._persist_file}: {e}")

    def persist(self) -> None:
        """Public wrapper to persist the state machine to the configured file.

        This is a thin wrapper around the internal `_persist()` method and is
        intended to be called by external callers (e.g. agents) after
        important operations.
        """
        self._persist()

    def transition(self, target: AgentState) -> bool:
        if target in self._allowed.get(self.state, []):
            logger.debug(f"State transition: {self.state.value} -> {target.value}")
            self.state = target
            self.last_transition_time = datetime.now(UTC)
            self._persist()
            return True
        logger.warning(f"Invalid state transition attempted: {self.state.value} -> {target.value}")
        return False

    def get_state(self) -> str:
        return self.state.value

    def reset(self):
        logger.debug("State machine reset to idle")
        self.state = AgentState.IDLE
        self.last_transition_time = datetime.now(UTC)
        self._persist()

    def can_transition(self, target: AgentState) -> bool:
        """Return True if transition from current state to target is allowed."""
        return target in self._allowed.get(self.state, [])
