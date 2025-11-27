"""
LangGraph 기반 마피아 게임
Interrupt + Checkpointer 방식 사용
"""

from graph.workflow import create_game_graph
from graph.state import GameState
from langgraph.types import Command
import os


def print_message(message):
    """메시지 출력"""
    if hasattr(message, 'name') and message.name:
        print(f"\n💬 {message.name}: {message.content}")
    else:
        print(f"\n📢 {message.content}")


def print_characters(state: GameState):
    """캐릭터 목록 출력 (의심 수치 포함)"""
    print("\n" + "=" * 70)
    print(f"👥 참가자 목록 (Round {state.get('round_number', 1)} - {state.get('day_night', 'day').upper()})")
    print("=" * 70)
    
    alive_status = state.get("alive_status", {})
    suspicion_counts = state.get("suspicion_counts", {})
    
    for i, char in enumerate(state["characters"], 1):
        name = char['name']
        is_alive = alive_status.get(name, True)
        status_mark = "🟢 생존" if is_alive else "🔴 사망"
        suspicion = suspicion_counts.get(name, 0)
        
        print(f"\n{i}. {name} [{status_mark}] (의심: {suspicion})")
        print(f"   나이: {char.get('age', '?')}세")
        print(f"   직업: {char.get('job', '?')}")
        print(f"   성격: {char.get('personality', '?')}")
    print("=" * 70)


def print_menu():
    """메뉴 출력"""
    print("\n" + "=" * 70)
    print("🎮 무엇을 하시겠습니까?")
    print("=" * 70)
    print("1. 다수와 논의하기")
    print("2. 특정 AI와 대화하기")
    print("3. 범인 투표")
    print("4. 생존자 목록 보기")
    print("5. 밤 행동 로그 확인")
    print("6. 라운드 요약 확인")
    print("7. 다음 라운드 진행 (밤으로 이동)")
    print("9. 특정 AI 의심하기")
    print("q. 게임 종료")
    print("=" * 70)


