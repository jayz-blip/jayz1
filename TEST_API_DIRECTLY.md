# API 직접 테스트 가이드

## 🔍 Network 탭에서 요청을 찾을 수 없는 경우

요청이 보이지 않으면 API를 직접 테스트해보세요.

## 🚀 방법 1: 브라우저에서 직접 테스트

### Cloudflare Pages Functions 테스트

브라우저 주소창에 입력:

```
https://jayz1.pages.dev/api/chat
```

**예상 결과**:
- ✅ 405 Method Not Allowed: 정상 (GET 요청이므로)
- ❌ 404 Not Found: Functions가 작동하지 않음
- ❌ 500 Internal Server Error: 서버 오류

### Workers 직접 테스트

Workers URL에 직접 접속:

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

## 🚀 방법 2: 브라우저 콘솔에서 직접 테스트

**F12** → **Console 탭**에서 다음 코드 실행:

```javascript
// Cloudflare Pages Functions 테스트
fetch('/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ message: '안녕하세요' })
})
.then(response => {
  console.log('상태 코드:', response.status);
  return response.json();
})
.then(data => {
  console.log('응답:', data);
})
.catch(error => {
  console.error('오류:', error);
});
```

**예상 결과**:
- ✅ 상태 코드: 200
- ✅ 응답: `{ response: "...", sources: [...] }`
- ❌ 오류: 오류 메시지 확인

## 🚀 방법 3: curl 사용 (PowerShell)

```powershell
# Cloudflare Pages Functions 테스트
curl -X POST https://jayz1.pages.dev/api/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"안녕하세요\"}'
```

## 🔍 문제 진단

### 시나리오 1: /api/chat이 404 오류

**원인**: Cloudflare Pages Functions가 작동하지 않음

**해결**:
1. `functions/api/[[path]].js` 파일 확인
2. 재배포
3. Cloudflare Pages Functions 로그 확인

### 시나리오 2: /api/chat이 500 오류

**원인**: `BACKEND_URL` 환경 변수가 설정되지 않음

**해결**:
1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL` 추가 (Workers URL)
3. 재배포

### 시나리오 3: CORS 오류

**원인**: CORS 설정 문제

**해결**:
1. Workers 코드에서 CORS 헤더 확인
2. Pages Functions에서 CORS 헤더 확인

---

**브라우저 콘솔에서 위 코드를 실행하고 결과를 알려주세요!**

