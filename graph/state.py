"""
LangGraph용 게임 State 정의
모든 에이전트가 공유하는 게임 상태
"""

from typing import Annotated, TypedDict, List, Optional, Dict
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
    phase: str  # 게임 페이즈: "intro", "discussion", "voting", "end", "night", "one_on_one"
    day_night: str  # "day" or "night"
    turn_count: int  # 현재 라운드에서 몇 명이 말했는지

    # 캐릭터 정보
    characters: List[dict]  # 모든 캐릭터 정보
    mafia_name: Optional[str]  # 범인 이름 (비밀)
    alive_status: Dict[str, bool]  # 생존 여부 {이름: True/False}
    suspicion_counts: Dict[str, int]  # 의심 횟수 {이름: count}

    # 로그 및 요약
    night_logs: List[str]  # 밤 행동 로그
    round_summary: Optional[str]  # 이전 라운드 요약 (Legacy)
    round_summaries: Dict[int, str]  # 라운드별 요약 {라운드: 요약}
    death_log: List[str]  # 사망 로그

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
