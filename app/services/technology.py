from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateResource
from app.models import Technology
from app.repositories import TechnologyRepository
from app.schemas import TechnologyCreate


class TechnologyService:
    def __init__(self, db: Session):
        self.repository = TechnologyRepository(db)

    def create(self, data: TechnologyCreate) -> Technology:
        clean_name = data.name.strip()
        if self.repository.get_by_name(clean_name):
            raise DuplicateResource("Tecnologia já cadastrada")

        technology = Technology(name=clean_name)
        try:
            return self.repository.create(technology)
        except IntegrityError as exc:
            self.repository.db.rollback()
            raise DuplicateResource("Tecnologia já cadastrada") from exc

    def list_all(self) -> list[Technology]:
        return self.repository.list_all()
