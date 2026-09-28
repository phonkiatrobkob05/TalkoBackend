import json

from google import genai
from google.genai import types

from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)


def generate(system_prompt: str, message: str, history: list[dict] | None = None) -> str:
    contents: list[types.Content] = []

    if history:
        for turn in history:
            contents.append(
                types.Content(
                    role=turn["role"],
                    parts=[types.Part(text=turn["content"])],
                )
            )

    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return response.text or ""


def generate_word_info(word: str) -> dict:
    prompt = (
        f'For the English word "{word}", return a JSON object with keys: '
        "pronunciation (IPA notation), translation (Thai), "
        "example (one simple English sentence using the word), "
        "example_translation (Thai translation of that sentence)."
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    data = json.loads(response.text or "{}")
    return {
        "pronunciation": data.get("pronunciation", ""),
        "translation": data.get("translation", ""),
        "example": data.get("example", ""),
        "example_translation": data.get("example_translation", ""),
    }
