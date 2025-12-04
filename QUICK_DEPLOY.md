# 빠른 배포 체크리스트 ⚡

## ✅ 완료된 작업

- [x] 코드 변경사항 커밋 및 푸시 완료
- [x] 배포 가이드 문서 작성 (`DEPLOY_GUIDE.md`)

## 🚀 다음 단계

### 1. Cloudflare Pages 배포 (프론트엔드)

1. **Cloudflare 대시보드 접속**: https://dash.cloudflare.com/
2. **Pages** → **Create a project** → **Connect to Git**
3. **저장소 선택**: `jayz-blip/jayz1`
4. **빌드 설정**:
   - Build command: `npm install && npm run build`
   - Build output directory: `dist`
5. **환경 변수** (백엔드 배포 후 설정):
   - `BACKEND_URL`: 백엔드 URL 입력
6. **Deploy** 클릭

### 2. 백엔드 배포 (Railway 권장)

1. **Railway 접속**: https://railway.app/
2. **New Project** → **Deploy from GitHub repo**
3. **저장소 선택**: `jayz-blip/jayz1`
4. **서비스 설정**:
   - Root Directory: `backend`
   - Start Command: `python main.py`
5. **환경 변수 설정**:
   - `OPENAI_API_KEY`: 실제 API 키 입력
   - `PORT`: `8000`
6. 배포 완료 후 URL 복사

### 3. 연결 설정

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **BACKEND_URL** 업데이트: Railway에서 받은 URL 입력
3. **재배포**: Deployments → Retry deployment

## 📝 중요 사항

- ⚠️ **OpenAI API 키**: `DEPLOY_GUIDE.md`에 실제 키가 포함되어 있지 않습니다. Railway/Render 대시보드에서 직접 입력하세요.
- 📁 **CSV 파일**: 프로젝트 루트에 있어야 합니다 (이미 포함됨)
- 🔗 **BACKEND_URL**: URL 끝에 `/`를 붙이지 마세요

## 🎯 배포 후 테스트

1. Cloudflare Pages URL 접속
2. 챗봇 인터페이스 확인
3. 테스트 질문:
   - "대한손해사정법인협회 최근에 무슨 문의가 있었냐"
   - "국제언어대학원대학교 근황 알려줘"

## 📚 자세한 가이드

전체 배포 가이드는 **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)**를 참고하세요.

