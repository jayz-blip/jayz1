# Cloudflare Workers로 백엔드 배포하기

Cloudflare Workers는 Python을 지원하지만, 현재 백엔드 구조(FastAPI, ChromaDB, Sentence Transformers)는 직접 배포하기 어렵습니다. Cloudflare 환경에 맞게 재구성하는 방법을 안내합니다.

## ⚠️ 제약사항

1. **FastAPI**: Cloudflare Workers는 FastAPI를 직접 지원하지 않음
2. **ChromaDB**: 파일 시스템 접근 불가, Cloudflare D1 또는 R2 사용 필요
3. **Sentence Transformers**: 모델 크기 제한, Cloudflare AI Workers 사용 권장

## 해결 방법

### 방법 1: Cloudflare Workers Python + D1 (권장)

벡터 DB를 Cloudflare D1로, 임베딩을 Cloudflare AI Workers로 변경합니다.

### 방법 2: 하이브리드 구조

- **프론트엔드**: Cloudflare Pages
- **백엔드 API**: Cloudflare Workers Python (간단한 프록시)
- **실제 처리**: Railway/Render 등 (외부 API로 호출)

### 방법 3: Cloudflare Workers Python으로 완전 재구성

현재 백엔드를 Cloudflare Workers에 맞게 재작성합니다.

---

## 방법 1: Cloudflare Workers Python 구현

### 1단계: Workers 프로젝트 구조 생성

```
backend-worker/
├── wrangler.toml
├── requirements.txt
├── src/
│   └── worker.py
└── .dev.vars (로컬 개발용)
```

### 2단계: wrangler.toml 설정

```toml
name = "chatbot-api"
main = "src/worker.py"
compatibility_date = "2024-01-01"

[env.production]
name = "chatbot-api"

# D1 데이터베이스 (벡터 DB 대신)
[[env.production.d1_databases]]
binding = "DB"
database_name = "chatbot-db"
database_id = "your-database-id"

# AI Workers (임베딩용)
[env.production.ai]
binding = "AI"
```

### 3단계: Worker 코드 작성

`backend-worker/src/worker.py`:

```python
from js import Response, Request
import json

async def on_fetch(request, env):
    """Cloudflare Workers 요청 핸들러"""
    url = request.url
    path = url.pathname
    
    # CORS 헤더
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    
    # OPTIONS 요청 처리
    if request.method == "OPTIONS":
        return Response.new(None, headers=headers, status=204)
    
    # API 라우팅
    if path == "/api/chat":
        return await handle_chat(request, env, headers)
    elif path == "/":
        return Response.new(
            json.dumps({"message": "사내용 채팅 AI API", "status": "running"}),
            headers={**headers, "Content-Type": "application/json"}
        )
    else:
        return Response.new("Not Found", status=404)

async def handle_chat(request, env, headers):
    """채팅 요청 처리"""
    try:
        # 요청 본문 파싱
        body = await request.json()
        message = body.get("message", "")
        
        # Cloudflare AI Workers로 임베딩 생성
        embedding = await env.AI.run(
            "@cf/baai/bge-base-en-v1.5",  # 임베딩 모델
            {"text": [message]}
        )
        
        # D1에서 유사한 문서 검색 (간단한 예시)
        # 실제로는 벡터 검색을 구현해야 함
        results = await env.DB.prepare(
            "SELECT * FROM documents ORDER BY RANDOM() LIMIT 3"
        ).all()
        
        # 응답 생성 (간단한 예시)
        response_text = f"질문: {message}\n\n관련 문서를 찾았습니다."
        
        return Response.new(
            json.dumps({
                "response": response_text,
                "sources": [{"content": r.content} for r in results]
            }),
            headers={**headers, "Content-Type": "application/json"}
        )
    except Exception as e:
        return Response.new(
            json.dumps({"error": str(e)}),
            headers={**headers, "Content-Type": "application/json"},
            status=500
        )
```

### 4단계: 배포

```bash
# Wrangler CLI 설치
npm install -g wrangler

# 로그인
wrangler login

# D1 데이터베이스 생성
wrangler d1 create chatbot-db

# 배포
wrangler deploy
```

---

## 방법 2: 하이브리드 구조 (가장 현실적) ⭐

현재 백엔드를 그대로 유지하면서 Cloudflare에서 프록시 역할만 하는 방법입니다.

### 구조

```
프론트엔드 (Cloudflare Pages)
    ↓
Cloudflare Workers (프록시/캐싱)
    ↓
백엔드 API (Railway/Render 등)
```

### Cloudflare Workers 프록시 구현

`functions/api/[[path]].js` (이미 있음)를 수정:

```javascript
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);
  
  // 외부 백엔드 URL (Railway, Render 등)
  const backendUrl = context.env.BACKEND_URL || 'https://your-backend.railway.app';
  
  const path = context.params.path ? `/${context.params.path.join('/')}` : '';
  const apiUrl = `${backendUrl}/api${path}${url.search}`;
  
  try {
    const response = await fetch(apiUrl, {
      method: request.method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: request.method !== 'GET' && request.method !== 'HEAD' 
        ? await request.text() 
        : null,
    });
    
    const data = await response.text();
    
    return new Response(data, {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Proxy error', message: error.message }), 
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}
```

### 환경 변수 설정

Cloudflare Pages → Settings → Environment variables:
- `BACKEND_URL`: Railway/Render 등에서 배포한 백엔드 URL

---

## 방법 3: 완전 재구성 (고급)

현재 백엔드를 Cloudflare Workers Python + D1 + AI Workers로 완전히 재작성합니다.

### 필요한 변경사항

1. **벡터 DB**: ChromaDB → Cloudflare D1 + 벡터 검색 로직 직접 구현
2. **임베딩**: Sentence Transformers → Cloudflare AI Workers
3. **API**: FastAPI → Cloudflare Workers Python 핸들러

이 방법은 상당한 코드 수정이 필요합니다.

---

## 추천: 방법 2 (하이브리드)

**가장 현실적이고 빠른 방법**은:
1. 백엔드는 Railway/Render에 배포 (현재 코드 그대로)
2. Cloudflare Pages Functions로 프록시 설정 (이미 구현됨)
3. 환경 변수로 백엔드 URL 연결

이렇게 하면:
- ✅ 현재 코드 수정 최소화
- ✅ Cloudflare의 CDN 이점 활용
- ✅ 빠른 배포

---

## 다음 단계

1. **백엔드를 Railway/Render에 배포** (`DEPLOY_BACKEND.md` 참고)
2. **Cloudflare Pages Functions 프록시 사용** (이미 구현됨)
3. **환경 변수 설정**: `BACKEND_URL`에 백엔드 URL 입력

이 방법이 가장 간단하고 안정적입니다!

