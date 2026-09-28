from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scenario import Scenario


def list_scenarios(db: Session) -> list[Scenario]:
    return list(db.scalars(select(Scenario)))


def get_scenario(db: Session, scenario_id: int) -> Scenario | None:
    return db.get(Scenario, scenario_id)
