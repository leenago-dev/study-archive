"""
간단한 테스트 클라이언트
REST API와 WebSocket을 테스트하기 위한 스크립트
"""

import asyncio
import json
import requests
import websockets
from typing import Optional


def test_rest_api(message: str, session_id: str = "test_user"):
    """REST API 테스트"""
    print(f"\n{'='*60}")
    print("REST API 테스트")
    print(f"{'='*60}\n")

    url = "http://localhost:8000/chat"
    payload = {"message": message, "session_id": session_id}

    print(f"📤 요청: {message}")
    print(f"🔗 URL: {url}\n")

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()
        print(f"✅ 응답 수신:")
        print(f"Session ID: {data['session_id']}")
        print(f"\n🤖 에이전트 응답:\n{data['response']}\n")

        return data
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None


async def test_websocket(message: str, session_id: str = "test_user"):
    """WebSocket 테스트"""
    print(f"\n{'='*60}")
    print("WebSocket 테스트 (실시간 스트리밍)")
    print(f"{'='*60}\n")

    uri = f"ws://localhost:8000/ws/{session_id}"

    print(f"📤 메시지: {message}")
    print(f"🔗 연결: {uri}\n")

    try:
        async with websockets.connect(uri) as websocket:
            # 메시지 전송
            await websocket.send(message)
            print("🤖 에이전트 응답 (스트리밍):\n")

            # 응답 수신
            full_response = ""
            async for msg in websocket:
                data = json.loads(msg)

                if data["type"] == "start":
                    print("🟢 응답 시작...")
                elif data["type"] == "stream":
                    content = data["content"]
                    print(content, end="", flush=True)
                    full_response += content
                elif data["type"] == "end":
                    print("\n\n✅ 응답 완료!")
                    break
                elif data["type"] == "error":
                    print(f"\n❌ 오류: {data['content']}")
                    break

            return full_response
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
        return None


def test_history(session_id: str = "test_user"):
    """대화 히스토리 조회 테스트"""
    print(f"\n{'='*60}")
    print("대화 히스토리 조회")
    print(f"{'='*60}\n")

    url = f"http://localhost:8000/history/{session_id}"

    print(f"🔗 URL: {url}\n")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()
        history = data["history"]

        print(f"✅ 히스토리 조회 완료 (총 {len(history)}개 메시지)\n")

        for i, msg in enumerate(history, 1):
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                continue  # 시스템 메시지는 스킵

            emoji = "👤" if role == "user" else "🤖"
            role_name = "사용자" if role == "user" else "에이전트"

            print(f"{emoji} {role_name} (메시지 {i}):")
            # 긴 내용은 잘라서 표시
            if len(content) > 200:
                print(f"  {content[:200]}...")
            else:
                print(f"  {content}")
            print()

        return history
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None


def test_health():
    """헬스 체크 테스트"""
    print(f"\n{'='*60}")
    print("헬스 체크")
    print(f"{'='*60}\n")

    url = "http://localhost:8000/health"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        print("✅ 서버 상태:")
        print(f"  - 상태: {data['status']}")
        print(f"  - 모델: {data['model']}")
        print(f"  - 버전: {data['version']}\n")

        return data
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return None


async def run_all_tests():
    """모든 테스트 실행"""
    print("\n" + "=" * 60)
    print("🧪 웹 검색 챗봇 에이전트 테스트 시작")
    print("=" * 60)

    # 1. 헬스 체크
    health = test_health()
    if not health:
        print("\n⚠️ 서버가 실행되지 않았습니다. 먼저 서버를 시작하세요:")
        print("   python main.py")
        return

    # 2. REST API 테스트
    session_id = "test_user_demo"
    test_rest_api("안녕하세요! 당신은 누구인가요?", session_id)

    await asyncio.sleep(1)

    # 3. WebSocket 테스트
    await test_websocket("최신 AI 뉴스를 간단히 요약해줘", session_id)

    await asyncio.sleep(1)

    # 4. 히스토리 조회
    test_history(session_id)

    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60 + "\n")


def main():
    """메인 함수"""
    print("\n🚀 테스트 클라이언트 시작\n")
    print("다음 중 하나를 선택하세요:")
    print("1. 모든 테스트 실행")
    print("2. REST API만 테스트")
    print("3. WebSocket만 테스트")
    print("4. 히스토리 조회")
    print("5. 헬스 체크")
    print("0. 종료\n")

    while True:
        choice = input("선택 (0-5): ").strip()

        if choice == "0":
            print("\n👋 종료합니다.\n")
            break
        elif choice == "1":
            asyncio.run(run_all_tests())
        elif choice == "2":
            message = input("메시지 입력: ").strip()
            if message:
                test_rest_api(message)
        elif choice == "3":
            message = input("메시지 입력: ").strip()
            if message:
                asyncio.run(test_websocket(message))
        elif choice == "4":
            session_id = input("세션 ID (기본값: test_user): ").strip() or "test_user"
            test_history(session_id)
        elif choice == "5":
            test_health()
        else:
            print("❌ 잘못된 선택입니다.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자에 의해 중단되었습니다.\n")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}\n")
