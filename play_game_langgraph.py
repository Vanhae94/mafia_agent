"""
LangGraph 기반 마피아 게임
Interrupt + Checkpointer 방식 사용
"""

from graph.workflow import create_game_graph
from graph.state import GameState


def print_message(message):
    """메시지 출력"""
    if hasattr(message, 'name') and message.name:
        print(f"\n💬 {message.name}: {message.content}")
    else:
        print(f"\n📢 {message.content}")


def print_characters(state: GameState):
    """캐릭터 목록 출력"""
    print("\n" + "=" * 70)
    print("👥 참가자 목록")
    print("=" * 70)
    for i, char in enumerate(state["characters"], 1):
        print(f"\n{i}. {char['name']}")
        print(f"   나이: {char.get('age', '?')}세")
        print(f"   직업: {char.get('job', '?')}")
        print(f"   성격: {char.get('personality', '?')}")
    print("=" * 70)


def print_menu():
    """메뉴 출력"""
    print("\n" + "=" * 70)
    print("🎮 무엇을 하시겠습니까?")
    print("=" * 70)
    print("1. AI 대화 보기 (AI 3명이 자유롭게 대화)")
    print("2. 특정 AI와 대화하기")
    print("3. 범인 투표")
    print("4. 생존자 목록 보기")
    print("5. 게임 종료")
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

    # LangSmith 추적 상태 확인
    import os
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

    # Command 객체 임포트 (재개용)
    from langgraph.types import Command

    # Thread ID - 이 ID로 checkpointer에서 state를 추적
    thread_id = "mafia_game_session_1"
    config = {"configurable": {"thread_id": thread_id}}

    # 초기 상태로 실행
    # setup → wait_user → interrupt 발생 → 그래프 중단
    print("\n🎲 게임 세팅 중...")

    # 첫 실행 - setup부터 시작
    # 이미 실행된 적이 있는지 확인하기 위해 state를 먼저 가져와 봄
    current_state = app.get_state(config)
    if current_state.next:
        print("🔄 기존 게임 세션을 불러옵니다...")
        state = current_state.values
    else:
        result = app.invoke({}, config)
        state = result

    # wait_user에서 interrupt 발생했으므로 여기서 멈춤
    # checkpointer가 현재 state 저장

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
        print_menu()

        choice = input("\n선택 (1-5): ").strip()

        if choice == "1":
            # AI들끼리 자유롭게 대화
            print("\n" + "=" * 70)
            print("💬 AI 대화 라운드")
            print("=" * 70)
            print("\n AI들이 자유롭게 대화합니다...")

            # user_input 주입 후 그래프 재개
            # wait_user에서 멈춘 지점부터 계속 실행:
            # wait_user → user_input → character_speak (3번) → wait_user → interrupt
            result = app.invoke(
                Command(resume={"user_input": "[AI들끼리 자유롭게 대화를 시작합니다]"}),
                config
            )
            state = result

            # 새로 추가된 메시지들만 출력
            messages = state.get("messages", [])
            new_messages = messages[last_message_count:]

            for msg in new_messages:
                # 시스템 메시지 (트리거)는 출력 안 함
                if hasattr(msg, 'name') and msg.name != "유저":
                    print_message(msg)
                elif not hasattr(msg, 'name'):
                    # 시스템 메시지
                    if "[AI들끼리" not in msg.content:
                        print_message(msg)

            last_message_count = len(messages)

            print("\n" + "=" * 70)

        elif choice == "2":
            # 특정 AI와 대화하기
            print("\n" + "-" * 70)
            print("💬 누구와 대화하시겠습니까?")
            print("-" * 70)

            for i, char in enumerate(state["characters"], 1):
                print(f"{i}. {char['name']} ({char.get('job', '?')})")

            print("-" * 70)

            try:
                target_num = int(input("\n번호 선택 (1-5): ").strip())
                if 1 <= target_num <= len(state["characters"]):
                    target_char = state["characters"][target_num - 1]

                    print(f"\n💬 {target_char['name']}와 1:1 대화를 시작합니다.")
                    print("   (종료하려면 'q' 또는 'exit'를 입력하세요)")
                    print("=" * 70)

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
                            # 1:1 모드 유지를 위해 phase 정보도 함께 전달 (선택적)
                            user_message = f"[{target_char['name']}에게] {question}"
                            
                            # 첫 진입 시 또는 계속 대화 시 one_on_one 페이즈로 설정
                            # nodes.py에서 user_input이 있으면 phase를 one_on_one으로 유지하도록 처리됨
                            # 하지만 명시적으로 phase를 보낼 수도 있음 (nodes.py 수정에 따라 다름)
                            # 여기서는 nodes.py가 state['phase']를 확인하므로, 
                            # 첫 진입 시에는 이전에 discussion이었을 수 있으므로 resume 데이터에 phase를 포함하는 것이 안전
                            
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
                    # wait_user → vote → END
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
            # 생존자 목록 (현재는 모두 생존)
            print_characters(state)

        elif choice == "5":
            # 게임 종료
            print("\n게임을 종료합니다.")
            print(f"💡 참고: 범인은 '{state['mafia_name']}'이었습니다.")
            game_over = True

        else:
            print("❌ 1-5 사이의 숫자를 입력하세요.")

    print("\n" + "=" * 70)
    print("🎮 게임이 종료되었습니다!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
