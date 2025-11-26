# Cloudflare Workers Python 백엔드

D1 데이터베이스와 Cloudflare AI Workers를 사용한 채팅 AI 백엔드입니다.

## 설정

### 1. D1 데이터베이스 생성 및 연결

```bash
# Wrangler CLI 설치 (아직 안 했다면)
npm install -g wrangler

# 로그인
wrangler login

# D1 데이터베이스 생성
wrangler d1 create chatbot-db

# 생성된 database_id를 wrangler.toml에 입력
```

### 2. wrangler.toml 설정

`wrangler.toml` 파일에서 `database_id`를 실제 D1 데이터베이스 ID로 변경:

```toml
[[d1_databases]]
binding = "DB"
database_name = "chatbot-db"
database_id = "your-actual-database-id-here"  # 여기 변경!
```

### 3. 데이터 로드

```bash
# 1. 스키마 생성
wrangler d1 execute chatbot-db --local --file=scripts/setup_d1.sql

# 2. CSV 데이터를 SQL로 변환
python scripts/load_data.py

# 3. 데이터 삽입 (로컬)
wrangler d1 execute chatbot-db --local --file=scripts/insert_data.sql

# 4. 프로덕션에 배포
wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
```

### 4. 환경 변수 설정 (선택사항)

Cloudflare Workers 대시보드에서:
- `OPENAI_API_KEY`: OpenAI API 키 (더 자연스러운 응답 생성용)

### 5. 배포

```bash
# 로컬 테스트
wrangler dev

# 프로덕션 배포
wrangler deploy
```

## API 엔드포인트

- `GET /`: 상태 확인
- `POST /api/chat`: 채팅 요청
  ```json
  {
    "message": "질문 내용"
  }
  ```
- `POST /api/reload`: 데이터 재로드 (별도 스크립트 필요)

## 주의사항

1. **임베딩 생성**: 현재는 간단한 해시 기반 임베딩을 사용하지만, 실제로는 Cloudflare AI Workers를 사용해야 합니다.
2. **데이터 크기**: D1은 무료 티어에서 5GB 제한이 있습니다.
3. **벡터 검색**: D1은 벡터 검색을 직접 지원하지 않으므로, 모든 문서를 가져와서 JavaScript에서 유사도 계산을 합니다. 대량 데이터에는 비효율적일 수 있습니다.

## 개선 방안

1. **벡터 DB 마이그레이션**: Pinecone, Weaviate 등 전용 벡터 DB 사용
2. **배치 처리**: 대량 데이터는 배치로 처리
3. **캐싱**: 자주 사용되는 쿼리 결과 캐싱

