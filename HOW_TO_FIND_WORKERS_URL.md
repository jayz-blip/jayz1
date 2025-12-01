# Workers URL 찾기 가이드

## 🔍 Workers URL 확인 방법

### 방법 1: Cloudflare 대시보드에서 확인 (가장 쉬움)

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com

2. **Workers & Pages 클릭**
   - 왼쪽 메뉴에서 "Workers & Pages" 선택

3. **Workers 탭 클릭**
   - 상단에 "Workers"와 "Pages" 탭이 있음
   - **"Workers"** 탭 클릭

4. **`chatbot-api` 프로젝트 클릭**
   - 프로젝트 목록에서 `chatbot-api` 찾기
   - 클릭

5. **Workers URL 확인**
   - 프로젝트 페이지 상단에 Workers URL이 표시됨
   - 예: `https://chatbot-api.your-subdomain.workers.dev`
   - **복사 아이콘** 클릭하여 복사

### 방법 2: 배포 시 표시된 URL 확인

Workers를 배포할 때 터미널에 URL이 표시됩니다:

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

**배포 성공 시 표시되는 메시지**:
```
✨  Deployed to https://chatbot-api.your-subdomain.workers.dev
```

### 방법 3: wrangler 명령어로 확인

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deployments list
```

이 명령어는 최근 배포 내역과 URL을 보여줍니다.

## 📋 Workers URL 형식

Workers URL은 다음과 같은 형식입니다:

```
https://[프로젝트명].[서브도메인].workers.dev
```

**예시**:
```
https://chatbot-api.your-subdomain.workers.dev
```

## 🔍 Workers URL이 보이지 않는 경우

### 경우 1: Workers가 배포되지 않음

**해결**: Workers 배포
```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

### 경우 2: 프로젝트 이름이 다름

**해결**: 
1. Workers 목록에서 프로젝트 찾기
2. 프로젝트 이름 확인 (`wrangler.toml`의 `name` 필드)

### 경우 3: 다른 계정에 배포됨

**해결**:
1. `npx wrangler whoami`로 현재 로그인된 계정 확인
2. 올바른 계정으로 로그인

## 🚀 빠른 확인 방법

**가장 간단한 방법**:
1. Cloudflare 대시보드 → Workers & Pages → Workers
2. `chatbot-api` 프로젝트 클릭
3. 상단에 표시된 URL 복사

---

**Workers URL을 찾았으면 Cloudflare Pages 환경 변수에 설정하세요!**

