# 500 오류 지속 해결 가이드

## 🔴 현재 문제

**Request failed with status code 500**이 계속 발생합니다.

## 🔍 문제 진단

500 오류는 Cloudflare Pages Functions에서 발생하고 있습니다. 가능한 원인:

1. **`BACKEND_URL` 환경 변수 문제**
2. **Workers가 작동하지 않음** (Error 1101)
3. **Pages Functions 코드 문제**

## 🚀 단계별 해결 방법

### 1단계: Network 탭에서 Response 확인

1. **F12** → **Network 탭**
2. **`/api/chat` 요청 클릭**
3. **Response 탭 확인**
4. **오류 메시지 복사**

**가능한 오류 메시지**:
- `"Backend URL not configured"`: `BACKEND_URL` 환경 변수 문제
- `"Proxy error"`: Workers URL 연결 실패
- 기타 오류 메시지

### 2단계: Cloudflare Pages 환경 변수 확인

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **`BACKEND_URL` 확인**:
   - ✅ 설정되어 있는지 확인
   - ✅ 값이 Workers URL과 정확히 일치하는지 확인
   - ✅ `https://`로 시작하는지 확인
   - ✅ 마지막에 `/`가 없는지 확인

**올바른 형식**:
```
https://chatbot-api.your-subdomain.workers.dev
```

### 3단계: Workers URL 직접 테스트

브라우저에서 Workers URL에 직접 접속:

```
https://chatbot-api.your-subdomain.workers.dev
```

**결과 확인**:
- ✅ 정상: JSON 응답 표시
- ❌ Error 1101: Workers 코드 문제

### 4단계: Workers 재배포 (Error 1101인 경우)

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

### 5단계: 간단한 테스트

Pages Functions를 간단하게 수정하여 테스트:

```javascript
// functions/api/[[path]].js
export async function onRequest(context) {
  const backendUrl = context.env.BACKEND_URL;
  
  if (!backendUrl) {
    return new Response(JSON.stringify({ 
      error: 'BACKEND_URL not set',
      message: 'Please set BACKEND_URL in Cloudflare Pages environment variables'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
  
  return new Response(JSON.stringify({ 
    message: 'Test successful',
    backendUrl: backendUrl,
    hasBackendUrl: !!backendUrl
  }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}
```

이 코드로 테스트하면 `BACKEND_URL`이 설정되어 있는지 확인할 수 있습니다.

## 🔧 빠른 해결 방법

### 방법 1: 환경 변수 재설정

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **`BACKEND_URL` 삭제**
3. **다시 추가**:
   - Variable name: `BACKEND_URL`
   - Value: Workers URL (정확히 복사해서 붙여넣기)
4. **Save** 클릭
5. **재배포 대기** (몇 분)

### 방법 2: Workers 확인 및 재배포

1. **Workers URL 직접 테스트**
2. **Error 1101이면 Workers 재배포**
3. **정상 작동 확인 후 Pages 재배포**

### 방법 3: Pages Functions 로그 확인

1. **Cloudflare Pages** → **프로젝트** → **Functions** 탭
2. **로그 확인**
3. **오류 메시지 확인**

## 📋 체크리스트

- [ ] Network 탭에서 Response 확인
- [ ] 오류 메시지 복사
- [ ] `BACKEND_URL` 환경 변수 확인
- [ ] Workers URL 직접 테스트
- [ ] Workers 재배포 (필요시)
- [ ] 환경 변수 재설정
- [ ] 재배포 대기

## 🆘 가장 중요한 것

**Network 탭 → Response 탭에서 정확한 오류 메시지를 확인하세요!**

오류 메시지를 알려주시면 더 정확한 해결책을 제시할 수 있습니다.

---

**Network 탭의 Response 내용을 알려주세요!**

