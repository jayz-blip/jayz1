# Cloudflare Pages 배포 가이드

## 문제 해결: MIME Type 오류

이 가이드는 Cloudflare Pages에서 발생하는 "Expected a JavaScript-or-Wasm module script but the server responded with a MIME type of "text/jsx"" 오류를 해결합니다.

## 해결 방법

### 1. 빌드 설정 확인

Cloudflare Pages 대시보드에서:
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Root directory**: `/` (프로젝트 루트)

### 2. 환경 변수 설정 (선택사항)

Cloudflare Pages → Settings → Environment variables:
- `NODE_VERSION`: `18` 또는 `20`
- `BACKEND_URL`: 백엔드 API URL (예: `https://your-backend.workers.dev`)

### 3. 빌드 및 배포

```bash
# 로컬에서 빌드 테스트
npm run build

# 빌드 결과 확인
ls -la dist/
```

### 4. API 프록시 설정

백엔드 API가 별도로 호스팅되는 경우, Cloudflare Pages Functions를 사용하여 프록시를 설정할 수 있습니다.

#### 방법 1: Cloudflare Pages Functions (권장)

`functions/api/[[path]].js` 파일이 자동으로 `/api/*` 경로를 처리합니다.

#### 방법 2: 환경 변수로 API URL 설정

프론트엔드 코드에서 환경 변수 사용:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### 5. MIME Type 헤더

`public/_headers` 파일이 자동으로 적용되어 올바른 MIME type을 설정합니다.

## 배포 후 확인사항

1. 브라우저 개발자 도구 → Network 탭에서 JavaScript 파일이 `application/javascript` MIME type으로 로드되는지 확인
2. Console에서 오류가 없는지 확인
3. API 요청이 정상적으로 작동하는지 확인

## 문제가 계속 발생하는 경우

1. **캐시 삭제**: Cloudflare 대시보드에서 캐시 삭제
2. **빌드 로그 확인**: Cloudflare Pages → Deployments → 최신 배포의 빌드 로그 확인
3. **로컬 빌드 테스트**: `npm run build && npm run preview`로 로컬에서 테스트

## 백엔드 배포

백엔드는 별도로 배포해야 합니다:

### 옵션 1: 다른 호스팅 서비스
- Railway, Render, Fly.io, Heroku 등 사용
- 환경 변수에 `BACKEND_URL` 설정

### 옵션 2: Cloudflare Workers (별도 설정 필요)
- 백엔드를 Workers로 배포하려면 별도 프로젝트로 설정

## 중요 사항

- `wrangler.toml` 파일은 Cloudflare Pages에서 사용하지 않습니다 (Workers 전용)
- Functions 파일명은 `[[path]].js` 형식 (이중 대괄호)을 사용해야 합니다
- 빌드 명령어가 설정되어 있어야 합니다: `npm run build`

