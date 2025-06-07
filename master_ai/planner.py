import json
import re
from typing import Any, Dict

from pydantic_ai import Agent

from models.plan import Plan


class MasterAI:
    """Corrected Master AI implementation using pydantic-ai."""

    def __init__(self, model):
        """Initialize with a specific model."""
        self.agent = Agent(
            model=model,
            system_prompt=(
                "You are a master planning AI. Your job is to break down user requests "
                "into a series of actionable steps that can be executed by specialized agents. "
                "Create a comprehensive plan with clear step descriptions and agent configurations. "
                "Each step should have a system_prompt and task_prompt in its agent_config.\n\n"
                "IMPORTANT: You must respond with ONLY valid JSON in this exact format:\n"
                "{\n"
                '  "user_request": "The original user request",\n'
                '  "title": "Plan title",\n'
                '  "description": "Plan description",\n'
                '  "steps": [\n'
                "    {\n"
                '      "step_number": 1,\n'
                '      "description": "Step description",\n'
                '      "agent_config": {\n'
                '        "system_prompt": "System prompt for this step",\n'
                '        "task_prompt": "Task prompt for this step"\n'
                "      },\n"
                '      "dependencies": [],\n'
                '      "status": "pending",\n'
                '      "result": ""\n'
                "    }\n"
                "  ],\n"
                '  "status": "awaiting_confirmation"\n'
                "}\n\n"
                "Do not include any text before or after the JSON. Only return valid JSON."
                "Check your response carefully to ensure it is valid JSON and follows the exact same format as above."
            ),
            # output_type=Plan,
            # system_prompt=(
            #     'You are a master planning AI. Your job is to break down user requests '
            #     'into a series of actionable steps that can be executed by specialized agents. '
            #     'Create a comprehensive plan with clear step descriptions and agent configurations. '
            #     'Each step should have a system_prompt and task_prompt in its agent_config.'
            # ),
        )

    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract and parse JSON from model response."""
        # Clean the response
        response_text = response_text.strip()

        print(f"Raw response from model: {response_text}")

        # Try to find JSON in the response using regex
        json_pattern = r"\{.*\}"
        match = re.search(json_pattern, response_text, re.DOTALL)

        if match:
            json_str = match.group()
        else:
            # If no JSON found, assume the entire response is JSON
            json_str = response_text

        print(f"Extracted JSON string: {json_str}")

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Failed to parse JSON from model response: {e}\nResponse: {response_text}"
            )

    async def generate_plan(self, user_request: str) -> Plan:
        """Generate a plan based on user request."""
        prompt = f"Create a detailed plan for this request: {user_request}"
        result = await self.agent.run(prompt)

        # Parse the response manually
        json_data = self._extract_json_from_response(str(result.output))

        # Ensure user_request is included
        json_data["user_request"] = user_request

        # Validate and create Plan object
        return Plan(**json_data)

    def generate_plan_sync(self, user_request: str) -> Plan:
        """Synchronous version of generate_plan."""
        prompt = f"Create a detailed plan for this request: {user_request}"
        result = self.agent.run_sync(prompt)

        # Parse the response manually
        json_data = self._extract_json_from_response(str(result.output))

        # Ensure user_request is included
        json_data["user_request"] = user_request

        # Validate and create Plan object
        return Plan(**json_data)  # Validate and create Plan object
        return Plan(**json_data)
