"""
app/api/v1/auth.py

✅ 인증(Auth) API 라우터
- POST /auth/register : 회원가입
- POST /auth/login    : 로그인(JWT 발급)

📌 이 파일은 "HTTP 레이어(프레젠테이션 레이어)"
- 요청/응답(Pydantic)
- 인증 흐름 제어
- HTTP 예외(HTTPException)
를 담당한다.

DB CRUD는 repository로 넘긴다.
보안(JWT/비밀번호)은 core/security로 넘긴다.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import security                  # 비밀번호 검증/토큰 생성 같은 보안 유틸
from app.core.config import settings           # 토큰 만료시간 등 설정값
from app.db.deps import get_db                 # 요청마다 DB 세션 주입하는 Depends
from app.repository import user_repository     # User 관련 DB 접근(CRUD)
from app.schemas.user import UserCreate, UserResponse  # 요청/응답 스키마(DTO)

# ✅ 이 파일에서 제공할 라우터 객체
router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,               # ✅ 응답 JSON을 UserResponse 형태로 강제
    status_code=status.HTTP_201_CREATED,       # ✅ 성공 시 201 Created 반환
)
def register_user(
    user: UserCreate,                          # ✅ 요청 바디(JSON)를 검증/파싱한 결과
    db: Session = Depends(get_db),             # ✅ 요청당 DB 세션 1개 주입
) -> UserResponse:
    """
    ✅ 회원가입

    흐름:
    1) 이메일 중복 체크
    2) 없으면 유저 생성(비밀번호는 repository 내부에서 해싱)
    3) 생성된 유저 반환 (비밀번호는 응답에 포함 X)
    """

    # 1) 이미 등록된 이메일인지 확인
    existing_user = user_repository.get_user_by_email(db, user.email)
    if existing_user:
        # 이미 존재하면 400 에러
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 2) 새 유저 생성 (비밀번호 해싱 포함)
    new_user = user_repository.create_user(db, user.email, user.password)

    # 3) SQLAlchemy User 객체를 반환하면
    #    Pydantic(UserResponse, orm_mode=True)가 JSON으로 변환해준다.
    return new_user


@router.post("/login")
def login_user(
    user: UserCreate,                          # ✅ 로그인 요청(email/password)
    db: Session = Depends(get_db),             # ✅ DB 세션 주입
):
    """
    ✅ 로그인 + JWT 발급

    흐름:
    1) 이메일로 사용자 조회
    2) 비밀번호 검증
    3) 만료시간 설정
    4) JWT 토큰 생성 후 반환
    """

    # 1) 이메일로 사용자 조회
    db_user = user_repository.get_user_by_email(db, user.email)
    if not db_user:
        # 보안상 "이메일 틀림/비번 틀림"을 구분하지 않고 동일 메시지
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    # 2) 비밀번호 검증 (평문 vs 해시 비교)
    if not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    # 3) 토큰 만료 시간(기본 설정값) 적용
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # 4) JWT 생성 (sub(subject)에 이메일을 넣는다)
    token = security.create_access_token(
        subject=db_user.email,
        expires_delta=expires,
    )

    # 5) 클라이언트는 이후 요청부터 Authorization 헤더에 아래처럼 넣는다:
    #    Authorization: Bearer <access_token>
    return {
        "access_token": token,
        "token_type": "bearer",
    }
