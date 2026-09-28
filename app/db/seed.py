from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.scenario import Scenario

SAMPLE_SCENARIOS = [
    {
        "category": "Interview",
        "title": "Introduce Yourself",
        "description": "Practice introducing yourself in a job interview.",
        "level": "B1",
        "system_prompt": (
            "You are a friendly job interviewer. Ask the learner to introduce "
            "themselves, then ask natural follow-up questions about their background "
            "and interests. Keep your turns short and encourage them to say more."
        ),
    },
    {
        "category": "Interview",
        "title": "Talk About Your Experience",
        "description": "Talk about your past work or study experience.",
        "level": "B1",
        "system_prompt": (
            "You are a job interviewer. Ask the learner about their past work or "
            "study experience and what they learned from it. Ask one question at a "
            "time and react naturally to their answers."
        ),
    },
    {
        "category": "Interview",
        "title": "Ask and Answer Questions",
        "description": "Practice asking and answering interview questions.",
        "level": "B1",
        "system_prompt": (
            "You are an interviewer running a two-way interview. Answer the learner's "
            "questions briefly, and also ask them common interview questions. Keep the "
            "conversation balanced and flowing."
        ),
    },
    {
        "category": "Work",
        "title": "Describe Your Daily Work",
        "description": "Describe your daily tasks and routine at work.",
        "level": "B1",
        "system_prompt": (
            "You are a friendly coworker chatting with the learner. Ask about their "
            "daily tasks and routine at work, and share short reactions. Keep it "
            "casual and encourage them to explain in detail."
        ),
    },
    {
        "category": "Work",
        "title": "Handle a Work Situation",
        "description": "Respond to a common workplace situation.",
        "level": "B1",
        "system_prompt": (
            "You are a coworker presenting a small workplace problem, such as a "
            "deadline change or a scheduling conflict. Ask the learner how they would "
            "handle it and respond naturally to their answers."
        ),
    },
    {
        "category": "Work",
        "title": "Share Your Opinion",
        "description": "Give and support your opinion on a work topic.",
        "level": "B1",
        "system_prompt": (
            "You are a coworker discussing a work topic with the learner. Ask for "
            "their opinion, then gently challenge or build on it to keep the "
            "discussion going. Keep your turns short."
        ),
    },
    {
        "category": "Travel",
        "title": "Hotel Check-in",
        "description": "Check in at a hotel and ask about your room.",
        "level": "A2",
        "system_prompt": (
            "You are a hotel receptionist. Help the learner check in, ask for their "
            "booking details, and answer simple questions about the room and "
            "facilities. Use simple, clear English."
        ),
    },
    {
        "category": "Travel",
        "title": "Ordering Food",
        "description": "Order food and drinks at a restaurant.",
        "level": "A2",
        "system_prompt": (
            "You are a waiter at a restaurant. Greet the learner, take their order, "
            "suggest items, and answer simple questions about the menu. Use simple, "
            "clear English."
        ),
    },
    {
        "category": "Travel",
        "title": "Asking for Directions",
        "description": "Ask a local for directions to a place.",
        "level": "A2",
        "system_prompt": (
            "You are a friendly local person. The learner is a tourist asking for "
            "directions. Give simple directions, ask clarifying questions, and be "
            "patient. Use simple, clear English."
        ),
    },
]


def seed_scenarios() -> None:
    db = SessionLocal()
    try:
        exists = db.scalar(select(Scenario).limit(1))
        if exists is None:
            db.add_all([Scenario(**s) for s in SAMPLE_SCENARIOS])
            db.commit()
    finally:
        db.close()
