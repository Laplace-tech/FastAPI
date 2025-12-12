"""
app/core/security.py

✅ 보안(Security) 유틸 모듈
- 비밀번호: 해싱(hash) / 검증(verify)
- JWT: 생성(encode) / 검증+디코딩(decode)

JWT 한 줄 요약:
- 서버가 "이 토큰은 내가 만들었음(위조 아님)"을 서명(signature)으로 증명한다.
- 서버는 토큰을 검증해서 "누구(sub)인지"를 확인한다.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ✅ 비밀번호 해싱/검증 도구 설정
# - schemes=["bcrypt"] : bcrypt 알고리즘 사용
# - deprecated="auto"  : 오래된 해시 방식 교체 지원(지금은 크게 신경 X)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    ✅ 평문 비밀번호 -> 해시 문자열로 변환

    왜 해시로 저장하냐?
    - DB가 유출돼도 평문 비밀번호가 그대로 노출되지 않게 하려고
    - 해시는 "원래 문자열"로 되돌리기 어렵다(일방향)
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    ✅ 비밀번호 검증

    - plain_password  : 사용자가 로그인 시 입력한 평문
    - hashed_password : DB에 저장된 해시 문자열

    내부적으로:
    - plain_password를 같은 방식으로 처리해서 hashed_password와 비교한다.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    ✅ JWT Access Token 생성

    subject:
    - 토큰 주인(우리는 이메일을 넣는다)
    - JWT payload의 "sub" 필드로 들어간다.

    expires_delta:
    - 토큰 만료 시간(예: timedelta(minutes=60))
    - None이면 settings.ACCESS_TOKEN_EXPIRE_MINUTES 기본값 사용

    반환:
    - JWT 문자열(클라이언트가 Authorization: Bearer <token>으로 보낼 값)
    """

    # 1) 만료 시간(exp) 계산 (UTC 기준으로 통일)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # 2) JWT payload 구성
    # - sub: 토큰 주체(누구 토큰인지)
    # - exp: 만료 시간(이 시간 지나면 jwt.decode에서 자동으로 만료 처리됨)
    payload = {
        "sub": subject,
        "exp": expire,
    }

    # 3) payload + 비밀키 + 알고리즘으로 "서명된 토큰 문자열" 생성
    # - settings.JWT_SECRET_KEY가 같아야만 검증이 통과한다.
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def decode_access_token(token: str) -> Optional[str]:
    """
    ✅ JWT 검증 + subject(sub) 추출

    성공:
    - 토큰이 유효하면 payload에서 sub(이메일)를 반환

    실패:
    - 서명 불일치(위조)
    - 만료(exp 지남)
    - 포맷 이상
    이런 경우 None 반환
    """
    try:
        # jwt.decode는 아래를 한 번에 수행한다:
        # - 서명 검증(SECRET_KEY로)
        # - 만료 시간(exp) 검증
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        # 우리가 만들 때 sub에 이메일을 넣었으니 꺼내서 반환
        subject: Optional[str] = payload.get("sub")
        return subject

    except JWTError:
        # JWT 관련 에러는 전부 "유효하지 않은 토큰"으로 취급
        return None
