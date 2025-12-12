"""
app/api/v1/documents.py

✅ 역할
- 문서 업로드: /documents/upload
- 내 문서 목록: /documents/me

이 파일도 "HTTP 입구(프레젠테이션 레이어)"다.
파일 저장(로컬) + DB 메타데이터 기록을 처리한다.
"""

import os
import uuid
from typing import List

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db

# ✅ 로그인한 사용자(User)를 꺼내오는 의존성(JWT 검증 포함)
from app.core.auth_dep import get_current_user

from app.models.user import User

# ✅ 문서 관련 DB 작업은 repository에 위임
from app.repository.document_repository import (
    create_document,
    get_documents_by_owner,
)

from app.schemas.document import DocumentResponse

router = APIRouter()

# ✅ 업로드 파일을 저장할 폴더(로컬 저장)
UPLOAD_DIR = "app/uploads"

# ✅ 서버 시작 시 uploads 폴더 없으면 생성
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),                  # ✅ multipart/form-data 로 업로드된 파일
    db: Session = Depends(get_db),                 # ✅ DB 세션
    current_user: User = Depends(get_current_user) # ✅ JWT 기반 로그인 유저
) -> DocumentResponse:
    """
    ✅ 문서 업로드 처리 흐름

    1) 파일 MIME 타입 검사 (PDF/DOCX만 허용)
    2) 파일명 충돌 방지를 위해 UUID 파일명 생성
    3) uploads 폴더에 실제 파일 저장
    4) DB에 문서 메타데이터(원본명/경로/타입/소유자) 저장
    5) 저장된 문서 정보를 반환
    """

    # 1) 허용할 MIME 타입 목록
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
 
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed.",
        )

    # 2) 원본 파일명과 확장자 추출
    original_filename = file.filename or "unknown"
    ext = original_filename.split(".")[-1]  # 예: report.pdf -> pdf

    # 3) UUID 파일명 생성 (파일명 중복 방지)
    unique_filename = f"{uuid.uuid4()}.{ext}"

    # 4) 저장 경로 생성
    save_path = os.path.join(UPLOAD_DIR, unique_filename)

    # 5) 실제 파일 저장
    # ⚠️ 지금 방식은 file 전체를 한 번에 읽는다(큰 파일이면 부담될 수 있음)
    #    나중에 스트리밍 방식으로 개선 가능.
    with open(save_path, "wb") as buffer:
        buffer.write(file.file.read())

    # 6) DB에 메타데이터 저장
    doc = create_document(
        db=db,
        filename=original_filename,
        file_path=save_path,
        content_type=file.content_type,
        owner_id=current_user.id,
    )

    return doc


@router.get(
    "/me",
    response_model=List[DocumentResponse],
)
def list_my_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[DocumentResponse]:
    """
    ✅ 내 문서 목록 조회

    - Authorization: Bearer <token> 필요
    - 현재 로그인한 사용자의 id 기준으로 documents를 조회해서 반환
    """

    docs = get_documents_by_owner(db, owner_id=current_user.id)
    return docs
