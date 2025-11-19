"""
LangGraph용 게임 State 정의
모든 에이전트가 공유하는 게임 상태
"""

from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages


class GameState(TypedDict):
    """
    마피아 게임의 전체 상태

    LangGraph의 모든 노드가 이 상태를 공유하고 업데이트합니다.
    """

    # 대화 기록 (자동으로 메시지 추가)
    messages: Annotated[List, add_messages]

    # 게임 정보
    round_number: int  # 현재 라운드
    phase: str  # 게임 페이즈: "intro", "discussion", "voting", "end"
    turn_count: int  # 현재 라운드에서 몇 명이 말했는지
    ai_turns_per_round: int  # 한 라운드당 AI가 말하는 횟수 (기본 3)

    # 캐릭터 정보
    characters: List[dict]  # 모든 캐릭터 정보
    mafia_name: Optional[str]  # 범인 이름 (비밀)

    # 현재 턴
    current_speaker: Optional[str]  # 현재 말하는 사람
    next_speaker: Optional[str]  # 다음 차례

    # 유저 입력
    user_input: Optional[str]  # 유저가 입력한 내용
    user_target: Optional[str]  # 유저가 지목한 캐릭터

    # 투표 결과
    votes: dict  # {투표자: 피투표자}
    accused: Optional[str]  # 지목된 사람
    game_result: Optional[str]  # "win" 또는 "lose"
