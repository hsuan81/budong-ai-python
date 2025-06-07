from typing import Literal, Optional

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    system_prompt: str = Field(
        ..., description="Prompt that sets the behavior of the agent"
    )
    task_prompt: str = Field(..., description="Specific instruction for the task")
    # tools: Optional[List[str]] = Field(default=None, description="Optional list of tools the agent can use")


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
