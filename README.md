# 🕵️ 마피아 추리 게임

AI 에이전트를 활용한 텍스트 기반 추리 게임

## 🎮 게임 소개

5명의 개성있는 AI 캐릭터 중 1명이 범인(마피아)입니다!
AI들과 자유롭게 대화하며 단서를 찾고, 누가 범인인지 추리하세요.

### 특징
- 🎭 **5명의 다양한 캐릭터**: 대학생, 회사원, 예술가, 셰프, 은퇴 교사
- 🎲 **무작위 범인 선정**: 매번 다른 사람이 범인
- 💬 **자유로운 대화**: 특정 캐릭터와 1:1 대화 또는 전체 대화
- 🔍 **추리 게임**: 대화 속에서 단서를 찾아 범인 찾기

## 🚀 실행 방법

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에 Google API 키가 있는지 확인

### 3. 게임 시작!
```bash
python play_game.py
```

## 🎯 게임 진행 방법

1. **게임 시작**: 5명의 캐릭터 소개
2. **AI 대화 관찰**: AI들끼리 대화하는 것을 보며 분위기 파악
3. **질문하기**: 의심스러운 사람에게 질문
4. **단서 수집**: 대화 속 이상한 점 찾기
5. **범인 투표**: 범인이라고 생각하는 사람 지목

## 📁 프로젝트 구조

```
mafia_agent/
├── play_game.py              # 🎮 게임 실행 파일 (메인)
├── test_new_characters.py    # 캐릭터 시스템 테스트
├── phase2_demo.py            # AI 대화 데모
├── main.py                   # Phase 1 데모
│
├── game/
│   ├── mafia_game.py         # 게임 관리 (캐릭터 생성, 범인 선정)
│   └── gameplay_manager.py   # 게임플레이 (대화, 투표)
│
├── agents/
│   ├── character_agent.py    # AI 캐릭터 엔진
│   └── conversation_manager.py  # AI 대화 관리
│
├── characters/               # 캐릭터 정의
│   ├── student.py           # 김민지 (대학생)
│   ├── office_worker.py     # 박준호 (회사원)
│   ├── artist.py            # 최수아 (예술가)
│   ├── chef.py              # 이성민 (셰프)
│   └── teacher.py           # 한영희 (교사)
│
├── CHARACTERS.md            # 캐릭터 상세 설명
└── README.md               # 이 파일
```

## 👥 등장 캐릭터

| 이름 | 나이 | 직업 | 성격 |
|------|------|------|------|
| 김민지 | 22세 | 대학생 | 활발, 감정적, 호기심 많음 |
| 박준호 | 32세 | 회사원 | 침착, 논리적, 신중함 |
| 최수아 | 28세 | 일러스트레이터 | 감성적, 직관적, 관찰력 좋음 |
| 이성민 | 35세 | 셰프 | 유쾌, 솔직, 다혈질 |
| 한영희 | 63세 | 은퇴 교사 | 지혜로움, 온화함, 경험 많음 |

자세한 설명은 [CHARACTERS.md](CHARACTERS.md) 참고

## 📋 개발 진행 상황

### ✅ Phase 1: 단일 AI 캐릭터
- LangChain 기본 사용법
- 한 명의 AI와 대화

### ✅ Phase 2: 멀티 AI 에이전트
- 여러 AI가 서로 대화
- 대화 관리 시스템

### ✅ Phase 3: 완전한 게임
- 5명의 개성있는 캐릭터
- 무작위 범인 시스템
- 유저 참여 대화
- 투표 시스템

### 🔜 Phase 4: 웹 인터페이스 (예정)
- FastAPI 백엔드
- React/Vue 프론트엔드
- 실시간 채팅 UI

## 💡 핵심 기술

### LangChain 활용
- **ChatGoogleGenerativeAI**: Gemini AI 모델 사용
- **Message System**: 대화 기록 관리
  - SystemMessage: 캐릭터 성격 정의
  - HumanMessage: 유저/다른 캐릭터 입력
  - AIMessage: AI 응답

### 게임 시스템
- **MafiaGame**: 캐릭터 생성 및 범인 선정
- **GameplayManager**: 대화 흐름 관리
- **CharacterAgent**: 개별 AI 캐릭터 로직

## 🔧 기술 스택

- Python 3.13
- LangChain
- Google Gemini AI (gemini-2.0-flash)
- python-dotenv

## 📚 학습 포인트

1. **AI 에이전트 설계**: 성격을 가진 AI 만들기
2. **멀티 에이전트 시스템**: 여러 AI 간 대화
3. **프롬프트 엔지니어링**: 자연스러운 대화 유도
4. **게임 로직**: 턴제 게임 시스템

## 🎓 튜토리얼

각 Phase별로 학습하며 진행:
1. `python main.py` - 기본 AI 대화
2. `python phase2_demo.py` - AI 간 대화
3. `python test_new_characters.py` - 캐릭터 테스트
4. `python play_game.py` - 완전한 게임

## 🤝 기여

이 프로젝트는 LangChain과 AI 에이전트 학습을 위한 교육용 프로젝트입니다.
