from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFound
from app.models import Feedback
from app.repositories import FeedbackRepository, ProjectRepository
from app.schemas import FeedbackCreate, FeedbackResult


class FeedbackService:
    def __init__(self, db: Session):
        self.feedback_repository = FeedbackRepository(db)
        self.project_repository = ProjectRepository(db)

    def create(self, project_id: int, data: FeedbackCreate) -> FeedbackResult:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ResourceNotFound("Projeto não encontrado")

        feedback = Feedback(
            rating=data.rating,
            comment=data.comment.strip(),
            project_id=project_id,
        )
        created = self.feedback_repository.create(feedback)
        project.average_rating = self.feedback_repository.average_for_project(project_id)
        self.project_repository.save(project)

        return FeedbackResult(
            feedback=created,
            project_average_rating=project.average_rating,
        )
