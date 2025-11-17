"""
마피아 게임 - 실제 플레이 프로그램
유저가 AI들과 대화하며 범인을 찾는 게임
"""

from game.mafia_game import MafiaGame
from game.gameplay_manager import GameplayManager
from characters import student, office_worker, artist, chef, teacher


def print_menu():
    """메뉴 출력"""
    print("\n" + "=" * 70)
    print("🎮 무엇을 하시겠습니까?")
    print("=" * 70)
    print("1. AI들끼리 대화 보기 (1라운드)")
    print("2. 특정 사람에게 말 걸기")
    print("3. 모두에게 말하기")
    print("4. 범인 투표하기")
    print("5. 참가자 목록 보기")
    print("6. 게임 종료")
    print("=" * 70)


def show_participants(game):
    """참가자 목록 출력"""
    print("\n" + "=" * 70)
    print("👥 참가자 목록")
    print("=" * 70)
    for i, char in enumerate(game.characters, 1):
        print(f"\n{i}. {char.name}")
        print(f"   나이: {char.age}세")
        print(f"   직업: {char.job}")
        print(f"   성격: {char.personality}")
    print("=" * 70)


def talk_to_someone(gameplay):
    """특정 사람에게 말 걸기"""
    print("\n" + "-" * 70)
    print("누구에게 말을 걸까요?")
    print("-" * 70)

    for i, char in enumerate(gameplay.game.characters, 1):
        print(f"{i}. {char.name} ({char.job})")

    print("-" * 70)

    while True:
        try:
            choice = input("\n번호를 선택하세요 (1-5): ").strip()
            choice_num = int(choice)

            if 1 <= choice_num <= len(gameplay.game.characters):
                selected = gameplay.game.characters[choice_num - 1]
                break
            else:
                print("❌ 1-5 사이의 숫자를 입력하세요.")
        except ValueError:
            print("❌ 숫자를 입력하세요.")

    # 메시지 입력
    message = input(f"\n{selected.name}에게 할 말: ").strip()

    if not message:
        print("❌ 메시지를 입력하세요.")
        return

    # 응답 받기
    print()
    mafia_mark = "🔴" if selected == gameplay.game.mafia else "💚"
    response = gameplay.talk_to_character(selected.name, message)
    print(f"{mafia_mark} {selected.name}:")
    print(f"   {response}")


def talk_to_all(gameplay):
    """모두에게 말하기"""
    message = input("\n모두에게 할 말: ").strip()

    if not message:
        print("❌ 메시지를 입력하세요.")
        return

    gameplay.broadcast_to_all(message)


def main():
    print("\n" + "=" * 70)
    print("🎭 마피아 추리 게임에 오신 것을 환영합니다!")
    print("=" * 70)
    print("\n게임 규칙:")
    print("  • 5명 중 1명이 범인(마피아)입니다")
    print("  • AI들과 대화하며 단서를 찾으세요")
    print("  • 누가 범인인지 추리하세요")
    print("  • 범인을 맞히면 승리!")
    print("\n" + "=" * 70)
    input("\n엔터를 눌러 게임을 시작하세요...")

    # 게임 세팅
    character_modules = [student, office_worker, artist, chef, teacher]
    game = MafiaGame(character_modules)
    game.setup_game()

    # 게임플레이 매니저 생성
    gameplay = GameplayManager(game)

    # 참가자 목록 보여주기
    show_participants(game)

    print("\n💡 힌트: 먼저 'AI들끼리 대화 보기'를 선택해서 분위기를 파악해보세요!")

    # 게임 루프
    game_over = False

    while not game_over:
        print_menu()

        choice = input("\n선택 (1-6): ").strip()

        if choice == "1":
            # AI 대화
            gameplay.start_free_discussion(num_rounds=1)

        elif choice == "2":
            # 특정 사람에게 말 걸기
            talk_to_someone(gameplay)

        elif choice == "3":
            # 모두에게 말하기
            talk_to_all(gameplay)

        elif choice == "4":
            # 투표
            result = gameplay.vote_mafia()
            game_over = True

        elif choice == "5":
            # 참가자 목록
            show_participants(game)

        elif choice == "6":
            # 게임 종료
            print("\n게임을 종료합니다.")
            print(f"참고: 범인은 {game.mafia.name}이었습니다.")
            game_over = True

        else:
            print("❌ 1-6 사이의 숫자를 입력하세요.")

    print("\n" + "=" * 70)
    print("🎮 게임이 종료되었습니다. 감사합니다!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
