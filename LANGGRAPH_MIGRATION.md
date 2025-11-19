# 🔄 LangGraph 마이그레이션 가이드

## 왜 LangGraph로 전환했나요?

### 이전 방식의 한계
- 수동으로 대화 흐름 관리
- 에이전트 간 상태 공유 어려움
- 복잡한 조건부 로직 처리 곤란
- 디버깅과 모니터링 어려움

### LangGraph의 장점
✅ **State 관리**: 모든 에이전트가 하나의 State 공유
✅ **명확한 흐름**: Graph로 게임 로직 시각화
✅ **조건부 분기**: Conditional Edges로 복잡한 로직 처리
✅ **LangSmith 통합**: 실시간 모니터링 및 디버깅
✅ **확장성**: 새로운 노드 추가가 쉬움

---

## 핵심 구조

### 1. State (graph/state.py)
```python
class GameState(TypedDict):
    messages: List          # 대화 기록
    round_number: int       # 현재 라운드
    phase: str             # 게임 페이즈
    characters: List       # 캐릭터 정보
    mafia_name: str        # 범인
    current_speaker: str   # 현재 발언자
    votes: dict            # 투표 결과
    game_result: str       # 게임 결과
```

**State는 모든 노드가 공유하는 중앙 저장소**입니다.

---

### 2. Nodes (graph/nodes.py)

각 기능을 독립된 Node로 정의:

#### setup_game_node
- 게임 초기화
- 캐릭터 로드
- 범인 무작위 선정

#### character_speak_node
- 특정 캐릭터가 발언
- `current_speaker`를 확인
- 범인이면 특별 프롬프트 추가

#### user_input_node
- 유저 입력 처리
- 메시지 추가

#### vote_node
- 투표 처리
- 결과 판정

#### next_turn_node
- 다음 캐릭터로 턴 이동

---

### 3. Workflow (graph/workflow.py)

Node들을 연결하여 Graph 구성:

```
[START]
   ↓
setup_game_node
   ↓
next_turn_node
   ↓
[조건부 분기]
   ├─→ character_speak_node → next_turn
   ├─→ user_input_node → next_turn
   ├─→ vote_node → [END]
   └─→ [END]
```

---

## 이전 코드 vs LangGraph

### 이전: 수동 루프
```python
# 수동으로 순서 관리
for character in characters:
    response = character.chat(message)
    current_message = update(response)
```

### LangGraph: 자동 흐름
```python
# Graph가 자동으로 실행
state = app.invoke(state)
```

---

## 주요 파일

### 새로 추가된 파일
- `graph/state.py` - State 정의
- `graph/nodes.py` - 각 기능 Node
- `graph/workflow.py` - Graph 구성
- `play_game_langgraph.py` - LangGraph 기반 메인 게임

### 유지되는 파일
- `characters/*.py` - 캐릭터 정의 (그대로 사용)
- `requirements.txt` - 의존성 (langgraph 추가)

### 삭제/대체될 파일
- `game/gameplay_manager.py` → `graph/nodes.py`로 대체
- `game/mafia_game.py` → `setup_game_node`로 대체
- `agents/conversation_manager.py` → Graph 흐름으로 대체
- `play_game.py` → `play_game_langgraph.py`로 대체

---

## 실행 방법

### 1. 패키지 업데이트
```bash
pip install -r requirements.txt
```

### 2. LangGraph 버전 실행
```bash
python play_game_langgraph.py
```

### 3. 그래프 시각화 (선택)
```bash
python graph/workflow.py
```

---

## LangSmith 모니터링 (선택)

LangSmith를 사용하면 실시간으로 에이전트 동작을 모니터링할 수 있습니다.

### 설정
1. LangSmith 계정 생성: https://smith.langchain.com
2. API 키 받기
3. `.env`에 추가:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-api-key
LANGCHAIN_PROJECT=mafia-game
```

### 확인
- 대시보드에서 실시간으로 에이전트 흐름 확인
- 각 노드의 입력/출력 추적
- 성능 분석

---

## 확장 가능성

LangGraph 구조로 쉽게 추가 가능:

### 1. 새로운 노드 추가
```python
def new_feature_node(state):
    # 새 기능
    return {"new_field": value}

workflow.add_node("new_feature", new_feature_node)
```

### 2. 복잡한 분기 추가
```python
def complex_routing(state):
    if condition1:
        return "path_a"
    elif condition2:
        return "path_b"
    else:
        return "path_c"

workflow.add_conditional_edges(
    "some_node",
    complex_routing,
    {"path_a": "node_a", "path_b": "node_b", "path_c": "node_c"}
)
```

### 3. Human-in-the-loop
```python
# 유저 승인이 필요한 단계
workflow.add_node("wait_approval", wait_for_human_approval)
```

---

## 다음 단계

- [ ] 더 복잡한 게임 페이즈 추가
- [ ] AI 간 토론 기능 강화
- [ ] 메모리/검색 기능 추가
- [ ] 웹 인터페이스 통합
- [ ] LangSmith 대시보드 활용

---

## 학습 자료

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangSmith 가이드](https://docs.smith.langchain.com/)
- [마이그레이션 가이드](https://docs.langchain.com/oss/python/migrate/langgraph-v1)
