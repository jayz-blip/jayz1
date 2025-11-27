# D1 + Workers 배포 단계별 가이드

## 현재 상태
✅ D1 데이터베이스 ID 입력 완료

## 다음 단계

### 1단계: Wrangler CLI 설치 및 로그인

```bash
# Wrangler CLI 설치 (Node.js가 설치되어 있어야 함)
npm install -g wrangler

# Cloudflare 로그인
wrangler login
```

### 2단계: D1 스키마 생성

```bash
cd worker
wrangler d1 execute chatbot-db --local --file=scripts/setup_d1.sql
```

로컬 테스트 후 프로덕션에도 적용:
```bash
wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

### 3단계: CSV 데이터를 D1에 로드

```bash
# CSV 데이터를 SQL로 변환
python scripts/load_data.py

# 생성된 SQL 파일 확인
# scripts/insert_data.sql 파일이 생성되었는지 확인

# 프로덕션 D1에 데이터 삽입
wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
```

**주의**: 데이터가 많으면 시간이 걸릴 수 있습니다.

### 4단계: Workers 배포

```bash
cd worker
npm install
wrangler deploy
```

배포 성공 시 Workers URL이 표시됩니다:
```
✨  Deployed to https://chatbot-api.your-subdomain.workers.dev
```

### 5단계: Cloudflare Pages 환경 변수 설정

1. Cloudflare Pages 대시보드 접속
2. 프로젝트 선택 → **Settings** → **Environment variables**
3. **Add variable** 클릭
4. 다음 추가:
   - **Variable name**: `BACKEND_URL`
   - **Value**: Workers URL (예: `https://chatbot-api.your-subdomain.workers.dev`)
5. **Save** 클릭

### 6단계: 테스트

1. Cloudflare Pages URL 접속 (예: `https://jayz1.pages.dev`)
2. 채팅창에 질문 입력
3. 응답 확인

---

## 빠른 명령어 (한 번에)

```bash
# 1. Wrangler 설치 및 로그인
npm install -g wrangler
wrangler login

# 2. D1 스키마 생성
cd worker
wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql

# 3. 데이터 로드
python scripts/load_data.py
wrangler d1 execute chatbot-db --file=scripts/insert_data.sql

# 4. Workers 배포
npm install
wrangler deploy
```

---

## 문제 해결

### Wrangler가 설치되지 않을 때

Node.js가 설치되어 있는지 확인:
```bash
node --version
npm --version
```

설치되어 있지 않으면 Node.js를 먼저 설치하세요.

### D1 명령어가 작동하지 않을 때

```bash
# 로그인 확인
wrangler whoami

# 로그인 안 되어 있으면
wrangler login
```

### 데이터 로드 오류

- CSV 파일이 프로젝트 루트에 있는지 확인
- `scripts/load_data.py` 실행 시 경로 확인
- SQL 파일이 너무 크면 배치로 나눠서 실행

---

## 확인 사항

각 단계 후 확인:

- [ ] D1 스키마 생성 완료
- [ ] CSV 데이터가 SQL로 변환됨 (`scripts/insert_data.sql` 파일 생성)
- [ ] D1에 데이터 삽입 완료
- [ ] Workers 배포 성공 (URL 확인)
- [ ] Cloudflare Pages 환경 변수 설정 완료
- [ ] 테스트 성공

