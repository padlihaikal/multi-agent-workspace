from state import State
from llm import ask

def planner(state: State) -> dict:
    system_prompt = "You are a planner. Create a short plan in 2-3 steps."
    user_prompt = f"Create a plan for this task: {state['task']}"

    plan = ask(system_prompt, user_prompt)
    return {"plan": plan}

def worker (state: State):
    read_review = state.get("review", "")
    attempts = state.get("attempts", 0)
    attempts += 1

    system_prompt = "You are a worker. Execute the task by following the provided plan."
    user_prompt = f"Task: {state['task']}\nPlan: {state['plan']}"

    if read_review:
        user_prompt += f"\nReviewer feedback: {read_review}"

    result = ask(system_prompt, user_prompt)
    return {
        "result": result,
        "attempts": attempts,
        "review": ""
        }

def reviewer (state: State) -> dict:
    system_prompt = (
        "You are a reviewer. Strictly verify whether "
        "the result addresses the task. "
        "respond ONLY in APPROVED OR REVISE . "
        "APPROVED - The result answers the task correctly. "
        "REVISE - The result does not explain enough details. "
    )
    user_prompt = (
        f"Task: {state['task']}\n"
        f"Plan: {state['plan']}\n"
        f"Result: {state['result']}"
    )

    review = ask(system_prompt, user_prompt)

    return {"review": review}