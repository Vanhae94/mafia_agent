"""
캐릭터 AI 에이전트
LangChain을 사용하여 성격을 가진 AI를 만듭니다
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class CharacterAgent:
    """성격을 가진 AI 캐릭터"""

    def __init__(self, character_info):
        """
        캐릭터 에이전트 초기화

        Args:
            character_info: 캐릭터 정보 딕셔너리
                - name: 이름
                - age: 나이 (선택)
                - job: 직업 (선택)
                - personality: 성격
                - prompt: 시스템 프롬프트
        """
        # 전체 정보 저장
        self.character_info = character_info

        # 자주 쓰는 정보는 속성으로
        self.name = character_info["name"]
        self.age = character_info.get("age", None)
        self.job = character_info.get("job", character_info.get("role", ""))
        self.personality = character_info["personality"]
        self.system_prompt = character_info["prompt"]

        # Google Gemini AI 모델 초기화
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        # 대화 기록 저장
        self.conversation_history = [
            SystemMessage(content=self.system_prompt)
        ]

    def chat(self, user_message):
        """
        사용자와 대화

        Args:
            user_message: 사용자의 메시지

        Returns:
            AI의 응답
        """
        # 사용자 메시지를 대화 기록에 추가
        self.conversation_history.append(HumanMessage(content=user_message))

        # AI에게 전체 대화 내역을 보내서 응답 받기
        response = self.llm.invoke(self.conversation_history)

        # AI 응답을 대화 기록에 추가
        self.conversation_history.append(AIMessage(content=response.content))

        return response.content

    def get_info(self):
        """캐릭터 정보 출력"""
        return f"""
=== 캐릭터 정보 ===
이름: {self.name}
역할: {self.role}
성격: {self.personality}
==================
"""
