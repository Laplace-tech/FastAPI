"""
app/core/config.py

✅ 프로젝트 전역 설정(Settings) 관리 모듈

왜 필요한가?
- DB 주소, JWT 비밀키 같은 설정값은 "코드에 박지 말고" 외부에서 주입해야 한다.
- 개발/배포 환경이 바뀌어도 코드는 그대로 두고 설정만 바꾸기 위함이다.

여기서 하는 일:
- 프로젝트 루트의 .env 파일을 읽는다.
- 환경변수 값을 Settings 객체(settings.xxx)로 꺼내 쓸 수 있게 한다.

스프링 비유:
- application.yml / application.properties + @ConfigurationProperties 같은 역할
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# ✅ 이 파일 위치: C:/project/app/core/config.py
# Path(__file__).resolve()  -> 현재 파일의 절대 경로
# parents[0] = core 폴더
# parents[1] = app 폴더
# parents[2] = project 루트(C:/project)
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    BaseSettings를 상속한 설정 클래스
    - 환경변수(.env 포함)에서 설정값을 읽어오는 클래스

    BaseSettings를 상속하면:
    - 같은 이름의 환경변수가 존재하면 자동으로 값을 읽어서 필드에 채워준다.
      예) DATABASE_URL 환경변수가 있으면 DATABASE_URL 필드에 들어감
    """

    # ✅ SettingsConfigDict: BaseSettings 동작 옵션
    # - env_file: 여기 지정된 파일을 "환경변수처럼" 읽어준다.
    # - env_file_encoding: 파일 인코딩
    # - extra="ignore": .env에 있지만 클래스에 없는 값은 무시(에러 방지)
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"), 
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ------------------------------------------------------------
    # 기본값(default)
    # ------------------------------------------------------------
    # .env(환경변수)에 같은 이름이 있으면 .env 값이 우선 적용된다.

    # ✅ 프로젝트 이름
    PROJECT_NAME: str = "DocuMind - AI Document Intelligence"

    # ✅ DB 연결 문자열
    DATABASE_URL: str = "sqlite:///./test.db"

    # ✅ JWT 관련 설정
    JWT_SECRET_KEY: str = "dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


# 전역에서 한 번만 Settings를 생성해서 공유한다(싱글톤처럼 사용)
# 다른 파일에서는 `from app.core.config import settings` 로 가져다 쓴다.
settings = Settings()
