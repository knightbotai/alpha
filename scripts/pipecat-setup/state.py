"""
Mode State Machine for Alpha Bot

Enforces mode switching in code (not prompts). Supports two modes:
- CONCISE: Brief, direct responses for quick Q&A
- STORY: Longer, narrative responses for storytelling
"""

from enum import Enum
from typing import Optional


class BotMode(Enum):
    """Bot operating modes."""
    CONCISE = "concise"
    STORY = "story"


class ModeStateMachine:
    """
    State machine for bot mode switching.

    The mode determines how the LLM responds:
    - CONCISE: Short answers, minimal elaboration
    - STORY: Narrative flow, descriptive storytelling
    """

    # Keywords that trigger mode switches
    STORY_TRIGGERS = [
        "story", "tell", "narrate", "adventure", "tale",
        "describe", "what happens", "continue", "more",
        "once upon", "chapter", "episode",
    ]

    CONCISE_TRIGGERS = [
        "what is", "when did", "where is", "who is",
        "how do", "how many", "quick", "brief",
    ]

    def __init__(self, initial_mode: BotMode = BotMode.CONCISE):
        self._current_mode = initial_mode
        self._last_user_text: Optional[str] = None

    @property
    def mode(self) -> BotMode:
        return self._current_mode

    def detect_mode_from_text(self, text: str) -> BotMode:
        """
        Detect the appropriate mode based on user input.
        Returns the detected mode without changing state.
        """
        text_lower = text.lower()

        # Check for story triggers
        for trigger in self.STORY_TRIGGERS:
            if trigger in text_lower:
                return BotMode.STORY

        # Check for concise triggers
        for trigger in self.CONCISE_TRIGGERS:
            if trigger in text_lower:
                return BotMode.CONCISE

        # Default to current mode if ambiguous
        return self._current_mode

    def update_mode(self, text: str) -> BotMode:
        """
        Update mode based on user input.
        Returns the new mode.
        """
        detected = self.detect_mode_from_text(text)
        if detected != self._current_mode:
            self._current_mode = detected
        return self._current_mode

    def force_mode(self, mode: BotMode) -> BotMode:
        """
        Force a specific mode.
        """
        self._current_mode = mode
        return self._current_mode

    def get_system_prompt_suffix(self) -> str:
        """
        Get the system prompt suffix based on current mode.
        This is injected into the LLM prompt to enforce mode.
        """
        if self._current_mode == BotMode.CONCISE:
            return "\n\n[MODE: CONCISE] Respond briefly and directly. No unnecessary elaboration."
        else:
            return "\n\n[MODE: STORY] Respond in a narrative, storytelling manner. Use descriptive language."

    def should_truncate_response(self, text: str) -> bool:
        """
        Determine if response should be truncated based on mode.
        Concise mode = truncate story elements.
        """
        if self._current_mode == BotMode.CONCISE:
            # Truncate if too long
            return len(text) > 200
        return False