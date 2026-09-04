from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Feedback


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, feedback: Feedback) -> Feedback:
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def average_for_project(self, project_id: int) -> float:
        value = self.db.scalar(
            select(func.avg(Feedback.rating)).where(Feedback.project_id == project_id)
        )
        return round(float(value or 0.0), 2)
