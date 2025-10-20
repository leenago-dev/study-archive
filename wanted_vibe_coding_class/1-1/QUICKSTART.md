# 빠른 시작 가이드

## 1. API 키 발급

### OpenAI API 키
1. https://platform.openai.com/api-keys 접속
2. 로그인 후 "Create new secret key" 클릭
3. 생성된 키를 안전하게 보관

### Tavily Search API 키
1. https://tavily.com 접속
2. 계정 생성 후 대시보드로 이동
3. API 키를 확인하고 복사

## 2. 프로젝트 설정

```bash
# 프로젝트 디렉토리로 이동
cd /Users/leena/Desktop/nomad_coder_project/wanted_vibe_coding_class/1-1

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가:

```bash
# .env 파일 생성
cat > .env << EOF
OPENAI_API_KEY=sk-proj-your-key-here
TAVILY_API_KEY=tvly-your-key-here
HOST=0.0.0.0
PORT=8000
OPENAI_MODEL=gpt-4o-mini
EOF
```

또는 `env_example.txt`를 복사하여 수정:

```bash
cp env_example.txt .env
# 그런 다음 .env 파일을 열어서 실제 API 키로 수정
```

## 4. 서버 실행

```bash
# 직접 실행
python main.py

# 또는 uvicorn으로 실행
uvicorn main:app --reload
```

서버가 실행되면:
- 🌐 웹 클라이언트: http://localhost:8000
- 📚 API 문서: http://localhost:8000/docs
- ❤️ 헬스 체크: http://localhost:8000/health

## 5. 테스트

### 웹 브라우저로 테스트
1. http://localhost:8000 접속
2. 채팅창에 메시지 입력
3. 실시간 응답 확인

### cURL로 REST API 테스트

```bash
# 채팅 메시지 전송
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "최신 AI 뉴스를 검색해줘",
    "session_id": "test_user"
  }'

# 대화 히스토리 조회
curl "http://localhost:8000/history/test_user"

# 헬스 체크
curl "http://localhost:8000/health"
```

### Python으로 WebSocket 테스트

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/test_user"
    async with websockets.connect(uri) as websocket:
        # 메시지 전송
        await websocket.send("최신 AI 뉴스를 검색해줘")

        # 응답 수신
        async for message in websocket:
            data = json.loads(message)
            print(f"Type: {data['type']}")
            if data['type'] == 'stream':
                print(data['content'], end='', flush=True)
            elif data['type'] == 'end':
                print("\n\n응답 완료!")
                break

asyncio.run(test_websocket())
```

## 6. 문제 해결

### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

### 포트 충돌
`.env` 파일에서 `PORT`를 다른 값으로 변경:
```
PORT=8001
```

### API 키 오류
- `.env` 파일의 API 키가 올바른지 확인
- API 키 앞뒤에 따옴표나 공백이 없는지 확인
- OpenAI 계정에 충분한 크레딧이 있는지 확인

## 7. 주요 기능

### ✅ 웹 검색
- "최신 뉴스를 검색해줘"
- "2024년 파이썬 트렌드는?"
- "FastAPI vs Flask 비교해줘"

### ✅ 대화 기억
- 같은 session_id로 대화하면 이전 내용을 기억합니다

### ✅ 실시간 스트리밍
- WebSocket을 통해 응답을 실시간으로 받습니다

## 8. 다음 단계

- API 엔드포인트 커스터마이징
- 더 많은 도구 추가 (예: 계산기, 날씨 등)
- 프론트엔드 개선
- 데이터베이스 연동 (대화 히스토리 영구 저장)
- 배포 (Docker, AWS, etc.)
