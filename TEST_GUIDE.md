# 챗봇 테스트 가이드

## 테스트 방법

### 방법 1: 로컬에서 전체 테스트 (권장) ⭐

가장 빠르고 확실한 방법입니다.

#### 1단계: 백엔드 실행

```bash
# 백엔드 폴더로 이동
cd backend

# 가상환경 생성 (처음 한 번만)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 백엔드 실행
python main.py
```

백엔드가 `http://localhost:8000`에서 실행됩니다.

**중요**: 처음 실행 시 CSV 데이터를 로드하고 벡터화하므로 시간이 걸릴 수 있습니다 (몇 분 소요).

#### 2단계: 프론트엔드 실행 (새 터미널)

```bash
# 프로젝트 루트로 이동
cd ..

# 의존성 설치 (처음 한 번만)
npm install

# 프론트엔드 실행
npm run dev
```

프론트엔드가 `http://localhost:3000`에서 실행됩니다.

#### 3단계: 테스트

1. 브라우저에서 `http://localhost:3000` 접속
2. 채팅창에 질문 입력
3. 예: "담당자 변경 방법 알려줘", "SPF 레코드 설정 방법", "주문 통계 관련 문의"

---

### 방법 2: Cloudflare Pages에서 테스트

프론트엔드는 배포되었지만, 백엔드가 필요합니다.

#### 옵션 A: 백엔드를 Railway/Render에 배포

1. **백엔드 배포** (`DEPLOY_BACKEND.md` 참고)
   - Railway 또는 Render에 백엔드 배포
   - 배포 후 URL 확인 (예: `https://your-api.railway.app`)

2. **Cloudflare Pages 환경 변수 설정**
   - Cloudflare Pages → Settings → Environment variables
   - `BACKEND_URL`: 백엔드 URL 입력 (예: `https://your-api.railway.app`)

3. **테스트**
   - Cloudflare Pages URL 접속 (예: `https://jayz1.pages.dev`)
   - 채팅 테스트

#### 옵션 B: D1 + Cloudflare Workers 사용

1. **D1 데이터베이스 설정** (`DEPLOY_D1_SETUP.md` 참고)
   - D1 데이터베이스 ID 확인
   - `worker/wrangler.toml`에 database_id 입력
   - 데이터 로드

2. **Workers 배포**
   ```bash
   cd worker
   npm install
   wrangler deploy
   ```

3. **Cloudflare Pages 환경 변수 설정**
   - `BACKEND_URL`: Workers URL (예: `https://chatbot-api.your-subdomain.workers.dev`)

---

## 테스트 질문 예시

CSV 데이터에 포함된 내용을 기반으로 한 질문:

1. **담당자 관련**
   - "담당자 변경 방법 알려줘"
   - "담당자 추가는 어떻게 하나요?"

2. **SPF 레코드 관련**
   - "SPF 레코드 설정 방법"
   - "도메인 SPF 레코드 추가 요청"

3. **주문/결제 관련**
   - "주문 통계 관련 문의"
   - "일별 주문 통계는 어떻게 집계되나요?"

4. **SMS 관련**
   - "SMS 발송 오류"
   - "학습독려 SMS 관련 문의"

---

## 문제 해결

### 백엔드가 응답하지 않을 때

1. **백엔드 로그 확인**
   - 백엔드 터미널에서 오류 메시지 확인
   - 데이터 로딩이 완료되었는지 확인

2. **포트 확인**
   - 백엔드가 `http://localhost:8000`에서 실행 중인지 확인
   - 프론트엔드가 올바른 URL을 사용하는지 확인

### 프론트엔드에서 CORS 오류

- 백엔드의 CORS 설정 확인 (`backend/main.py`)
- 이미 `allow_origins=["*"]`로 설정되어 있음

### 데이터가 로드되지 않음

- CSV 파일이 프로젝트 루트에 있는지 확인
- 백엔드 로그에서 데이터 로딩 메시지 확인
- `chroma_db` 폴더가 생성되었는지 확인

---

## 빠른 테스트 (로컬)

가장 빠른 방법:

```bash
# 터미널 1: 백엔드
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py

# 터미널 2: 프론트엔드
npm install
npm run dev
```

그 다음 브라우저에서 `http://localhost:3000` 접속!

