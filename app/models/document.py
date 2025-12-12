"""
app/models/document.py

documents 테이블 ORM 모델

역할
- 업로드된 "문서 자체(바이너리)"는 로컬(app/uploads)에 저장
- DB에는 문서를 식별/관리하기 위한 "메타데이터"만 저장
  (원본 파일명, 서버 저장 경로, MIME 타입, 소유자 등)
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class Document(Base):
    """
    documents 테이블에 매핑되는 ORM 모델

    이 클래스가 하는 일
    - Document 인스턴스 1개 = documents 테이블의 row 1개
    - SQLAlchemy가 이 정의를 보고 테이블 스키마/쿼리 매핑을 처리한다.
    """

    # 실제 DB 테이블 이름
    __tablename__ = "documents"

    # ------------------------------------------------------------
    # 기본키(PK)
    # ------------------------------------------------------------
    # id: 문서 row를 유일하게 구분하는 키
    # - primary_key=True : PK 지정
    # - index=True       : 조회 성능을 위해 인덱스 생성(보통 PK는 기본 인덱스가 있긴 함)
    id = Column(Integer, primary_key=True, index=True)

    # ------------------------------------------------------------
    # 업로드 당시 사용자가 보낸 원본 파일명
    # ------------------------------------------------------------
    # 예: "report.pdf"
    filename = Column(String, nullable=False)

    # ------------------------------------------------------------
    # 서버에 저장된 파일 경로
    # ------------------------------------------------------------
    # 예: "uploads/uuid.pdf"
    # - 운영/배포 환경에서 프로젝트 경로가 바뀔 수 있으므로
    #   절대경로보다 상대경로를 저장하는 편이 이식성이 좋다.
    file_path = Column(String, nullable=False)

    # ------------------------------------------------------------
    # MIME 타입
    # ------------------------------------------------------------
    # 예: "application/pdf"
    # - 파일 다운로드/미리보기 등에서 Content-Type 설정에 활용 가능
    content_type = Column(String, nullable=False)

    # ------------------------------------------------------------
    # 소유자(Owner) 외래키
    # ------------------------------------------------------------
    # owner_id: 이 문서를 업로드한 사용자(users.id)를 가리킨다.
    # - ForeignKey("users.id") 로 users 테이블의 id와 연결
    # - 로그인 유저 기준 "내 문서 목록" 같은 기능 구현에 핵심
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
