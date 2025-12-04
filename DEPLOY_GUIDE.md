# 맑쥐피티 배포 가이드 🚀

## 📋 개요

맑쥐피티는 고객사별 문의 내역을 체크하는 사내 챗봇입니다.
- **프론트엔드**: Cloudflare Pages에 배포
- **백엔드**: Railway 또는 Render에 배포 (Python FastAPI)

## 🎯 배포 구조

```
사용자 → Cloudflare Pages (프론트엔드)
         ↓
    Cloudflare Functions (API 프록시)
         ↓
    Railway/Render (백엔드 API)
```

## 1️⃣ 깃허브 저장소 확인

✅ 이미 깃허브에 푸시 완료: `jayz-blip/jayz1`

## 2️⃣ Cloudflare Pages 배포 (프론트엔드)

### 단계 1: 프로젝트 생성

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com/
   - 로그인

2. **Pages 프로젝트 생성**
   - 왼쪽 메뉴: **Workers & Pages** → **Pages**
   - **Create a project** 클릭
   - **Connect to Git** 선택
   - GitHub 저장소 선택: `jayz-blip/jayz1`
   - **Begin setup** 클릭

### 단계 2: 빌드 설정

다음 설정을 입력:

- **Project name**: `malgpt` 또는 원하는 이름 (기존 프로젝트와 무관하게 새로 생성 가능)
- **Production branch**: `main`
- **Build command**: `npm install && npm run build`
- **Build output directory**: `dist`
- **Root directory**: `/` (기본값)

### 단계 3: 환경 변수 설정

**Settings** → **Environment variables**에서 추가:

- `NODE_VERSION`: `18`
- `BACKEND_URL`: 백엔드 배포 후 URL 입력 (예: `https://malgpt-api.railway.app`)

### 단계 4: 배포

- **Save and Deploy** 클릭
- 배포 완료 대기 (약 2-3분)
- 배포 완료 후 URL 확인 (예: `https://malgpt.pages.dev`)

## 3️⃣ 백엔드 배포

### 옵션 A: Render.com 배포 (무료 플랜 제공) ⭐ 권장

**자세한 가이드는 [DEPLOY_RENDER.md](DEPLOY_RENDER.md)를 참고하세요.**

간단 요약:
1. **Render.com 접속**: https://render.com/
2. **New +** → **Web Service**
3. **GitHub 저장소 연결**: `jayz-blip/jayz1`
4. **설정**:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. **환경 변수**:
   - `OPENAI_API_KEY`: 실제 API 키 입력
   - `PORT`: `8000`
6. **Create Web Service** 클릭

### 옵션 B: Railway 배포 (유료 플랜 필요할 수 있음)

1. **Render 접속**
   - https://render.com/
   - GitHub로 로그인

2. **새 Web Service 생성**
   - **New** → **Web Service**
   - 저장소 연결: `jayz-blip/jayz1`

3. **서비스 설정**
   - **Name**: `malgpt-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

4. **환경 변수 설정**
   - **Environment** 탭에서 추가:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - ⚠️ **중요**: 실제 OpenAI API 키는 Render 대시보드에서 직접 입력하세요.

5. **배포 확인**
   - 배포 완료 후 URL 확인

## 4️⃣ 연결 설정

### Cloudflare Pages 환경 변수 업데이트

1. **Cloudflare Pages** → 프로젝트 선택
2. **Settings** → **Environment variables**
3. **BACKEND_URL** 업데이트:
   - Railway: `https://your-project.railway.app`
   - Render: `https://your-project.onrender.com`

4. **재배포**
   - **Deployments** → 최신 배포 → **Retry deployment**

## 5️⃣ 데이터 파일 확인

백엔드 배포 시 다음 CSV 파일이 필요합니다:

- `20251125_PPM학습용데이터_원글.csv`
- `20251125_PPM학습용데이터_댓글.csv`

이 파일들은 프로젝트 루트에 있어야 하며, 백엔드가 자동으로 로드합니다.

## 6️⃣ 테스트

### 프론트엔드 테스트

1. Cloudflare Pages URL 접속
2. 챗봇 인터페이스 확인
3. 테스트 질문:
   - "대한손해사정법인협회 최근에 무슨 문의가 있었냐"
   - "국제언어대학원대학교 근황 알려줘"

### 백엔드 테스트

```bash
curl -X POST https://your-backend-url/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "대한손해사정법인협회 최근에 무슨 문의가 있었냐"}'
```

## 🔧 문제 해결

### 프론트엔드가 백엔드에 연결되지 않는 경우

1. **Cloudflare Pages 환경 변수 확인**
   - `BACKEND_URL`이 올바르게 설정되었는지 확인
   - URL 끝에 `/`가 없어야 함

2. **CORS 오류 확인**
   - 백엔드에서 CORS 설정 확인 (`backend/main.py`)
   - Cloudflare Functions 프록시 확인 (`functions/api/[[path]].js`)

3. **네트워크 오류 확인**
   - 브라우저 개발자 도구 → Network 탭
   - API 요청 상태 확인

### 백엔드가 데이터를 로드하지 않는 경우

1. **CSV 파일 경로 확인**
   - 파일이 프로젝트 루트에 있는지 확인
   - Railway/Render에서 파일 경로 확인

2. **로그 확인**
   - Railway/Render 대시보드에서 로그 확인
   - 데이터 로딩 오류 메시지 확인

## 📝 체크리스트

### 깃허브
- [x] 코드 커밋 및 푸시 완료
- [x] 저장소 연결 확인

### Cloudflare Pages
- [ ] 프로젝트 생성
- [ ] 빌드 설정 완료
- [ ] 환경 변수 설정 (`BACKEND_URL`)
- [ ] 배포 완료
- [ ] URL 확인

### 백엔드 (Railway/Render)
- [ ] 프로젝트 생성
- [ ] 서비스 설정 완료
- [ ] 환경 변수 설정 (`OPENAI_API_KEY`)
- [ ] 배포 완료
- [ ] URL 확인
- [ ] API 테스트 완료

### 연결
- [ ] Cloudflare Pages `BACKEND_URL` 업데이트
- [ ] 재배포 완료
- [ ] 전체 시스템 테스트 완료

## 🎉 배포 완료!

모든 설정이 완료되면:
- 프론트엔드: `https://your-project.pages.dev`
- 백엔드: `https://your-api.railway.app` (또는 Render)

챗봇이 정상 작동하는지 테스트해보세요!

