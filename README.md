# 맑쥐피티 🤖💬

맑은소프트 사내용 고객사 문의 관리 챗봇입니다.
고객사별 최근 문의 내역과 답변 현황을 간편하게 확인할 수 있습니다.

CSV 데이터를 학습한 RAG(Retrieval Augmented Generation) 기반 채팅 AI 시스템입니다.

## 주요 기능

- 🏢 **고객사별 근황 체크**: 고객사명을 입력하면 최근 문의 내역과 답변 현황을 요약해서 제공
- 📚 CSV 파일 기반 지식 베이스 구축
- 🔍 의미 기반 검색 (Semantic Search)
- 💬 자연스러운 대화형 인터페이스
- 🎨 깔끔하고 귀여운 UI 디자인
- 🔄 실시간 데이터 재로드 지원
- 🤖 OpenAI GPT 연동으로 더 자연스러운 요약 제공

## 기술 스택

### 백엔드
- FastAPI: RESTful API 서버
- ChromaDB: 벡터 데이터베이스
- Sentence Transformers: 다국어 임베딩 모델
- OpenAI API (선택사항): GPT 모델 연동

### 프론트엔드
- React: UI 프레임워크
- Vite: 빌드 도구
- Axios: HTTP 클라이언트

## 설치 및 실행

### 1. 백엔드 설정

```bash
# Python 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (선택사항 - OpenAI 사용 시)
# backend/.env 파일 생성 후:
# OPENAI_API_KEY=your_api_key_here
```

### 2. 프론트엔드 설정

```bash
# 의존성 설치
npm install
```

### 3. 실행

**터미널 1 - 백엔드:**
```bash
cd backend
python main.py
```

**터미널 2 - 프론트엔드:**
```bash
npm run dev
```

브라우저에서 `http://localhost:3000` 접속

## 데이터 구조

프로젝트 루트에 다음 CSV 파일이 있어야 합니다:
- `20251125_PPM학습용데이터_원글.csv`: 고객 문의 원글 데이터
- `20251125_PPM학습용데이터_댓글.csv`: 고객 문의 답변 데이터

## API 엔드포인트

- `GET /`: API 상태 확인
- `POST /api/chat`: 채팅 메시지 전송
  ```json
  {
    "message": "질문 내용"
  }
  ```
- `POST /api/reload`: 데이터 재로드

## OpenAI API 사용 (선택사항)

OpenAI API를 사용하면 더 자연스러운 답변을 생성할 수 있습니다.

1. `backend/.env` 파일 생성
2. `OPENAI_API_KEY=your_api_key_here` 추가
3. 백엔드 재시작

API 키가 없어도 로컬 모델로 동작합니다.

## 프로젝트 구조

```
.
├── backend/
│   ├── main.py           # FastAPI 서버
│   ├── rag_system.py     # RAG 시스템 구현
│   └── .env.example      # 환경 변수 예시
├── src/
│   ├── App.jsx           # 메인 컴포넌트
│   ├── App.css           # 스타일
│   ├── main.jsx          # 진입점
│   └── index.css         # 전역 스타일
├── requirements.txt      # Python 의존성
├── package.json          # Node 의존성
├── vite.config.js        # Vite 설정
└── README.md             # 이 파일
```

## 🚀 배포

### 빠른 배포 가이드

자세한 배포 가이드는 **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)**를 참고하세요.

### 배포 구조

- **프론트엔드**: Cloudflare Pages
- **백엔드**: Railway 또는 Render (Python FastAPI)

### 주요 단계

1. **깃허브 푸시** ✅ (완료)
2. **Cloudflare Pages 배포**
   - GitHub 저장소 연결
   - 빌드 설정: `npm install && npm run build`
   - 출력 디렉토리: `dist`
3. **백엔드 배포** (Railway 권장)
   - Root Directory: `backend`
   - 환경 변수: `OPENAI_API_KEY` 설정
4. **연결 설정**
   - Cloudflare Pages 환경 변수에 `BACKEND_URL` 설정

자세한 내용은 `DEPLOY_GUIDE.md` 참고

## 백엔드 배포 (Cloudflare에서 실행하기)

### ⚡ 가장 간단한 방법: 하이브리드 구조 (권장)

**현재 백엔드를 그대로 유지하면서 Cloudflare를 통해 서비스하는 방법:**

1. **백엔드를 Railway/Render에 배포**
   - Python FastAPI를 그대로 사용
   - `DEPLOY_BACKEND.md` 참고

2. **Cloudflare Pages Functions로 프록시 설정** (이미 구현됨 ✅)
   - `functions/api/[[path]].js` 파일이 자동으로 `/api/*` 경로를 프록시합니다

3. **환경 변수 설정**
   - Cloudflare Pages → Settings → Environment variables
   - `BACKEND_URL`: Railway/Render에서 배포한 백엔드 URL 입력
     예: `https://your-api.railway.app`

이렇게 하면:
- ✅ 프론트엔드와 백엔드 모두 Cloudflare 네트워크를 통해 서비스
- ✅ 현재 코드 수정 최소화
- ✅ Cloudflare의 CDN 및 보안 기능 활용

### 🔧 Cloudflare Workers Python으로 완전 재구성 (고급)

현재 백엔드를 Cloudflare Workers Python으로 재작성하는 방법도 있습니다.
- `DEPLOY_CLOUDFLARE_WORKERS.md` 참고
- ⚠️ ChromaDB, Sentence Transformers 등은 제약이 있어 재구성 필요

### 📚 자세한 가이드

- **Railway/Render 배포**: `DEPLOY_BACKEND.md`
- **Cloudflare Workers 재구성**: `DEPLOY_CLOUDFLARE_WORKERS.md`

## 라이선스

MIT
