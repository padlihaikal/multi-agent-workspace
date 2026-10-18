# Multi Agent Workspace

## Description
A multi-agent workflow built with LangGraph. A planner creates a plan, a worker executes it, a reviewer checks the result, and a supervisor decides which agent runs next.

## Features
- Planner, worker, and reviewer agents powered by an LLM
- LLM-based supervisor that chooses the next step
- Python rule guard: LLM routing that contradicts the state is rejected
- Fallback to rule-based routing when the LLM call fails
- Revision loop: reviewer replies `APPROVED` or `REVISE`, with a maximum of 3 attempts
- Automatic retry (up to 3 attempts) for failed LLM calls

## Tech Stack
- Python
- LangGraph
- Groq API (OpenAI-compatible SDK)
- python-dotenv

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/Cendra10/multi-agent-workspace.git
   cd multi-agent-workspace
```
2. Create and activate a virtual environment:
```bash
   python -m venv .venv
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Create a `.env` file:
```
   GROQ_API_KEY=your_api_key
```

## Usage
Run the workflow:

```bash
python main.py
```

## Project Structure
```text
multi-agent-workspace/
    llm.py            # LLM client and ask() helper
    state.py          # Shared workflow state
    agents.py         # Planner, worker, and reviewer nodes
    supervisor.py     # Routing logic, rule guard, and fallback
    main.py           # Builds and runs the graph
    requirements.txt  # Python dependencies
    .gitignore
    README.md
```

## Example
```text
$ python main.py
LLM routing rejected: review. Using fallback: worker
APPROVED 1
```
The first line shows the rule guard correcting a wrong LLM routing choice. The last line shows the review result and the number of worker attempts.

## Future Improvement
- Make it interactive with a Q&A flow
- Fail fast on invalid API key errors instead of retrying
- Extend the rule-based supervisor (currently it only returns planner, worker, review, and END)
- Teach the supervisor prompt the `REVISE` rule

## License
MIT License