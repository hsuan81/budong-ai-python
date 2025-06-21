from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from models.agents import AgentConfig


class GeneratePlanArgs(BaseModel):
    user_request: str = Field(
        ..., description="The user's original request in natural language"
    )


class Step(BaseModel):
    step_number: int
    description: str
    agent_config: AgentConfig = Field(
        ..., description="Configuration for the agent executing this step"
    )
    status: Literal["pending", "in_progress", "completed", "failed"] = Field(
        default="pending"
    )
    result: Optional[str] = Field(
        default=None, description="Result of executing this step"
    )
    feedback: Optional[str] = Field(
        default=None, description="Human feedback on the step"
    )
    feedback: Optional[str] = Field(
        default=None, description="Human feedback on the step"
    )


class Plan(BaseModel):
    user_request: str
    title: str = Field(description="Title of the plan")
    description: str = Field(
        description="Brief description of what the plan accomplishes"
    )
    steps: List[Step] = Field(description="List of steps to execute")
    status: Literal["planned", "executing", "complete"] = (
        "planned"  # Default status when a plan is created
    )
