from typing import TypedDict

class State (TypedDict):
    task: str
    plan: str
    review: str
    result: str
    attempts: int