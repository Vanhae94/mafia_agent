from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from graph.workflow import create_game_graph
from langgraph.types import Command
import uuid
import os

app = FastAPI(title="Phantom Log API")

# In-memory storage for simplicity (in a real app, use a database)
# LangGraph checkpointer handles the actual state persistence if configured,
# but here we just need to manage thread_ids.
# Since we are using MemorySaver in create_game_graph (assumed), 
# we just need to keep track of the thread_id for the session.

class GameStartRequest(BaseModel):
    player_name: str = "User"

class ActionRequest(BaseModel):
    thread_id: str
    action_type: str  # "chat", "vote", "next"
    content: Optional[str] = None
    target: Optional[str] = None

class GameStateResponse(BaseModel):
    thread_id: str
    round_number: int
    phase: str
    day_night: str
    messages: List[Dict[str, Any]]
    characters: List[Dict[str, Any]]
    alive_status: Dict[str, bool]
    suspicion_counts: Dict[str, int]
    night_logs: List[str]
    clues: List[str]
    game_over: bool
    winner: Optional[str] = None

# Initialize Graph
game_graph = create_game_graph()

def format_messages(messages):
    formatted = []
    for msg in messages:
        sender = msg.name if hasattr(msg, 'name') else "System"
        content = msg.content
        formatted.append({"sender": sender, "content": content})
    return formatted

@app.post("/api/game/start", response_model=GameStateResponse)
async def start_game(request: GameStartRequest):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial invocation
    # This will run until the first interrupt (likely wait_for_user_node)
    result = game_graph.invoke({}, config)
    
    # Get the state after invocation
    state = game_graph.get_state(config).values
    
    return {
        "thread_id": thread_id,
        "round_number": state.get("round_number", 1),
        "phase": state.get("phase", "setup"),
        "day_night": state.get("day_night", "day"),
        "messages": format_messages(state.get("messages", [])),
        "characters": state.get("characters", []),
        "alive_status": state.get("alive_status", {}),
        "suspicion_counts": state.get("suspicion_counts", {}),
        "night_logs": state.get("night_logs", []),
        "clues": state.get("clues", []),
        "game_over": False,
        "winner": None
    }

@app.get("/api/game/state/{thread_id}", response_model=GameStateResponse)
async def get_game_state(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    current_state = game_graph.get_state(config)
    
    if not current_state.values:
        raise HTTPException(status_code=404, detail="Game session not found")
        
    state = current_state.values
    
    # Check for game over condition (if applicable)
    game_result = state.get("game_result")
    game_over = game_result is not None
    
    return {
        "thread_id": thread_id,
        "round_number": state.get("round_number", 1),
        "phase": state.get("phase", "unknown"),
        "day_night": state.get("day_night", "day"),
        "messages": format_messages(state.get("messages", [])),
        "characters": state.get("characters", []),
        "alive_status": state.get("alive_status", {}),
        "suspicion_counts": state.get("suspicion_counts", {}),
        "night_logs": state.get("night_logs", []),
        "clues": state.get("clues", []),
        "game_over": game_over,
        "winner": state.get("phantom_name") if game_over else None
    }

@app.post("/api/game/action", response_model=GameStateResponse)
async def perform_action(request: ActionRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    current_state = game_graph.get_state(config)
    
    if not current_state.values:
        raise HTTPException(status_code=404, detail="Game session not found")

    # Determine resume data based on action type
    resume_data = {}
    
    if request.action_type == "chat":
        # User chatting
        resume_data = {
            "user_input": request.content,
            # If in one_on_one, we might need to maintain phase, but user_input_node handles it
        }
    elif request.action_type == "next":
        # Just pressing enter/next
        resume_data = {"action": "next"}
    elif request.action_type == "vote":
        # Voting for phantom
        resume_data = {"user_target": request.target}
    elif request.action_type == "suspect":
        # Suspecting someone
        resume_data = {
            "user_input": "suspect",
            "user_target": request.target
        }
    elif request.action_type == "night_start":
         # Manually triggering night phase (if needed)
         resume_data = {"phase": "night"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action type")

    # Resume the graph
    try:
        game_graph.invoke(Command(resume=resume_data), config)
    except Exception as e:
        # If graph finishes or errors
        print(f"Graph execution error or finish: {e}")
        pass

    # Fetch updated state
    updated_state = game_graph.get_state(config).values
    
    game_result = updated_state.get("game_result")
    game_over = game_result is not None

    return {
        "thread_id": request.thread_id,
        "round_number": updated_state.get("round_number", 1),
        "phase": updated_state.get("phase", "unknown"),
        "day_night": updated_state.get("day_night", "day"),
        "messages": format_messages(updated_state.get("messages", [])),
        "characters": updated_state.get("characters", []),
        "alive_status": updated_state.get("alive_status", {}),
        "suspicion_counts": updated_state.get("suspicion_counts", {}),
        "night_logs": updated_state.get("night_logs", []),
        "clues": updated_state.get("clues", []),
        "game_over": game_over,
        "winner": updated_state.get("phantom_name") if game_over else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
