"""
Metrics for evaluating AI-generated pitch decks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


CANONICAL_SLIDE_TYPES = [
    "Problem",
    "Solution",
    "Market",
    "Business Model",
    "Traction",
    "Team",
    "Financials",
    "Ask",
]


@dataclass
class DeckMetrics:
    coverage: float
    structure: float
    lexical_similarity: float
    hallucination_proxy: float


def _normalize_title(title: str) -> str:
    return title.strip().lower()


def compute_coverage(ref_deck: Dict, gen_deck: Dict) -> float:
    """Binary coverage of canonical slide types based on slide titles."""
    gen_titles = {_normalize_title(s.get("title", "")) for s in gen_deck.get("slides", [])}

    covered = 0
    for c in CANONICAL_SLIDE_TYPES:
        if _normalize_title(c) in gen_titles:
            covered += 1

    return covered / len(CANONICAL_SLIDE_TYPES) if CANONICAL_SLIDE_TYPES else 0.0


def compute_structure_score(gen_deck: Dict) -> float:
    """Simple heuristic for structural quality.

    - Target number of slides: between 8 and 14.
    - Penalize gaps or duplicates in slide indices.
    """
    slides = gen_deck.get("slides", [])
    if not slides:
        return 0.0

    indices = [s.get("index", i + 1) for i, s in enumerate(slides)]
    n = len(indices)

    # Slide count score (ideal 10 slides, full credit 8-14).
    if n < 4:
        count_score = 0.0
    elif 8 <= n <= 14:
        count_score = 1.0
    else:
        # linear penalty outside [8, 14]
        count_score = max(0.0, 1.0 - abs(n - 11) / 10.0)

    # Continuity score: penalize missing / duplicate indices.
    unique_indices = sorted(set(indices))
    expected_range = list(range(min(unique_indices), max(unique_indices) + 1))
    continuity_penalty = len(expected_range) - len(unique_indices)
    continuity_score = max(0.0, 1.0 - continuity_penalty / max(1, len(expected_range)))

    return 0.6 * count_score + 0.4 * continuity_score


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in text.split() if t.strip()]


def compute_lexical_similarity(ref_deck: Dict, gen_deck: Dict) -> float:
    """Jaccard similarity between all text tokens in ref vs. gen deck."""

    def collect_text(deck: Dict) -> str:
        parts: List[str] = []
        for slide in deck.get("slides", []):
            parts.append(slide.get("title", ""))
            parts.append(slide.get("goal", ""))
            for kp in slide.get("key_points", []) or []:
                parts.append(kp)
            parts.append(slide.get("visuals_description", ""))
        return " ".join(parts)

    ref_tokens = set(_tokenize(collect_text(ref_deck)))
    gen_tokens = set(_tokenize(collect_text(gen_deck)))

    if not ref_tokens or not gen_tokens:
        return 0.0

    intersect = len(ref_tokens & gen_tokens)
    union = len(ref_tokens | gen_tokens)
    return intersect / union if union else 0.0


def compute_hallucination_proxy(input_brief: str, gen_deck: Dict) -> float:
    """Very rough proxy: fraction of tokens in generation not seen in brief.

    This is *not* a true hallucination metric, but useful as a sanity check in lab work.
    Higher values mean more "novel" tokens relative to the input brief.
    """
    brief_tokens = set(_tokenize(input_brief))
    gen_tokens: List[str] = []

    for slide in gen_deck.get("slides", []):
        gen_tokens.extend(_tokenize(slide.get("title", "")))
        gen_tokens.extend(_tokenize(slide.get("goal", "")))
        for kp in slide.get("key_points", []) or []:
            gen_tokens.extend(_tokenize(kp))

    if not gen_tokens:
        return 0.0

    unseen = [t for t in gen_tokens if t not in brief_tokens]
    return len(unseen) / len(gen_tokens)


def compute_all_metrics(
    ref_deck: Dict,
    gen_deck: Dict,
    input_brief: str,
) -> DeckMetrics:
    return DeckMetrics(
        coverage=compute_coverage(ref_deck, gen_deck),
        structure=compute_structure_score(gen_deck),
        lexical_similarity=compute_lexical_similarity(ref_deck, gen_deck),
        hallucination_proxy=compute_hallucination_proxy(input_brief, gen_deck),
    )
