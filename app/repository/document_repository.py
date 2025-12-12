"""
app/repository/document_repository.py

Document 관련 DB 작업을 담당하는 Repository 모듈

역할
- "문서를 DB에 어떻게 저장/조회할지"만 책임진다.
- FastAPI(라우터)나 비즈니스 로직은 여기서 처리하지 않는다.
  (예: 파일 저장, 권한 체크, 요청/응답 포맷 등은 다른 레이어에서 처리)
"""

from typing import List
from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    *,
    filename: str,
    file_path: str,
    content_type: str,
    owner_id: int,
) -> Document:
    """
    문서 메타데이터를 DB에 저장한다. (INSERT)

    Args:
        db: SQLAlchemy Session (요청 단위로 주입됨)
        filename: 사용자가 업로드한 원본 파일 이름 (예: "report.pdf")
        file_path: 서버에 저장된 상대 경로 (예: "uploads/uuid.pdf")
        content_type: MIME 타입 (예: "application/pdf")
        owner_id: 소유자 users.id (외래키)

    Returns:
        저장된 Document ORM 객체
        - commit 이후 생성된 id 등이 반영된 상태로 반환됨
    """

    # 1) ORM 객체 생성 (아직 DB에 INSERT 된 상태는 아님)
    db_document = Document(
        filename=filename,
        file_path=file_path,
        content_type=content_type,
        owner_id=owner_id,
    )

    # 2) 세션에 추가 → commit 시점에 INSERT가 실제 실행됨
    db.add(db_document)
    db.commit()

    # 3) DB에서 생성된 값(자동 증가 id 등)을 객체에 다시 채움
    # - commit 후 refresh를 하면 최신 상태가 보장됨
    db.refresh(db_document)

    return db_document


def get_documents_by_owner(db: Session, owner_id: int) -> List[Document]:
    """
    특정 사용자의 문서 목록을 조회한다. (SELECT)

    Args:
        db: SQLAlchemy Session
        owner_id: 조회할 사용자 ID (users.id)

    Returns:
        해당 사용자가 소유한 Document 리스트
    """

    # owner_id가 일치하는 문서만 필터링해서 전부 조회
    return db.query(Document).filter(Document.owner_id == owner_id).all()
