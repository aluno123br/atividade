from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Project, Technology, project_technology


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return self.get_by_id(project.id)  # type: ignore[return-value]

    def get_by_id(self, project_id: int) -> Project | None:
        stmt = (
            select(Project)
            .options(selectinload(Project.technologies))
            .where(Project.id == project_id)
        )
        return self.db.scalar(stmt)

    def list_filtered(
        self,
        technology: str | None,
        page: int,
        size: int,
    ) -> tuple[list[Project], int]:
        stmt = select(Project).options(selectinload(Project.technologies))
        count_stmt = select(func.count(func.distinct(Project.id)))

        if technology:
            stmt = (
                stmt.join(project_technology, Project.id == project_technology.c.project_id)
                .join(Technology, Technology.id == project_technology.c.technology_id)
                .where(Technology.name.ilike(technology))
            )
            count_stmt = (
                count_stmt.select_from(Project)
                .join(project_technology, Project.id == project_technology.c.project_id)
                .join(Technology, Technology.id == project_technology.c.technology_id)
                .where(Technology.name.ilike(technology))
            )
        else:
            count_stmt = count_stmt.select_from(Project)

        total = int(self.db.scalar(count_stmt) or 0)
        stmt = stmt.order_by(Project.id.desc()).offset(page * size).limit(size)
        projects = list(self.db.scalars(stmt).unique().all())
        return projects, total

    def save(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return self.get_by_id(project.id)  # type: ignore[return-value]
