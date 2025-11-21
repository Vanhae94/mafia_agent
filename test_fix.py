
import os
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from langgraph.graph.message import add_messages
from graph.nodes import wait_for_user_node

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
workflow.add_node("wait", wait_for_user_node) # Use the actual node
workflow.add_node("process", process_input_node)

workflow.set_entry_point("setup")
workflow.add_edge("setup", "wait")
workflow.add_conditional_edges("wait", after_wait, {"process": "process", "wait": "wait"})
workflow.add_edge("process", "wait")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Simulation
def run_simulation():
    config = {"configurable": {"thread_id": "test_fix_thread_1"}}
    
    print("\n1. Initial Run")
    # Should run setup -> wait -> interrupt
    app.invoke({}, config)
    
    # Check state
    state = app.get_state(config)
    print(f"\nState after run 1: {state}")
    print(f"Next: {state.next}")
    
    if not state.next:
        print("❌ Graph finished or no next step. Interrupt failed?")
    else:
        print("✅ Graph paused at:", state.next)

    print("\n2. Second Run (Providing Input)")
    
    # Use Command(resume=...) explicitly as we did in the main game
    from langgraph.types import Command
    print("Using Command(resume=...)")
    result = app.invoke(Command(resume={"user_input": "hello"}), config)

    print(f"\nResult state: {result.get('user_input')}, count: {result.get('count')}")
    
    if result.get('count') == 1:
        print("\n✅ SUCCESS: State updated and graph progressed.")
    else:
        print("\n❌ FAILURE: State did not update or graph did not progress.")

if __name__ == "__main__":
    run_simulation()
