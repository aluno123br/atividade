from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import FeedbackCreate, FeedbackResult, PaginatedProjects, ProjectCreate, ProjectOut
from app.services import FeedbackService, ProjectService

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    return ProjectService(db).create(payload)


@router.get("", response_model=PaginatedProjects)
def list_projects(
    technology: str | None = Query(default=None, min_length=1),
    page: int = Query(default=0, ge=0),
    size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return ProjectService(db).list_projects(technology, page, size)


@router.post("/{project_id}/feedbacks", response_model=FeedbackResult, status_code=status.HTTP_201_CREATED)
def create_feedback(project_id: int, payload: FeedbackCreate, db: Session = Depends(get_db)):
    return FeedbackService(db).create(project_id, payload)


@router.put("/{project_id}/upvote", response_model=ProjectOut)
def upvote_project(project_id: int, db: Session = Depends(get_db)):
    return ProjectService(db).upvote(project_id)
