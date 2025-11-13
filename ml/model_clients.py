"""
Model clients abstraction for AI Pitch Deck Generator experiments.

We don't actually call external APIs here – instead we define interfaces
and a simple EchoModel client that can be used in offline tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ModelConfig:
    name: str
    provider: str
    mode: str  # "llm" or "vlm"
    max_tokens: int
    temperature: float = 0.3


class BaseModelClient:
    """Abstract interface for a pitch deck generation model."""

    def __init__(self, config: ModelConfig):
        self.config = config

    def generate_deck(self, brief: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a pitch deck JSON structure from a textual brief.

        Expected return format:
        {
          "slides": [
            {
              "index": 1,
              "title": "Problem",
              "goal": "Explain the core problem",
              "key_points": ["..."],
              "visuals_description": "..."
            },
            ...
          ]
        }
        """
        raise NotImplementedError


class EchoModelClient(BaseModelClient):
    """Simple baseline model that returns a trivial deck based on a template.

    This is used as an offline baseline without external API calls.
    """

    DEFAULT_SLIDE_TITLES: List[str] = [
        "Problem",
        "Solution",
        "Market",
        "Business Model",
        "Traction",
        "Team",
        "Financials",
        "Ask",
    ]

    def generate_deck(self, brief: str, constraints: Dict[str, Any]) -> Dict[str, Any]:
        slides: List[Dict[str, Any]] = []
        style = constraints.get("tone", "neutral")
        language = constraints.get("language", "en")

        for idx, title in enumerate(self.DEFAULT_SLIDE_TITLES, start=1):
            slides.append(
                {
                    "index": idx,
                    "title": title,
                    "goal": f"Auto-generated baseline slide for {title.lower()}",
                    "key_points": [
                        f"[{language}] [{style}] Stub content for {title} based on brief.",
                    ],
                    "visuals_description": "Placeholder visual suggestion (wireframe only).",
                }
            )

        return {"slides": slides, "meta": {"model": self.config.name}}
