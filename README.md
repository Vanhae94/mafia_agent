# 🕵️ 마피아 추리 게임

AI 에이전트를 활용한 텍스트 기반 추리 게임 프로젝트

## 📋 현재 진행 상황: Phase 1

### ✅ Phase 1: 단일 AI 캐릭터와 대화
- **목표**: LangChain 기본 사용법 익히기
- **구현 완료**: 의심 많은 형사 캐릭터와 대화 시스템

## 🚀 실행 방법

### 1. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에 API 키가 설정되어 있는지 확인하세요.

### 3. 프로그램 실행
```bash
python main.py
```

### 4. 대화하기
- 형사와 자유롭게 대화하세요
- 종료하려면 `quit` 또는 `종료`를 입력하세요

## 📁 프로젝트 구조

```
mafia_agent/
├── main.py                 # 메인 실행 파일
├── agents/
│   └── character_agent.py  # AI 캐릭터 에이전트
├── characters/
│   └── detective.py        # 형사 캐릭터 정의
├── requirements.txt        # 필요한 패키지
├── .env                    # API 키 (비공개)
└── README.md              # 이 파일
```

## 🎯 다음 단계 (Phase 2)

- [ ] 여러 개의 캐릭터 추가 (용의자, 목격자 등)
- [ ] AI끼리 대화하는 기능
- [ ] 캐릭터 간 상호작용

## 💡 코드 설명

### 1. `characters/detective.py`
캐릭터의 **성격과 특성**을 정의합니다.
- 형사의 말투, 성격, 행동 방식을 프롬프트로 작성
- 나중에 다른 캐릭터도 같은 방식으로 추가 가능

### 2. `agents/character_agent.py`
실제로 AI와 **대화를 처리**하는 핵심 코드입니다.
- LangChain의 ChatGoogleGenerativeAI 사용
- 대화 기록(conversation_history)을 저장해서 문맥 유지
- SystemMessage: AI에게 역할 부여
- HumanMessage: 사용자 메시지
- AIMessage: AI 응답

### 3. `main.py`
사용자가 실행하는 **메인 프로그램**입니다.
- 캐릭터를 생성하고
- 콘솔에서 대화를 주고받음

## 📚 학습 포인트

### LangChain 핵심 개념
1. **LLM (Language Model)**: AI 모델 (여기서는 Gemini 사용)
2. **Messages**: 대화를 구조화
   - SystemMessage: AI의 역할/성격 정의
   - HumanMessage: 사용자 입력
   - AIMessage: AI 응답
3. **Conversation History**: 대화 기록으로 문맥 유지

### 왜 이렇게 나눴나요?
- **characters/**: 캐릭터 설정만 관리 → 쉽게 추가/수정
- **agents/**: AI 로직 → 재사용 가능
- **main.py**: 실행 로직 → 게임 흐름 관리

## 🔧 기술 스택

- Python 3.x
- LangChain (AI 프레임워크)
- Google Gemini AI (생성형 AI)
- python-dotenv (환경 변수 관리)
