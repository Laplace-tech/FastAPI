"""
tests/test_smoke.py

✅ 기준선(스모크) 테스트
- register/login이 성공한다.
- 토큰으로 /documents/me 가 200으로 성공한다.

이 테스트가 통과하면:
"기본 인증 + 보호된 엔드포인트"가 안 깨졌다는 최소 보장을 얻는다.
"""

import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_login_and_documents_me():
    email = f"user-{uuid.uuid4()}@example.com"
    password = "NoMooHyunFeelingIsGood"

    result_register = client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert result_register.status_code == 201, result_register.text
    assert result_register.json()["email"] == email

    result_login = client.post(
        "/auth/login",
        json={"email": email, "password": password},
    )
    assert result_login.status_code == 200, result_login.text

    login_data = result_login.json()
    assert "access_token" in login_data, login_data
    token = login_data["access_token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}
    result_me = client.get("/documents/me", headers=headers)
    assert result_me.status_code == 200, result_me.text

    payload = result_me.json()
    assert isinstance(payload, list), payload
