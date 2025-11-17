"""
게임 플레이 매니저
- 유저와 AI 간 대화 관리
- 턴 시스템
- 투표 시스템
"""

import time


class GameplayManager:
    """게임 플레이를 관리하는 클래스"""

    def __init__(self, mafia_game):
        """
        초기화

        Args:
            mafia_game: MafiaGame 인스턴스
        """
        self.game = mafia_game
        self.round_number = 0
        self.conversation_log = []

    def start_free_discussion(self, num_rounds=2):
        """
        자유 토론 시작
        AI들끼리 대화하고, 중간중간 유저가 참여 가능

        Args:
            num_rounds: 토론 라운드 수
        """
        print("\n" + "=" * 70)
        print("💬 자유 토론 시작!")
        print("=" * 70)
        print("AI들이 서로 대화합니다. 원하면 언제든 개입할 수 있어요.")
        print("(AI 대화 중 아무 때나 입력하면 됩니다)")
        print("=" * 70 + "\n")

        topic = "여러분, 자기소개를 간단히 하고 어젯밤에 무엇을 했는지 말해주세요."

        for round_num in range(num_rounds):
            print(f"\n--- 🔄 Round {round_num + 1} ---\n")

            # AI들 순서대로 발언
            current_message = topic if round_num == 0 else "방금 전 대화에 대해 자유롭게 의견을 말해주세요."

            for char in self.game.characters:
                # AI 응답
                response = char.chat(current_message)

                # 출력
                mafia_mark = "🔴" if char == self.game.mafia else "💚"
                print(f"{mafia_mark} {char.name} ({char.job}):")
                print(f"   {response}\n")

                # 로그 저장
                self.conversation_log.append({
                    "speaker": char.name,
                    "message": response,
                    "is_mafia": char == self.game.mafia
                })

                # 다음 메시지 준비
                current_message = f"{char.name}이(가): '{response[:100]}...' 라고 말했습니다. 이에 대해 자유롭게 반응해주세요."

                time.sleep(0.3)

    def talk_to_character(self, character_name, user_message):
        """
        유저가 특정 캐릭터에게 말 걸기

        Args:
            character_name: 대화할 캐릭터 이름
            user_message: 유저의 메시지

        Returns:
            캐릭터의 응답
        """
        char = self.game.get_character_by_name(character_name)

        if not char:
            return f"❌ '{character_name}'라는 사람을 찾을 수 없습니다."

        # 캐릭터 응답
        response = char.chat(f"[유저가 당신에게 말합니다] {user_message}")

        # 로그 저장
        self.conversation_log.append({
            "speaker": "유저 → " + character_name,
            "message": user_message,
            "is_mafia": False
        })
        self.conversation_log.append({
            "speaker": character_name,
            "message": response,
            "is_mafia": char == self.game.mafia
        })

        return response

    def broadcast_to_all(self, user_message):
        """
        유저가 모두에게 말하기

        Args:
            user_message: 유저의 메시지
        """
        print(f"\n👤 유저: {user_message}\n")

        self.conversation_log.append({
            "speaker": "유저 (전체)",
            "message": user_message,
            "is_mafia": False
        })

        # 모든 AI가 응답
        for char in self.game.characters:
            response = char.chat(f"[유저가 모두에게 말합니다] {user_message}")

            mafia_mark = "🔴" if char == self.game.mafia else "💚"
            print(f"{mafia_mark} {char.name}:")
            print(f"   {response}\n")

            self.conversation_log.append({
                "speaker": char.name,
                "message": response,
                "is_mafia": char == self.game.mafia
            })

            time.sleep(0.3)

    def vote_mafia(self):
        """
        범인 투표
        유저가 범인이라고 생각하는 사람 지목
        """
        print("\n" + "=" * 70)
        print("🗳️  투표 시간!")
        print("=" * 70)
        print("\n누가 범인이라고 생각하시나요?\n")

        # 캐릭터 목록 출력
        for i, char in enumerate(self.game.characters, 1):
            print(f"{i}. {char.name} ({char.job}, {char.age}세)")

        print("\n" + "-" * 70)

        # 유저 입력
        while True:
            try:
                choice = input("\n번호를 선택하세요 (1-5): ").strip()
                choice_num = int(choice)

                if 1 <= choice_num <= len(self.game.characters):
                    selected = self.game.characters[choice_num - 1]
                    break
                else:
                    print("❌ 1-5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("❌ 숫자를 입력하세요.")

        # 결과 확인
        print("\n" + "=" * 70)
        print(f"당신의 선택: {selected.name}")
        print("=" * 70)

        if selected == self.game.mafia:
            print("\n🎉 정답입니다! 범인을 찾았습니다!")
            print(f"   {selected.name}이(가) 범인이었습니다.")
            return True
        else:
            print("\n😢 틀렸습니다!")
            print(f"   {selected.name}은(는) 범인이 아닙니다.")
            print(f"   진짜 범인은 {self.game.mafia.name}입니다.")
            return False

    def show_conversation_log(self):
        """대화 로그 출력"""
        print("\n" + "=" * 70)
        print("📜 대화 기록")
        print("=" * 70 + "\n")

        for entry in self.conversation_log:
            speaker = entry['speaker']
            message = entry['message'][:80] + "..." if len(entry['message']) > 80 else entry['message']
            print(f"{speaker}: {message}\n")
