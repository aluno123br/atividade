from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Comment = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=1000)]


class FeedbackCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Comment


class FeedbackOut(BaseModel):
    id: int
    rating: int
    comment: str
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FeedbackResult(BaseModel):
    feedback: FeedbackOut
    project_average_rating: float
