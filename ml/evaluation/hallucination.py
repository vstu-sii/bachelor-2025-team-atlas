import re
from typing import Any, Dict, List, Set


NUM_PATTERN = re.compile(r"\d[\d,.]*")


def _deck_to_text(deck: Dict[str, Any]) -> str:
    slides = deck.get("slides") or []
    parts: List[str] = []
    for s in slides:
        parts.append(str(s.get("title", "")))
        for b in s.get("bullets") or []:
            parts.append(str(b))
    return " ".join(parts)


def _extract_numbers(text: str) -> Set[str]:
    nums = set(NUM_PATTERN.findall(text))
    # нормализуем запятые/точки
    normed = set()
    for n in nums:
        normed.add(n.replace(",", ""))
    return normed


def numeric_hallucinations(
    input_brief: str,
    target_deck: Dict[str, Any],
    generated_deck: Dict[str, Any],
) -> Dict[str, float]:
    """
    Возвращает количество чисел, которые появились только в сгенерированном деке.
    Это не идеальная метрика, но даёт сигнал по “левым” цифрам.
    """
    base_text = input_brief + " " + _deck_to_text(target_deck)
    gen_text = _deck_to_text(generated_deck)

    base_nums = _extract_numbers(base_text)
    gen_nums = _extract_numbers(gen_text)

    bad_nums = gen_nums - base_nums

    return {
        "numeric_hallucinations": float(len(bad_nums)),
        "has_numeric_hallucinations": 1.0 if bad_nums else 0.0,
    }
