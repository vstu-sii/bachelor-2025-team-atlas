from typing import Any, Dict, List, Tuple

import math
import re

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer


REQUIRED_SECTIONS = {"Problem", "Solution", "Market", "Business Model", "Team", "Ask"}


def _deck_to_text(deck: Dict[str, Any]) -> str:
    """Конвертирует дек (dict со списком slides) в один текст для BLEU/ROUGE."""
    slides = deck.get("slides") or []
    parts: List[str] = []
    for s in slides:
        title = (s.get("title") or "").strip()
        bullets = s.get("bullets") or []
        parts.append(title)
        for b in bullets:
            if isinstance(b, str):
                parts.append(b.strip())
    return " ".join(p for p in parts if p)


def _tokenize(text: str) -> List[str]:
    """Простейший токенизатор по пробелам и знакам препинания."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return [t for t in text.split() if t]


def compute_structure_metrics(
    generated_deck: Dict[str, Any],
    target_slide_count: int | None = None,
) -> Dict[str, float]:
    """Метрики структуры: покрытие секций, длина дека."""
    slides = generated_deck.get("slides") or []
    sections_present = set()

    for s in slides:
        section = (s.get("section") or "").strip()
        if section:
            sections_present.add(section)

    coverage = 0.0
    if REQUIRED_SECTIONS:
        coverage = len(REQUIRED_SECTIONS & sections_present) / len(REQUIRED_SECTIONS)

    slide_count = len(slides)
    slide_count_ok = 1.0
    if target_slide_count:
        # допустим ±2 слайда
        slide_count_ok = 1.0 if abs(slide_count - target_slide_count) <= 2 else 0.0

    return {
        "slide_count": float(slide_count),
        "section_coverage": float(coverage),
        "slide_count_ok": float(slide_count_ok),
    }


def compute_text_metrics(
    target_deck: Dict[str, Any],
    generated_deck: Dict[str, Any],
) -> Dict[str, float]:
    """BLEU + ROUGE-L между эталонным и сгенерированным деком."""
    ref_text = _deck_to_text(target_deck)
    hyp_text = _deck_to_text(generated_deck)

    ref_tokens = _tokenize(ref_text)
    hyp_tokens = _tokenize(hyp_text)

    if not ref_tokens or not hyp_tokens:
        return {"bleu": 0.0, "rouge_l_f": 0.0}

    smoothing = SmoothingFunction().method1
    bleu = sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smoothing)

    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    scores = scorer.score(" ".join(ref_tokens), " ".join(hyp_tokens))
    rouge_l_f = scores["rougeL"].fmeasure

    return {"bleu": float(bleu), "rouge_l_f": float(rouge_l_f)}


def evaluate_pair(
    input_brief: str,
    target_deck: Dict[str, Any],
    generated_deck: Dict[str, Any],
    target_slide_count: int | None = None,
) -> Dict[str, float]:
    """
    Комплексная оценка одной пары (бриф, эталон, предсказание).
    """
    metrics: Dict[str, float] = {}
    metrics.update(compute_structure_metrics(generated_deck, target_slide_count))
    metrics.update(compute_text_metrics(target_deck, generated_deck))
    return metrics
