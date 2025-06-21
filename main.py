from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from config import Config
from executor.executor import AgentExecutor
from master_ai.planner import MasterAI

config = Config()


model = OpenAIModel(
    config.model, provider=OpenRouterProvider(api_key=config.openrouter_api_key)
)
master = MasterAI(model=model)

# Generate a plan
request = "Develop a marketing strategy for a new product launch, including social media campaigns and email marketing."
print(f"Generating plan for: {request}")

plan = master.generate_plan_sync(request)
print(f"\nGenerated plan: {plan.title}")
print(f"Description: {plan.description}")
print(f"Number of steps: {len(plan.steps)}")
print(f"Plan status: {plan.status}")

# Execute the plan
executor = AgentExecutor(model=model)
completed_plan = executor.execute_plan(plan)

# Display results
print("\n" + "=" * 50)
print("EXECUTION RESULTS")
print("=" * 50)

for step in completed_plan.steps:
    print(f"\n--- Step {step.step_number}: {step.description} ---")
    print(f"Status: {step.status}")
    if step.result:
        print(f"Output:\n{step.result}")
