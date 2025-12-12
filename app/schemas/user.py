"""
app/schemas/user.py

API 입출력 스키마(Pydantic)

역할
- 요청(JSON)을 검증/파싱해서 Python 객체로 변환
- 응답(JSON) 형식을 고정해서 클라이언트와 계약(Contract)을 만든다

Spring 비유
- RequestDTO / ResponseDTO
"""

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """
    회원가입/로그인 요청 바디 스키마

    - email: 이메일 형식 검증(EmailStr)
    - password: 평문 비밀번호 (요청에서만 받고 DB에는 해시로 저장)
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    회원가입 응답 스키마

    보안 포인트
    - 비밀번호(평문/해시)는 절대 응답에 포함하면 안 된다.
    """
    id: int
    email: EmailStr

    # ✅ Pydantic v2: ORM 객체(SQLAlchemy 모델)를 그대로 넣어도
    # 이 스키마로 변환할 수 있게 해주는 옵션
    model_config = ConfigDict(from_attributes=True)
