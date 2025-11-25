# 🕵️ 마피아 추리 게임

**LangGraph 기반 멀티 에이전트 AI 추리 게임**

## 🎮 게임 소개

5명의 개성있는 AI 캐릭터 중 1명이 범인(마피아)입니다!
AI들과 자유롭게 대화하며 단서를 찾고, 누가 범인인지 추리하세요.

### ✨ 특징
- 🎭 **5명의 다양한 캐릭터**: 각자 고유한 성격, 직업, 말투
- 🎲 **무작위 범인 선정**: 매 게임마다 다른 범인
- 💬 **자유로운 대화**: AI와 자연스러운 대화
- 🔍 **추리 게임**: 대화 속 단서로 범인 찾기
- 🔥 **LangGraph + LangSmith**: 최신 멀티 에이전트 시스템

---

## 🚀 빠른 시작

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에 API 키 설정:
```env
GOOGLE_API_KEY=your-google-api-key
```

### 3. 게임 시작!
```bash
python play_game_langgraph.py
```

---

## 🎯 게임 진행 방법

1. **게임 시작**: 5명의 캐릭터 소개
2. **AI 대화 관찰**: AI들끼리 대화하며 분위기 파악
3. **질문하기**: 모두에게 질문 던지기
4. **단서 수집**: 이상한 점 찾기
5. **범인 투표**: 범인이라 생각하는 사람 지목

---

## 👥 등장 캐릭터

| 이름 | 나이 | 직업 | 성격 |
|------|------|------|------|
| 한기옥 | 24세 | 대학생 | 활발, 감정적, 호기심 많음 |
| 박준호 | 32세 | 회사원 | 침착, 논리적, 신중함 |
| 정소은 | 28세 | 일러스트레이터 | 감성적, 직관적, 관찰력 |
| 이성민 | 35세 | 셰프 | 유쾌, 솔직, 다혈질 |
| 한영희 | 63세 | 은퇴 교사 | 지혜로움, 온화함, 경험 많음 |

자세한 설명: [CHARACTERS.md](CHARACTERS.md)

---

## 🏗️ 프로젝트 구조

```
mafia_agent/
├── 🎮 play_game_langgraph.py   ⭐ LangGraph 메인 게임
│
├── 📊 graph/                   LangGraph 시스템
│   ├── state.py               # GameState 정의
│   ├── nodes.py               # 기능 노드들
│   └── workflow.py            # Graph 구성
│
├── 🎭 characters/             캐릭터 정의
│   ├── student.py
│   ├── office_worker.py
│   ├── artist.py
│   ├── chef.py
│   └── teacher.py
│
└── 📚 문서
    ├── README.md              # 이 파일
    ├── CHARACTERS.md          # 캐릭터 상세
    ├── LANGGRAPH_MIGRATION.md # 마이그레이션 가이드
    └── PROJECT_STRUCTURE.md   # 전체 구조
```

---

## 💡 핵심 기술: LangGraph

### 왜 LangGraph인가?

**기존 방식의 한계:**
- 수동 상태 관리
- 복잡한 흐름 제어
- 디버깅 어려움

**LangGraph 장점:**
✅ **State 관리**: 모든 에이전트가 하나의 State 공유
✅ **명확한 흐름**: Graph로 게임 로직 시각화
✅ **조건부 분기**: 복잡한 로직 쉽게 처리
✅ **LangSmith 통합**: 실시간 모니터링
✅ **확장성**: 새로운 기능 추가 용이

### LangGraph 구조

```
[START]
   ↓
setup_game (캐릭터 생성, 범인 선정)
   ↓
next_turn (턴 진행)
   ↓
[조건부 분기]
   ├─→ character_speak (AI 발언)
   ├─→ wait_for_user (사용자 입력 대기 - Interrupt)
   │         ↓
   │    (Command로 재개)
   │         ↓
   ├─→ user_input (유저 입력)
   ├─→ vote (투표)
   └─→ [END]
```

**핵심 메커니즘: Interrupt & Resume**
- **Interrupt**: `wait_for_user` 노드에서 그래프 실행을 일시 중단하고 사용자 입력을 기다립니다.
- **Resume**: 사용자가 입력을 제공하면 `Command(resume=...)`를 통해 중단된 지점에서 그래프를 재개합니다.
- 이를 통해 웹 서버나 CLI 환경에서 비동기적인 사용자 상호작용을 완벽하게 지원합니다.

자세한 내용: [LANGGRAPH_MIGRATION.md](LANGGRAPH_MIGRATION.md)

---

## 🔧 기술 스택

- **Python 3.13**
- **LangChain** - AI 프레임워크
- **LangGraph** - 멀티 에이전트 오케스트레이션
- **LangSmith** - 모니터링 (선택)
- **Google Gemini AI** - 생성형 AI

---

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

### ✅ Phase 4: LangGraph 전환
- State 기반 멀티 에이전트
- Graph로 게임 흐름 관리
- LangSmith 통합 준비

### 🔜 Phase 5: 웹 인터페이스 (예정)
- FastAPI 백엔드
- React 프론트엔드
- 실시간 채팅 UI

---

## 🎓 학습 튜토리얼

### 단계별 학습
```bash
# 1단계: 기본 AI 대화
python main.py

# 2단계: AI 간 대화
python phase2_demo.py

# 3단계: 캐릭터 시스템
python test_new_characters.py

# 4단계: LangGraph 게임
python play_game_langgraph.py

# 5단계: Interrupt/Resume 테스트
python test_fix.py

# 6단계: 그래프 시각화
python graph/workflow.py
```

---

## 🔍 LangSmith 모니터링 (선택)

실시간으로 AI 에이전트 동작을 추적하고 디버깅할 수 있습니다.

### 설정
1. https://smith.langchain.com 에서 계정 생성
2. API 키 발급
3. `.env`에 추가:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=mafia-game
```

### 대시보드에서 확인 가능
- 각 노드의 입출력
- 실행 시간
- 에러 추적
- 대화 흐름

---

## 📚 학습 포인트

1. **AI 에이전트 설계**: 성격을 가진 AI 만들기
2. **멀티 에이전트 시스템**: LangGraph로 여러 AI 조율
3. **State 관리**: 중앙 집중식 상태 관리
4. **프롬프트 엔지니어링**: 자연스러운 대화 유도
5. **Graph 기반 흐름 제어**: 복잡한 로직을 선언적으로 표현

---

## 🛠️ 개발 가이드

### 새 캐릭터 추가
1. `characters/new_character.py` 생성
2. `get_character_info()` 정의
3. `graph/nodes.py`에서 import

### 새 기능 추가
1. `graph/nodes.py`에 노드 함수 작성
2. `graph/workflow.py`에서 그래프에 연결

### 디버깅
- LangSmith 대시보드 활용
- `graph/workflow.py` 실행해서 그래프 구조 확인

---

## 📖 관련 문서

- [캐릭터 상세 설명](CHARACTERS.md)
- [LangGraph 마이그레이션 가이드](LANGGRAPH_MIGRATION.md)
- [프로젝트 구조 상세](PROJECT_STRUCTURE.md)
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangSmith 가이드](https://docs.smith.langchain.com/)

---

## 🤝 기여

이 프로젝트는 LangChain과 LangGraph를 활용한 멀티 에이전트 시스템 학습을 위한 교육용 프로젝트입니다.

---

## 📝 라이선스

이 프로젝트는 학습 목적으로 만들어졌습니다.
