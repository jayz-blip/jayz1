# 사내용 채팅 AI 🤖💬

CSV 데이터를 학습한 RAG(Retrieval Augmented Generation) 기반 채팅 AI 시스템입니다.

## 주요 기능

- 📚 CSV 파일 기반 지식 베이스 구축
- 🔍 의미 기반 검색 (Semantic Search)
- 💬 자연스러운 대화형 인터페이스
- 🎨 깔끔하고 귀여운 UI 디자인
- 🔄 실시간 데이터 재로드 지원

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

## 라이선스

MIT
