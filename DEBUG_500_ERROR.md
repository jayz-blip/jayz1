# 500 오류 심층 디버깅

## 🔴 현재 문제

**Request failed with status code 500**이 계속 발생합니다.

백엔드 URL은 맞다고 하니, 다른 곳에 문제가 있을 것입니다.

## 🔍 단계별 확인

### 1단계: Network 탭에서 정확한 오류 메시지 확인 (가장 중요!)

1. **F12** → **Network 탭**
2. **채팅 메시지 전송**
3. **`/api/chat` 요청 클릭**
4. **Response 탭 클릭**
5. **전체 응답 내용 복사**

**확인할 내용**:
- 오류 메시지
- `backendUrl` 값
- `apiUrl` 값
- `error` 메시지
- `message` 내용

### 2단계: Workers URL 직접 테스트

브라우저에서 Workers URL에 직접 접속:

```
https://chatbot-api.jayz-407.workers.dev
```

**결과 확인**:
- ✅ 정상: JSON 응답 표시
- ❌ Error 1101: Workers 코드 문제

### 3단계: Workers API 직접 테스트

브라우저 콘솔에서:

```javascript
fetch('https://chatbot-api.jayz-407.workers.dev/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ message: '안녕하세요' })
})
.then(response => {
  console.log('상태:', response.status);
  return response.text();
})
.then(data => {
  console.log('응답:', data);
  try {
    const json = JSON.parse(data);
    console.log('JSON:', json);
  } catch (e) {
    console.log('텍스트:', data);
  }
})
.catch(error => {
  console.error('오류:', error);
});
```

## 🔧 가능한 원인

### 원인 1: Workers가 Error 1101 발생

**증상**: Workers URL에 접속해도 Error 1101

**해결**: Workers 코드 수정 및 재배포

### 원인 2: D1 데이터베이스 접근 문제

**증상**: Workers는 작동하지만 D1 쿼리 시 오류

**확인**: D1 바인딩 확인

### 원인 3: AI Workers 바인딩 문제

**증상**: 임베딩 생성 시 오류

**확인**: AI 바인딩 확인

### 원인 4: Pages Functions 코드 문제

**증상**: 프록시 과정에서 오류

**확인**: Pages Functions 로그 확인

## 🚀 즉시 확인할 사항

### 1. Network 탭 Response 확인

**가장 중요한 것**: Network 탭 → Response 탭에서 정확한 오류 메시지를 확인하세요!

오류 메시지 예시:
```json
{
  "error": "Backend error",
  "status": 500,
  "data": "..."
}
```

또는:
```json
{
  "error": "Proxy error",
  "message": "..."
}
```

### 2. Workers URL 직접 테스트

```
https://chatbot-api.jayz-407.workers.dev
```

### 3. Workers 재배포

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

---

**가장 먼저 Network 탭의 Response 내용을 알려주세요!**

**그리고 Workers URL을 직접 테스트한 결과도 알려주세요!**

