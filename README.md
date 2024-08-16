# MATAC System (Multi-Agent Task Allocation and Coordination)

MATAC is a Python-based system designed for multi-agent task allocation and coordination using natural language processing and state machine concepts.

## Features

- Dynamic task allocation based on agent skills
- State-based agent management (idle, assigned, executing, completed)
- Asynchronous task execution
- Natural language task description and allocation
- Integration with OpenAI's GPT models for intelligent decision-making

## Components

1. **Agent**: Represents individual agents with specific skills and state management.
2. **TaskAllocator**: Handles task assignment to the most suitable agent.
3. **TaskSignature**: Defines the structure for task descriptions and allocations.

## Prerequisites

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/matac.git
   cd matac
   ```

2. Install dependencies:
   ```
   pip install dspy python-dotenv transitions
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Initialize agents with specific skills:
   ```python
   agents = [
       Agent(llm, name="Agent 1", skills=["frontend", "backend"]),
       Agent(llm, name="Agent 2", skills=["backend"]),
       Agent(llm, name="Agent 3", skills=["frontend", "design"])
   ]
   ```

2. Create a TaskAllocator:
   ```python
   task_allocator = TaskAllocator(llm, agents)
   ```

3. Define tasks and run the main execution loop:
   ```python
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
   ```

## Customization

- Modify the `Agent` class to add more states or transitions as needed.
- Extend the `TaskAllocator` to implement more sophisticated allocation strategies.
- Adjust the GPT model or prompt in the `TaskAllocator` for different allocation behaviors.

## File Structure

- `matac.py`: Main script containing the MATAC system implementation
- `scratchpad/`: Directory for temporary files (automatically created)
- `versions/`: Directory for version control (automatically created)

## Contributing

Contributions to improve MATAC are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- DSPy library for simplifying AI model interactions
- Transitions library for state machine implementation
