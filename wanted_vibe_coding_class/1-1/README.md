# 원티드 바이브코딩 마스터 실습 파일입니다.
ref: https://event.wanted.co.kr/pre_ax_skillup_02

---

# 웹 검색 챗봇 에이전트 (LangGraph + FastAPI)

Context7 MCP의 최신 기술을 활용한 웹 검색 기능을 갖춘 AI 챗봇 에이전트입니다.

## 주요 기능

- 🤖 **LangGraph 기반 에이전트**: 상태 관리와 도구 호출을 지원하는 고급 에이전트
- 🔍 **웹 검색**: Tavily Search API를 통한 실시간 웹 검색
- 💬 **대화 메모리**: 대화 히스토리를 유지하는 상태 관리
- 🚀 **FastAPI 서버**: REST API 및 WebSocket 지원
- ⚡ **스트리밍 응답**: 실시간 응답 스트리밍

## 기술 스택

- **Backend Framework**: FastAPI 0.115.13
- **Agent Framework**: LangGraph 0.2.74
- **LLM**: OpenAI GPT (langchain-openai)
- **Search Tool**: Tavily Search API
- **Server**: Uvicorn (ASGI)

## 설치 방법

1. 저장소 클론 및 디렉토리 이동:
```bash
cd /Users/leena/Desktop/nomad_coder_project/wanted_vibe_coding_class/1-1
```

2. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

3. 의존성 설치:
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정:
`.env` 파일을 생성하고 다음 내용을 추가:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## 사용 방법

### 서버 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API 테스트

서버 실행 후 브라우저에서 접속:
- **API 문서**: http://localhost:8000/docs
- **WebSocket 클라이언트**: http://localhost:8000

### REST API 예제

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "최신 AI 뉴스를 검색해줘",
    "session_id": "user123"
  }'
```

### WebSocket 연결

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/user123');
ws.onmessage = (event) => {
  console.log('Received:', event.data);
};
ws.send('최신 AI 뉴스를 검색해줘');
```

## 프로젝트 구조

```
.
├── main.py                 # FastAPI 애플리케이션 진입점
├── agent.py                # LangGraph 에이전트 구현
├── config.py               # 설정 및 환경 변수
├── requirements.txt        # Python 의존성
├── .env                    # 환경 변수 (생성 필요)
└── README.md              # 프로젝트 문서
```

## API 엔드포인트

### POST /chat
단일 메시지 처리 및 응답

**Request:**
```json
{
  "message": "사용자 메시지",
  "session_id": "세션 ID (선택사항)"
}
```

**Response:**
```json
{
  "response": "에이전트 응답",
  "session_id": "세션 ID"
}
```

### WebSocket /ws/{session_id}
실시간 양방향 통신

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트를 환영합니다!
