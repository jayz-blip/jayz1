# Workers 재배포 가이드

## 🚀 Workers 재배포 방법

### 1단계: PowerShell 열기

1. **PowerShell 또는 CMD 창 열기**
2. **프로젝트 루트로 이동** (필요시)

### 2단계: worker 폴더로 이동

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
```

### 3단계: Workers 재배포

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
✨  Deployed to https://chatbot-api.jayz-407.workers.dev
```

**이 URL을 복사해두세요!**

## ⚠️ 주의사항

1. **반드시 `worker` 폴더에서 실행**: `wrangler.toml` 파일이 있는 폴더여야 합니다.

2. **배포 시간**: 보통 1-2분 정도 소요됩니다.

3. **로그인 확인**: 처음 배포하는 경우 `npx wrangler login`이 필요할 수 있습니다.

## 🔍 배포 확인

배포 후 다음 명령어로 상태를 확인할 수 있습니다:

```powershell
npx wrangler deployments list
```

## 📋 전체 명령어 순서

```powershell
# 1. worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 2. 배포 실행
npx wrangler deploy

# 3. 배포 완료 대기 (1-2분)

# 4. Workers URL 테스트
# 브라우저에서: https://chatbot-api.jayz-407.workers.dev
```

## 🆘 문제 해결

### "wrangler not found" 오류

**해결**:
```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npm install
npx wrangler deploy
```

### "not logged in" 오류

**해결**:
```powershell
npx wrangler login
```
브라우저가 열리면 Cloudflare 계정으로 로그인

### 배포 실패

**확인**:
- `wrangler.toml` 파일이 올바른지 확인
- `src/worker.py` 파일이 존재하는지 확인
- 오류 메시지 확인

---

**지금 바로 재배포하세요! 🚀**

