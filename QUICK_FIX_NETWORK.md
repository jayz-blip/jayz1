# Network Error 빠른 해결 가이드

## 🚀 즉시 확인할 사항

### 1. 브라우저 콘솔 확인

1. **F12 키** 누르기
2. **Console 탭** 확인
3. **오류 메시지 복사** (특히 빨간색 오류)

### 2. Network 탭 확인

1. **Network 탭** 클릭
2. **채팅 메시지 전송**
3. **`/api/chat` 요청 찾기**
4. **상태 코드 확인**:
   - 200: 성공
   - 404: 경로 오류
   - 500: 서버 오류
   - CORS: CORS 오류

### 3. Workers URL 확인

```powershell
# Cloudflare 대시보드에서 확인
# Workers & Pages → Workers → chatbot-api
```

### 4. 환경 변수 확인

```powershell
# Cloudflare Pages → Settings → Environment variables
# BACKEND_URL 값 확인
```

## 🔧 일반적인 해결 방법

### 방법 1: Workers 재배포

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

### 방법 2: 환경 변수 재설정

1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL` 삭제 후 다시 추가
3. 정확한 Workers URL 입력
4. 재배포

### 방법 3: 브라우저 캐시 삭제

1. **Ctrl + Shift + Delete**
2. **캐시된 이미지 및 파일** 선택
3. **삭제**
4. **페이지 새로고침 (Ctrl + F5)**

---

**브라우저 콘솔의 정확한 오류 메시지를 알려주시면 더 구체적인 해결책을 제시할 수 있습니다!**

