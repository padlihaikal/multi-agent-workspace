from langgraph.graph import StateGraph, START
from state import State
from supervisor import supervisor_llm
from agents import planner, worker, reviewer

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