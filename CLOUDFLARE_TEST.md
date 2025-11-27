# Cloudflare 환경에서 테스트하기

## 현재 상황

- ✅ 프론트엔드: Cloudflare Pages에 배포됨 (jayz1.pages.dev)
- ✅ D1 데이터베이스: 연결 완료
- ⏳ 백엔드: Cloudflare Workers Python으로 배포 필요

## 테스트 방법

### 방법 1: Cloudflare Workers Python + D1 사용 (권장) ⭐

D1을 이미 연결했다고 하셨으니 이 방법을 사용하세요.

#### 1단계: D1 데이터베이스 ID 확인

```bash
wrangler d1 list
```

출력 예시:
```
┌──────────────────────────────────────┬──────────────┐
│ id                                   │ name         │
├──────────────────────────────────────┼──────────────┤
│ xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx │ chatbot-db   │
└──────────────────────────────────────┴──────────────┘
```

#### 2단계: wrangler.toml 업데이트

`worker/wrangler.toml` 파일을 열고 `database_id`를 실제 ID로 변경:

```toml
[[d1_databases]]
binding = "DB"
database_name = "chatbot-db"
database_id = "실제-D1-데이터베이스-ID"  # 여기에 실제 ID 입력
```

#### 3단계: D1 스키마 생성

```bash
cd worker
wrangler d1 execute chatbot-db --local --file=scripts/setup_d1.sql
```

#### 4단계: 데이터 로드

```bash
# CSV 데이터를 SQL로 변환
python scripts/load_data.py

# 로컬 D1에 데이터 삽입 (테스트용)
wrangler d1 execute chatbot-db --local --file=scripts/insert_data.sql

# 프로덕션 D1에 데이터 삽입
wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
```

#### 5단계: Workers 배포

```bash
cd worker
npm install
wrangler deploy
```

배포 후 Workers URL이 표시됩니다:
```
✨  Deployed to https://chatbot-api.your-subdomain.workers.dev
```

#### 6단계: Cloudflare Pages 환경 변수 설정

1. Cloudflare Pages 대시보드 접속
2. 프로젝트 선택 → **Settings** → **Environment variables**
3. 다음 환경 변수 추가:
   - `BACKEND_URL`: Workers URL (예: `https://chatbot-api.your-subdomain.workers.dev`)

#### 7단계: 테스트

1. Cloudflare Pages URL 접속 (예: `https://jayz1.pages.dev`)
2. 채팅창에 질문 입력
3. 응답 확인

---

### 방법 2: Railway/Render에 백엔드 배포 후 프록시 사용

현재 Python FastAPI 코드를 그대로 사용하는 방법입니다.

#### 1단계: Railway에 백엔드 배포

1. https://railway.app 접속
2. "New Project" → "Deploy from GitHub repo"
3. 레포지토리 선택
4. 설정:
   - **Root Directory**: `backend`
   - **Start Command**: `python main.py`
5. 환경 변수 설정 (선택사항):
   - `OPENAI_API_KEY`: OpenAI API 키

#### 2단계: 배포 URL 확인

Railway에서 생성된 URL 확인 (예: `https://your-api.railway.app`)

#### 3단계: Cloudflare Pages 환경 변수 설정

1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL`: Railway URL 입력 (예: `https://your-api.railway.app`)

#### 4단계: 테스트

1. Cloudflare Pages URL 접속
2. 채팅 테스트

---

## 빠른 체크리스트

### Cloudflare Workers + D1 방법

- [ ] D1 데이터베이스 ID 확인 (`wrangler d1 list`)
- [ ] `worker/wrangler.toml`에 database_id 입력
- [ ] D1 스키마 생성
- [ ] CSV 데이터를 D1에 로드
- [ ] Workers 배포 (`wrangler deploy`)
- [ ] Cloudflare Pages에 `BACKEND_URL` 환경 변수 설정
- [ ] 테스트

### Railway 방법

- [ ] Railway에 백엔드 배포
- [ ] 배포 URL 확인
- [ ] Cloudflare Pages에 `BACKEND_URL` 환경 변수 설정
- [ ] 테스트

---

## 문제 해결

### Workers 배포 오류

```bash
# 로그인 확인
wrangler whoami

# 로그인 안 되어 있으면
wrangler login
```

### D1 데이터 로드 오류

- CSV 파일이 프로젝트 루트에 있는지 확인
- `scripts/load_data.py` 실행 시 경로 확인

### 프론트엔드에서 연결 오류

1. 브라우저 콘솔(F12) 확인
2. `BACKEND_URL` 환경 변수가 올바른지 확인
3. Workers/Railway URL이 정상 작동하는지 확인

---

## 추천 방법

**D1을 이미 연결했다면**: Cloudflare Workers Python + D1 방법 사용
- 모든 것이 Cloudflare에서 실행
- 빠르고 간단

**빠르게 테스트하고 싶다면**: Railway 방법 사용
- 현재 코드 그대로 사용
- 설정이 간단

어떤 방법을 사용하시겠어요?

