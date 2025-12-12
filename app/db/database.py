"""
app/db/database.py

SQLAlchemy DB 인프라 설정 모듈

구성 요소
- engine        : DB 연결 관리자(커넥션/풀 관리)
- SessionLocal  : DB 세션(Session) 생성 공장
- Base          : ORM 모델들이 상속할 베이스 클래스

Spring 비유
- DataSource + EntityManagerFactory(또는 SessionFactory) 느낌
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# ------------------------------------------------------------
# 1) DB URL 가져오기
# ------------------------------------------------------------
# - 환경(개발/운영)에 따라 바뀌는 값이므로 config(settings)에서 가져온다.
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


# ------------------------------------------------------------
# 2) engine 생성 (DB 연결 관리자)
# ------------------------------------------------------------
# engine 역할
# - DB에 연결하는 진입점
# - 커넥션 풀(재사용) 관리
# - 실제 SQL 실행을 위한 저수준 통로

# SQLite 주의사항
# - SQLite는 기본적으로 같은 스레드에서만 커넥션을 쓰게 제한(check_same_thread=True)
# - FastAPI는 요청을 여러 스레드에서 처리할 수 있으므로(특히 sync 엔드포인트)
#   이 제한이 걸리면 오류가 날 수 있다.
# - 그래서 SQLite를 쓸 때는 보통 check_same_thread=False로 완화한다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # ✅ SQLite 전용 옵션
)


# ------------------------------------------------------------
# 3) SessionLocal = 세션(Session) 생성 공장
# ------------------------------------------------------------
# Session 역할(= DB 작업 단위 / 트랜잭션 단위)
# - 조회: db.query(...)
# - 추가: db.add(...)
# - 반영: db.commit()
# - 되돌림: db.rollback()

# 옵션 설명
# - autocommit=False : 자동 커밋 안 함 → 우리가 명시적으로 commit 해야 DB 반영
# - autoflush=False  : 필요한 시점에만 flush → 예측 가능한 동작(초보자에게도 안정적)
# - bind=engine      : 이 Session은 위에서 만든 engine을 통해 DB와 통신
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ------------------------------------------------------------
# 4) Base = ORM 모델 정의 기반
# ------------------------------------------------------------
# ORM 모델(User, Document 등)을 만들 때:
# class User(Base): ...
# 처럼 Base를 상속하면 SQLAlchemy가 "이건 테이블 매핑 대상"으로 인식한다.
Base = declarative_base()
