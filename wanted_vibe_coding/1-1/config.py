"""
설정 관리 모듈
환경 변수를 로드하고 애플리케이션 설정을 관리합니다.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # API 키
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")

    # 서버 설정
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # LLM 설정
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    # Tavily 검색 설정
    tavily_max_results: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False


# 싱글톤 설정 인스턴스
settings = Settings()


def validate_settings():
    """필수 설정 값 검증"""
    if not settings.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    if not settings.tavily_api_key:
        raise ValueError(
            "TAVILY_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."
        )

    print("✅ 설정 검증 완료")
    print(f"   - OpenAI Model: {settings.openai_model}")
    print(f"   - Tavily Max Results: {settings.tavily_max_results}")
    print(f"   - Server: {settings.host}:{settings.port}")
