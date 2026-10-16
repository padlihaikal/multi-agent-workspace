from langgraph.graph import StateGraph, START, END
from state import State
from llm import ask
from agents import planner, worker, reviewer

MAX_ATTEMPTS = 3

def supervisor (state: State) -> str:
    plan = state.get("plan")
    result = state.get("result")
    review = state.get("review")
    attempts = state.get("attempts", 0)

    if not plan:
        return ("planner")
    elif not result:
        return ("worker")
    elif not review:
        return ("review")
    elif review .startswith ("REVISE") and attempts < MAX_ATTEMPTS:
        return ("worker")
    else:
        return END

def supervisor_llm(state:State) -> str:
    system_prompt = (
        "Choose exactly one: planner, worker, review or FINISH. "
        "If plan is missing, choose planner. "
        "If plan exists but result is missing, choose worker. "
        "If plan and result exists but review is missing, choose review. "
        "If all exist, choose FINISH. "
        "Reply with one word only. "
    )
    user_prompt = (
        f"Task: {state.get('task', '')}\n"
        f"Plan: {state.get('plan', '')}\n"
        f"Result: {state.get('result', '')}\n"
        f"Review: {state.get('review', '')}"
    )
    try:
        source = ask(system_prompt, user_prompt)
        source_result = source.strip().lower()
        print(f"Supervisor chose: {source_result}")

        if source_result == "finish":
            source_result = END
        
    except Exception as e :
        print(f"LLM error: {e}")
        #print("LLM error, falling back to Python rules")
        return supervisor(state)

    return source_result

builder = StateGraph(State)
builder.add_node("planner", planner)
builder.add_node("worker", worker)
builder.add_node("review", reviewer)
builder.add_conditional_edges(START, supervisor_llm)
builder.add_conditional_edges("planner", supervisor_llm)
builder.add_conditional_edges("worker", supervisor_llm)
builder.add_conditional_edges("review", supervisor_llm)

graph = builder.compile()

output = graph.invoke({
    "task": "Explain what a REST API is in 3 sentences"
})
print(output["review"], output["attempts"])