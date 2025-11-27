"""
LangGraph Nodes
각 기능을 Node로 정의
"""

from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.types import interrupt
import os
from dotenv import load_dotenv
import random
import json

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
        "ai_turns_per_round": 3,
        "messages": [SystemMessage(content="게임이 시작되었습니다.")],
        "votes": {},
        "current_speaker": characters[0]["name"],
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

    # 의심 수치 반영
    suspicion_counts = state.get("suspicion_counts", {})
    my_suspicion = suspicion_counts.get(speaker_name, 0)
    
    system_prompt += f"\n\n[상태 정보]\n현재 당신의 의심 수치: {my_suspicion}\n"
    
    if my_suspicion >= 1:
        system_prompt += "사람들이 당신을 의심하고 있습니다. 다소 방어적이거나 예민하게 반응하세요.\n"

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
        if my_suspicion >= 2:
            system_prompt += """
🚨 [위기 상황] 의심 수치가 매우 높습니다! (2 이상)
당신은 지금 매우 당황하고 있습니다.
- 말이 빨라지거나, 횡설수설하거나, 앞뒤가 안 맞는 말을 하세요.
- "아니, 그게 아니라...", "잠깐만요, 제 말 좀 들어보세요!" 같은 표현을 쓰며 필사적으로 변명하세요.
- 말실수를 하거나 과도하게 화를 내는 것도 좋습니다.
"""
    else:
        # 시민인데 의심받는 경우
        if my_suspicion >= 2:
            system_prompt += """
🚨 [위기 상황] 억울하게 의심받고 있습니다! (의심 수치 2 이상)
당신은 결백한데 몰리고 있어 매우 답답하고 화가 납니다.
- 강하게 부인하고, 논리적으로 반박하려 노력하세요.
- "증거가 있나요?", "왜 저를 의심하시죠?"라며 따지세요.
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
    suspicion_counts = state.get("suspicion_counts", {})
    
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

[의심 수치]
{json.dumps(suspicion_counts, ensure_ascii=False)}

최근 대화:
"""
    for msg in recent_messages:
        sender = msg.name if hasattr(msg, 'name') else "System"
        prompt += f"- {sender}: {msg.content}\n"
        
    prompt += """
위 대화 흐름을 보고, 다음으로 말하기에 가장 적절한 캐릭터의 이름을 하나만 출력하세요.

**선정 기준:**
1. 직전 발언이 특정인에게 질문했다면, 그 사람이 대답해야 합니다.
2. 누군가 의심받거나 공격받았다면, 그 사람이 변론해야 합니다. (의심 수치가 높은 사람에게 발언 기회를 주세요)
3. 그렇지 않다면, 대화에 자연스럽게 끼어들거나 화제를 전환할 사람을 고르세요.
4. 직전 발언자는 가급적 제외하세요 (연속 발언 지양).

**출력 형식:**
캐릭터 이름만 딱 하나 출력하세요. (예: "김철수")
"""

    # LLM 호출
    response = llm.invoke([HumanMessage(content=prompt)])
    next_speaker = response.content.strip()
    
    # 유효성 검사 (생존자 목록에 있는지)
    found = False
    for name in alive_names:
        if name in next_speaker:
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
    (사실상 discussion 모드에서는 select_next_speaker가 역할을 대신하지만,
     기존 로직 호환성을 위해 유지)
    """
    return {}


def wait_for_user_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    사용자 입력을 기다리는 노드
    LangGraph interrupt를 트리거해 그래프 실행을 일시 중단한다.
    """
    resume_data = interrupt("wait_user")
    
    if resume_data is not None:
        return resume_data
        
    return state


def suspicion_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    사용자가 특정 캐릭터를 의심하는 노드
    """
    target_name = state.get("user_target")
    suspicion_counts = state.get("suspicion_counts", {})
    
    if target_name and target_name in suspicion_counts:
        suspicion_counts[target_name] += 1
        message = f"👁️ 유저가 {target_name}을(를) 의심합니다. (의심 수치: {suspicion_counts[target_name]})"
    else:
        message = "⚠️ 의심 대상을 찾을 수 없습니다."
        
    return {
        "suspicion_counts": suspicion_counts,
        "messages": [SystemMessage(content=message)],
        "user_target": None, # 타겟 초기화
        "user_input": None   # 입력 초기화
    }


def ai_suspicion_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    라운드 종료 시 AI들이 서로를 의심하는 노드
    """
    messages = state.get("messages", [])
    characters = state.get("characters", [])
    alive_status = state.get("alive_status", {})
    suspicion_counts = state.get("suspicion_counts", {})
    
    # 생존자 목록
    alive_names = [char["name"] for char in characters if alive_status.get(char["name"], True)]
    
    if len(alive_names) < 2:
        return {}

    # LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # 최근 대화 분석 (최대 20개)
    recent_messages = messages[-20:]
    
    prompt = f"""
현재 생존자: {', '.join(alive_names)}

최근 대화 내용을 바탕으로, AI 캐릭터들이 서로를 의심할 만한 상황인지 분석하세요.
각 캐릭터별로 가장 의심스러운 사람을 1명씩 지목하거나, 없으면 "None"을 선택하세요.

**분석 기준:**
1. 말이 앞뒤가 안 맞거나, 거짓말을 하는 것 같은 사람
2. 지나치게 방어적이거나, 반대로 지나치게 공격적인 사람
3. 마피아 같은 행동을 보인 사람

**출력 형식 (JSON):**
{{
    "의심행동": [
        {{"suspect": "의심하는사람이름", "target": "의심받는사람이름", "reason": "이유"}}
    ]
}}
주의: "suspect"와 "target"은 반드시 생존자 이름이어야 합니다.
"""

    for msg in recent_messages:
        sender = msg.name if hasattr(msg, 'name') else "System"
        prompt += f"- {sender}: {msg.content}\n"
        
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        # JSON 파싱 시도
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
            
        result = json.loads(content)
        suspicion_updates = []
        
        for item in result.get("의심행동", []):
            suspect = item.get("suspect")
            target = item.get("target")
            
            if suspect in alive_names and target in alive_names and suspect != target:
                suspicion_counts[target] += 1
                suspicion_updates.append(f"{suspect} -> {target} 의심 (+1)")
                
        if suspicion_updates:
            summary = "🕵️ [AI 의심 현황]\n" + "\n".join(suspicion_updates)
            return {
                "suspicion_counts": suspicion_counts,
                "messages": [SystemMessage(content=summary)]
            }
            
    except Exception as e:
        print(f"AI Suspicion Error: {e}")
        
    return {}