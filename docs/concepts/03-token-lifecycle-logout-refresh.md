
<!-- docs/concepts/03-token-lifecycle-logout-refresh.md -->
# 토큰 수명주기: 만료/재발급/로그아웃 무효화

## 1) 왜 “수명주기”가 중요한가
토큰은 곧 권한이다. 유출 시 피해를 줄이려면:
- 토큰 수명(exp)을 짧게
- 폐기(로그아웃/강제 만료) 전략을 명확히
- 재발급 정책을 문서화
해야 운영에서 사고가 덜 난다.

---

## 2) 최소 운영급 정책(권장)
- Access Token 만료: 30~60분
- 로그아웃: 즉시 무효화(아래 전략 중 1개 선택)
- 사용자 비활성화(is_active=false): 즉시 차단(DB 확인)

---

## 3) 로그아웃 무효화 전략 비교
### A) token_version (추천: 단순/강력)
- user 테이블에 token_version 정수 저장
- 발급 시 token_version claim 포함
- 요청 시 DB와 token_version 비교
- 로그아웃: token_version += 1

특징:
- “모든 토큰 무효화” 성격이 강함(전 기기 로그아웃)
- 저장소 운영이 필요 없어 초기 서비스에 최적

### B) 블랙리스트(jti)
- 토큰에 jti(고유 ID) 발급
- 로그아웃: jti를 Redis/DB에 저장
- 요청 시 jti 조회 후 차단
- 만료된 jti 청소 필요

특징:
- 특정 토큰만 끊을 수 있어 정교함
- 운영 비용(저장소, 청소, 가용성)이 생김

---

## 4) Refresh Token을 도입한다면(확장 설계)
Refresh를 “안전하게” 하려면 보통 이 개념이 따라온다:
- Refresh Token Rotation: 재발급 때마다 refresh를 새로 주고, 이전 refresh는 폐기
- 탈취 탐지: 이미 폐기된 refresh로 재발급 시도하면 계정 보호(강제 로그아웃 등)
- 저장 위치: HttpOnly cookie 선호(브라우저 기준)

DocuMind 1차 목표는:
- Access + token_version으로 운영급 달성
- Refresh는 “2차 개선 과제”로 문서화(면접에서 확장성 설명 포인트)

---

## 5) “강제 로그아웃”/비밀번호 변경 시 정책
실무에서 자주 묻는 케이스:
- 비밀번호 변경
- 관리자에 의한 계정 잠금
- 침해 의심

이때 token_version을 증가시키면:
- 기존 토큰이 전부 무효화되어 즉시 대응 가능하다.
