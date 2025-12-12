"""
app/core/auth_dep.py

✅ "현재 로그인한 사용자(User)"를 뽑아주는 FastAPI Depends

라우터에서 이렇게 쓰면:
    current_user: User = Depends(get_current_user)

FastAPI가 자동으로:
1) Authorization 헤더에서 Bearer 토큰을 읽고
2) JWT를 검증해서 sub(이메일)을 뽑고
3) DB에서 해당 이메일의 User를 조회해서
4) current_user로 User ORM 객체를 주입해준다.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_access_token     # JWT 검증 + sub 추출
from app.db.deps import get_db                         # 요청당 DB 세션 주입
from app.repository.user_repository import get_user_by_email  # 유저 조회(이메일)
from app.models.user import User                       # 반환 타입(ORM 모델)

# ✅ Authorization: Bearer <token> 형태를 파싱해주는 도구
# - 성공하면 HTTPAuthorizationCredentials 객체를 준다.
# - 실패하면(헤더 없거나 포맷 이상) FastAPI가 403/401 계열로 처리한다.
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),  # ✅ Bearer 토큰 파싱 결과
    db: Session = Depends(get_db),                                   # ✅ DB 세션
) -> User:
    """
    ✅ 현재 요청을 보낸 사용자를 찾아서 반환한다.

    처리 순서:
    1) credentials에서 JWT 문자열(token) 추출
    2) token을 검증해서 이메일(sub) 추출
    3) DB에서 이메일로 User 조회
    4) User 객체 반환
    """

    # 1) Bearer 토큰 문자열만 뽑기
    # credentials 구조:
    # - credentials.scheme == "Bearer"
    # - credentials.credentials == "<JWT 문자열>"
    token = credentials.credentials

    # 2) JWT 검증 + sub(subject) 추출
    # - 유효하면 이메일(sub) 문자열이 나온다.
    # - 만료/위조/포맷 오류면 None
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # 3) 토큰에서 나온 이메일로 DB에서 사용자 조회
    user = get_user_by_email(db, email)
    if user is None:
        # 토큰은 유효한데 사용자가 없다면:
        # - 탈퇴했거나
        # - DB가 초기화됐거나
        # - 이상한 토큰을 들고 온 케이스
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # 4) 검증 통과 → 현재 사용자(User ORM 객체) 반환
    return user
