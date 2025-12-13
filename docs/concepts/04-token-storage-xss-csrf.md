<!-- docs/concepts/04-token-storage-xss-csrf.md -->
# 토큰 저장/전송 보안: XSS/CSRF/HTTPS

## 1) 결론부터(실무 요약)
- HTTPS는 필수다(토큰이 네트워크에서 새면 끝).
- 브라우저에서 토큰 저장은 트레이드오프다:
  - LocalStorage: 구현 쉬움, XSS에 취약
  - HttpOnly Cookie: XSS에 강함, CSRF 방어 설계 필요

---

## 2) Bearer 토큰 전송의 기본
API 요청 헤더:
Authorization: Bearer <access_token>

장점:
- CSRF 영향이 상대적으로 적음(자동 전송 쿠키가 아니니까)
- 모바일/서버-서버 통신에도 그대로 적용 가능

주의:
- 토큰을 JS가 들고 있는 경우(XSS) 탈취 위험이 커진다.

---

## 3) 저장 위치 옵션 비교(브라우저 기준)
### A) LocalStorage
- 장점: 단순
- 단점: XSS 뚫리면 토큰이 그대로 탈취됨

필수 대응:
- 프론트에서 CSP(Content Security Policy) 강화
- 입력값 sanitization/취약 라이브러리 최소화

### B) HttpOnly Cookie
- 장점: JS로 접근 불가 → XSS로 토큰 탈취 난이도 상승
- 단점: 쿠키는 브라우저가 자동 전송 → CSRF 위험 증가

CSRF 방어:
- SameSite=Lax/Strict 설정
- 필요 시 CSRF 토큰(Double Submit) 전략

---

## 4) DocuMind 적용 관점
현재는 백엔드 포트폴리오라:
- API는 Bearer 방식(Authorization 헤더)로 설계하되,
- 문서에 “추후 Cookie 기반 인증으로 전환 가능”을 남겨두면 면접에서 확장성 설명이 좋아진다.

---

## 5) 절대 금지/실수 포인트
- .env(시크릿) 커밋 금지
- 토큰에 민감정보 넣지 말기
- 디버그 로그에 Authorization 헤더 찍지 말기(운영사고 1순위)
