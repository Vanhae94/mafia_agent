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

    # 초기 생존 상태 및 의심 카운트 설정
    alive_status = {char["name"]: True for char in characters}
    suspicion_counts = {char["name"]: 0 for char in characters}

    return {
        "characters": characters,
        "mafia_name": mafia["name"],
        "round_number": 1,
        "phase": "discussion",
        "day_night": "day",
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
        "alive_status": alive_status,
        "suspicion_counts": suspicion_counts,
        "night_logs": [],
        "round_summary": "",
        "death_log": []
    }


def night_phase_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    밤 페이즈 처리 노드
    - 라운드 증가
    - 희생자 선정 (마피아 제외, 생존자 중 랜덤)
    - 생존 상태 업데이트
    - 밤 행동 로그 생성
    """
    characters = state.get("characters", [])
    mafia_name = state.get("mafia_name")
    alive_status = state.get("alive_status", {})
    round_number = state.get("round_number", 1)
    
    # 생존자 목록 (마피아 제외)
    targets = [
        char for char in characters 
        if char["name"] != mafia_name and alive_status.get(char["name"], True)
    ]
    
    night_log_entry = ""
    victim_name = None
    
    if targets:
        # 희생자 선정
        victim = random.choice(targets)
        victim_name = victim["name"]
        
        # 사망 처리
        alive_status[victim_name] = False
        
        # 로그 생성
        night_log_entry = f"Round {round_number} Night: {victim_name}이(가) 습격당해 사망했습니다."
        
        # 시스템 메시지 추가
        message = f"🌙 밤이 지났습니다.\n안타깝게도 {victim_name}이(가) 살해당한 채 발견되었습니다."
    else:
        message = "🌙 밤이 지났습니다. 아무 일도 일어나지 않았습니다."

    return {
        "round_number": round_number + 1,
        "phase": "discussion", # 다시 낮 토론으로
        "day_night": "day",
        "alive_status": alive_status,
        "night_logs": [night_log_entry] if night_log_entry else [],
        "messages": [SystemMessage(content=message)],
        "turn_count": 0
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

    # 초기 생존 상태 및 의심 카운트 설정
    alive_status = {char["name"]: True for char in characters}
    suspicion_counts = {char["name"]: 0 for char in characters}

    return {
        "characters": characters,
        "mafia_name": mafia["name"],
        "round_number": 1,
        "phase": "discussion",
        "day_night": "day",
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
        "alive_status": alive_status,
        "suspicion_counts": suspicion_counts,
        "night_logs": [],
        "round_summary": "",
        "death_log": []
    }


def night_phase_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    밤 페이즈 처리 노드
    - 라운드 증가
    - 희생자 선정 (마피아 제외, 생존자 중 랜덤)
    - 생존 상태 업데이트
    - 밤 행동 로그 생성
    """
    characters = state.get("characters", [])
    mafia_name = state.get("mafia_name")
    alive_status = state.get("alive_status", {})
    round_number = state.get("round_number", 1)
    
    # 생존자 목록 (마피아 제외)
    targets = [
        char for char in characters 
        if char["name"] != mafia_name and alive_status.get(char["name"], True)
    ]
    
    night_log_entry = ""
    victim_name = None
    
    if targets:
        # 희생자 선정
        victim = random.choice(targets)
        victim_name = victim["name"]
        
        # 사망 처리
        alive_status[victim_name] = False
        
        # 로그 생성
        night_log_entry = f"Round {round_number} Night: {victim_name}이(가) 습격당해 사망했습니다."
        
        # 시스템 메시지 추가
        message = f"🌙 밤이 지났습니다.\n안타깝게도 {victim_name}이(가) 살해당한 채 발견되었습니다."
    else:
        message = "🌙 밤이 지났습니다. 아무 일도 일어나지 않았습니다."

    return {
        "round_number": round_number + 1,
        "phase": "discussion", # 다시 낮 토론으로
        "day_night": "day",
        "alive_status": alive_status,
        "night_logs": [night_log_entry] if night_log_entry else [],
        "messages": [SystemMessage(content=message)],
        "turn_count": 0
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


def select_next_speaker_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    다음 발언자를 결정하는 노드 (LLM 기반)
    대화 맥락을 분석하여 가장 적절한 캐릭터를 선정함
    """
    messages = state.get("messages", [])
    characters = state.get("characters", [])
    alive_status = state.get("alive_status", {})
    current_speaker = state.get("current_speaker")
    
    # 생존한 캐릭터 이름 목록
    alive_names = [char["name"] for char in characters if alive_status.get(char["name"], True)]
    
    if not alive_names:
        return {}
        
    # LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # 최근 대화 (마지막 5개)
    recent_messages = messages[-5:]
    
    # 프롬프트 구성
    prompt = f"""
현재 생존자: {', '.join(alive_names)}
직전 발언자: {current_speaker}

최근 대화:
"""
    for msg in recent_messages:
        sender = msg.name if hasattr(msg, 'name') else "System"
        prompt += f"- {sender}: {msg.content}\n"
        
    prompt += """
위 대화 흐름을 보고, 다음으로 말하기에 가장 적절한 캐릭터의 이름을 하나만 출력하세요.

**선정 기준:**
1. 직전 발언이 특정인에게 질문했다면, 그 사람이 대답해야 합니다.
2. 누군가 의심받거나 공격받았다면, 그 사람이 변론해야 합니다.
3. 그렇지 않다면, 대화에 자연스럽게 끼어들거나 화제를 전환할 사람을 고르세요.
4. 직전 발언자는 가급적 제외하세요 (연속 발언 지양).

**출력 형식:**
캐릭터 이름만 딱 하나 출력하세요. (예: "김철수")
"""

    # LLM 호출
    response = llm.invoke([HumanMessage(content=prompt)])
    next_speaker = response.content.strip()
    
    # 유효성 검사 (생존자 목록에 있는지)
    # LLM이 이상한 답을 줄 경우를 대비해 후처리
    found = False
    for name in alive_names:
        if name in next_speaker: # 이름이 포함되어 있으면 인정
            next_speaker = name
            found = True
            break
            
    if not found:
        # 실패 시 랜덤 선정 (직전 발언자 제외 노력)
        candidates = [n for n in alive_names if n != current_speaker]
        if not candidates:
            candidates = alive_names
        next_speaker = random.choice(candidates)
        
    return {"current_speaker": next_speaker}


def user_input_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    유저 입력 처리 노드
    사용자가 입력한 후 다음 라운드로 진행
    """
    user_input = state.get("user_input", "")

    if not user_input:
        return state

    # 종료 명령어 처리 (1:1 모드에서 복귀)
    if user_input.lower() in ["q", "exit", "quit"]:
        return {
            "phase": "discussion",
            "user_input": None,
            "messages": [SystemMessage(content="1:1 대화를 종료하고 토론 모드로 돌아갑니다.")]
        }

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
        "turn_count": 0,  # 턴 카운트 리셋
        "round_number": current_round + 1  # 라운드 증가
    }

    # 현재 페이즈가 one_on_one이면 페이즈 유지
    if state.get("phase") == "one_on_one":
        updates["phase"] = "one_on_one"
        
        # 1:1 모드에서는 특정 대상 지목 로직 유지
        import re
        match = re.search(r"\[(.*?)에게\]", user_input)
        if match:
            target_name = match.group(1)
            characters = state.get("characters", [])
            for char in characters:
                if char["name"] == target_name:
                    updates["current_speaker"] = target_name
                    break
    elif state.get("phase") == "free_discussion":
        updates["phase"] = "free_discussion"
        # free_discussion 모드에서는 특정 대상 지목 로직 제거 (select_next_speaker_node가 처리)
    else:
        updates["phase"] = "discussion"
        # discussion 모드에서는 특정 대상 지목 로직 제거
        # 다음 화자는 select_next_speaker_node에서 결정됨

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
    # 1:1 모드이면 턴 넘기지 않음
    if state.get("phase") == "one_on_one":
        return {}

    characters = state.get("characters", [])
    current = state.get("current_speaker")
    turn_count = state.get("turn_count", 0)
    ai_turns_per_round = state.get("ai_turns_per_round", 3)
    alive_status = state.get("alive_status", {})

    if not characters:
        return state

    # 현재 인덱스 찾기
    current_idx = -1
    for i, char in enumerate(characters):
        if char["name"] == current:
            current_idx = i
            break

    # 다음 생존 캐릭터 찾기
    next_idx = current_idx
    next_speaker = None
    
    # 최대 캐릭터 수만큼 반복해서 생존자 찾기
    for _ in range(len(characters)):
        next_idx = (next_idx + 1) % len(characters)
        candidate = characters[next_idx]["name"]
        if alive_status.get(candidate, True):
            next_speaker = candidate
            break
            
    # 생존자가 없거나 혼자 남은 경우 (게임 종료 조건이지만 여기서는 처리 안 함)
    if not next_speaker:
        return {}

    # 무한 루프: turn_count 제한 없이 계속 AI 턴
    # 사용자가 개입(interrupt)하여 멈추거나 종료할 때까지 계속됨
    current_speaker = state.get("current_speaker")
    
    # 생존한 캐릭터 이름 목록
    alive_names = [char["name"] for char in characters if alive_status.get(char["name"], True)]
    
    if not alive_names:
        return {}
        
    # LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # 최근 대화 (마지막 5개)
    recent_messages = messages[-5:]
    
    # 프롬프트 구성
    prompt = f"""
현재 생존자: {', '.join(alive_names)}
직전 발언자: {current_speaker}

최근 대화:
"""
    for msg in recent_messages:
        sender = msg.name if hasattr(msg, 'name') else "System"
        prompt += f"- {sender}: {msg.content}\n"
        
    prompt += """
위 대화 흐름을 보고, 다음으로 말하기에 가장 적절한 캐릭터의 이름을 하나만 출력하세요.

**선정 기준:**
1. 직전 발언이 특정인에게 질문했다면, 그 사람이 대답해야 합니다.
2. 누군가 의심받거나 공격받았다면, 그 사람이 변론해야 합니다.
3. 그렇지 않다면, 대화에 자연스럽게 끼어들거나 화제를 전환할 사람을 고르세요.
4. 직전 발언자는 가급적 제외하세요 (연속 발언 지양).

**출력 형식:**
캐릭터 이름만 딱 하나 출력하세요. (예: "김철수")
"""

    # LLM 호출
    response = llm.invoke([HumanMessage(content=prompt)])
    next_speaker = response.content.strip()
    
    # 유효성 검사 (생존자 목록에 있는지)
    # LLM이 이상한 답을 줄 경우를 대비해 후처리
    found = False
    for name in alive_names:
        if name in next_speaker: # 이름이 포함되어 있으면 인정
            next_speaker = name
            found = True
            break
            
    if not found:
        # 실패 시 랜덤 선정 (직전 발언자 제외 노력)
        candidates = [n for n in alive_names if n != current_speaker]
        if not candidates:
            candidates = alive_names
        next_speaker = random.choice(candidates)
        
    return {"current_speaker": next_speaker}


