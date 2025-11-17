"""
마피아 게임 메인 시스템
- 캐릭터 생성
- 범인 선정
- 게임 진행 관리
"""

import random
from agents.character_agent import CharacterAgent
from langchain_core.messages import SystemMessage


class MafiaGame:
    """마피아 게임을 관리하는 클래스"""

    def __init__(self, character_modules):
        """
        게임 초기화

        Args:
            character_modules: 캐릭터 모듈 리스트
                예: [student, office_worker, artist, chef, teacher]
        """
        self.character_modules = character_modules
        self.characters = []
        self.mafia = None  # 범인 캐릭터
        self.game_started = False

    def setup_game(self):
        """게임 세팅: 캐릭터 생성 및 범인 선정"""
        print("\n" + "=" * 60)
        print("🎮 마피아 게임 준비 중...")
        print("=" * 60)

        # 1. 캐릭터들 생성
        print("\n📝 캐릭터 생성 중...")
        for module in self.character_modules:
            char_info = module.get_character_info()
            character = CharacterAgent(char_info)
            self.characters.append(character)
            print(f"  ✓ {character.name} ({character.job}) - {character.personality}")

        # 2. 무작위로 범인 선정
        print("\n🎲 범인을 무작위로 선정하는 중...")
        self.mafia = random.choice(self.characters)

        # 3. 범인에게 역할 부여
        self._assign_mafia_role()

        print(f"\n🤫 범인이 선정되었습니다! (이름은 비밀)")
        print(f"   총 {len(self.characters)}명 중 1명이 범인입니다.\n")

        self.game_started = True

    def _assign_mafia_role(self):
        """범인에게 특별한 지시 추가"""
        mafia_instruction = """

=== 중요: 당신의 역할 ===
🔴 당신은 이번 게임의 **범인(마피아)**입니다.

범인으로서의 임무:
1. 다른 사람들에게 들키지 않기
2. 평소 성격대로 행동하되, 의심받지 않도록 조심
3. 필요하면 거짓 알리바이를 만들어내기
4. 자연스럽게 다른 사람을 의심하기

주의사항:
- 절대로 "저는 범인입니다" 같은 말을 하지 마세요
- 평소 성격을 유지하며 자연스럽게 행동하세요
- 너무 방어적이면 의심받을 수 있습니다
- 적절히 다른 사람들과 대화하며 섞이세요

목표: 끝까지 들키지 않고 살아남기!
========================
"""
        # 범인의 대화 기록에 역할 추가
        self.mafia.conversation_history.append(
            SystemMessage(content=mafia_instruction)
        )

    def reveal_mafia(self):
        """범인 공개 (디버그용 또는 게임 종료 시)"""
        if not self.game_started:
            print("⚠️  게임이 아직 시작되지 않았습니다.")
            return

        print("\n" + "=" * 60)
        print("🎭 범인 공개!")
        print("=" * 60)
        print(f"\n범인은... 🔴 {self.mafia.name} ({self.mafia.job}) 입니다!")
        print("=" * 60 + "\n")

    def get_character_list(self):
        """캐릭터 목록 반환"""
        return [
            {
                "name": char.name,
                "age": char.character_info.get("age", "?"),
                "job": char.job,
                "personality": char.personality,
                "is_mafia": char == self.mafia
            }
            for char in self.characters
        ]

    def get_character_by_name(self, name):
        """이름으로 캐릭터 찾기"""
        for char in self.characters:
            if char.name == name:
                return char
        return None
