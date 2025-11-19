# 🔍 LangSmith 설정 가이드

LangSmith를 사용하면 LangGraph 실행을 실시간으로 추적하고 디버깅할 수 있습니다.

## 1단계: LangSmith 계정 생성

1. https://smith.langchain.com 접속
2. 계정 생성 (GitHub 또는 이메일)
3. 무료로 시작 가능

## 2단계: API 키 발급

1. 로그인 후 우측 상단 프로필 클릭
2. `Settings` 선택
3. `API Keys` 탭
4. `Create API Key` 클릭
5. 키 복사

## 3단계: .env 파일에 추가

`.env` 파일 열고 다음 줄 추가:

```env
# LangSmith API 키 (여기에 복사한 키 붙여넣기)
LANGCHAIN_API_KEY=lsv2_pt_xxxxxxxxxxxxxxxxxxxxxxx

# 추적 활성화 (이미 설정됨)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="mafia-game"
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
```

## 4단계: 게임 실행

```bash
python play_game_langgraph.py
```

## 5단계: LangSmith 대시보드 확인

1. https://smith.langchain.com 접속
2. 좌측 메뉴에서 `Projects` 클릭
3. `mafia-game` 프로젝트 선택
4. 실행 내역 확인!

---

## 🎯 LangSmith에서 볼 수 있는 것

### 1. 실행 추적 (Traces)
- 전체 게임 플로우
- 각 노드 실행 순서
- 실행 시간

### 2. 노드별 상세 정보
- **Input**: 노드에 들어온 State
- **Output**: 노드가 반환한 State
- **LLM 호출**: AI에게 보낸 프롬프트와 응답

### 3. 에러 추적
- 어느 노드에서 에러가 났는지
- 에러 메시지
- 에러 발생 시 State 상태

### 4. 성능 분석
- 각 노드 실행 시간
- LLM 응답 속도
- 병목 지점 파악

---

## 📊 대시보드 사용법

### 실행 목록 보기
```
Projects > mafia-game > Runs
```
- 각 게임 실행이 하나의 Run으로 표시됨

### 특정 실행 상세 보기
Run 클릭 시:
- **Graph View**: 노드 흐름 시각화
- **Timeline**: 시간순 실행 순서
- **Metadata**: State 변경 사항

### LLM 호출 추적
각 노드 클릭 시:
- **Inputs**: 프롬프트
- **Outputs**: AI 응답
- **Token 사용량**

---

## 🐛 디버깅 예시

### 에러 발생 시

1. **LangSmith 대시보드** 열기
2. 빨간색으로 표시된 Run 클릭
3. 에러 난 노드 확인
4. Input/Output State 확인
5. 문제 원인 파악!

### 예시: character_speak_node에서 에러

대시보드에서 확인 가능:
```json
Input State: {
  "current_speaker": "김민지",
  "characters": [...],
  ...
}

Error: KeyError: 'prompt'
→ 캐릭터 정보에 'prompt' 필드가 없음!
```

---

## ⚙️ 설정 옵션

### 프로젝트 이름 변경
`.env` 파일:
```env
LANGCHAIN_PROJECT="my-custom-name"
```

### 추적 비활성화 (필요시)
```env
LANGCHAIN_TRACING_V2=false
```

### 특정 실행만 추적
코드에서:
```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # 활성화
```

---

## 💡 팁

1. **매 실행마다 새 Run 생성**: 게임 시작할 때마다 대시보드에 기록
2. **Run에 태그 추가 가능**: 나중에 찾기 쉽게
3. **팀원과 공유**: URL 복사해서 다른 사람도 볼 수 있음
4. **피드백 기능**: 특정 응답에 👍/👎 표시 가능

---

## 🚨 문제 해결

### "API key not found" 에러
→ `.env` 파일에 `LANGCHAIN_API_KEY` 추가했는지 확인

### 대시보드에 아무것도 안 보임
→ `.env` 파일에 `LANGCHAIN_TRACING_V2=true` 설정 확인

### 너무 많은 데이터
→ `LANGCHAIN_PROJECT` 이름을 변경해서 새 프로젝트 시작

---

## 📚 더 알아보기

- [LangSmith 공식 문서](https://docs.smith.langchain.com/)
- [LangGraph + LangSmith 가이드](https://langchain-ai.github.io/langgraph/how-tos/visualization/)
