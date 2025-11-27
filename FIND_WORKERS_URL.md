# Workers URL 찾기 가이드

## 🔍 Workers URL이란?

Workers URL은 Cloudflare Workers에 배포된 백엔드 API의 주소입니다.

**형식**: `https://chatbot-api.your-subdomain.workers.dev`

이 URL을 사용하여:
- 프론트엔드에서 백엔드 API를 호출합니다
- Cloudflare Pages 환경 변수에 설정합니다

## 📍 Workers URL 찾는 방법

### 방법 1: 배포 시 자동 표시 (가장 쉬움)

`npx wrangler deploy` 명령어를 실행하면 배포 완료 후 자동으로 URL이 표시됩니다:

```
✨  Deployed to https://chatbot-api.your-subdomain.workers.dev
```

**이 메시지에서 URL을 복사하세요!**

### 방법 2: Cloudflare 대시보드에서 확인

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com

2. **Workers & Pages 클릭**
   - 왼쪽 메뉴에서 "Workers & Pages" 선택

3. **Workers 프로젝트 선택**
   - `chatbot-api` 프로젝트 클릭

4. **URL 확인**
   - 상단에 Workers URL이 표시됩니다
   - 예: `https://chatbot-api.your-subdomain.workers.dev`

### 방법 3: wrangler 명령어로 확인

```powershell
# worker 폴더에서
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deployments list
```

이 명령어는 최근 배포 내역과 URL을 보여줍니다.

## 🚀 아직 배포하지 않았다면

Workers를 배포하면 자동으로 URL이 생성됩니다:

```powershell
# worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 배포 실행
npx wrangler deploy
```

배포가 완료되면 다음과 같은 메시지가 표시됩니다:

```
✨  Deployed to https://chatbot-api.your-subdomain.workers.dev
```

**이 URL을 복사해두세요!**

## 📋 Workers URL 사용 방법

Workers URL을 받으면:

1. **Cloudflare Pages 환경 변수 설정**
   - Cloudflare Pages → Settings → Environment variables
   - `BACKEND_URL`: Workers URL 입력

2. **테스트**
   - Workers URL에 직접 접속하여 확인
   - 예: `https://chatbot-api.your-subdomain.workers.dev`

## ⚠️ 주의사항

- **Workers URL은 배포 후에만 생성됩니다**
- **각 Workers마다 고유한 URL이 생성됩니다**
- **URL 형식**: `https://[프로젝트명].[서브도메인].workers.dev`

---

## 🔍 빠른 확인 방법

```powershell
# 1. worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 2. 배포 상태 확인
npx wrangler deployments list
```

또는 Cloudflare 대시보드에서 직접 확인하세요!

---

**Workers를 배포하면 자동으로 URL이 표시됩니다! 🚀**

