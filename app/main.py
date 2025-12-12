"""
app/main.py

✅ 이 파일의 정체: "FastAPI 앱 조립(Assembly) / 진입점"

여기서 하는 일:
1) FastAPI app 생성
2) 라우터 붙이기(/auth, /documents)
3) ORM 모델 등록 + 테이블 생성
"""

from fastapi import FastAPI

from app.db.database import engine, Base

# ✅ 아래 import가 매우 중요!
# Base.metadata.create_all이 "테이블 만들기"를 하려면,
# 먼저 User/Document 모델이 import되어 Base.metadata에 등록되어 있어야 한다.
from app.models import user, document  # noqa: F401

from app.api.v1.auth import router as auth_router
from app.api.v1.documents import router as documents_router


# ✅ 개발 편의용: 앱 시작 시 테이블 자동 생성
# (실무에서는 Alembic 마이그레이션을 쓰는 게 정석)
Base.metadata.create_all(bind=engine)


# ✅ FastAPI 앱 생성
app = FastAPI(
    title="DocuMind - AI Document Intelligence API",
    description="DocuMind API 문서입니다.",
)


# ✅ 라우터 등록
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(documents_router, prefix="/documents", tags=["Documents"])


@app.get("/")
def root():
    """
    ✅ 헬스 체크
    - 서버가 살아있는지 확인하는 기본 엔드포인트
    """
    return {"message": "DocuMind API is running"}
