import json
import os
from typing import Any, Dict

from openai import OpenAI
from langfuse import Langfuse

from ml.prompt_templates import (
    PitchDeckPromptConfig,
    build_deck_generation_messages,
    build_slide_regeneration_messages,
)

# LLM-клиент
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4.1-mini")

# Langfuse (ключи берутся из env: LANGFUSE_PUBLIC_KEY / SECRET_KEY / HOST)
_langfuse = Langfuse()


def _extract_json(text: str) -> Dict[str, Any]:
    """Парсинг JSON из ответа модели (с учётом ```json ... ```)."""
    text = text.strip()
    if text.startswith("```"):
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start : end + 1]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Не удалось распарсить JSON из ответа LLM: {e}\n{text[:500]}")


def _chat_completion(messages):
    """Один вызов LLM с логированием в Langfuse."""
    trace = _langfuse.trace(
        name="llm_chat_completion",
        input={"messages": messages},
        metadata={"model": _MODEL_NAME},
    )
    try:
        resp = _client.chat.completions.create(
            model=_MODEL_NAME,
            messages=messages,
            temperature=0.4,
        )
        content = resp.choices[0].message.content
        trace.output = {"content": content}
        trace.end()
        return content
    except Exception as e:
        trace.error = str(e)
        trace.end()
        raise


def generate_deck(brief: str, config: PitchDeckPromptConfig) -> Dict[str, Any]:
    """
    Генерация полного дека.
    Возвращает dict вида: {"slides": [...]}.
    """
    if not brief or not brief.strip():
        raise ValueError("brief не должен быть пустым")

    messages = build_deck_generation_messages(brief, config)
    raw = _chat_completion(messages)
    data = _extract_json(raw)

    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("Модель вернула некорректный формат: нет списка slides")

    # лёгкая нормализация
    norm_slides = []
    for i, s in enumerate(slides, start=1):
        norm_slides.append(
            {
                "id": s.get("id", i),
                "section": (s.get("section") or "").strip(),
                "title": (s.get("title") or "").strip(),
                "bullets": [b.strip() for b in (s.get("bullets") or []) if isinstance(b, str) and b.strip()],
            }
        )

    return {"slides": norm_slides}


def regenerate_slide(
    brief: str,
    existing_deck: Dict[str, Any],
    slide_id: int,
    config: PitchDeckPromptConfig,
) -> Dict[str, Any]:
    """
    Перегенерация одного слайда по id.
    Возвращает dict с полями: id, section, title, bullets.
    """
    if slide_id <= 0:
        raise ValueError("slide_id должен быть > 0")

    messages = build_slide_regeneration_messages(
        brief=brief,
        existing_deck=existing_deck,
        slide_id=slide_id,
        config=config,
    )
    raw = _chat_completion(messages)
    slide = _extract_json(raw)

    required = ["id", "section", "title", "bullets"]
    if not all(k in slide for k in required):
        raise ValueError(f"Некорректный формат слайда, нет полей: {required}")

    slide["section"] = (slide.get("section") or "").strip()
    slide["title"] = (slide.get("title") or "").strip()
    slide["bullets"] = [
        b.strip() for b in (slide.get("bullets") or []) if isinstance(b, str) and b.strip()
    ]

    return slide
