# matac.py
import dspy
import os
from dspy.functional import TypedPredictor
from dotenv import load_dotenv
from transitions import Machine
import asyncio
from typing import List

load_dotenv()

# Create a language model using the Claude API
llm = dspy.OpenAI(
    model='gpt-4o',
    api_key=os.environ['OPENAI_API_KEY'],
    max_tokens=2000
)

dspy.settings.configure(lm=llm)

if not os.path.exists('scratchpad'):
    os.makedirs('scratchpad')

if not os.path.exists('versions'):
    os.makedirs('versions')

class TaskSignature(dspy.Signature):
    task_description = dspy.InputField(desc="The description of the task")
    agent_id = dspy.OutputField(desc="The ID of the agent assigned to the task")
    rationale = dspy.OutputField(desc="The rationale for the task assignment")

class Agent(Machine):
    def __init__(self, llm, name, skills=None):
        self.llm = llm
        self.skills = skills or []
        self.task = None
        states = ['idle', 'assigned', 'executing', 'completed']
        Machine.__init__(self, states=states, initial='idle')
        self.name = name  # Set the name attribute after Machine initialization
        print(f"Agent initialized with name: {self.name}")  # Debug statement
        self.add_transition('assign_task', 'idle', 'assigned')
        self.add_transition('start_execution', 'assigned', 'executing')
        self.add_transition('complete_task', 'executing', 'completed')
        self.add_transition('reset', 'completed', 'idle')

    async def execute_task(self):
        if self.task:
            self.start_execution()
            print(f"{self.name} executing task: {self.task['description']}")
            # Simulate task execution
            prompt = f"{self.name}, imagine you are an AI agent with skills in {', '.join(self.skills)}. Please provide a detailed response on how you would execute the following task: {self.task['description']}. Be specific and provide relevant examples or steps."
            response = self.llm(prompt).pop()
            self.task['execution_result'] = response
            print(f"{self.name} completed task: {self.task['description']} with result: {response}")
            self.complete_task()
            self.task = None

class TaskAllocator:
    def __init__(self, llm, agents: List[Agent]):
        self.llm = llm
        self.agents = agents

    def allocate_task(self, task_description):
        prompt = f"""
        The task is described as follows: "{task_description}". 
        Assign this task to the most suitable agent based on their skills.

        Available agents and their skills:
        - Agent 1: frontend, backend
        - Agent 2: backend
        - Agent 3: frontend, design

        Provide the response in the following format:
        Agent ID: [agent_id]
        Rationale: [rationale]
        """
        response = self.llm(prompt).pop()
        print(f"Response from Claude: {response}")

        # Parse the response to extract agent_id and rationale
        lines = response.strip().split("\n")
        agent_id = None
        rationale = None
        for line in lines:
            if line.strip().startswith("Agent ID:"):
                agent_id = line.strip().split(":")[-1].strip()  # Extract agent ID without adding "Agent" prefix
            elif line.strip().startswith("Rationale:"):
                rationale = line.strip().split(":", 1)[-1].strip()

        if agent_id and rationale:
            print(f"Looking for agent with ID: {agent_id}")
            print(f"Available agents: {[agent.name for agent in self.agents]}")
            agent = next((agent for agent in self.agents if agent_id in agent.name), None)
            if agent:
                print(f"Found agent: {agent.name}")
                if agent.state == 'idle':
                    agent.task = {'description': task_description, 'rationale': rationale}
                    agent.assign_task()
                    print(f"Task '{task_description}' allocated to {agent.name} with rationale: {rationale}")
                else:
                    print(f"Agent {agent.name} is already assigned a task. Skipping task allocation.")
            else:
                print(f"Agent with ID {agent_id} not found.")
        else:
            print("Unable to parse the response and allocate the task.")

    async def coordinate_execution(self):
        tasks = [agent.execute_task() for agent in self.agents if agent.state == 'assigned']
        await asyncio.gather(*tasks)

# Initialize agents
agents = [
    Agent(llm, name="Agent 1", skills=["frontend", "backend"]),
    Agent(llm, name="Agent 2", skills=["backend"]),
    Agent(llm, name="Agent 3", skills=["frontend", "design"])
]

# Initialize task allocator
task_allocator = TaskAllocator(llm, agents)

# Main execution loop
tasks_to_allocate = [
    "Build the user interface",
    "Set up the database",
    "Design the user experience"
]

async def main():
    for task in tasks_to_allocate:
        task_allocator.allocate_task(task)
    await task_allocator.coordinate_execution()

asyncio.run(main())
