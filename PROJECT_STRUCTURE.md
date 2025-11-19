# 📁 프로젝트 구조

## 전체 디렉토리 구조

```
mafia_agent/
│
├── 🎮 게임 실행 파일
│   ├── play_game_langgraph.py    ⭐ LangGraph 버전 (메인)
│   ├── play_game.py              (레거시)
│   ├── test_new_characters.py    (테스트용)
│   ├── phase2_demo.py            (데모)
│   └── main.py                   (Phase 1 데모)
│
├── 📊 LangGraph 시스템 (핵심)
│   └── graph/
│       ├── state.py              # GameState 정의
│       ├── nodes.py              # 각 기능 Node
│       └── workflow.py           # Graph 구성
│
├── 🎭 캐릭터 정의
│   └── characters/
│       ├── student.py            # 김민지 (대학생)
│       ├── office_worker.py      # 박준호 (회사원)
│       ├── artist.py             # 최수아 (예술가)
│       ├── chef.py               # 이성민 (셰프)
│       └── teacher.py            # 한영희 (교사)
│
├── 🤖 레거시 시스템 (참고용)
│   ├── agents/
│   │   ├── character_agent.py    # 개별 AI 엔진
│   │   └── conversation_manager.py
│   └── game/
│       ├── mafia_game.py
│       └── gameplay_manager.py
│
├── 📚 문서
│   ├── README.md                 # 프로젝트 소개
│   ├── CHARACTERS.md             # 캐릭터 설명
│   ├── LANGGRAPH_MIGRATION.md    # 마이그레이션 가이드
│   ├── PROJECT_STRUCTURE.md      # 이 파일
│   └── CLAUDE.md                 # 개발 노트
│
└── ⚙️ 설정
    ├── requirements.txt          # 패키지 의존성
    └── .env                      # API 키 (비공개)
```

---

## 🎯 어떤 파일을 실행해야 하나요?

### ⭐ 메인 게임
```bash
python play_game_langgraph.py
```
**LangGraph 기반 멀티 에이전트 마피아 게임**

### 📖 학습용 데모
```bash
# Phase 1: 단일 AI와 대화
python main.py

# Phase 2: AI 간 대화
python phase2_demo.py

# 캐릭터 시스템 테스트
python test_new_characters.py
```

### 🔧 개발/디버깅
```bash
# 그래프 구조 시각화
python graph/workflow.py
```

---

## 📊 LangGraph 시스템 상세

### graph/state.py
**GameState 정의** - 모든 노드가 공유하는 중앙 상태

```python
GameState = {
    "messages": [],         # 대화 기록
    "characters": [],       # 캐릭터 정보
    "mafia_name": "...",   # 범인
    "current_speaker": "", # 현재 발언자
    "phase": "discussion", # 게임 페이즈
    ...
}
```

### graph/nodes.py
**노드 함수들** - 각 기능을 독립된 노드로 구현

- `setup_game_node`: 게임 초기화
- `character_speak_node`: 캐릭터 발언
- `user_input_node`: 유저 입력 처리
- `vote_node`: 투표 처리
- `next_turn_node`: 턴 진행

### graph/workflow.py
**그래프 구성** - 노드를 연결하여 게임 흐름 정의

```python
setup → next_turn → [조건부 분기]
                      ├─ character_speak
                      ├─ user_input
                      └─ vote → END
```

---

## 🎭 캐릭터 시스템

### 캐릭터 정의 구조
각 `characters/*.py` 파일:

```python
# 캐릭터 프롬프트
CHARACTER_PROMPT = """
당신은 ... 입니다.

성격: ...
말투: ...
"""

# 정보 반환 함수
def get_character_info():
    return {
        "name": "...",
        "age": 22,
        "job": "...",
        "personality": "...",
        "prompt": CHARACTER_PROMPT
    }
```

### 캐릭터 목록
1. **김민지** (22세, 대학생) - 활발, 감정적
2. **박준호** (32세, 회사원) - 침착, 논리적
3. **최수아** (28세, 예술가) - 감성적, 직관적
4. **이성민** (35세, 셰프) - 유쾌, 솔직
5. **한영희** (63세, 교사) - 지혜로움, 관찰력

---

## 🤖 레거시 vs LangGraph

### 레거시 시스템 (참고용)
- `agents/character_agent.py`: 개별 AI 관리
- `agents/conversation_manager.py`: 대화 흐름 관리
- `game/mafia_game.py`: 게임 상태 관리
- `game/gameplay_manager.py`: 게임 플레이 로직

**문제점:**
- 수동 상태 관리
- 복잡한 흐름 제어
- 디버깅 어려움

### LangGraph 시스템 (현재)
- `graph/state.py`: 중앙 상태 관리
- `graph/nodes.py`: 기능별 노드
- `graph/workflow.py`: 선언적 흐름 정의

**장점:**
- 자동 상태 관리
- 명확한 흐름
- LangSmith 통합

---

## 🔧 확장 가이드

### 새 캐릭터 추가
1. `characters/new_character.py` 생성
2. `get_character_info()` 함수 정의
3. `graph/nodes.py`의 `setup_game_node`에 import 추가

### 새 기능 노드 추가
1. `graph/nodes.py`에 함수 정의
```python
def new_feature_node(state):
    # 로직
    return {"field": value}
```

2. `graph/workflow.py`에 노드 추가
```python
workflow.add_node("new_feature", new_feature_node)
workflow.add_edge("some_node", "new_feature")
```

### 새 게임 페이즈 추가
1. `graph/state.py`의 `phase` 값 확장
2. `graph/nodes.py`에 페이즈별 로직 추가
3. `graph/workflow.py`에 조건부 엣지 추가

---

## 📦 의존성

### 핵심 패키지
- `langgraph` - 멀티 에이전트 오케스트레이션
- `langgraph-checkpoint` - State 체크포인트
- `langsmith` - 모니터링 및 디버깅
- `langchain-google-genai` - Gemini AI
- `langchain-core` - 기본 컴포넌트

### 설치
```bash
pip install -r requirements.txt
```

---

## 🎓 학습 경로

### 1단계: 기본 이해
- `main.py` 실행 - 단일 AI 대화
- `characters/student.py` 읽기 - 캐릭터 정의 방법

### 2단계: 멀티 에이전트
- `phase2_demo.py` 실행 - AI 간 대화
- `agents/conversation_manager.py` 읽기

### 3단계: LangGraph
- `graph/state.py` 읽기 - State 구조
- `graph/nodes.py` 읽기 - Node 구현
- `graph/workflow.py` 읽기 - Graph 구성
- `play_game_langgraph.py` 실행

### 4단계: 확장
- 새 캐릭터 추가해보기
- 새 노드 추가해보기
- LangSmith 연동해보기

---

## 🐛 디버깅

### 그래프 구조 확인
```bash
python graph/workflow.py
```

### LangSmith로 추적
`.env`에 설정 추가:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-key
```

### 로그 확인
각 노드의 입출력은 LangSmith 대시보드에서 확인 가능

---

## 📝 TODO

- [ ] 더 복잡한 대화 시나리오
- [ ] AI 간 자동 의심/질문 기능
- [ ] 게임 기록 저장/불러오기
- [ ] 웹 UI 개발
- [ ] 음성 인터페이스
