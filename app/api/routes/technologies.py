from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TechnologyCreate, TechnologyOut
from app.services import TechnologyService

router = APIRouter(prefix="/api/technologies", tags=["Technologies"])


@router.post("", response_model=TechnologyOut, status_code=status.HTTP_201_CREATED)
def create_technology(payload: TechnologyCreate, db: Session = Depends(get_db)):
    return TechnologyService(db).create(payload)


@router.get("", response_model=list[TechnologyOut])
def list_technologies(db: Session = Depends(get_db)):
    return TechnologyService(db).list_all()
