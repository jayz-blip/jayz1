# Network Error 디버깅 가이드

## 🔍 Network Error 원인 분석

Network Error가 발생하는 주요 원인:

1. **Workers URL이 잘못 설정됨**
2. **Workers가 배포되지 않음**
3. **CORS 문제**
4. **API 엔드포인트 경로 문제**
5. **환경 변수가 제대로 로드되지 않음**

## 🔧 해결 방법

### 1단계: 브라우저 콘솔 확인

1. **F12 키를 눌러 개발자 도구 열기**
2. **Console 탭 확인**
   - 오류 메시지 확인
   - 빨간색 오류 메시지 찾기
3. **Network 탭 확인**
   - `/api/chat` 요청 찾기
   - 상태 코드 확인 (404, 500, CORS 오류 등)
   - 요청 URL 확인

### 2단계: Workers URL 확인

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com
2. **Workers & Pages** → **Workers** 클릭
3. **`chatbot-api` 프로젝트** 클릭
4. **Workers URL 복사**
   - 예: `https://chatbot-api.your-subdomain.workers.dev`

### 3단계: Cloudflare Pages 환경 변수 확인

1. **Cloudflare Pages 대시보드 접속**
2. **프로젝트 선택** → **Settings** → **Environment variables**
3. **`BACKEND_URL` 확인**
   - 값이 Workers URL과 일치하는지 확인
   - 예: `https://chatbot-api.your-subdomain.workers.dev`
4. **재배포** (환경 변수를 수정했다면)

### 4단계: Workers 직접 테스트

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

만약 오류가 발생하면 Workers가 제대로 배포되지 않은 것입니다.

### 5단계: API 엔드포인트 테스트

브라우저에서 직접 테스트:

```
https://chatbot-api.your-subdomain.workers.dev/api/chat
```

또는 curl 사용:

```powershell
curl -X POST https://chatbot-api.your-subdomain.workers.dev/api/chat `
  -H "Content-Type: application/json" `
  -d '{"message": "안녕하세요"}'
```

## 📋 체크리스트

- [ ] 브라우저 콘솔 오류 확인
- [ ] Network 탭에서 요청 상태 확인
- [ ] Workers URL 확인
- [ ] Cloudflare Pages 환경 변수 확인
- [ ] Workers 직접 테스트
- [ ] API 엔드포인트 테스트

## 🔍 일반적인 오류 메시지

### "Failed to fetch" 또는 "Network Error"
- **원인**: Workers URL이 잘못되었거나 Workers가 배포되지 않음
- **해결**: Workers URL 확인 및 재배포

### "CORS policy" 오류
- **원인**: CORS 설정 문제
- **해결**: Workers 코드에서 CORS 헤더 확인

### "404 Not Found"
- **원인**: API 경로가 잘못됨
- **해결**: Workers 코드의 라우팅 확인

### "500 Internal Server Error"
- **원인**: Workers 코드 오류
- **해결**: Workers 로그 확인

## 🚀 빠른 해결 방법

1. **Workers URL 확인 및 복사**
2. **Cloudflare Pages 환경 변수에 정확히 입력**
3. **재배포**
4. **브라우저 캐시 삭제 후 다시 시도**

---

**브라우저 콘솔과 Network 탭의 오류 메시지를 알려주시면 더 정확한 해결책을 제시할 수 있습니다!**

