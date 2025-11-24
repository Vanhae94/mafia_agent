"""
LangGraph Nodes
각 기능을 Node로 정의
"""

from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.types import interrupt
import os
from dotenv import load_dotenv
import random

load_dotenv()


def setup_game_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    게임 초기 세팅 노드
    - 캐릭터 정보 로드
    - 무작위 범인 선정
    """
    from characters import student, office_worker, artist, chef, teacher

    character_modules = [student, office_worker, artist, chef, teacher]

    # 캐릭터 정보 수집
    characters = []
    for module in character_modules:
        char_info = module.get_character_info()
        characters.append(char_info)

    # 무작위 범인 선정
    mafia = random.choice(characters)

    return {
        "characters": characters,
        "mafia_name": mafia["name"],
        "round_number": 1,
        "phase": "discussion",
        "turn_count": 0,
        "ai_turns_per_round": 3,  # 한 라운드당 AI 3명이 말함
        "messages": [SystemMessage(content="게임이 시작되었습니다.")],
        "votes": {},
        "current_speaker": characters[0]["name"],  # 첫 번째 캐릭터부터 시작
        "next_speaker": None,
        "user_input": None,
        "user_target": None,
        "accused": None,
        "game_result": None,
    }


def character_speak_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    캐릭터가 말하는 노드
    current_speaker에 해당하는 캐릭터가 발언
    """
    speaker_name = state.get("current_speaker")

    if not speaker_name:
        return state

    # 해당 캐릭터 찾기
    character = None
    for char in state["characters"]:
        if char["name"] == speaker_name:
            character = char
            break

    if not character:
        return state

    # LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 시스템 프롬프트 구성
    system_prompt = character["prompt"]

    # 범인이라면 특별 지시 추가
    if character["name"] == state["mafia_name"]:
        system_prompt += """

=== 중요: 당신의 역할 ===
🔴 당신은 이번 게임의 **범인(마피아)**입니다.

범인으로서의 임무:
1. 다른 사람들에게 들키지 않기
2. 평소 성격대로 행동하되, 의심받지 않도록 조심
3. 필요하면 거짓 알리바이를 만들어내기
4. 자연스럽게 다른 사람을 의심하기
========================
"""

    # 대화 맥락 구성
    conversation = [SystemMessage(content=system_prompt)]

    # 최근 대화 기록 추가 (마지막 5개)
    recent_messages = state.get("messages", [])[-5:]
    conversation.extend(recent_messages)

    # 프롬프트: 짧고 간결하게 발언하기
    prompt = """지금까지의 대화 흐름을 보고, 당신의 성격에 맞게 자연스럽게 한마디 하세요.

**중요 규칙:**
- 반드시 100자 이내로 짧게 말하세요
- 일상 대화처럼 자연스럽게
- 한 번에 한 가지 생각만 표현하세요
- 불필요한 설명은 생략하세요
"""
    conversation.append(HumanMessage(content=prompt))

    # AI 응답 생성
    response = llm.invoke(conversation)

    # 메시지 추가
    new_message = AIMessage(
        content=response.content,
        name=character["name"]
    )

    # 턴 카운트 증가
    new_turn_count = state.get("turn_count", 0) + 1

    return {
        "messages": [new_message],
        "turn_count": new_turn_count
    }


def user_input_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    유저 입력 처리 노드
    사용자가 입력한 후 다음 라운드로 진행
    """
    user_input = state.get("user_input", "")

    if not user_input:
        return state

    # 유저 메시지 추가
    user_message = HumanMessage(
        content=user_input,
        name="유저"
    )

    # 다음 라운드로 진행
    current_round = state.get("round_number", 1)
    
    # 기본 업데이트 값
    updates = {
        "messages": [user_message],
        "user_input": None,  # 초기화
        "phase": "discussion",  # 다시 토론 페이즈로
        "turn_count": 0,  # 턴 카운트 리셋
        "round_number": current_round + 1  # 라운드 증가
    }
    
    # 특정 대상 지목 확인 ([이름에게])
    import re
    match = re.search(r"\[(.*?)에게\]", user_input)
    if match:
        target_name = match.group(1)
        # 캐릭터 리스트에 존재하는지 확인
        characters = state.get("characters", [])
        for char in characters:
            if char["name"] == target_name:
                updates["current_speaker"] = target_name
                break

    return updates


def vote_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    투표 처리 노드
    """
    user_target = state.get("user_target")
    mafia_name = state.get("mafia_name")

    if not user_target:
        return state

    # 결과 판정
    if user_target == mafia_name:
        result = "win"
        message = f"🎉 정답입니다! {user_target}이(가) 범인이었습니다!"
    else:
        result = "lose"
        message = f"😢 틀렸습니다. {user_target}은(는) 범인이 아닙니다. 진짜 범인은 {mafia_name}입니다."

    return {
        "accused": user_target,
        "game_result": result,
        "phase": "end",
        "messages": [SystemMessage(content=message)]
    }


def next_turn_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    다음 턴으로 진행
    - AI 턴이 남았으면 다음 캐릭터로
    - AI 턴이 끝났으면 사용자 턴으로 (turn_count 리셋하지 않음)
    """
    characters = state.get("characters", [])
    current = state.get("current_speaker")
    turn_count = state.get("turn_count", 0)
    ai_turns_per_round = state.get("ai_turns_per_round", 3)

    if not characters:
        return state

    # 현재 인덱스 찾기
    current_idx = -1
    for i, char in enumerate(characters):
        if char["name"] == current:
            current_idx = i
            break

    # 다음 캐릭터 인덱스
    next_idx = (current_idx + 1) % len(characters)
    next_speaker = characters[next_idx]["name"]

    # turn_count가 ai_turns_per_round에 도달했으면 사용자 턴
    # 아니면 계속 AI 턴
    if turn_count >= ai_turns_per_round:
        # 사용자 턴으로 전환 (current_speaker는 그대로)
        return {
            "phase": "user_turn"
        }
    else:
        # 다음 AI 캐릭터로
        return {
            "current_speaker": next_speaker
        }


def wait_for_user_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    사용자 입력을 기다리는 노드
    LangGraph interrupt를 트리거해 그래프 실행을 일시 중단한다.
    """
    # interrupt는 재개 시 제공된 데이터(예: invoke를 통해)를 반환합니다.
    resume_data = interrupt("wait_user")
    
    # 데이터가 제공되었다면 상태를 업데이트하기 위해 반환합니다.
    if resume_data:
        return resume_data
        
    return state