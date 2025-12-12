"""
app/db/deps.py

✅ DB 세션(Session) 의존성(Depends) 제공 모듈

FastAPI에서는 라우터 함수 파라미터에 이렇게 꽂아서 쓴다:
    from fastapi import Depends
    from sqlalchemy.orm import Session

    @router.get("/items")
    def read_items(db: Session = Depends(get_db)):
        ...

이렇게 하면 FastAPI가 요청마다:
1) DB 세션을 만들고(SessionLocal())
2) 라우터에 db로 주입해주고
3) 요청 처리가 끝나면 세션을 닫는다(db.close())
"""

from app.db.database import SessionLocal


def get_db():
    """
    ✅ 요청 1개당 DB Session 1개를 생성해서 제공하는 제너레이터 함수

    왜 제너레이터(yield)로 하냐?
    - "요청 처리 동안만" 세션을 열어두고
    - 요청이 끝나면 "무조건" 닫게 만들려고 (finally 보장)

    흐름:
    - db = SessionLocal()   -> 세션 생성(연결 준비)
    - yield db              -> 라우터가 이 세션으로 DB 작업 수행
    - finally: db.close()   -> 성공/에러 상관없이 세션 정리
    """

    # ✅ SessionLocal()은 "세션을 만들어주는 공장(클래스/팩토리)"이고,
    #    db는 그 결과로 만들어진 "세션 객체(인스턴스)"를 담는 변수다.
    db = SessionLocal()

    try:
        # ✅ 여기서 라우터 함수로 db가 전달된다.
        #    라우터가 끝날 때까지(응답 반환/예외 발생까지) 이 줄에서 멈춰있는다.
        yield db

    finally:
        # ✅ 요청이 정상 종료되든, 예외가 터지든 무조건 실행된다.
        #    세션을 닫아줘야 커넥션 누수/락 문제를 방지한다.
        db.close()
