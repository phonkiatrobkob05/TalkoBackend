from google import genai
from google.genai import types

from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

# system prompt สำหรับ Talko - ปรับได้ตาม scenario
SYSTEM_PROMPT = (
    "You are a friendly language-learning conversation partner. "
    "Keep replies short, natural, and encourage the learner to keep talking."
)


def generate_reply(message: str, history: list[dict] | None = None) -> str:
    """ส่งข้อความผู้ใช้ + ประวัติการคุย ไปให้ Gemini แล้วคืนคำตอบเป็น text"""
    contents: list[types.Content] = []

    if history:
        for turn in history:
            contents.append(
                types.Content(
                    role=turn["role"],  # "user" หรือ "model"
                    parts=[types.Part(text=turn["content"])],
                )
            )

    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text or ""
