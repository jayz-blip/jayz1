# 502 Bad Gateway 오류 해결 가이드

## 문제 상황
- Status Code: 502 Bad Gateway
- Render 백엔드 서버가 응답하지 않음

## 가능한 원인

### 1. 백엔드 서버 크래시
- ChromaDB 초기화 오류
- 메모리 부족
- 코드 오류

### 2. 백엔드가 sleep 모드
- Render 무료 플랜은 15분간 요청이 없으면 sleep 모드
- 첫 요청 시 30-50초 소요

### 3. 백엔드 로딩 중
- 모델 로딩 중
- 데이터 로딩 중

## 해결 방법

### 1. Render 로그 확인
1. Render 대시보드 → `jayznew` 서비스
2. **Logs** 탭 클릭
3. 최근 오류 메시지 확인

### 2. 백엔드 상태 확인
1. Render 대시보드 → `jayznew` 서비스
2. **Metrics** 탭에서 CPU/메모리 사용량 확인
3. **Events** 탭에서 최근 이벤트 확인

### 3. 백엔드 재시작
1. Render 대시보드 → `jayznew` 서비스
2. **Manual Deploy** → **Clear build cache & deploy**

### 4. 간단한 헬스체크 엔드포인트 추가
- `/health` 엔드포인트 추가
- RAG 시스템 없이 응답하는 엔드포인트

## 예상 해결 시간
- 재배포: 5-10분
- 첫 요청 대기: 30-50초 (sleep 모드인 경우)

