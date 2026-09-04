from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints, field_validator

from app.schemas.technology import TechnologyOut

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Description = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=5000)]


class ProjectCreate(BaseModel):
    title: Title
    description: Description
    repository_url: HttpUrl
    demo_url: HttpUrl | None = None
    profile_id: int = Field(gt=0)
    technology_ids: list[int] = Field(min_length=1)

    @field_validator("technology_ids")
    @classmethod
    def technology_ids_must_be_unique(cls, value: list[int]) -> list[int]:
        if any(item <= 0 for item in value):
            raise ValueError("Todos os IDs de tecnologia devem ser maiores que zero")
        if len(value) != len(set(value)):
            raise ValueError("A lista de tecnologias não pode conter IDs repetidos")
        return value


class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    repository_url: str
    demo_url: str | None
    profile_id: int
    average_rating: float
    upvotes: int
    technologies: list[TechnologyOut]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedProjects(BaseModel):
    items: list[ProjectOut]
    total: int
    page: int
    size: int
    pages: int
