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
        The ta
