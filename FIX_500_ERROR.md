# 500 Internal Server Error 해결 가이드

## 🔍 문제

**Status Code**: 500 Internal Server Error
**Request URL**: `https://jayz1.pages.dev/api/chat`

이것은 Cloudflare Pages Functions에서 오류가 발생했다는 의미입니다.

## 🔧 해결 방법

### 1단계: Response 탭에서 오류 메시지 확인

1. **Network 탭**에서 `/api/chat` 요청 클릭
2. **Response 탭** 클릭
3. **오류 메시지 확인**

**가능한 오류 메시지**:
- `"Backend URL not configured"`: `BACKEND_URL` 환경 변수가 설정되지 않음
- `"Proxy error"`: Workers URL에 연결할 수 없음
- 기타 오류 메시지

### 2단계: Cloudflare Pages 환경 변수 확인

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com
2. **Pages** → **프로젝트 선택** → **Settings** → **Environment variables**
3. **확인 사항**:
   - ✅ `BACKEND_URL`이 설정되어 있는지 확인
   - ✅ 값이 Workers URL과 정확히 일치하는지 확인
   - ✅ `https://`로 시작하는지 확인
   - ✅ 마지막에 `/`가 없는지 확인

**올바른 형식**:
```
https://chatbot-api.your-subdomain.workers.dev
```

**잘못된 형식**:
```
http://chatbot-api.your-subdomain.workers.dev  (http가 아닌 https)
chatbot-api.your-subdomain.workers.dev  (https:// 없음)
https://chatbot-api.your-subdomain.workers.dev/  (마지막에 / 있음)
```

### 3단계: Workers URL 확인

1. **Cloudflare 대시보드** → **Workers & Pages** → **Workers**
2. **`chatbot-api` 프로젝트** 클릭
3. **Workers URL 복사**
4. **브라우저에서 직접 접속하여 테스트**:
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

### 4단계: Workers 재배포 (필요시)

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

### 5단계: 환경 변수 재설정

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **`BACKEND_URL` 삭제 후 다시 추가**
3. **정확한 Workers URL 입력**
4. **Save** 클릭
5. **재배포 대기**

## 📋 체크리스트

- [ ] Response 탭에서 오류 메시지 확인
- [ ] `BACKEND_URL` 환경 변수 확인
- [ ] Workers URL 직접 테스트
- [ ] Workers 재배포 (필요시)
- [ ] 환경 변수 재설정
- [ ] 재배포 대기

## 🔍 일반적인 오류 메시지

### "Backend URL not configured"
**원인**: `BACKEND_URL` 환경 변수가 설정되지 않음

**해결**:
1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL` 추가 (Workers URL)
3. 재배포

### "Proxy error" 또는 "fetch failed"
**원인**: Workers URL에 연결할 수 없음

**해결**:
1. Workers URL이 올바른지 확인
2. Workers가 배포되었는지 확인
3. Workers URL에 직접 접속하여 테스트

### "Network Error"
**원인**: 네트워크 문제 또는 Workers가 응답하지 않음

**해결**:
1. Workers 재배포
2. 잠시 후 다시 시도

---

**가장 먼저 Response 탭에서 오류 메시지를 확인하세요!**

