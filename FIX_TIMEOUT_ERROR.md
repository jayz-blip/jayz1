# 타임아웃 오류 해결 가이드

## 🔴 발견된 오류

**오류 메시지**: "요청은 보냈지만 응답을 받지 못함: XMLHttpRequest"

**원인**: Workers가 응답하지 않거나 타임아웃되었습니다.

## ✅ 해결 방법

### 1. 프론트엔드 타임아웃 추가

`src/App.jsx`에 30초 타임아웃을 추가했습니다:

```javascript
const response = await axios.post(`${API_URL}/chat`, {
  message: input
}, {
  timeout: 30000, // 30초 타임아웃
  headers: {
    'Content-Type': 'application/json'
  }
})
```

### 2. Workers 성능 최적화

`worker/src/worker.py`에서:
- D1 쿼리 LIMIT을 100에서 500으로 증가 (더 많은 문서 검색)
- 문서 처리 최대 개수 제한 (500개)

### 3. Workers 재배포 필요

코드를 수정했으니 Workers를 재배포해야 합니다:

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npm run deploy
```

또는:

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

## 🔍 문제 진단

### 가능한 원인

1. **Workers 타임아웃**: Workers가 30초 내에 응답하지 않음
2. **D1 쿼리 느림**: 데이터베이스 쿼리가 너무 오래 걸림
3. **AI Workers 느림**: 임베딩 생성이 너무 오래 걸림
4. **무한 루프**: 코드에서 무한 루프 발생

### 확인 사항

1. **Workers 로그 확인**:
   - Cloudflare 대시보드 → Workers & Pages → Workers
   - `chatbot-api` 프로젝트 → "관찰 가능성" 탭
   - 최근 오류 메시지 확인

2. **Workers 직접 테스트**:
   - `https://chatbot-api.jayz-407.workers.dev` 접속
   - 응답이 오는지 확인

3. **D1 데이터 확인**:
   - 데이터가 너무 많으면 쿼리가 느려질 수 있음
   - LIMIT을 더 줄여볼 수 있음

## 🚀 다음 단계

### 1단계: Workers 재배포

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

### 2단계: 프론트엔드 재배포

프론트엔드 변경사항을 GitHub에 푸시하면 Cloudflare Pages가 자동으로 재배포합니다:

```powershell
cd C:\Users\malgn\Desktop\malgpt
git add -A
git commit -m "Add timeout to API requests"
git push origin main
```

### 3단계: 테스트

재배포 후:
1. **Cloudflare Pages에서 채팅 테스트**
2. **브라우저 콘솔 확인**
3. **Workers 로그 확인**

## 📋 체크리스트

- [ ] 프론트엔드 타임아웃 추가 완료
- [ ] Workers 성능 최적화 완료
- [ ] Workers 재배포
- [ ] 프론트엔드 재배포
- [ ] 테스트 완료

---

**Workers를 재배포하면 타임아웃 문제가 해결될 것입니다!**

**재배포 후 테스트해보세요!**

