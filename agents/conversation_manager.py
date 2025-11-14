"""
대화 관리자
여러 AI 캐릭터들이 서로 대화하도록 관리합니다
"""

import time


class ConversationManager:
    """여러 캐릭터 간의 대화를 관리하는 클래스"""

    def __init__(self, characters):
        """
        대화 관리자 초기화

        Args:
            characters: CharacterAgent 객체들의 리스트
        """
        self.characters = characters
        self.conversation_log = []  # 전체 대화 기록

    def start_conversation(self, topic, num_turns=3):
        """
        AI들끼리 대화를 시작합니다

        Args:
            topic: 대화 주제
            num_turns: 각 캐릭터가 말할 횟수

        Returns:
            대화 기록 리스트
        """
        print("=" * 60)
        print(f"💬 대화 주제: {topic}")
        print("=" * 60)
        print()

        # 첫 번째 캐릭터가 주제에 대해 먼저 말함
        current_message = topic

        for turn in range(num_turns):
            print(f"\n--- Round {turn + 1} ---\n")

            for character in self.characters:
                # 이전 대화 내용을 바탕으로 응답
                response = character.chat(current_message)

                # 화면에 출력
                print(f"🗣️  {character.name} ({character.role}):")
                print(f"   {response}")
                print()

                # 대화 기록에 저장
                self.conversation_log.append({
                    "character": character.name,
                    "role": character.role,
                    "message": response
                })

                # 다음 캐릭터는 이 응답에 반응
                current_message = f"{character.name}이(가) 이렇게 말했습니다: '{response}'. 이에 대해 당신의 생각을 말해주세요."

                # 좀 더 자연스럽게 보이도록 약간의 딜레이
                time.sleep(0.5)

        return self.conversation_log

    def get_conversation_summary(self):
        """대화 요약 반환"""
        summary = "\n=== 대화 요약 ===\n"
        for entry in self.conversation_log:
            summary += f"{entry['character']} ({entry['role']}): {entry['message'][:50]}...\n"
        return summary
