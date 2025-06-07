import asyncio
from typing import Optional
from core.master_ai import MasterAI
from core.agent_factory import AgentFactory
from core.execution_engine import ExecutionEngine
from utils.ai_client import AIClient, MockAIClient

class CLIInterface:
    """Command-line interface for the dynamic agent system"""
    
    def __init__(self):
        self.ai_client = MockAIClient()  # Use mock client for MVP
        self.master_ai = MasterAI(self.ai_client)
        self.agent_factory = AgentFactory(self.ai_client)
        self.execution_engine = ExecutionEngine(self.master_ai, self.agent_factory)
    
    async def run(self):
        """Main CLI loop"""
        print("🤖 Dynamic Agent System MVP")
        print("Available commands: plan, modify, execute, status, quit")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == "quit":
                    break
                elif command == "plan":
                    await self._handle_plan_creation()
                elif command == "modify":
                    await self._handle_plan_modification()
                elif command == "execute":
                    await self._handle_execution()
                elif command == "status":
                    await self._handle_status()
                else:
                    print("Unknown command. Available: plan, modify, execute, status, quit")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    async def _handle_plan_creation(self):
        """Handle plan creation"""
        user_request = input("Enter your request: ").strip()
        if not user_request:
            print("Request cannot be empty")
            return
        
        print("🔄 Creating plan...")
        plan = await self.master_ai.create_plan(user_request)
        
        print(f"\n📋 Plan created: {plan.id}")
        print(f"Description: {plan.description}")
        print(f"Steps: {len(plan.steps)}")
        for i, step in enumerate(plan.steps, 1):
            print(f"  {i}. {step.description}")
        print(f"Required agents: {plan.required_agents}")
        
        confirm = input("\nConfirm this plan? (y/n): ").strip().lower()
        if confirm == 'y':
            print("Plan confirmed and ready for execution")
        else:
            print("Plan created but not confirmed")
    
    async def _handle_plan_modification(self):
        """Handle plan modification"""
        if not self.master_ai.plans:
            print("No plans available to modify")
            return
        
        # Show available plans
        print("Available plans:")
        for plan_id, plan in self.master_ai.plans.items():
            print(f"  {plan_id}: {plan.description}")
        
        plan_id = input("Enter plan ID to modify: ").strip()
        if plan_id not in self.master_ai.plans:
            print("Plan not found")
            return
        
        modifications = input("Enter modifications: ").strip()
        
        print("🔄 Modifying plan...")
        updated_plan = await self.master_ai.modify_plan(plan_id, modifications)
        
        print(f"\n📋 Plan updated: {plan_id}")
        print(f"Description: {updated_plan.description}")
        for i, step in enumerate(updated_plan.steps, 1):
            print(f"  {i}. {step.description}")
    
    async def _handle_execution(self):
        """Handle plan execution"""
        if not self.master_ai.plans:
            print("No plans available to execute")
            return
        
        # Show available plans
        print("Available plans:")
        for plan_id, plan in self.master_ai.plans.items():
            print(f"  {plan_id}: {plan.description} (Status: {plan.status})")
        
        plan_id = input("Enter plan ID to execute: ").strip()
        if plan_id not in self.master_ai.plans:
            print("Plan not found")
            return
        
        print("🚀 Executing plan...")
        result = await self.execution_engine.execute_plan(plan_id)
        
        print(f"\n✅ Execution completed: {result['status']}")
        print(f"Summary: {result['summary']}")
        
        # Show detailed results
        for i, step_result in enumerate(result['results'], 1):
            print(f"\nStep {i}: {step_result.status}")
            if step_result.output:
                print(f"Output: {step_result.output[:200]}...")
            if step_result.error_message:
                print(f"Error: {step_result.error_message}")
    
    async def _handle_status(self):
        """Show system status"""
        print(f"\n📊 System Status")
        print(f"Plans: {len(self.master_ai.plans)}")
        print(f"Agents: {len(self.agent_factory.agents)}")
        
        if self.master_ai.plans:
            print("\nPlans:")
            for plan_id, plan in self.master_ai.plans.items():
                print(f"  {plan_id}: {plan.status}")
        
        if self.agent_factory.agents:
            print("\nAgents:")
            for agent_id, agent in self.agent_factory.agents.items():
                print(f"  {agent_id}: {agent.spec.role}")