def main():
    print("\n" + "=" * 70)
    print("🎭 마피아 추리 게임 (LangGraph 버전)")
    print("=" * 70)
    print("\n🔥 LangGraph + LangSmith 기반 멀티 에이전트 시스템")
    print("\n게임 규칙:")
    print("  • 5명 중 1명이 범인(마피아)입니다")
    print("  • AI들과 대화하며 단서를 찾으세요")
    print("  • 누가 범인인지 추리하세요")
    print("  • 밤이 되면 마피아가 활동하여 희생자가 발생합니다")

    # LangSmith 추적 상태 확인
    if os.getenv("LANGCHAIN_TRACING_V2") == "true":
        if os.getenv("LANGCHAIN_API_KEY"):
            print("\n🔍 LangSmith 추적 활성화됨!")
            print("   → https://smith.langchain.com 에서 실시간 추적 가능")
        else:
            print("\n⚠️  LangSmith 추적 설정됨 (API 키 필요)")
            print("   → LANGSMITH_SETUP.md 참고")

    print("\n" + "=" * 70)
    input("\n엔터를 눌러 게임을 시작하세요...")

    # 그래프 생성 (checkpointer 포함)
    app = create_game_graph()

    # Thread ID - 이 ID로 checkpointer에서 state를 추적
    thread_id = "mafia_game_session_1"
    config = {"configurable": {"thread_id": thread_id}}

    # 초기 상태로 실행
    print("\n🎲 게임 세팅 중...")

    # 첫 실행 - setup부터 시작
    current_state = app.get_state(config)
    if current_state.next:
        print("🔄 기존 게임 세션을 불러옵니다...")
        state = current_state.values
    else:
        result = app.invoke({}, config)
        state = result

    print(f"\n✅ 게임이 시작되었습니다!")
    print(f"   총 {len(state['characters'])}명의 캐릭터가 참여합니다.")
    print(f"   이 중 1명이 범인입니다.")

    # 캐릭터 목록 보기
    print_characters(state)

    # 현재 메시지 개수 추적 (새 메시지만 출력하기 위해)
    last_message_count = len(state.get("messages", []))

    # 게임 루프
    game_over = False

    while not game_over:
        # 현재 페이즈 확인
        current_phase = state.get("phase")
        
        # 밤 페이즈 처리 (자동 진행 또는 알림)
        if current_phase == "night":
            print("\n🌙 밤이 되었습니다. 마피아가 활동합니다...")
            # 밤 페이즈 진행을 위해 그래프 재개
            result = app.invoke(
                Command(resume={"phase": "night"}),
                config
            )
            state = result
            
            # 밤 결과 출력
            messages = state.get("messages", [])
            new_messages = messages[last_message_count:]
            for msg in new_messages:
                print_message(msg)
            last_message_count = len(messages)
            
            print_characters(state)
            continue # 다시 메뉴 출력

        print_menu()

        choice = input("\n선택 > ").strip()

        if choice == "1":
            # AI들끼리 자유롭게 대화 (수동 진행 모드)
            print("\n" + "=" * 70)
            print("💬 AI 대화 라운드")
            print("=" * 70)
            print("\n[안내] AI들의 대화를 관전합니다.")
            print(" - Enter: 다음 대화 진행")
            print(" - 텍스트 입력: 대화에 끼어들기")
            print(" - 'q' 또는 'exit': 대화 종료 및 메뉴로 복귀")
            
            result = app.invoke(
                Command(resume={
                    "user_input": "[AI들끼리 자유롭게 대화를 시작합니다]",
                    "phase": "free_discussion",
                    "action": "next"
                }),
                config
            )
            state = result
            
            # 메시지 출력
            messages = state.get("messages", [])
            new_messages = messages[last_message_count:]
            for msg in new_messages:
                if hasattr(msg, 'name') and msg.name != "유저":
                    print_message(msg)
                elif not hasattr(msg, 'name') and "[AI들끼리" not in msg.content:
                    print_message(msg)
            last_message_count = len(messages)

            # 대화 루프
            while True:
                user_action = input("\n(Enter:다음, 입력:끼어들기, q:종료) > ").strip()
                
                if user_action.lower() in ['q', 'exit', 'quit']:
                    print("\n⏹️ 대화 관전을 종료합니다.")
                    break
                
                if not user_action:
                    # Enter 입력: 다음 턴 진행
                    result = app.invoke(
                        Command(resume={"action": "next"}),
                        config
                    )
                else:
                    # 텍스트 입력: 끼어들기
                    result = app.invoke(
                        Command(resume={"user_input": user_action}),
                        config
                    )

                state = result
                
                # 메시지 출력
                messages = state.get("messages", [])
                new_messages = messages[last_message_count:]
                for msg in new_messages:
                    if hasattr(msg, 'name') and msg.name != "유저":
                        print_message(msg)
                    elif not hasattr(msg, 'name') and "[AI들끼리" not in msg.content:
                        print_message(msg)
                last_message_count = len(messages)

            print("\n" + "=" * 70)

        elif choice == "2":
            # 특정 AI와 대화하기
            print("\n" + "-" * 70)
            print("💬 누구와 대화하시겠습니까?")
            print("-" * 70)
            
            alive_status = state.get("alive_status", {})

            for i, char in enumerate(state["characters"], 1):
                status = "🟢" if alive_status.get(char['name'], True) else "🔴(사망)"
                print(f"{i}. {char['name']} ({char.get('job', '?')}) {status}")

            print("-" * 70)

            try:
                target_num = int(input("\n번호 선택 (1-5): ").strip())
                if 1 <= target_num <= len(state["characters"]):
                    target_char = state["characters"][target_num - 1]
                    
                    # 사망자 확인
                    if not alive_status.get(target_char['name'], True):
                        print(f"\n❌ {target_char['name']}님은 사망하여 대화할 수 없습니다.")
                        continue

                    print(f"\n💬 {target_char['name']}와 1:1 대화를 시작합니다.")
                    print("   (종료하려면 'q' 또는 'exit'를 입력하세요)")
                    print("=" * 70)

                    # 1:1 모드 진입
                    result = app.invoke(
                        Command(resume={"phase": "one_on_one", "user_input": f"[{target_char['name']}에게] 안녕?"}),
                        config
                    )
                    state = result
                    last_message_count = len(state.get("messages", []))

                    while True:
                        # 질문 입력
                        question = input(f"\n나 ({target_char['name']}에게): ").strip()

                        if question.lower() in ['q', 'exit', 'quit']:
                            print("\n👋 대화를 종료합니다.")
                            # 종료 신호 전송 (토론 모드로 복귀)
                            result = app.invoke(
                                Command(resume={"user_input": "exit", "phase": "discussion"}),
                                config
                            )
                            state = result
                            break

                        if question:
                            # user_input 주입 후 그래프 재개
                            user_message = f"[{target_char['name']}에게] {question}"
                            
                            resume_data = {
                                "user_input": user_message,
                                "phase": "one_on_one" 
                            }
                            
                            result = app.invoke(
                                Command(resume=resume_data),
                                config
                            )
                            state = result

                            # 새로 추가된 메시지들만 출력
                            messages = state.get("messages", [])
                            new_messages = messages[last_message_count:]

                            for msg in new_messages:
                                print_message(msg)

                            last_message_count = len(messages)
                        else:
                            print("❌ 질문을 입력하세요.")
                else:
                    print("❌ 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("❌ 숫자를 입력하세요.")

        elif choice == "3":
            # 범인 투표
            print("\n" + "-" * 70)
            print("🗳️  누가 범인이라고 생각하시나요?")
            print("-" * 70)

            for i, char in enumerate(state["characters"], 1):
                print(f"{i}. {char['name']} ({char.get('job', '?')})")

            print("-" * 70)

            try:
                vote = int(input("\n번호 선택 (1-5): ").strip())
                if 1 <= vote <= len(state["characters"]):
                    selected = state["characters"][vote - 1]

                    print(f"\n🎯 {selected['name']}을(를) 범인으로 지목합니다...")

                    # user_target 주입 후 그래프 재개
                    result = app.invoke(
                        Command(resume={"user_target": selected["name"]}),
                        config
                    )
                    state = result

                    # 결과 메시지 출력
                    messages = state.get("messages", [])
                    new_messages = messages[last_message_count:]

                    for msg in new_messages:
                        print_message(msg)

                    game_over = True
                else:
                    print("❌ 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("❌ 숫자를 입력하세요.")

        elif choice == "4":
            # 생존자 목록
            print_characters(state)
            
        elif choice == "5":
            # 밤 행동 로그 확인
            print("\n" + "=" * 70)
            print("🌙 지난 밤 행동 로그")
            print("=" * 70)
            night_logs = state.get("night_logs", [])
            if night_logs:
                for log in night_logs:
                    print(f"- {log}")
            else:
                print("아직 기록된 로그가 없습니다.")
            print("=" * 70)
            
        elif choice == "6":
            # 라운드 요약 확인
            print("\n" + "=" * 70)
            print("📝 라운드 요약")
            print("=" * 70)
            summary = state.get("round_summary", "")
            if summary:
                print(summary)
            else:
                print("아직 요약된 내용이 없습니다.")
            print("=" * 70)
            
        elif choice == "7":
            # 다음 라운드 진행 (밤으로 이동)
            print("\n🌙 밤이 깊어갑니다... 다음 라운드로 넘어갑니다.")
            
            result = app.invoke(
                Command(resume={"phase": "night"}),
                config
            )
            state = result
            
            # 밤 페이즈 로직이 실행되고 다시 wait_user로 돌아옴
            messages = state.get("messages", [])
            new_messages = messages[last_message_count:]
            for msg in new_messages:
                print_message(msg)
            last_message_count = len(messages)

        elif choice == "9":
            # 특정 AI 의심하기
            print("\n" + "-" * 70)
            print("👁️ 누구를 의심하시겠습니까?")
            print("-" * 70)
            
            alive_status = state.get("alive_status", {})
            suspicion_counts = state.get("suspicion_counts", {})

            for i, char in enumerate(state["characters"], 1):
                status = "🟢" if alive_status.get(char['name'], True) else "🔴(사망)"
                suspicion = suspicion_counts.get(char['name'], 0)
                print(f"{i}. {char['name']} ({char.get('job', '?')}) {status} (의심: {suspicion})")

            print("-" * 70)

            try:
                target_num = int(input("\n번호 선택 (1-5): ").strip())
                if 1 <= target_num <= len(state["characters"]):
                    target_char = state["characters"][target_num - 1]
                    
                    # 사망자 확인
                    if not alive_status.get(target_char['name'], True):
                        print(f"\n❌ {target_char['name']}님은 사망하여 의심할 수 없습니다.")
                        continue

                    print(f"\n👁️ {target_char['name']}을(를) 의심합니다...")
                    
                    # 의심 액션 전송
                    result = app.invoke(
                        Command(resume={"user_input": "suspect", "user_target": target_char["name"]}),
                        config
                    )
                    state = result
                    
                    # 결과 메시지 출력
                    messages = state.get("messages", [])
                    new_messages = messages[last_message_count:]
                    for msg in new_messages:
                        print_message(msg)
                    last_message_count = len(messages)
                    
                else:
                    print("❌ 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("❌ 숫자를 입력하세요.")

        elif choice.lower() in ['q', 'exit']:
            # 게임 종료
            print("\n게임을 종료합니다.")
            print(f"💡 참고: 범인은 '{state['mafia_name']}'이었습니다.")
            game_over = True

        else:
            print("❌ 올바른 번호를 입력하세요.")

    print("\n" + "=" * 70)
    print("🎮 게임이 종료되었습니다!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
