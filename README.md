# 🕵️ Phantom Log (LangGraph Edition)

**LangGraph**와 **Google Gemini**를 활용한 멀티 에이전트 마피아 게임 프로젝트입니다.
5명의 AI 캐릭터와 사용자가 함께 추리하고 대화하며 범인(팬텀)을 찾아내는 텍스트 기반 게임입니다.

## 🌟 주요 기능 (Key Features)

*   **멀티 에이전트 시스템**: 5명의 AI 캐릭터가 각자의 성격(Personality)과 직업(Job)을 가지고 독립적으로 사고하고 대화합니다.
*   **LangGraph 기반 워크플로우**: 게임의 상태(State)와 흐름(Workflow)을 그래프 구조로 관리하여 복잡한 게임 로직(낮/밤, 투표, 토론 등)을 유연하게 처리합니다.
*   **의심 시스템 (Suspicion System)**:
    *   **유저 의심**: 사용자가 특정 AI를 의심하면 해당 캐릭터의 의심 수치가 증가합니다.
    *   **AI 상호 의심**: 라운드 종료 시 AI들이 대화 내용을 분석하여 서로를 의심하고 평가합니다.
    *   **반응형 대화**: 의심 수치가 높아지면 캐릭터들이 방어적이거나 당황하는 등 감정적인 반응을 보입니다.
*   **동적 화자 선정 (Dynamic Speaker Selection)**: 대화 맥락을 분석하여 다음 발언자를 LLM이 자동으로 선정, 자연스러운 토론 흐름을 만듭니다.
*   **낮/밤 사이클**: 낮에는 자유 토론과 추리를, 밤에는 팬텀의 습격(희생자 발생) 이벤트가 진행됩니다.
*   **현장 단서 시스템**: 게임 진행 중 현장에서 발견되는 단서를 통해 범인을 추리합니다.
*   **웹 UI 지원**: React 기반 프론트엔드와 FastAPI 백엔드를 통해 웹 브라우저에서 플레이할 수 있습니다.

## 🛠️ 기술 스택 (Tech Stack)

### Backend
*   **Language**: Python 3.10+
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Agent Framework**: [LangGraph](https://langchain-ai.github.io/langgraph/), [LangChain](https://www.langchain.com/)
*   **LLM**: Google Gemini (via `langchain-google-genai`)
*   **Monitoring**: [LangSmith](https://smith.langchain.com/) (Optional, for tracing)

### Frontend
*   **Framework**: [React](https://react.dev/) 18
*   **Build Tool**: [Vite](https://vitejs.dev/)
*   **HTTP Client**: [Axios](https://axios-http.com/)
*   **Icons**: [Lucide React](https://lucide.dev/)

## 📂 프로젝트 구조 (Directory Structure)

```
mafia_agent/
├── backend/                # FastAPI 백엔드 서버
│   └── main.py             # API 엔드포인트 정의
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   │   ├── ActionPanel.jsx     # 사용자 액션 패널
│   │   │   ├── CharacterStatus.jsx # 캐릭터 상태 표시
│   │   │   └── ChatLog.jsx         # 채팅 로그 표시
│   │   ├── App.jsx         # 메인 앱 컴포넌트
│   │   └── main.jsx        # 앱 진입점
│   └── package.json
├── characters/             # AI 캐릭터 정의 모듈
│   ├── artist.py           # 예술가 캐릭터
│   ├── chef.py             # 요리사 캐릭터
│   ├── office_worker.py    # 회사원 캐릭터
│   ├── student.py          # 대학생 캐릭터
│   └── teacher.py          # 선생님 캐릭터
├── graph/                  # LangGraph 핵심 로직
│   ├── nodes.py            # 그래프 노드 (게임 로직 단위)
│   ├── state.py            # 게임 상태 스키마 (GameState)
│   └── workflow.py         # 그래프 구성 및 엣지 정의
├── play_game_langgraph.py  # CLI 게임 실행 엔트리포인트
├── requirements.txt        # Python 의존성 패키지 목록
└── .env                    # 환경 변수 (API Key 등)
```

## 🧩 아키텍처 및 로직 (Architecture)

이 프로젝트는 **StateGraph**를 사용하여 게임의 흐름을 제어합니다.

### 0. Graph 구조 시각화

![alt text](image.png)

### 1. GameState (상태 관리)
게임의 모든 데이터는 `GameState` 딕셔너리에 저장되어 노드 간에 전달됩니다.
- `characters`: 캐릭터 정보 목록
- `messages`: 대화 로그
- `phase`: 현재 게임 단계 (`intro`, `discussion`, `voting`, `night`, `one_on_one`, `end`)
- `suspicion_counts`: 캐릭터별 의심 수치
- `alive_status`: 생존 여부
- `clues`: 현장 단서 목록
- `night_logs`: 밤 행동 로그

### 2. Workflow (게임 흐름)
주요 노드와 흐름은 다음과 같습니다:

1.  **Setup**: 게임 초기화, 팬텀(범인) 선정.
2.  **Discussion Loop**:
    *   `select_next_speaker`: 대화 맥락을 분석해 다음 화자 선정.
    *   `character_speak`: 선정된 캐릭터가 LLM을 통해 발언 생성 (의심 수치 반영).
    *   `wait_user`: 사용자의 개입(끼어들기, 의심하기, 투표 등)을 대기.
3.  **Suspicion**: 사용자가 특정 AI를 의심하면 수치 증가.
4.  **AI Suspicion**: 낮 토론 종료 후, AI들이 서로를 평가하여 의심 수치 업데이트.
5.  **Night Phase**: 팬텀이 생존자 중 한 명을 습격(제거).
6.  **Vote**: 사용자가 범인을 지목하여 승패 결정.

### 3. API 엔드포인트
- `POST /api/game/start`: 새 게임 세션 시작
- `GET /api/game/state/{thread_id}`: 현재 게임 상태 조회
- `POST /api/game/action`: 사용자 액션 수행 (채팅, 투표, 의심 등)

## 🚀 설치 및 실행 (Installation & Usage)

### 1. 환경 설정
필요한 패키지를 설치합니다.

```bash
# Backend 의존성 설치
pip install -r requirements.txt

# Frontend 의존성 설치
cd frontend
npm install
```

### 2. API 키 설정
`.env` 파일을 생성하고 Google API 키를 입력합니다.
```env
GOOGLE_API_KEY=your_api_key_here
# LANGCHAIN_TRACING_V2=true  # (선택) LangSmith 추적 활성화
# LANGCHAIN_API_KEY=your_langchain_api_key
```

### 3. 게임 실행

#### 방법 1: CLI 모드 (터미널)
```bash
python play_game_langgraph.py
```

#### 방법 2: 웹 UI 모드
```bash
# 터미널 1: Backend 서버 실행
cd backend
uvicorn main:app --reload --port 8000

# 터미널 2: Frontend 개발 서버 실행
cd frontend
npm run dev
```
브라우저에서 `http://localhost:5173`으로 접속합니다.

### 4. 플레이 방법
- **자유 토론**: AI들의 대화를 지켜보거나, 직접 대화에 끼어들어 질문할 수 있습니다.
- **의심하기**: 수상한 행동을 하는 AI를 지목하여 압박(의심 수치 증가)할 수 있습니다.
- **1:1 대화**: 특정 캐릭터와 따로 대화하며 심문할 수 있습니다.
- **투표**: 범인을 확신하면 투표하여 게임을 끝낼 수 있습니다.
