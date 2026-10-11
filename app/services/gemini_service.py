import json
import time

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)


def _generate(contents: list[types.Content], config: types.GenerateContentConfig, attempts: int = 4):
    last_error: Exception | None = None
    for index in range(attempts):
        try:
            return client.models.generate_content(
                model=settings.gemini_model,
                contents=contents,
                config=config,
            )
        except ServerError as error:
            last_error = error
            time.sleep(2.0 * (index + 1))
        except ClientError as error:
            last_error = error
            if getattr(error, "code", None) == 429:
                time.sleep(2.0 * (index + 1))
            else:
                raise
    raise last_error if last_error is not None else RuntimeError("generate failed")


def _history_contents(history: list[dict] | None) -> list[types.Content]:
    contents: list[types.Content] = []
    if history:
        for turn in history:
            contents.append(
                types.Content(role=turn["role"], parts=[types.Part(text=turn["content"])])
            )
    return contents


def _criteria_block(pass_criteria: list[str] | None, min_pass: int) -> tuple[str, int]:
    criteria = pass_criteria or []
    required = min_pass if min_pass else len(criteria)
    lines = "\n".join(f"- {c}" for c in criteria) if criteria else "- (no specific conditions)"
    return lines, required


def generate(system_prompt: str, message: str, history: list[dict] | None = None) -> str:
    contents = _history_contents(history)
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))
    response = _generate(contents, types.GenerateContentConfig(system_instruction=system_prompt))
    return response.text or ""


def generate_conversation(
    system_prompt: str,
    objective: str,
    pass_criteria: list[str] | None,
    min_pass: int,
    message: str,
    history: list[dict] | None = None,
) -> dict:
    lines, required = _criteria_block(pass_criteria, min_pass)
    instruction = (
        system_prompt
        + f" The learner's overall goal is: {objective}."
        + " These are the pass conditions:\n"
        + lines
        + f"\nMark finished=true ONLY when at least {required} of these conditions are clearly met "
        "across the whole conversation so far. If fewer are met, keep finished=false and gently "
        "guide the learner toward what is still missing. "
        "Return a JSON object with keys: reply (your spoken reply as a string) and "
        "finished (boolean)."
    )
    contents = _history_contents(history)
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))
    response = _generate(
        contents,
        types.GenerateContentConfig(system_instruction=instruction, response_mime_type="application/json"),
    )
    data = json.loads(response.text or "{}")
    return {"reply": data.get("reply", ""), "finished": bool(data.get("finished", False))}


def generate_feedback(
    objective: str,
    pass_criteria: list[str] | None,
    min_pass: int,
    level: str,
    history: list[dict],
    metrics: dict | None,
) -> dict:
    transcript = "\n".join(f"{turn['role']}: {turn['content']}" for turn in history)
    metrics_text = json.dumps(metrics) if metrics else "none"
    lines, required = _criteria_block(pass_criteria, min_pass)
    prompt = (
        "You are an English speaking examiner using IELTS and CEFR inspired criteria. "
        f"The learner's CEFR level is {level}. The scenario goal was: {objective}. "
        "Pass conditions (objectiveMet is true only when at least "
        f"{required} of them are clearly met):\n{lines}\n"
        f"Client-side fluency metrics (pauses and timing), may be empty: {metrics_text}. "
        "Evaluate only the learner's turns in this conversation transcript:\n"
        f"{transcript}\n\n"
        "Return a JSON object with keys: overall (int 0-100), "
        "scores (object with clarity, context, continuity, each int 0-100), "
        "objectiveMet (boolean), strengths (array of short strings), "
        "improvements (array of short strings). "
        "clarity = grammar and word accuracy; context = how well the learner fits the scenario goal; "
        "continuity = fluency and coherence, using the fluency metrics when provided."
    )
    response = _generate(
        [types.Content(role="user", parts=[types.Part(text=prompt)])],
        types.GenerateContentConfig(response_mime_type="application/json"),
    )
    data = json.loads(response.text or "{}")
    scores = data.get("scores", {})
    return {
        "overall": int(data.get("overall", 0)),
        "scores": {
            "clarity": int(scores.get("clarity", 0)),
            "context": int(scores.get("context", 0)),
            "continuity": int(scores.get("continuity", 0)),
        },
        "objectiveMet": bool(data.get("objectiveMet", False)),
        "strengths": list(data.get("strengths", [])),
        "improvements": list(data.get("improvements", [])),
    }


def generate_word_info(word: str) -> dict:
    prompt = (
        f'For the English word "{word}", return a JSON object with keys: '
        "pronunciation (IPA notation), translation (Thai), "
        "example (one simple English sentence using the word), "
        "example_translation (Thai translation of that sentence)."
    )
    response = _generate(
        [types.Content(role="user", parts=[types.Part(text=prompt)])],
        types.GenerateContentConfig(response_mime_type="application/json"),
    )
    data = json.loads(response.text or "{}")
    return {
        "pronunciation": data.get("pronunciation", ""),
        "translation": data.get("translation", ""),
        "example": data.get("example", ""),
        "example_translation": data.get("example_translation", ""),
    }
