from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from graph.workflow import create_game_graph
from langgraph.types import Command
import uuid
import os

app = FastAPI(title="Phantom Log API")

# 간단한 인메모리 저장소 (실제 앱에서는 데이터베이스 사용 권장)
# LangGraph checkpointer가 설정된 경우 실제 상태 유지를 처리하지만,
# 여기서는 thread_id만 관리하면 됩니다.
# create_game_graph에서 MemorySaver를 사용한다고 가정하므로,
# 세션의 thread_id만 추적하면 됩니다.

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
    round_summaries: Dict[int, str]
    game_over: bool
    winner: Optional[str] = None

# 그래프 초기화
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
    
    # 초기 실행
    # 첫 번째 인터럽트(아마도 wait_for_user_node)까지 실행됩니다
    result = game_graph.invoke({}, config)
    
    # 실행 후 상태 가져오기
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
        "round_summaries": state.get("round_summaries", {}),
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
    
    # 게임 종료 조건 확인 (해당되는 경우)
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
        "round_summaries": state.get("round_summaries", {}),
        "game_over": game_over,
        "winner": state.get("phantom_name") if game_over else None
    }

@app.post("/api/game/action", response_model=GameStateResponse)
async def perform_action(request: ActionRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    current_state = game_graph.get_state(config)
    
    if not current_state.values:
        raise HTTPException(status_code=404, detail="Game session not found")

    # 액션 타입에 따라 재개 데이터 결정
    resume_data = {}
    
    if request.action_type == "chat":
        # 사용자 채팅
        content = request.content
        resume_data = {"user_input": content}
        
        # 1:1 대화 패턴 감지 ([이름에게] 메시지)
        if content and content.startswith("[") and "에게]" in content:
            resume_data["phase"] = "one_on_one"
    elif request.action_type == "next":
        # 단순히 엔터/다음 누르기
        resume_data = {"action": "next"}
    elif request.action_type == "vote":
        # 팬텀 투표
        resume_data = {"user_target": request.target}
    elif request.action_type == "suspect":
        # 누군가를 의심하기
        resume_data = {
            "user_input": "suspect",
            "user_target": request.target
        }
    elif request.action_type == "one_on_one":
        # 1:1 대화 시작 요청
        # 그래프가 이를 처리할 수 있도록 phase를 변경하거나 특정 입력을 전달해야 함
        # 현재 로직상 1:1은 채팅 패턴으로 감지되지만, 명시적 요청도 처리
        resume_data = {
            "phase": "one_on_one",
            "user_target": request.target
        }
    elif request.action_type == "night_start":
         # 수동으로 밤 페이즈 시작 (필요한 경우)
         resume_data = {"phase": "night"}
    else:
        raise HTTPException(status_code=400, detail=f"Invalid action type: {request.action_type}")

    # 그래프 재개
    try:
        game_graph.invoke(Command(resume=resume_data), config)
    except Exception as e:
        # 그래프가 완료되거나 에러가 발생한 경우
        print(f"Graph execution error or finish: {e}")
        pass

    # 업데이트된 상태 가져오기
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
        "round_summaries": updated_state.get("round_summaries", {}),
        "game_over": game_over,
        "winner": updated_state.get("phantom_name") if game_over else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
