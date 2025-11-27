# Cloudflare Pages 빌드 오류 해결

## 문제

Cloudflare Pages가 자동으로 `requirements.txt`를 감지해서 Python을 설치하려고 하며, pandas와 Python 3.13 호환성 문제로 빌드가 실패합니다.

## 해결 방법

### 방법 1: Cloudflare Pages 대시보드에서 빌드 설정 (권장)

1. **Cloudflare Pages 대시보드** 접속
2. 프로젝트 선택 → **Settings** → **Builds & deployments**
3. 다음 설정 확인/수정:
   - **Build command**: `npm install && npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `/` (기본값)
   - **Python version**: **설정하지 않음** (비워둠)

### 방법 2: 환경 변수 설정

Cloudflare Pages → Settings → Environment variables:
- `SKIP_PYTHON`: `true` 추가

### 방법 3: 빌드 스크립트 사용

`build.sh` 파일을 사용하도록 빌드 명령어 변경:
- **Build command**: `bash build.sh`

## 중요 사항

- `requirements.txt`는 `backend/` 폴더에 있어야 합니다 (프론트엔드 빌드와 분리)
- 프론트엔드 빌드에는 Python이 필요하지 않습니다
- 백엔드는 별도로 배포해야 합니다 (Railway, Render 등)

## 확인

빌드 로그에서 다음이 보이면 안 됩니다:
- ❌ `Installing project dependencies: pip install -r requirements.txt`
- ❌ `Detected the following tools from environment: ... python@...`

다음만 보여야 합니다:
- ✅ `Installing project dependencies: npm install`
- ✅ `added X packages`

