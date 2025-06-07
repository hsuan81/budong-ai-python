from typing import List, Literal

from pydantic import BaseModel, Field

from models.step import Step


class GeneratePlanArgs(BaseModel):
    user_request: str = Field(
        ..., description="The user's original request in natural language"
    )


class Plan(BaseModel):
    user_request: str
    title: str = Field(description="Title of the plan")
    description: str = Field(
        description="Brief description of what the plan accomplishes"
    )
    steps: List[Step] = Field(description="List of steps to execute")
    status: Literal["awaiting_confirmation", "executing", "complete"] = (
        "awaiting_confirmation"
    )
