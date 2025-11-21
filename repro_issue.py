
import os
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from langgraph.graph.message import add_messages

# Mock State
class GameState(TypedDict):
    messages: Annotated[list, add_messages]
    phase: str
    user_input: str | None
    count: int

# Nodes
def setup_node(state: GameState) -> Dict[str, Any]:
    print("--- SETUP NODE RUNNING ---")
    return {"phase": "setup", "count": 0, "messages": []}

def wait_node(state: GameState) -> Dict[str, Any]:
    print("--- WAIT NODE RUNNING ---")
    # Current implementation in the user's code:
    interrupt("wait_user")
    return state

def process_input_node(state: GameState) -> Dict[str, Any]:
    print(f"--- PROCESS INPUT NODE: {state.get('user_input')} ---")
    return {"user_input": None, "count": state["count"] + 1}

# Edges
def after_wait(state: GameState) -> str:
    print(f"--- CHECKING AFTER WAIT: input={state.get('user_input')} ---")
    if state.get("user_input"):
        return "process"
    return "wait"

# Graph Construction
workflow = StateGraph(GameState)
workflow.add_node("setup", setup_node)
workflow.add_node("wait", wait_node)
workflow.add_node("process", process_input_node)

workflow.set_entry_point("setup")
workflow.add_edge("setup", "wait")
workflow.add_conditional_edges("wait", after_wait, {"process": "process", "wait": "wait"})
workflow.add_edge("process", "wait")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Simulation
def run_simulation():
    config = {"configurable": {"thread_id": "test_thread_1"}}
    
    print("\n1. Initial Run")
    # Should run setup -> wait -> interrupt
    app.invoke({}, config)
    
    print("\n2. Second Run (Providing Input)")
    # Should resume from wait. 
    # If logic is wrong, it might restart setup OR loop at wait.
    result = app.invoke({"user_input": "hello"}, config)
    
    print(f"\nResult state: {result.get('user_input')}, count: {result.get('count')}")

if __name__ == "__main__":
    run_simulation()
