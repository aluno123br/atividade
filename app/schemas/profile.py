from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl, StringConstraints

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=120)]
Bio = Annotated[str, StringConstraints(strip_whitespace=True, max_length=1000)]


class ProfileCreate(BaseModel):
    name: Name
    bio: Bio | None = None
    email: EmailStr
    github_url: HttpUrl
    linkedin_url: HttpUrl | None = None


class ProfileOut(BaseModel):
    id: int
    name: str
    bio: str | None
    email: EmailStr
    github_url: str
    linkedin_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