def user_input_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    유저 입력 처리 노드
    사용자가 입력한 후 다음 라운드로 진행
    """
    user_input = state.get("user_input", "")

    if not user_input:
        return state

    # 종료 명령어 처리 (1:1 모드에서 복귀)
    if user_input.lower() in ["q", "exit", "quit"]:
        return {
            "phase": "discussion",
            "user_input": None,
            "messages": [SystemMessage(content="1:1 대화를 종료하고 토론 모드로 돌아갑니다.")]
        }

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
        "turn_count": 0,  # 턴 카운트 리셋
        "round_number": current_round + 1  # 라운드 증가
    }

    # 현재 페이즈가 one_on_one이면 페이즈 유지
    if state.get("phase") == "one_on_one":
        updates["phase"] = "one_on_one"
        
        # 1:1 모드에서는 특정 대상 지목 로직 유지
        import re
        match = re.search(r"\[(.*?)에게\]", user_input)
        if match:
            target_name = match.group(1)
            characters = state.get("characters", [])
            for char in characters:
                if char["name"] == target_name:
                    updates["current_speaker"] = target_name
                    break
    elif state.get("phase") == "free_discussion":
        updates["phase"] = "free_discussion"
        # free_discussion 모드에서는 특정 대상 지목 로직 제거 (select_next_speaker_node가 처리)
    else:
        updates["phase"] = "discussion"
        # discussion 모드에서는 특정 대상 지목 로직 제거
        # 다음 화자는 select_next_speaker_node에서 결정됨

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
    # 1:1 모드이면 턴 넘기지 않음
    if state.get("phase") == "one_on_one":
        return {}

    characters = state.get("characters", [])
    current = state.get("current_speaker")
    turn_count = state.get("turn_count", 0)
    ai_turns_per_round = state.get("ai_turns_per_round", 3)
    alive_status = state.get("alive_status", {})

    if not characters:
        return state

    # 현재 인덱스 찾기
    current_idx = -1
    for i, char in enumerate(characters):
        if char["name"] == current:
            current_idx = i
            break

    # 다음 생존 캐릭터 찾기
    next_idx = current_idx
    next_speaker = None
    
    # 최대 캐릭터 수만큼 반복해서 생존자 찾기
    for _ in range(len(characters)):
        next_idx = (next_idx + 1) % len(characters)
        candidate = characters[next_idx]["name"]
        if alive_status.get(candidate, True):
            next_speaker = candidate
            break
            
    # 생존자가 없거나 혼자 남은 경우 (게임 종료 조건이지만 여기서는 처리 안 함)
    if not next_speaker:
        return {}

    # 무한 루프: turn_count 제한 없이 계속 AI 턴
    # 사용자가 개입(interrupt)하여 멈추거나 종료할 때까지 계속됨
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
    # resume_data가 {} (빈 딕셔너리)일 수도 있으므로 None이 아니면 반환
    if resume_data is not None:
        return resume_data
        
    return state