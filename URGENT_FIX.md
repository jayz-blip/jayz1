# 긴급 수정: localhost:8000 오류 해결

## 🔴 현재 문제

프론트엔드가 여전히 `localhost:8000/api/chat`으로 요청을 보내고 있습니다.

## ✅ 수정 완료

1. **프론트엔드 코드 개선**
   - 프로덕션 환경에서는 항상 `/api` 사용
   - 로컬 개발 환경에서만 `VITE_API_URL` 사용

2. **Cloudflare Pages Functions 개선**
   - `BACKEND_URL`이 없으면 명확한 오류 메시지 반환
   - 디버깅을 위한 로그 추가

## 🚀 즉시 확인할 사항

### 1. Cloudflare Pages 환경 변수 확인 (필수!)

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com
2. **Pages** → **프로젝트 선택** → **Settings** → **Environment variables**
3. **확인 사항**:
   - ✅ `BACKEND_URL`이 설정되어 있는지 확인
   - ✅ 값이 Workers URL과 일치하는지 확인
   - ❌ `VITE_API_URL`이 있다면 **삭제**

### 2. 재배포 확인

1. **Cloudflare Pages 대시보드** → **Deployments** 탭
2. **최신 배포 상태 확인**
   - ✅ 성공: 녹색 체크 표시
   - ❌ 실패: 빨간색 X 표시
3. **배포가 완료될 때까지 대기** (보통 2-3분)

### 3. 브라우저 캐시 완전 삭제

1. **Ctrl + Shift + Delete** 누르기
2. **모든 항목 선택**:
   - ✅ 쿠키 및 기타 사이트 데이터
   - ✅ 캐시된 이미지 및 파일
   - ✅ 오프라인 웹 콘텐츠
3. **시간 범위**: "전체 기간"
4. **데이터 삭제** 클릭
5. **브라우저 완전히 종료 후 재시작**
6. **페이지 접속 후 Ctrl + F5** (강제 새로고침)

### 4. 브라우저 콘솔 확인

1. **F12** 키 누르기
2. **Console 탭** 확인
3. **채팅 메시지 전송**
4. **확인할 내용**:
   - `🔗 API URL: /api` (올바름)
   - `🌐 현재 호스트: jayz1.pages.dev` (또는 실제 도메인)
   - `localhost:8000`이 보이면 안 됨

## 🔍 문제 진단

### 시나리오 1: 여전히 localhost:8000으로 요청

**원인**: 브라우저 캐시 또는 재배포 미완료

**해결**:
1. 브라우저 완전히 종료 후 재시작
2. 시크릿 모드에서 테스트
3. 재배포 완료 대기

### 시나리오 2: /api로 요청하지만 404 오류

**원인**: Cloudflare Pages Functions가 작동하지 않음

**해결**:
1. `functions/api/[[path]].js` 파일이 있는지 확인
2. 재배포
3. Cloudflare Pages Functions 로그 확인

### 시나리오 3: /api로 요청하지만 500 오류

**원인**: `BACKEND_URL` 환경 변수가 설정되지 않음

**해결**:
1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL` 추가 (Workers URL)
3. 재배포

## 📋 체크리스트

- [ ] Cloudflare Pages 환경 변수 확인
  - [ ] `BACKEND_URL` 설정됨
  - [ ] `VITE_API_URL` 삭제됨
- [ ] 재배포 완료 대기
- [ ] 브라우저 캐시 완전 삭제
- [ ] 브라우저 재시작
- [ ] 시크릿 모드에서 테스트
- [ ] 브라우저 콘솔 확인

## 🆘 여전히 문제가 있다면

브라우저 콘솔의 다음 정보를 알려주세요:

1. **API URL**: `🔗 API URL: ???`
2. **현재 호스트**: `🌐 현재 호스트: ???`
3. **Network 탭**:
   - 요청 URL
   - 상태 코드
   - 오류 메시지

---

**가장 중요한 것: `BACKEND_URL` 환경 변수가 설정되어 있어야 합니다!**

