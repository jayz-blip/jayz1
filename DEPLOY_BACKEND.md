# 백엔드 배포 가이드

현재 백엔드는 Python FastAPI를 사용하므로, Cloudflare Workers가 아닌 Python을 지원하는 호스팅 서비스를 사용해야 합니다.

## 옵션 1: Railway (권장) ⭐

가장 간단하고 빠른 배포 방법입니다.

### 배포 단계

1. **Railway 계정 생성**
   - https://railway.app 접속
   - GitHub로 로그인

2. **프로젝트 생성**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 레포지토리 선택

3. **서비스 설정**
   - Root Directory: `/backend` 설정
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

4. **환경 변수 설정**
   - Settings → Variables에서 추가:
     - `OPENAI_API_KEY`: (선택사항) OpenAI API 키

5. **CSV 파일 업로드**
   - Railway는 파일 시스템이 영구적이므로, CSV 파일을 프로젝트에 포함시키거나
   - Railway의 Volume 기능 사용

6. **도메인 설정**
   - Settings → Networking → Generate Domain
   - 생성된 URL을 프론트엔드 환경 변수에 설정

### 프론트엔드 연결

Cloudflare Pages → Settings → Environment variables:
- `VITE_API_URL`: Railway에서 생성된 도메인 URL

---

## 옵션 2: Render

### 배포 단계

1. **Render 계정 생성**
   - https://render.com 접속
   - GitHub로 로그인

2. **Web Service 생성**
   - "New" → "Web Service"
   - GitHub 레포지토리 연결
   - 설정:
     - **Name**: `company-chatbot-api`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`

3. **환경 변수 설정**
   - Environment → Environment Variables:
     - `OPENAI_API_KEY`: (선택사항)

4. **도메인 확인**
   - 배포 완료 후 생성된 URL 확인

---

## 옵션 3: Fly.io

### 배포 단계

1. **Fly.io CLI 설치**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **로그인**
   ```bash
   fly auth login
   ```

3. **프로젝트 초기화**
   ```bash
   cd backend
   fly launch
   ```

4. **배포**
   ```bash
   fly deploy
   ```

---

## 옵션 4: PythonAnywhere (간단한 옵션)

무료 Python 호스팅 서비스입니다.

1. https://www.pythonanywhere.com 가입
2. Files 탭에서 파일 업로드
3. Web 앱 생성 및 설정

---

## 중요 사항

### CSV 파일 처리

백엔드는 CSV 파일을 읽어야 하므로:

1. **방법 1**: CSV 파일을 Git에 포함 (현재 상태)
2. **방법 2**: 호스팅 서비스의 파일 시스템 사용
3. **방법 3**: 클라우드 스토리지 (S3, Cloudflare R2 등) 사용

### 벡터 DB (ChromaDB)

ChromaDB는 로컬 파일 시스템을 사용하므로:
- 호스팅 서비스의 영구 스토리지 필요
- 또는 클라우드 벡터 DB (Pinecone, Weaviate 등)로 마이그레이션 고려

### 메모리 요구사항

- Sentence Transformers 모델 로딩: ~500MB
- ChromaDB: 데이터 크기에 따라 다름
- 최소 1GB RAM 권장

---

## 프론트엔드 연결

백엔드 배포 후:

1. Cloudflare Pages → Settings → Environment variables
2. `VITE_API_URL` 추가: 백엔드 URL (예: `https://your-api.railway.app`)

또는 `functions/api/[[path]].js`에서 `BACKEND_URL` 환경 변수 설정

