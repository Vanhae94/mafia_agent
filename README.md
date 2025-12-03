# Phantom Log (LangGraph Edition)

**LangGraph**와 **Google Gemini**를 활용한 멀티 에이전트 마피아 게임 프로젝트입니다.
5명의 AI 캐릭터와 사용자가 함께 추리하고 대화하며 범인(팬텀)을 찾아내는 텍스트 기반 추리 게임입니다.

## 주요 기능 (Key Features)

### 멀티 에이전트 시스템
5명의 AI 캐릭터가 각자의 성격(Personality)과 직업(Job)을 가지고 독립적으로 사고하고 대화합니다.

| 캐릭터 | 나이 | 직업 | 성격 |
|--------|------|------|------|
| 한기옥 | 24세 | 대학생 (심리학과) | 활발함, 사교적, 감정적 |
| 정소은 | 28세 | 일러스트레이터 | 감성적, 직관적, 예민함 |
| 이성민 | 35세 | 이탈리안 레스토랑 셰프 | 유쾌함, 솔직함, 다혈질 |
| 박준호 | 32세 | IT 회사 PM | 침착함, 논리적, 신중함 |
| 한영희 | 63세 | 은퇴 초등교사 | 지혜로움, 관찰력, 온화함 |

### LangGraph 기반 워크플로우
게임의 상태(State)와 흐름(Workflow)을 그래프 구조로 관리하여 복잡한 게임 로직을 유연하게 처리합니다.

### 의심 시스템 (Suspicion System)
- **유저 의심**: 사용자가 특정 AI를 의심하면 해당 캐릭터의 의심 수치가 증가합니다.
- **AI 상호 의심**: 라운드 종료 시 AI들이 대화 내용을 분석하여 서로를 의심하고 평가합니다.
- **반응형 대화**: 의심 수치에 따라 캐릭터들의 감정 상태가 변화합니다.
  - 1~2: 약간의 신경 쓰임
  - 3~4: 불쾌함 및 방어적
  - 5+: 극도의 불안 및 패닉

### 동적 화자 선정 (Dynamic Speaker Selection)
LLM이 대화 맥락을 분석하여 다음 발언자를 자동으로 선정, 자연스러운 토론 흐름을 만듭니다.

### 낮/밤 사이클
- **낮**: 자유 토론, 1:1 대화, 의심하기, 투표
- **밤**: 팬텀의 습격으로 희생자 발생, 현장 단서 생성

### 현장 단서 시스템
밤마다 LLM이 팬텀의 특징(직업, 성격)을 암시하는 현장 단서를 생성합니다. 직접적인 언급 없이 감각적인 묘사로 힌트를 제공합니다.

### 라운드 요약 시스템
라운드 종료 시 LLM이 대화 내용을 요약하여 다음 라운드에서 캐릭터들이 기억할 수 있도록 합니다. (토큰 관리 및 장기 기억)

### 웹 UI 지원
React 기반 프론트엔드와 FastAPI 백엔드를 통해 웹 브라우저에서 플레이할 수 있습니다.

---

## 기술 스택 (Tech Stack)

