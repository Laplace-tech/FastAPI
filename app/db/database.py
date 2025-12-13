"""
app/db/database.py

SQLAlchemy DB 인프라 설정 모듈
- engine        : DB 연결 관리자(커넥션/풀 관리)
- SessionLocal  : DB 세션(Session) 생성 공장
- Base          : ORM 모델들이 상속할 베이스 클래스
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# SQLite 주의사항
# - SQLite는 기본적으로 같은 스레드에서만 커넥션을 쓰게 제한(check_same_thread=True)
# - FastAPI는 요청을 여러 스레드에서 처리할 수 있으므로(특히 sync 엔드포인트)
#   이 제한이 걸리면 오류가 날 수 있다.
# - 그래서 SQLite를 쓸 때는 보통 check_same_thread=False로 완화한다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, 
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# - Base = ORM 모델 정의 기반
# ORM 모델(User, Document 등)을 만들 때:
# User(Base): ..., Document(Base): ... 처럼 Base를 상속하면
# SQLAlchemy가 "이건 테이블 매핑 대상"으로 인식한다.
Base = declarative_base()
