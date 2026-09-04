from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

TechnologyName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]


class TechnologyCreate(BaseModel):
    name: TechnologyName


class TechnologyOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
