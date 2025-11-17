"""
새로운 캐릭터 시스템 테스트
- 5명의 일반인 캐릭터
- 무작위 범인 선정
- 범인 공개
"""

from game.mafia_game import MafiaGame
from characters import student, office_worker, artist, chef, teacher


def main():
    print("\n" + "=" * 70)
    print("🎭 마피아 게임 - 새로운 캐릭터 시스템 테스트")
    print("=" * 70)

    # 캐릭터 모듈 리스트
    character_modules = [
        student,
        office_worker,
        artist,
        chef,
        teacher
    ]

    # 게임 생성 및 세팅
    game = MafiaGame(character_modules)
    game.setup_game()

    # 캐릭터 목록 보기
    print("\n" + "=" * 70)
    print("👥 참가자 목록")
    print("=" * 70)
    for i, char in enumerate(game.characters, 1):
        print(f"\n{i}. {char.name}")
        print(f"   나이: {char.age}세")
        print(f"   직업: {char.job}")
        print(f"   성격: {char.personality}")

    print("\n" + "=" * 70)

    # 범인 공개 (테스트용)
    input("\n엔터를 누르면 범인이 공개됩니다... (디버그 모드)")
    game.reveal_mafia()

    # 간단한 대화 테스트
    print("\n" + "=" * 70)
    print("💬 간단한 대화 테스트")
    print("=" * 70)

    question = "어젯밤 10시에 어디 있었나요? 무엇을 하고 있었나요?"
    print(f"\n질문: {question}\n")

    for char in game.characters[:3]:  # 처음 3명만 테스트
        print(f"\n{'🔴' if char == game.mafia else '💚'} {char.name}:")
        response = char.chat(question)
        print(f"   {response}")
        print()

    print("=" * 70)
    print("\n✅ 테스트 완료!")
    print("   - 5명의 다양한 캐릭터 생성 ✓")
    print("   - 무작위 범인 선정 ✓")
    print("   - 각자 성격대로 응답 ✓")
    print("\n다음 단계: 실제 게임 플레이 시스템 구현")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
