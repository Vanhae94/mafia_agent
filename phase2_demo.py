"""
Phase 2 데모: 여러 AI 캐릭터가 서로 대화하기
"""

from agents.character_agent import CharacterAgent
from agents.conversation_manager import ConversationManager
from characters.detective import get_character_info as get_detective
from characters.suspect import get_character_info as get_suspect
from characters.witness import get_character_info as get_witness


def main():
    print("=" * 60)
    print("🎭  마피아 추리 게임 - Phase 2")
    print("     여러 AI 캐릭터가 대화합니다")
    print("=" * 60)
    print()

    # 3명의 캐릭터 생성
    print("캐릭터들을 생성하는 중...")
    detective = CharacterAgent(get_detective())
    suspect = CharacterAgent(get_suspect())
    witness = CharacterAgent(get_witness())

    characters = [detective, suspect, witness]

    # 캐릭터 정보 출력
    print("\n=== 등장 캐릭터 ===")
    for char in characters:
        print(f"  • {char.name} ({char.role}) - {char.personality}")
    print()

    # 대화 관리자 생성
    manager = ConversationManager(characters)

    # 시나리오: 어젯밤 사건에 대한 조사
    print("\n🔍 시나리오: 어젯밤 10시경 발생한 사건에 대해 조사 중입니다.\n")
    input("엔터를 누르면 대화가 시작됩니다...")
    print()

    # AI들끼리 대화 시작
    manager.start_conversation(
        topic="어젯밤 10시경 당신은 어디에 있었습니까? 무엇을 하고 있었나요?",
        num_turns=2  # 각자 2번씩 발언
    )

    # 대화 요약
    print("\n" + "=" * 60)
    print(manager.get_conversation_summary())
    print("=" * 60)

    print("\n✅ Phase 2 데모가 완료되었습니다!")
    print("   3명의 AI가 각자의 성격대로 대화하는 것을 보셨나요?")


if __name__ == "__main__":
    main()
