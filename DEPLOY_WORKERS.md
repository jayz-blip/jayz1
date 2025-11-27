# Workers 배포 가이드

## 🚀 Workers 배포 방법

### 1단계: worker 폴더로 이동

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
```

### 2단계: 배포 실행

```powershell
npx wrangler deploy
```

## 📋 배포 과정

배포를 실행하면:

1. **코드 업로드**: Worker 코드가 Cloudflare에 업로드됩니다
2. **의존성 확인**: Python 의존성이 확인됩니다
3. **배포 완료**: Workers URL이 표시됩니다

## ✅ 예상 결과

배포가 성공하면 다음과 같은 메시지가 표시됩니다:

```
✨  Deployed to https://chatbot-api.your-subdomain.workers.dev
```

**이 URL을 복사해두세요!** 다음 단계에서 사용합니다.

## 🔍 배포 확인

배포 후 다음 명령어로 상태를 확인할 수 있습니다:

```powershell
npx wrangler deployments list
```

## ⚠️ 주의사항

1. **반드시 `worker` 폴더에서 실행**: `wrangler.toml` 파일이 있는 폴더여야 합니다.

2. **첫 배포 시**: Cloudflare 계정 인증이 필요할 수 있습니다.
   - `npx wrangler login` 실행 (이미 했다면 생략)

3. **배포 시간**: 보통 1-2분 정도 소요됩니다.

## 📋 배포 후 다음 단계

배포가 완료되면:

1. ✅ Workers URL 복사
2. 🔗 Cloudflare Pages 환경 변수 설정
   - `BACKEND_URL`: Workers URL 입력
3. 🎉 테스트

---

## 🚀 빠른 배포 명령어

```powershell
# 1. worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 2. 배포 실행
npx wrangler deploy
```

---

**지금 바로 배포하세요! 🚀**

