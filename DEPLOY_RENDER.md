# Render.com 백엔드 배포 가이드 (무료) 🆓

## Render.com 무료 플랜

Render.com은 무료 플랜을 제공하며 Python FastAPI 배포를 지원합니다.

## 1단계: Render.com 가입 및 로그인

1. **Render.com 접속**: https://render.com/
2. **Sign Up** 클릭
3. **GitHub로 로그인** 선택 (권장)
4. GitHub 계정으로 인증

## 2단계: 새 Web Service 생성

1. **Dashboard**에서 **New +** 버튼 클릭
2. **Web Service** 선택
3. **Connect account** 클릭 (GitHub 연결)
4. **Connect** 버튼으로 저장소 연결 승인

## 3단계: 저장소 선택 및 설정

1. **Repository**: `jayz-blip/jayz1` 선택
2. **Branch**: `main` (기본값)
3. **Name**: `malgpt-api` 또는 원하는 이름
4. **Region**: `Singapore` 또는 가까운 지역 선택
5. **Root Directory**: `backend` 입력 ⚠️ **중요**
6. **Environment**: `Python 3` 선택
7. **Build Command**: `pip install -r requirements.txt`
8. **Start Command**: `python main.py`

## 4단계: 환경 변수 설정

**Environment Variables** 섹션에서:

1. **Add Environment Variable** 클릭
2. 다음 변수 추가:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: 실제 OpenAI API 키 입력
3. **Add Environment Variable** 다시 클릭
4. 다음 변수 추가:
   - **Key**: `PORT`
   - **Value**: `8000`

## 5단계: 배포

1. **Create Web Service** 클릭
2. 배포 시작 (약 5-10분 소요)
3. 배포 완료 후 **URL 확인** (예: `https://malgpt-api.onrender.com`)

## 6단계: Cloudflare Pages 연결

1. **Cloudflare Pages** → `jayznew` 프로젝트
2. **Settings** → **Environment variables**
3. **Add variable** 클릭
4. **Variable name**: `BACKEND_URL`
5. **Value**: Render에서 받은 URL 입력 (예: `https://malgpt-api.onrender.com`)
6. **Save** 클릭
7. **Deployments** → 최신 배포 → **Retry deployment**

## ⚠️ Render 무료 플랜 제한사항

- **Sleep Mode**: 15분간 요청이 없으면 자동으로 sleep 모드로 전환
- 첫 요청 시 약 30초 정도 깨어나는 시간 필요
- **월 750시간 무료** (충분함)

## 🔧 문제 해결

### 배포 실패 시

1. **Logs** 탭에서 오류 확인
2. **Root Directory**가 `backend`로 설정되었는지 확인
3. **Build Command**가 올바른지 확인

### CSV 파일 경로 오류

- CSV 파일은 프로젝트 루트에 있어야 합니다
- Render는 자동으로 GitHub에서 파일을 가져옵니다

## ✅ 배포 확인

배포 완료 후:

```bash
curl https://your-render-url.onrender.com/
```

응답이 오면 정상 작동 중입니다!

