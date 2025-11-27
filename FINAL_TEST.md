# 최종 테스트 가이드 🎉

## ✅ 완료된 작업

1. ✅ D1 스키마 생성 (로컬 및 원격)
2. ✅ CSV 데이터 로드 (31,251개 행)
3. ✅ Workers 배포
4. ✅ 환경 변수 설정
   - ✅ Workers: `OPENAI_API_KEY`
   - ✅ Pages: `BACKEND_URL`

## 🧪 테스트 방법

### 1단계: Workers API 테스트

Workers URL에 직접 접속하여 API가 정상 작동하는지 확인:

```powershell
# 브라우저에서 Workers URL 접속
# 예: https://chatbot-api.your-subdomain.workers.dev
```

**예상 결과**:
```json
{
  "message": "사내용 채팅 AI API",
  "status": "running"
}
```

### 2단계: Cloudflare Pages에서 테스트

1. **Cloudflare Pages URL 접속**
   - 예: `https://jayz1.pages.dev`

2. **채팅창에 질문 입력**
   - 예: "안녕하세요"
   - 예: "PPM에 대해 알려주세요"
   - 예: "고객 문의 처리 방법"

3. **응답 확인**
   - AI가 CSV 데이터를 기반으로 답변하는지 확인
   - 응답이 정상적으로 표시되는지 확인

### 3단계: 브라우저 개발자 도구 확인

1. **F12 키를 눌러 개발자 도구 열기**
2. **Console 탭 확인**
   - 오류 메시지가 없는지 확인
3. **Network 탭 확인**
   - API 요청이 정상적으로 전송되는지 확인
   - 응답 상태 코드가 200인지 확인

## 🔍 문제 해결

### 문제 1: "데이터가 로드되지 않았습니다" 오류

**원인**: D1 데이터베이스에 데이터가 없거나 연결 문제

**해결**:
```powershell
# 데이터 확인
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler d1 execute chatbot-db --remote --command="SELECT COUNT(*) FROM documents;"
```

### 문제 2: "CORS 오류" 또는 "연결 오류"

**원인**: `BACKEND_URL` 환경 변수가 잘못 설정되었거나 Workers URL이 잘못됨

**해결**:
1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL` 확인 및 수정
3. 재배포

### 문제 3: "임베딩 생성 오류"

**원인**: Cloudflare AI Workers 바인딩 문제

**해결**:
1. `wrangler.toml`에서 AI 바인딩 확인
2. Workers 재배포

### 문제 4: 응답이 느림

**원인**: 데이터가 많거나 임베딩 계산 시간

**해결**: 정상적인 현상입니다. 첫 요청은 시간이 걸릴 수 있습니다.

## 📋 체크리스트

- [x] D1 스키마 생성
- [x] 데이터 로드
- [x] Workers 배포
- [x] 환경 변수 설정
- [ ] Workers API 테스트
- [ ] Cloudflare Pages 테스트
- [ ] 채팅 기능 테스트

## 🎯 예상 동작

1. **사용자가 질문 입력**
2. **프론트엔드가 `/api/chat`으로 요청 전송**
3. **Cloudflare Pages Functions가 Workers로 프록시**
4. **Workers가 D1에서 관련 데이터 검색**
5. **Cloudflare AI Workers로 임베딩 생성 및 유사도 계산**
6. **OpenAI API로 응답 생성 (선택사항)**
7. **사용자에게 응답 표시**

## 🚀 다음 단계

모든 테스트가 성공하면:

1. ✅ **배포 완료!**
2. 📊 **사용량 모니터링**
   - Cloudflare 대시보드에서 Workers 사용량 확인
   - D1 데이터베이스 사용량 확인
3. 🔧 **최적화** (필요시)
   - 응답 속도 개선
   - 데이터 추가
   - UI 개선

---

## 🎉 축하합니다!

모든 설정이 완료되었습니다! 이제 채팅 AI를 사용할 수 있습니다.

**테스트를 진행하고 문제가 있으면 알려주세요!**

