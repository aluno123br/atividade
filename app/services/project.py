import math

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ResourceNotFound
from app.models import Project
from app.repositories import ProfileRepository, ProjectRepository, TechnologyRepository
from app.schemas import PaginatedProjects, ProjectCreate, ProjectOut


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.project_repository = ProjectRepository(db)
        self.profile_repository = ProfileRepository(db)
        self.technology_repository = TechnologyRepository(db)

    def create(self, data: ProjectCreate) -> Project:
        profile = self.profile_repository.get_by_id(data.profile_id)
        if not profile:
            raise ResourceNotFound("Perfil informado não foi encontrado")

        technologies = self.technology_repository.get_many_by_ids(data.technology_ids)
        found_ids = {item.id for item in technologies}
        missing = sorted(set(data.technology_ids) - found_ids)
        if missing:
            raise BusinessRuleError(
                f"Tecnologias não encontradas: {', '.join(str(item) for item in missing)}"
            )

        project = Project(
            title=data.title.strip(),
            description=data.description.strip(),
            repository_url=str(data.repository_url),
            demo_url=str(data.demo_url) if data.demo_url else None,
            profile_id=data.profile_id,
            technologies=technologies,
        )
        return self.project_repository.create(project)

    def list_projects(self, technology: str | None, page: int, size: int) -> PaginatedProjects:
        projects, total = self.project_repository.list_filtered(technology, page, size)
        pages = math.ceil(total / size) if total else 0
        return PaginatedProjects(
            items=[ProjectOut.model_validate(project) for project in projects],
            total=total,
            page=page,
            size=size,
            pages=pages,
        )

    def upvote(self, project_id: int) -> Project:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise ResourceNotFound("Projeto não encontrado")
        project.upvotes += 1
        return self.project_repository.save(project)
