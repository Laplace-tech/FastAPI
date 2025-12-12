"""
app/schemas/document.py

✅ Document 관련 "응답 DTO" (Pydantic 스키마)

역할:
- API가 클라이언트에게 돌려주는 JSON 형태를 고정한다.
- SQLAlchemy ORM 객체(Document)를 그대로 반환해도
  Pydantic이 자동으로 이 스키마 형태로 변환할 수 있게 설정한다.
"""

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """
    ✅ 문서 조회/업로드 API에서 반환할 응답 모델
    """

    # ✅ Pydantic v2 설정:
    # from_attributes=True 이면 ORM 객체의 "속성"을 읽어서 스키마로 변환 가능
    model_config = ConfigDict(from_attributes=True)

    # 문서 PK
    id: int

    # 사용자가 업로드한 원본 파일 이름
    filename: str

    # 서버에 저장된 파일 경로 (보통 "uploads/uuid.pdf" 같은 상대경로 권장)
    file_path: str

    # 파일의 MIME 타입 (예: application/pdf)
    content_type: str

    # 문서 소유자(User.id)
    owner_id: int
