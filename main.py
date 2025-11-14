"""
마피아 게임 - Phase 1: 첫 번째 AI와 대화하기
"""

from agents.character_agent import CharacterAgent
from characters.detective import get_character_info


def main():
    print("=" * 50)
    print("🕵️  마피아 추리 게임 - Phase 1")
    print("=" * 50)
    print()

    # 형사 캐릭터 생성
    detective_info = get_character_info()
    detective = CharacterAgent(detective_info)

    # 캐릭터 정보 출력
    print(detective.get_info())
    print("💬 대화를 시작합니다!")
    print("   (종료하려면 'quit' 또는 '종료'를 입력하세요)")
    print("-" * 50)
    print()

    # 형사의 첫 인사
    first_message = detective.chat("안녕하세요, 제 소개를 간단히 해주세요.")
    print(f"🕵️  {detective.name}: {first_message}")
    print()

    # 대화 루프
    while True:
        # 사용자 입력
        user_input = input("👤 당신: ")
        print()

        # 종료 조건
        if user_input.lower() in ['quit', '종료', 'exit', '그만']:
            print("대화를 종료합니다. 수고하셨습니다!")
            break

        # 빈 입력 무시
        if not user_input.strip():
            continue

        # AI 응답 받기
        response = detective.chat(user_input)
        print(f"🕵️  {detective.name}: {response}")
        print()


if __name__ == "__main__":
    main()
