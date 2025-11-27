# localhost:8000 오류 해결

## 🔍 문제

브라우저 콘솔에서 `localhost:8000/api/chat`으로 요청을 보내고 있습니다.

**원인**: 
- Cloudflare Pages에서는 `localhost:8000`이 존재하지 않음
- 프론트엔드가 로컬 개발 환경용 URL을 사용하고 있음

## ✅ 해결 방법

### 수정 완료

코드를 수정하여 프로덕션 환경에서는 항상 `/api`를 사용하도록 변경했습니다.

### 확인 사항

1. **Cloudflare Pages 재배포 대기**
   - 변경사항이 자동으로 배포됩니다
   - 배포 완료까지 몇 분 소요될 수 있습니다

2. **브라우저 캐시 삭제**
   - **Ctrl + Shift + Delete**
   - **캐시된 이미지 및 파일** 선택
   - **삭제**
   - **페이지 새로고침 (Ctrl + F5)**

3. **Cloudflare Pages 환경 변수 확인**
   - `VITE_API_URL` 환경 변수가 설정되어 있다면 **삭제**하세요
   - 또는 빈 값으로 설정
   - `BACKEND_URL`만 설정되어 있어야 합니다

## 📋 환경 변수 설정

### Cloudflare Pages 환경 변수

**설정해야 할 변수**:
- `BACKEND_URL`: Workers URL (예: `https://chatbot-api.your-subdomain.workers.dev`)

**설정하지 말아야 할 변수**:
- `VITE_API_URL`: 설정하지 않거나 삭제 (프론트엔드가 `/api`를 사용하도록)

## 🔍 확인 방법

재배포 후 브라우저 콘솔에서:

1. **F12** 키 누르기
2. **Console 탭** 확인
3. **채팅 메시지 전송**
4. **API URL 확인**:
   - ✅ 올바른 경우: `🔗 API URL: /api`
   - ❌ 잘못된 경우: `🔗 API URL: http://localhost:8000`

## 🚀 빠른 해결

1. **Cloudflare Pages 대시보드** → **Settings** → **Environment variables**
2. **`VITE_API_URL` 변수가 있다면 삭제**
3. **`BACKEND_URL`만 확인**
4. **재배포 대기**
5. **브라우저 캐시 삭제 후 테스트**

---

**재배포가 완료되면 정상적으로 작동할 것입니다! 🎉**