### Backend
| 기술 | 설명 |
|------|------|
| Python 3.10+ | 메인 언어 |
| [FastAPI](https://fastapi.tiangolo.com/) | REST API 프레임워크 |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | 에이전트 워크플로우 |
| [LangChain](https://www.langchain.com/) | LLM 통합 프레임워크 |
| Google Gemini 2.0 Flash | LLM 모델 (`langchain-google-genai`) |
| [LangSmith](https://smith.langchain.com/) | 모니터링/트레이싱 (선택) |

### Frontend
| 기술 | 설명 |
|------|------|
| [React](https://react.dev/) 18 | UI 프레임워크 |
| [Vite](https://vitejs.dev/) | 빌드 도구 |
| [Tailwind CSS](https://tailwindcss.com/) | 스타일링 |
| [Framer Motion](https://www.framer.com/motion/) | 애니메이션 |
| [React Router](https://reactrouter.com/) | 라우팅 |
| [Axios](https://axios-http.com/) | HTTP 클라이언트 |
| [Lucide React](https://lucide.dev/) | 아이콘 |

---

## 프로젝트 구조 (Directory Structure)

```
mafia_agent/
├── backend/                    # FastAPI 백엔드 서버
│   └── main.py                 # API 엔드포인트 정의
│
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── api/
│   │   │   └── gameApi.js      # API 클라이언트
│   │   ├── components/
│   │   │   ├── ActionPanel.jsx     # 사용자 액션 버튼 패널
│   │   │   ├── CharacterCard.jsx   # 캐릭터 카드 (의심/1:1/투표)
│   │   │   ├── CharacterStatus.jsx # 캐릭터 상태 표시
│   │   │   ├── ChatLog.jsx         # 채팅 로그 표시
│   │   │   └── RightPanel.jsx      # 게임 정보 및 컨트롤 패널
│   │   ├── pages/
│   │   │   ├── StartPage.jsx   # 게임 시작 페이지
│   │   │   └── GamePage.jsx    # 메인 게임 페이지
│   │   ├── utils/
│   │   │   └── session.js      # 세션 ID 생성
│   │   ├── styles/
│   │   │   └── index.css       # 글로벌 스타일
│   │   ├── App.jsx             # 라우터 설정
│   │   └── main.jsx            # 앱 진입점
│   ├── tailwind.config.js      # Tailwind 설정 (커스텀 테마)
│   ├── vite.config.js          # Vite 설정
│   └── package.json
│
├── characters/                 # AI 캐릭터 정의 모듈
│   ├── __init__.py
│   ├── artist.py               # 정소은 (일러스트레이터)
│   ├── chef.py                 # 이성민 (셰프)
│   ├── office_worker.py        # 박준호 (회사원)
│   ├── student.py              # 한기옥 (대학생)
│   └── teacher.py              # 한영희 (은퇴 교사)
│
├── graph/                      # LangGraph 핵심 로직
│   ├── __init__.py
│   ├── nodes.py                # 그래프 노드 (게임 로직 단위)
│   ├── state.py                # 게임 상태 스키마 (GameState)
│   └── workflow.py             # 그래프 구성 및 엣지 정의
│
├── play_game_langgraph.py      # CLI 게임 실행 엔트리포인트
├── requirements.txt            # Python 의존성 패키지 목록
├── .env                        # 환경 변수 (API Key 등)
└── image.png                   # 그래프 구조 시각화 이미지
```

---

## 아키텍처 및 로직 (Architecture)

이 프로젝트는 **StateGraph**를 사용하여 게임의 흐름을 제어합니다.

### Graph 구조 시각화

![alt text](image.png)

### GameState (상태 관리)

게임의 모든 데이터는 `GameState` TypedDict에 저장되어 노드 간에 전달됩니다.

| 필드 | 타입 | 설명 |
|------|------|------|
| `messages` | List | 대화 로그 (자동 누적) |
| `characters` | List[dict] | 캐릭터 정보 목록 |
| `phantom_name` | str | 범인 이름 (비밀) |
| `round_number` | int | 현재 라운드 |
| `phase` | str | 게임 단계 (`discussion`, `free_discussion`, `one_on_one`, `night`, `voting`, `end`) |
| `day_night` | str | 낮/밤 (`day`, `night`) |
| `alive_status` | Dict[str, bool] | 생존 여부 |
| `suspicion_counts` | Dict[str, int] | 캐릭터별 의심 수치 |
| `clues` | List[str] | 현장 단서 목록 |
| `night_logs` | List[str] | 밤 행동 로그 |
| `round_summaries` | Dict[int, str] | 라운드별 요약 |

### 주요 노드 (Nodes)

| 노드 | 설명 |
|------|------|
| `setup_game_node` | 게임 초기화, 캐릭터 로드, 팬텀 선정 |
| `select_next_speaker_node` | LLM 기반 다음 화자 선정 |
| `character_speak_node` | 캐릭터 발언 생성 (의심 수치 반영) |
| `wait_for_user_node` | 사용자 입력 대기 (interrupt) |
| `user_input_node` | 사용자 입력 처리 |
| `suspicion_node` | 의심 수치 증가 처리 |
| `ai_suspicion_node` | AI간 상호 의심 평가 |
| `night_phase_node` | 밤 페이즈 (희생자 선정, 단서 생성) |
| `summarize_round_node` | 라운드 요약 및 메모리 관리 |
| `vote_node` | 투표 및 게임 종료 처리 |

### Workflow (게임 흐름)

1. **Setup**: 게임 초기화, 5명 중 1명을 팬텀으로 선정
2. **Discussion Loop**:
   - `select_next_speaker`: 대화 맥락 분석하여 다음 화자 선정 (직전 발언자 제외)
   - `character_speak`: 캐릭터 발언 생성 (의심 수치에 따라 감정 반응 변화)
   - `wait_user`: 사용자 개입 대기
3. **Suspicion**: 사용자가 특정 AI를 의심하면 수치 증가
4. **AI Suspicion**: 낮 토론 종료 후 AI들이 서로 평가
5. **Summarize Round**: 라운드 요약 생성 (토큰 관리)
6. **Night Phase**:
   - 팬텀이 생존자 중 1명 습격
   - LLM이 팬텀 특징을 암시하는 현장 단서 생성
7. **Vote**: 사용자가 범인 지목하여 승패 결정

---

## API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/game/start` | 새 게임 세션 시작 |
| GET | `/api/game/state/{thread_id}` | 현재 게임 상태 조회 |
| POST | `/api/game/action` | 사용자 액션 수행 |

### Action Types

| action_type | 설명 | 추가 파라미터 |
|-------------|------|---------------|
| `chat` | 채팅 메시지 전송 | `content` |
| `vote` | 팬텀 투표 | `target` |
| `suspect` | 캐릭터 의심하기 | `target` |
| `next` | 다음 턴으로 진행 | - |
| `night_start` | 밤 페이즈 시작 | - |
| `discuss` | AI 자유 토론 시작 | - |
| `end_discuss` | 논의 종료 | - |
| `start_one_on_one` | 1:1 대화 시작 | `target` |

---

## 설치 및 실행 (Installation & Usage)

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd mafia_agent

# Backend 의존성 설치
pip install -r requirements.txt

# Frontend 의존성 설치
cd frontend
npm install
```

### 2. API 키 설정

`.env` 파일을 생성하고 Google API 키를 입력합니다.

```env
GOOGLE_API_KEY=your_google_api_key_here

# (선택) LangSmith 추적 활성화
# LANGCHAIN_TRACING_V2=true
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

---

## 플레이 방법

| 액션 | 설명 |
|------|------|
| **자유 토론** | AI들의 대화를 지켜보거나, 직접 대화에 끼어들어 질문할 수 있습니다 |
| **의심하기** | 수상한 행동을 하는 AI를 지목하여 의심 수치를 증가시킵니다 |
| **1:1 대화** | 특정 캐릭터와 따로 대화하며 심문할 수 있습니다 |
| **투표** | 범인을 확신하면 투표하여 게임을 끝낼 수 있습니다 |
| **단서 확인** | 밤마다 발견되는 현장 단서를 확인하여 추리에 활용합니다 |
| **라운드 요약** | 이전 라운드들의 요약을 확인할 수 있습니다 |

---

## UI 테마

프론트엔드는 사이버펑크/느와르 스타일의 다크 테마를 사용합니다.

```javascript
// tailwind.config.js
colors: {
  noir: {
    900: '#09090b', // Main Background
    800: '#18181b', // Panel Background
    700: '#27272a', // Border
  },
  neon: {
    cyan: '#06b6d4',  // Safe/System
    pink: '#f43f5e',  // Danger/Suspect
  }
}
```
