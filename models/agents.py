from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    system_prompt: str = Field(
        ..., description="Prompt that sets the behavior of the agent"
    )
    task_prompt: str = Field(..., description="Specific instruction for the task")
    # tools: Optional[List[str]] = Field(default=None, description="Optional list of tools the agent can use")
