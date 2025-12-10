from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class PitchDeckPromptConfig:
    """Конфиг для генерации дека."""
    target_slide_count: int = 10
    tone: str = "formal"
    audience: str = "early-stage VC"
    language: str = "en"


SYSTEM_PROMPT_DECK_GENERATION = (
    "You are an AI assistant that generates investor pitch decks for startups. "
    "You always follow the instructions and output a valid JSON object with a list of slides. "
    "Each slide must have: 'id' (integer), 'section' (string), 'title' (string) and "
    "'bullets' (array of short sentences). Keep language concise and business-oriented."
)


def build_deck_generation_messages(
    brief: str,
    config: PitchDeckPromptConfig,
) -> List[Dict[str, Any]]:
    """
    Собирает сообщения (system + user) для генерации полного дека.
    Подходит для chat-based API (OpenAI, Anthropic и т.п.).
    """
    user_content = f"""
Generate an investor pitch deck for the following startup.

[STARTUP_BRIEF]
{brief.strip()}
[/STARTUP_BRIEF]

Requirements:
- Number of slides: {config.target_slide_count}
- Tone: {config.tone}
- Audience: {config.audience}
- Language: {config.language}
- Mandatory sections: Problem, Solution, Market, Business Model, Traction (if available), Team, Roadmap (optional), Ask.

Output format (JSON):
{{
  "slides": [
    {{
      "id": 1,
      "section": "Problem",
      "title": "...",
      "bullets": ["...", "..."]
    }},
    {{
      "id": 2,
      "section": "Solution",
      "title": "...",
      "bullets": ["...", "..."]
    }}
  ]
}}

Rules:
- Do NOT invent specific investor names or confidential partners.
- If the brief does not include numbers, use only generic indicative phrases (e.g. 'significant market', 'early traction').
- Bullets must be short and scannable.
"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT_DECK_GENERATION},
        {"role": "user", "content": user_content},
    ]


def build_slide_regeneration_messages(
    brief: str,
    existing_deck: Dict[str, Any],
    slide_id: int,
    config: PitchDeckPromptConfig,
) -> List[Dict[str, Any]]:
    """
    Промпт для перегенерации одного слайда с сохранением контекста дека.
    """
    user_content = f"""
You are improving a single slide inside an existing investor pitch deck.

[STARTUP_BRIEF]
{brief.strip()}
[/STARTUP_BRIEF]

[EXISTING_DECK_JSON]
{existing_deck}
[/EXISTING_DECK_JSON]

Task:
- Regenerate slide with id = {slide_id}.
- Keep the same high-level structure and section meaning.
- Improve clarity and conciseness of the title and bullets.
- Maintain tone: {config.tone}
- Audience: {config.audience}

Output format (JSON):
{{
  "id": {slide_id},
  "section": "...",
  "title": "...",
  "bullets": ["...", "..."]
}}
"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT_DECK_GENERATION},
        {"role": "user", "content": user_content},
    ]


def build_critique_deck_messages(
    brief: str,
    generated_deck: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Промпт для качественной оценки (можно использовать внутри evaluation-пайплайна).
    Модель возвращает текстовый разбор, а не JSON.
    """
    system_prompt = (
        "You are an expert VC who evaluates startup pitch decks for clarity and investor readiness."
    )

    user_content = f"""
You will be given a startup brief and a generated pitch deck (JSON).
Provide a short critique in English:
- Are all mandatory sections present?
- Is the story coherent with the brief?
- Are there any obvious hallucinations or invented facts?
- What are the top 3 improvements?

[STARTUP_BRIEF]
{brief.strip()}
[/STARTUP_BRIEF]

[GENERATED_DECK_JSON]
{generated_deck}
[/GENERATED_DECK_JSON]
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
