# D1 데이터베이스 설정 가이드

## 1단계: D1 데이터베이스 ID 확인

이미 D1을 연결했다고 하셨으니, 다음 명령어로 데이터베이스 ID를 확인하세요:

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

## 2단계: wrangler.toml 업데이트

`worker/wrangler.toml` 파일을 열고 `database_id`를 실제 ID로 변경:

```toml
[[d1_databases]]
binding = "DB"
database_name = "chatbot-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # 여기에 실제 ID 입력
```

## 3단계: 스키마 생성

```bash
cd worker
wrangler d1 execute chatbot-db --local --file=scripts/setup_d1.sql
```

## 4단계: 데이터 로드

```bash
# CSV 데이터를 SQL로 변환
python scripts/load_data.py

# 생성된 SQL 파일 확인
cat scripts/insert_data.sql

# 로컬 D1에 데이터 삽입
wrangler d1 execute chatbot-db --local --file=scripts/insert_data.sql

# 프로덕션 D1에 데이터 삽입
wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
```

## 5단계: 로컬 테스트

```bash
cd worker
npm install
wrangler dev
```

## 6단계: 배포

```bash
wrangler deploy
```

## 7단계: 프론트엔드 연결

Cloudflare Pages → Settings → Environment variables:
- `VITE_API_URL`: Workers URL (예: `https://chatbot-api.your-subdomain.workers.dev`)

또는 `functions/api/[[path]].js`에서 `BACKEND_URL` 환경 변수 설정

## 문제 해결

### D1 데이터베이스를 찾을 수 없을 때

```bash
# D1 데이터베이스 목록 확인
wrangler d1 list

# 데이터베이스가 없다면 새로 생성
wrangler d1 create chatbot-db
```

### 데이터 로드 오류

- CSV 파일 경로 확인: 프로젝트 루트에 CSV 파일이 있어야 합니다
- 파일 인코딩 확인: UTF-8로 저장되어 있어야 합니다
- SQL 파일 크기: 너무 크면 배치로 나눠서 실행

### Workers 배포 오류

- `wrangler.toml`의 `database_id` 확인
- 로그인 상태 확인: `wrangler whoami`
- 권한 확인: D1 데이터베이스에 대한 접근 권한 필요

