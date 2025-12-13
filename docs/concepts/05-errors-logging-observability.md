<!-- docs/concepts/05-errors-logging-observability.md -->
# 에러 처리/로그/관측성(운영 관점)

## 1) 운영에서 “문제 해결”의 현실
운영 장애 때 필요한 건 보통 3가지다:
- 어떤 요청이었는가? (입력)
- 어디서 터졌는가? (스택/모듈)
- 같은 문제가 재발하는가? (패턴)

이걸 위해 API는:
- 에러 응답 포맷을 통일하고
- 로그에 request_id를 붙이고
- 측정(응답시간/상태코드/에러율)을 가능하게 해야 한다.

---

## 2) 에러 응답 포맷 통일(권장)
권장 필드:
- code: 고정 에러 코드
- message: 사용자 메시지
- request_id: 추적용

예:
{
  "code": "DOC_NOT_FOUND",
  "message": "Document not found",
  "request_id": "6f0a..."
}

---

## 3) Structured Logging(구조화 로그)
단순 print/log 문자열 대신, 최소 다음은 항상 찍히게:
- timestamp
- level
- request_id
- method, path
- status_code
- elapsed_ms
- user_id(가능하면, 단 민감정보 제외)

이렇게 하면:
- “특정 request_id”로 에러 요청을 추적 가능
- “에러율/슬로우 요청”을 집계 가능

---

## 4) 요청ID(Request ID) 패턴
- 요청이 들어오면 middleware에서 request_id를 생성(또는 상류에서 온 값 사용)
- 응답 헤더와 로그에 같은 request_id를 넣는다

실무 팁:
- 프록시/게이트웨이(Nginx)도 request_id를 붙일 수 있다
- 앱은 “있으면 사용, 없으면 생성”이 베스트

---

## 5) 헬스체크(Health check)
운영/배포에서 필수:
- GET /health: 프로세스 살아있나(200)
- (선택) GET /ready: DB/Redis 연결 가능한가(준비 상태)

---

## 6) 에러 추적 도구(선택)
Sentry 같은 에러 트래킹을 붙이면:
- 예외 발생 시 스택트레이스/빈도/영향 범위를 자동 수집
포트폴리오에서는 “선택”이지만, 붙이면 운영 감각이 확 올라간다.
