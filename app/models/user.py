"""
app/models/user.py

✅ SQLAlchemy ORM 모델 = users 테이블 설계도

역할:
- DB의 users 테이블 구조를 파이썬 클래스로 표현한다.
- Base를 상속받으면 SQLAlchemy가 "테이블로 만들 클래스"로 인식한다.

주의:
- 비밀번호는 절대 평문 저장 금지 → 해시(hashed)로만 저장
"""

from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):
    """
    ✅ users 테이블에 매핑되는 ORM 클래스
    - __tablename__으로 실제 테이블 이름을 지정한다.
    """
    __tablename__ = "users"

    # ------------------------------------------------------------
    # id (Primary Key)
    # ------------------------------------------------------------
    # primary_key=True : 기본키(PK)
    # index=True       : 조회 성능을 위해 DB 인덱스 생성
    id = Column(Integer, primary_key=True, index=True)

    # ------------------------------------------------------------
    # email
    # ------------------------------------------------------------
    # unique=True      : 이메일 중복 금지(회원가입 중복 방지의 마지막 방어선)
    # index=True       : 이메일 조회(get_user_by_email)가 매우 많으므로 인덱스 추천
    # nullable=False   : NULL 금지(무조건 값이 있어야 함)
    email = Column(String, unique=True, index=True, nullable=False)

    # ------------------------------------------------------------
    # hashed_password
    # ------------------------------------------------------------
    # ✅ DB에는 해시된 비밀번호만 저장한다.
    # - 회원가입 시: 평문 → 해싱 → 저장
    # - 로그인 시: 평문 입력 → 해시 비교(verify)
    hashed_password = Column(String, nullable=False)
