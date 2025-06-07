from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from models.plan import Plan
from models.step import Step, AgentConfig

# class AgentExecutor:
#     def __init__(self, client: OpenAI):
#         self.client = client

#     def run_agent(self, config: dict) -> str:
#         response = self.client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": config["system_prompt"]},
#                 {"role": "user", "content": config["task_prompt"]}
#             ]
#         )
#         return response.choices[0].message.content.strip()

#     def execute_plan(self, plan: Plan) -> Plan:
#         for step in plan.steps:
#             step.status = "in_progress"
#             try:
#                 step.result = self.run_agent(step.agent_config.dict())
#                 step.status = "completed"
#             except Exception as e:
#                 step.result = f"Execution error: {e}"
#                 step.status = "failed"
#         plan.status = "complete"
#         return plan

class AgentExecutor:
    """Executor for running planned steps."""
    
    def __init__(self, model: OpenAIModel):
        self.model = model

    def run_agent(self, config: dict) -> str:
        """Run a single agent with the given configuration."""
        agent = Agent(
            model=self.model,
            system_prompt=config.get("system_prompt", "You are a helpful assistant.")
        )

        prompt = config.get("task_prompt")
        if not prompt:
            raise ValueError("task_prompt must be provided in the agent configuration.")
        
        result = agent.run_sync(prompt)
        return str(result.output)

    def run_agent_test(self, config: dict) -> str:
        return "This is a test run of the agent with the provided configuration."

    def execute_plan(self, plan: Plan) -> Plan:
        """Execute all steps in a plan."""
        for step in plan.steps:
            step.status = "in_progress"
            try:
                config = step.agent_config.model_dump() if isinstance(step.agent_config, BaseModel) else step.agent_config
                step.result = self.run_agent_test(config)
                # step.result = self.run_agent(config)
                step.status = "completed"
            except Exception as e:
                step.result = f"Execution error: {e}"
                step.status = "failed"
        
        plan.status = "complete"
        return plan
