"""
app/core/config.py

프로젝트 설정값을 한 곳에 모아두는 모듈

여기서 관리하는 값 예시
- DB 연결 주소
- JWT 비밀키 / 알고리즘 / 만료시간

Spring으로 비유하면:
- application.yml / application.properties 같은 역할

목표
- 설정이 흩어지지 않게 한 파일로 모으고
- 환경(개발/테스트/운영)마다 바뀌는 값은 여기서만 바꾸게 만들기
"""


class Settings:
    """
    프로젝트 전역 설정값 컨테이너

    현재는 '그냥 파이썬 클래스'로 작성되어 있음.
    - 장점: 단순하고 바로 이해됨
    - 단점: 운영 환경에서 비밀키(DB 비번 등)를 코드에 박아두기 위험

    실무형으로 개선할 때는 보통:
    - .env 파일 + pydantic BaseSettings(또는 Settings management)로 분리해서
      OS 환경변수로 값을 주입하는 방식으로 간다.
    """

    # ------------------------------------------------------------
    # 1) 서비스/문서에 표시할 프로젝트 이름
    # ------------------------------------------------------------
    # - FastAPI 문서(Swagger UI)에도 표시될 수 있음
    PROJECT_NAME: str = "DocuMind - AI Document Intelligence"

    # ------------------------------------------------------------
    # 2) DB 연결 문자열(Database URL)
    # ------------------------------------------------------------
    # sqlite:///./test.db 의미:
    # - SQLite를 사용하고
    # - "현재 작업 디렉토리" 기준으로 test.db 파일을 생성/사용한다는 뜻
    #
    # ⚠ 주의: 실행 위치에 따라 ./ 의 기준이 바뀔 수 있음
    # - uvicorn을 어디서 실행하느냐에 따라 test.db 위치가 달라질 수 있다.
    # - 그래서 실무에서는 절대경로로 고정하거나, 환경변수로 주입하는 방식을 씀.
    DATABASE_URL: str = "sqlite:///./test.db"

    # ------------------------------------------------------------
    # 3) JWT 관련 설정
    # ------------------------------------------------------------
    # JWT_SECRET_KEY:
    # - JWT는 서버가 secret key로 서명(signature)을 만들어 토큰 위조를 방지한다.
    # - 이 키가 노출되면 공격자가 "서버가 발급한 척" 토큰을 위조할 수 있어서 매우 위험.
    #
    # ✅ 개발 단계에서는 임시 문자열로 두고,
    # ✅ 운영 환경에서는 반드시 환경변수(.env / secret manager)로 뺀다.
    JWT_SECRET_KEY: str = "super-secret-key-change-in-prod"

    # JWT_ALGORITHM:
    # - 서명 알고리즘
    # - HS256 = (HMAC + SHA256) 방식으로, secret key 하나로 서명/검증을 한다.
    JWT_ALGORITHM: str = "HS256"

    # ACCESS_TOKEN_EXPIRE_MINUTES:
    # - access token(로그인 토큰)의 유효시간(분)
    # - 짧을수록 보안에 유리, 길수록 사용자 편의성이 올라감(로그인 덜 풀림)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


# settings 객체를 한 번만 생성해서(import 시점)
# 다른 모듈들이 from app.core.config import settings 로 가져다 쓰는 패턴
# - 중앙에서 설정을 관리하기 좋다.
settings = Settings()
