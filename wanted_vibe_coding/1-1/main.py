"""
FastAPI 서버 메인 애플리케이션
LangGraph 웹 검색 에이전트를 REST API 및 WebSocket으로 제공
"""

from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from config import settings, validate_settings
from agent import get_agent


# 요청/응답 모델
class ChatRequest(BaseModel):
    """채팅 요청 모델"""

    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    """채팅 응답 모델"""

    response: str
    session_id: str


class HistoryResponse(BaseModel):
    """대화 히스토리 응답 모델"""

    session_id: str
    history: list


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="웹 검색 챗봇 에이전트",
    description="LangGraph와 Tavily Search를 활용한 AI 챗봇 API",
    version="1.0.0",
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행"""
    print("\n🚀 서버 시작 중...")
    try:
        validate_settings()
        # 에이전트 초기화
        get_agent()
        print("✅ 모든 구성 요소 초기화 완료\n")
    except Exception as e:
        print(f"❌ 초기화 오류: {e}")
        raise


@app.get("/", response_class=HTMLResponse)
async def get_home():
    """홈페이지 - WebSocket 테스트 클라이언트"""
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>웹 검색 챗봇 에이전트</title>
            <meta charset="UTF-8">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .container {
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    width: 100%;
                    max-width: 800px;
                    height: 90vh;
                    max-height: 700px;
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px 30px;
                    border-radius: 20px 20px 0 0;
                }
                .header h1 {
                    font-size: 24px;
                    margin-bottom: 5px;
                }
                .header p {
                    font-size: 14px;
                    opacity: 0.9;
                }
                .connection-status {
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    margin-top: 10px;
                    background: rgba(255,255,255,0.2);
                }
                .connection-status.connected {
                    background: #10b981;
                }
                .connection-status.disconnected {
                    background: #ef4444;
                }
                #messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 20px;
                    background: #f9fafb;
                }
                .message {
                    margin-bottom: 16px;
                    display: flex;
                    animation: slideIn 0.3s ease-out;
                }
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .message.user {
                    justify-content: flex-end;
                }
                .message-content {
                    max-width: 70%;
                    padding: 12px 16px;
                    border-radius: 18px;
                    line-height: 1.5;
                }
                .message.user .message-content {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-bottom-right-radius: 4px;
                }
                .message.assistant .message-content {
                    background: white;
                    color: #1f2937;
                    border: 1px solid #e5e7eb;
                    border-bottom-left-radius: 4px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }
                .message.system .message-content {
                    background: #fef3c7;
                    color: #92400e;
                    font-size: 14px;
                    max-width: 100%;
                    text-align: center;
                    border-radius: 8px;
                }
                .input-area {
                    padding: 20px;
                    background: white;
                    border-top: 1px solid #e5e7eb;
                }
                .input-form {
                    display: flex;
                    gap: 10px;
                }
                #messageInput {
                    flex: 1;
                    padding: 12px 16px;
                    border: 2px solid #e5e7eb;
                    border-radius: 24px;
                    font-size: 15px;
                    outline: none;
                    transition: all 0.3s;
                }
                #messageInput:focus {
                    border-color: #667eea;
                    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                }
                #sendButton {
                    padding: 12px 24px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 24px;
                    font-size: 15px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s;
                    min-width: 100px;
                }
                #sendButton:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                }
                #sendButton:active {
                    transform: translateY(0);
                }
                #sendButton:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                    transform: none;
                }
                .typing-indicator {
                    display: none;
                    padding: 12px 16px;
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 18px;
                    width: fit-content;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }
                .typing-indicator.active {
                    display: block;
                }
                .typing-indicator span {
                    display: inline-block;
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: #9ca3af;
                    margin: 0 2px;
                    animation: typing 1.4s infinite;
                }
                .typing-indicator span:nth-child(2) {
                    animation-delay: 0.2s;
                }
                .typing-indicator span:nth-child(3) {
                    animation-delay: 0.4s;
                }
                @keyframes typing {
                    0%, 60%, 100% {
                        transform: translateY(0);
                    }
                    30% {
                        transform: translateY(-10px);
                    }
                }
                .examples {
                    padding: 10px 20px;
                    display: flex;
                    gap: 8px;
                    overflow-x: auto;
                    background: white;
                    border-top: 1px solid #e5e7eb;
                }
                .example-btn {
                    padding: 6px 12px;
                    background: #f3f4f6;
                    border: 1px solid #e5e7eb;
                    border-radius: 12px;
                    font-size: 13px;
                    cursor: pointer;
                    white-space: nowrap;
                    transition: all 0.3s;
                }
                .example-btn:hover {
                    background: #e5e7eb;
                    transform: translateY(-1px);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 웹 검색 챗봇 에이전트</h1>
                    <p>LangGraph + Tavily Search</p>
                    <div class="connection-status disconnected" id="status">연결 안됨</div>
                </div>
                <div id="messages"></div>
                <div class="examples">
                    <button class="example-btn" onclick="sendExample('최신 AI 뉴스를 검색해줘')">최신 AI 뉴스</button>
                    <button class="example-btn" onclick="sendExample('2024년 파이썬 트렌드는?')">파이썬 트렌드</button>
                    <button class="example-btn" onclick="sendExample('FastAPI vs Flask 비교해줘')">FastAPI vs Flask</button>
                </div>
                <div class="input-area">
                    <form class="input-form" onsubmit="sendMessage(event)">
                        <input
                            type="text"
                            id="messageInput"
                            placeholder="메시지를 입력하세요..."
                            autocomplete="off"
                            disabled
                        />
                        <button type="submit" id="sendButton" disabled>전송</button>
                    </form>
                </div>
            </div>
            <script>
                let ws;
                const messagesDiv = document.getElementById('messages');
                const messageInput = document.getElementById('messageInput');
                const sendButton = document.getElementById('sendButton');
                const statusDiv = document.getElementById('status');
                const sessionId = 'user_' + Math.random().toString(36).substr(2, 9);
                let currentAssistantMessage = null;

                function connect() {
                    ws = new WebSocket(`ws://${window.location.host}/ws/${sessionId}`);

                    ws.onopen = function(event) {
                        statusDiv.textContent = '연결됨';
                        statusDiv.className = 'connection-status connected';
                        messageInput.disabled = false;
                        sendButton.disabled = false;
                        addSystemMessage('✅ 서버에 연결되었습니다. 무엇을 도와드릴까요?');
                    };

                    ws.onmessage = function(event) {
                        const data = JSON.parse(event.data);

                        if (data.type === 'start') {
                            // 새 응답 시작
                            currentAssistantMessage = addMessage('assistant', '');
                            showTypingIndicator(true);
                        } else if (data.type === 'stream') {
                            // 스트리밍 청크
                            if (currentAssistantMessage) {
                                currentAssistantMessage.textContent += data.content;
                                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                            }
                        } else if (data.type === 'end') {
                            // 응답 완료
                            showTypingIndicator(false);
                            currentAssistantMessage = null;
                        } else if (data.type === 'error') {
                            // 오류 처리
                            showTypingIndicator(false);
                            addSystemMessage('❌ 오류: ' + data.content);
                        }
                    };

                    ws.onerror = function(error) {
                        console.error('WebSocket error:', error);
                        addSystemMessage('❌ 연결 오류가 발생했습니다.');
                    };

                    ws.onclose = function(event) {
                        statusDiv.textContent = '연결 끊김';
                        statusDiv.className = 'connection-status disconnected';
                        messageInput.disabled = true;
                        sendButton.disabled = true;
                        addSystemMessage('⚠️ 서버 연결이 끊어졌습니다. 5초 후 재연결을 시도합니다...');
                        setTimeout(connect, 5000);
                    };
                }

                function addMessage(role, content) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${role}`;

                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'message-content';
                    contentDiv.textContent = content;

                    messageDiv.appendChild(contentDiv);
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;

                    return contentDiv;
                }

                function addSystemMessage(content) {
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message system';

                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'message-content';
                    contentDiv.textContent = content;

                    messageDiv.appendChild(contentDiv);
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }

                function showTypingIndicator(show) {
                    let indicator = document.querySelector('.typing-indicator');
                    if (show && !indicator) {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = 'message assistant';

                        indicator = document.createElement('div');
                        indicator.className = 'typing-indicator active';
                        indicator.innerHTML = '<span></span><span></span><span></span>';

                        messageDiv.appendChild(indicator);
                        messagesDiv.appendChild(messageDiv);
                    } else if (!show && indicator) {
                        indicator.parentElement.remove();
                    }
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }

                function sendMessage(event) {
                    event.preventDefault();
                    const message = messageInput.value.trim();
                    if (message && ws.readyState === WebSocket.OPEN) {
                        addMessage('user', message);
                        ws.send(message);
                        messageInput.value = '';
                    }
                }

                function sendExample(text) {
                    messageInput.value = text;
                    messageInput.focus();
                }

                // 페이지 로드 시 연결
                connect();
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    채팅 메시지 처리 (REST API)

    Args:
        request: 채팅 요청 (메시지, 세션 ID)

    Returns:
        에이전트 응답
    """
    try:
        agent = get_agent()
        response = await agent.process_message(
            message=request.message, session_id=request.session_id
        )

        return ChatResponse(response=response, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    """
    대화 히스토리 조회

    Args:
        session_id: 세션 ID

    Returns:
        대화 히스토리
    """
    try:
        agent = get_agent()
        history = agent.get_conversation_history(session_id=session_id)

        return HistoryResponse(session_id=session_id, history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket 엔드포인트 (실시간 채팅)

    Args:
        websocket: WebSocket 연결
        session_id: 세션 ID
    """
    await websocket.accept()
    agent = get_agent()

    try:
        while True:
            # 클라이언트로부터 메시지 수신
            message = await websocket.receive_text()

            # 응답 시작 알림
            await websocket.send_json({"type": "start", "session_id": session_id})

            try:
                # 스트리밍 응답 생성
                async for chunk in agent.stream_message(message, session_id):
                    await websocket.send_json({"type": "stream", "content": chunk})

                # 응답 완료 알림
                await websocket.send_json({"type": "end", "session_id": session_id})

            except Exception as e:
                # 오류 발생 시
                await websocket.send_json({"type": "error", "content": str(e)})

    except WebSocketDisconnect:
        print(f"클라이언트 연결 종료: {session_id}")
    except Exception as e:
        print(f"WebSocket 오류: {e}")
        try:
            await websocket.close()
        except Exception:
            pass


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "model": settings.openai_model, "version": "1.0.0"}


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 웹 검색 챗봇 에이전트 서버")
    print("=" * 60)
    print(f"📍 서버 주소: http://{settings.host}:{settings.port}")
    print(f"📚 API 문서: http://{settings.host}:{settings.port}/docs")
    print(f"🔗 WebSocket: ws://{settings.host}:{settings.port}/ws/{{session_id}}")
    print("=" * 60 + "\n")

    uvicorn.run(app, host=settings.host, port=settings.port, log_level="info")
