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
            "You are a friendly job interviewer. Ask the learner to introduce themselves, "
            "then ask natural follow-up questions. Keep your turns short."
        ),
        "objective": "The learner introduces themselves with name, background, and one interest or strength.",
        "pass_criteria": [
            "The learner states their name",
            "The learner mentions their background (study or work)",
            "The learner mentions one interest or personal strength",
        ],
        "min_pass": 3,
    },
    {
        "category": "Interview",
        "title": "Talk About Your Experience",
        "description": "Talk about your past work or study experience.",
        "level": "B1",
        "system_prompt": (
            "You are a job interviewer. Ask the learner about their past work or study "
            "experience and what they learned. Ask one question at a time."
        ),
        "objective": "The learner describes one past experience and what they learned from it.",
        "pass_criteria": [
            "The learner describes one specific past experience",
            "The learner says what they learned or gained from it",
        ],
        "min_pass": 2,
    },
    {
        "category": "Interview",
        "title": "Ask and Answer Questions",
        "description": "Practice asking and answering interview questions.",
        "level": "B1",
        "system_prompt": (
            "You are an interviewer running a two-way interview. Answer the learner's "
            "questions briefly and also ask them common interview questions."
        ),
        "objective": "The learner both answers a question and asks the interviewer at least one relevant question.",
        "pass_criteria": [
            "The learner answers the interviewer's question",
            "The learner asks the interviewer at least one relevant question",
        ],
        "min_pass": 2,
    },
    {
        "category": "Work",
        "title": "Describe Your Daily Work",
        "description": "Describe your daily tasks and routine at work.",
        "level": "B1",
        "system_prompt": (
            "You are a friendly coworker. Ask about the learner's daily tasks and routine, "
            "and give short reactions."
        ),
        "objective": "The learner describes at least two daily tasks or parts of their routine.",
        "pass_criteria": [
            "The learner describes at least two distinct daily tasks",
            "The learner adds some detail such as when or how often",
        ],
        "min_pass": 2,
    },
    {
        "category": "Work",
        "title": "Handle a Work Situation",
        "description": "Respond to a common workplace situation.",
        "level": "B1",
        "system_prompt": (
            "You are a coworker presenting a small workplace problem such as a deadline "
            "change. Ask the learner how they would handle it."
        ),
        "objective": "The learner proposes a clear way to handle the situation.",
        "pass_criteria": [
            "The learner acknowledges the situation or problem",
            "The learner proposes a clear way to handle it",
            "The learner gives a reason for their choice",
        ],
        "min_pass": 2,
    },
    {
        "category": "Work",
        "title": "Share Your Opinion",
        "description": "Give and support your opinion on a work topic.",
        "level": "B1",
        "system_prompt": (
            "You are a coworker discussing a work topic. Ask for the learner's opinion, "
            "then gently build on or challenge it."
        ),
        "objective": "The learner states an opinion and gives at least one reason to support it.",
        "pass_criteria": [
            "The learner states a clear opinion",
            "The learner gives at least one supporting reason",
        ],
        "min_pass": 2,
    },
    {
        "category": "Travel",
        "title": "Hotel Check-in",
        "description": "Check in at a hotel and ask about your room.",
        "level": "A2",
        "system_prompt": (
            "You are a hotel receptionist. Help the learner check in and answer simple "
            "questions about the room. Use simple, clear English."
        ),
        "objective": "The learner gives booking details and asks at least one question about the room or facilities.",
        "pass_criteria": [
            "The learner gives booking or identity details to check in",
            "The learner asks at least one question about the room or facilities",
        ],
        "min_pass": 2,
    },
    {
        "category": "Travel",
        "title": "Ordering Food",
        "description": "Order food and drinks at a restaurant.",
        "level": "A2",
        "system_prompt": (
            "You are a waiter at a restaurant. Greet the learner, take their order, and "
            "answer simple questions about the menu."
        ),
        "objective": "The learner orders at least one food item and one drink.",
        "pass_criteria": [
            "The learner orders at least one food item",
            "The learner orders at least one drink",
        ],
        "min_pass": 2,
    },
    {
        "category": "Travel",
        "title": "Asking for Directions",
        "description": "Ask a local for directions to a place.",
        "level": "A2",
        "system_prompt": (
            "You are a friendly local person. The learner is a tourist asking for "
            "directions. Give simple directions and be patient."
        ),
        "objective": "The learner asks for directions to a place and confirms they understood.",
        "pass_criteria": [
            "The learner asks for directions to a specific place",
            "The learner confirms understanding, for example by repeating back or thanking",
        ],
        "min_pass": 2,
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
