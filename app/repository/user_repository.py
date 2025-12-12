"""
app/repository/user_repository.py

User 테이블(DB) 접근 전담 Repository

역할
- 오직 DB 조회/저장(쿼리)만 담당한다.
- HTTPException 같은 "웹 레이어 책임"은 여기서 하지 않는다.
  (예: 이메일 중복이면 409 던지기 같은 건 서비스/라우터에서 결정)

장점(레이어 분리)
- DB 로직을 한 곳에 모아서 유지보수 쉬움
- 테스트하기 쉬움(라우터 없이 DB 함수만 단독 테스트 가능)
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    이메일로 사용자 1명 조회

    Args:
        db: SQLAlchemy Session
        email: 조회할 이메일

    Returns:
        - 해당 이메일 유저가 있으면 User ORM 객체
        - 없으면 None
    """

    # .first(): 조건에 맞는 첫 번째 row 반환 (없으면 None)
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str) -> User:
    """
    사용자 생성(INSERT)

    Args:
        db: SQLAlchemy Session
        email: 가입 이메일
        password: 사용자가 입력한 평문 비밀번호

    Returns:
        생성된 User ORM 객체 (commit 이후 id가 채워진 상태)

    보안 포인트
    - 비밀번호는 절대 평문으로 DB에 저장하면 안 된다.
    - 반드시 해시(hash)로 변환해서 저장한다.
    """

    # 1) 평문 비밀번호를 해시로 변환
    hashed_pw = hash_password(password)

    # 2) ORM 객체 생성 (아직 DB에 반영되기 전)
    user = User(email=email, hashed_password=hashed_pw)

    # 3) 세션에 추가 → commit 시점에 INSERT 실행
    db.add(user)
    db.commit()

    # 4) DB에서 생성된 값(id 등)을 객체에 반영
    db.refresh(user)

    return user
