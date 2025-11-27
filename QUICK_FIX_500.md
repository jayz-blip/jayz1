# 500 오류 빠른 해결 가이드

## 🔴 현재 문제

**Request failed with status code 500**

이것은 Cloudflare Pages Functions에서 오류가 발생했다는 의미입니다.

## ✅ 즉시 확인할 사항

### 1. Cloudflare Pages 환경 변수 확인 (가장 중요!)

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com
2. **Pages** → **프로젝트 선택** → **Settings** → **Environment variables**
3. **확인 사항**:
   - ✅ `BACKEND_URL`이 설정되어 있는지 확인
   - ✅ 값이 Workers URL과 정확히 일치하는지 확인
   - ✅ `https://`로 시작하는지 확인
   - ✅ 마지막에 `/`가 없는지 확인

**올바른 형식 예시**:
```
https://chatbot-api.your-subdomain.workers.dev
```

### 2. Workers URL 직접 테스트

브라우저에서 Workers URL에 직접 접속:

```
https://chatbot-api.your-subdomain.workers.dev
```

**예상 결과**:
```json
{
  "message": "사내용 채팅 AI API",
  "status": "running"
}
```

**만약 오류가 발생하면**:
- Workers가 제대로 배포되지 않았습니다
- Workers를 재배포해야 합니다

### 3. Workers 재배포 (필요시)

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

### 4. 환경 변수 재설정

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **`BACKEND_URL` 삭제 후 다시 추가**
3. **정확한 Workers URL 입력** (복사해서 붙여넣기)
4. **Save** 클릭
5. **재배포 대기** (몇 분 소요)

## 🔍 문제 진단

### 시나리오 1: `BACKEND_URL`이 설정되지 않음

**증상**: Response에 "Backend URL not configured" 메시지

**해결**:
1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL` 추가
3. Workers URL 입력
4. 재배포

### 시나리오 2: Workers URL이 잘못됨

**증상**: Response에 "Proxy error" 또는 "fetch failed" 메시지

**해결**:
1. Workers URL 확인
2. `https://`로 시작하는지 확인
3. 마지막에 `/`가 없는지 확인
4. Workers URL에 직접 접속하여 테스트

### 시나리오 3: Workers가 배포되지 않음

**증상**: Workers URL에 접속해도 오류 발생

**해결**:
1. Workers 재배포
2. 배포 완료 대기
3. 다시 테스트

## 📋 빠른 해결 순서

1. ✅ **Cloudflare Pages 환경 변수 확인**
   - `BACKEND_URL` 설정 확인
   - Workers URL 정확히 입력

2. ✅ **Workers URL 직접 테스트**
   - 브라우저에서 접속
   - 정상 작동하는지 확인

3. ✅ **환경 변수 재설정** (필요시)
   - 삭제 후 다시 추가
   - 재배포 대기

4. ✅ **Workers 재배포** (필요시)
   - `npx wrangler deploy`
   - 배포 완료 대기

5. ✅ **브라우저 캐시 삭제 후 테스트**
   - Ctrl + Shift + Delete
   - 캐시 삭제
   - 페이지 새로고침

## 🚀 가장 가능성 높은 해결 방법

**`BACKEND_URL` 환경 변수가 설정되지 않았거나 잘못되었을 가능성이 높습니다.**

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **`BACKEND_URL` 확인 및 수정**
3. **재배포 대기**
4. **테스트**

---

**가장 먼저 `BACKEND_URL` 환경 변수를 확인하세요!**

