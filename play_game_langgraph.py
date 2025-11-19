"""
LangGraph 기반 마피아 게임
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
    print("1. AI 대화 1라운드 진행")
    print("2. 질문하기 (모두에게)")
    print("3. 범인 투표")
    print("4. 참가자 목록 보기")
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

    # 그래프 생성
    app = create_game_graph()

    # 초기 상태로 실행 (setup)
    print("\n🎲 게임 세팅 중...")
    state = app.invoke({})

    print(f"\n✅ 게임이 시작되었습니다!")
    print(f"   총 {len(state['characters'])}명의 캐릭터가 참여합니다.")
    print(f"   이 중 1명이 범인입니다.")

    # 캐릭터 목록 보기
    print_characters(state)

    # 게임 루프
    game_over = False

    while not game_over:
        print_menu()

        choice = input("\n선택 (1-5): ").strip()

        if choice == "1":
            # AI 대화 1라운드
            print("\n" + "=" * 70)
            print("💬 AI 대화 라운드")
            print("=" * 70)

            # 각 캐릭터가 한 번씩 발언
            for char in state["characters"]:
                # 현재 speaker 설정하고 실행
                state["current_speaker"] = char["name"]
                state = app.invoke(state)

                # 최신 메시지 출력
                if state["messages"]:
                    latest_msg = state["messages"][-1]
                    print_message(latest_msg)

            print("\n" + "=" * 70)

        elif choice == "2":
            # 질문하기
            question = input("\n모두에게 할 질문: ").strip()

            if question:
                # user_input 설정
                state["user_input"] = question
                state = app.invoke(state)

                # 모든 캐릭터가 답변
                for char in state["characters"]:
                    state["current_speaker"] = char["name"]
                    state = app.invoke(state)

                    # 최신 메시지 출력
                    if state["messages"]:
                        latest_msg = state["messages"][-1]
                        print_message(latest_msg)

        elif choice == "3":
            # 투표
            print("\n" + "-" * 70)
            print("🗳️  누가 범인이라고 생각하시나요?")
            print("-" * 70)

            for i, char in enumerate(state["characters"], 1):
                print(f"{i}. {char['name']}")

            print("-" * 70)

            try:
                vote = int(input("\n번호 선택 (1-5): ").strip())
                if 1 <= vote <= len(state["characters"]):
                    selected = state["characters"][vote - 1]

                    # 투표 설정
                    state["user_target"] = selected["name"]
                    state = app.invoke(state)

                    # 결과 메시지 출력
                    if state["messages"]:
                        latest_msg = state["messages"][-1]
                        print_message(latest_msg)

                    game_over = True
                else:
                    print("❌ 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("❌ 숫자를 입력하세요.")

        elif choice == "4":
            # 참가자 목록
            print_characters(state)

        elif choice == "5":
            # 게임 종료
            print(f"\n게임을 종료합니다.")
            print(f"참고: 범인은 {state['mafia_name']}이었습니다.")
            game_over = True

        else:
            print("❌ 1-5 사이의 숫자를 입력하세요.")

    print("\n" + "=" * 70)
    print("🎮 게임이 종료되었습니다!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
