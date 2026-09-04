from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateResource, ResourceNotFound
from app.models import Profile
from app.repositories import ProfileRepository
from app.schemas import ProfileCreate


class ProfileService:
    def __init__(self, db: Session):
        self.repository = ProfileRepository(db)

    def create(self, data: ProfileCreate) -> Profile:
        if self.repository.get_by_email(data.email):
            raise DuplicateResource("Já existe um perfil cadastrado com este e-mail")

        profile = Profile(
            name=data.name.strip(),
            bio=data.bio.strip() if data.bio else None,
            email=data.email.lower(),
            github_url=str(data.github_url),
            linkedin_url=str(data.linkedin_url) if data.linkedin_url else None,
        )
        try:
            return self.repository.create(profile)
        except IntegrityError as exc:
            self.repository.db.rollback()
            raise DuplicateResource("Não foi possível cadastrar o perfil por conflito de dados") from exc

    def get_by_id(self, profile_id: int) -> Profile:
        profile = self.repository.get_by_id(profile_id)
        if not profile:
            raise ResourceNotFound("Perfil não encontrado")
        return profile
