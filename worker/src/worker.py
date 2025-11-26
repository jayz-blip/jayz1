"""
Cloudflare Workers Python으로 구현한 채팅 AI 백엔드
D1 데이터베이스와 AI Workers를 사용합니다.
"""
from js import Response, Request
import json
import re

# HTML 태그 제거 함수
def clean_html(text):
    """HTML 태그 제거 및 텍스트 정리"""
    if not text or text == "":
        return ""
    # 간단한 HTML 태그 제거 (BeautifulSoup 대신 정규식 사용)
    text = re.sub(r'<[^>]+>', '', str(text))
    # 여러 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# 코사인 유사도 계산
def cosine_similarity(vec1, vec2):
    """두 벡터의 코사인 유사도 계산"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

async def on_fetch(request, env):
    """Cloudflare Workers 요청 핸들러"""
    url = request.url
    path = url.pathname
    
    # CORS 헤더
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json",
    }
    
    # OPTIONS 요청 처리
    if request.method == "OPTIONS":
        return Response.new(None, headers=headers, status=204)
    
    try:
        # API 라우팅
        if path == "/api/chat" and request.method == "POST":
            return await handle_chat(request, env, headers)
        elif path == "/api/reload" and request.method == "POST":
            return await handle_reload(env, headers)
        elif path == "/" and request.method == "GET":
            return Response.new(
                json.dumps({"message": "사내용 채팅 AI API", "status": "running"}),
                headers=headers
            )
        else:
            return Response.new(
                json.dumps({"error": "Not Found"}),
                headers=headers,
                status=404
            )
    except Exception as e:
        return Response.new(
            json.dumps({"error": str(e)}),
            headers=headers,
            status=500
        )

async def handle_chat(request, env, headers):
    """채팅 요청 처리"""
    try:
        # 요청 본문 파싱
        body_text = await request.text()
        body = json.loads(body_text)
        message = body.get("message", "")
        
        if not message:
            return Response.new(
                json.dumps({"error": "메시지가 필요합니다"}),
                headers=headers,
                status=400
            )
        
        # Cloudflare AI Workers로 쿼리 임베딩 생성
        query_embedding = await generate_embedding(env, message)
        
        # D1에서 모든 문서 가져오기
        result = await env.DB.prepare(
            "SELECT id, content, metadata, embedding FROM documents WHERE content IS NOT NULL AND content != ''"
        ).all()
        
        if not result.results:
            return Response.new(
                json.dumps({
                    "response": "죄송합니다. 아직 데이터가 로드되지 않았습니다. /api/reload를 먼저 호출해주세요.",
                    "sources": []
                }),
                headers=headers
            )
        
        # 유사도 계산 및 정렬
        similarities = []
        for doc in result.results:
            doc_embedding = json.loads(doc.embedding) if doc.embedding else None
            if doc_embedding:
                similarity = cosine_similarity(query_embedding, doc_embedding)
                similarities.append({
                    "similarity": similarity,
                    "content": doc.content,
                    "metadata": json.loads(doc.metadata) if doc.metadata else {}
                })
        
        # 유사도 순으로 정렬
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 상위 3개 선택
        top_results = similarities[:3]
        
        # 응답 생성
        if top_results and top_results[0]["similarity"] > 0.3:  # 유사도 임계값
            best_match = top_results[0]
            response_text = best_match["content"]
            
            # OpenAI API가 설정되어 있으면 더 자연스러운 응답 생성
            if env.OPENAI_API_KEY:
                response_text = await generate_ai_response(env, message, best_match["content"])
        else:
            response_text = "죄송합니다. 관련된 정보를 찾을 수 없습니다. 좀 더 구체적으로 질문해 주시면 도움을 드릴 수 있습니다."
        
        # 소스 정보 구성
        sources = [
            {
                "content": result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"],
                "metadata": result["metadata"],
                "similarity": result["similarity"]
            }
            for result in top_results
        ]
        
        return Response.new(
            json.dumps({
                "response": response_text,
                "sources": sources
            }),
            headers=headers
        )
        
    except Exception as e:
        return Response.new(
            json.dumps({"error": str(e)}),
            headers=headers,
            status=500
        )

async def generate_embedding(env, text):
    """Cloudflare AI Workers로 임베딩 생성"""
    try:
        # Cloudflare AI Workers 사용 (다국어 모델)
        response = await env.AI.run(
            "@cf/baai/bge-base-en-v1.5",  # 영어 모델 (한국어도 어느 정도 지원)
            {"text": [text]}
        )
        # 응답에서 임베딩 벡터 추출
        if hasattr(response, 'data') and response.data:
            return response.data[0] if isinstance(response.data, list) else response.data
        elif hasattr(response, 'embeddings'):
            return response.embeddings[0] if isinstance(response.embeddings, list) else response.embeddings
        else:
            # 응답 형식이 다를 수 있으므로 직접 접근 시도
            return response
    except Exception as e:
        print(f"임베딩 생성 오류: {e}")
        # 폴백: 간단한 해시 기반 벡터 (실제로는 사용하지 않음)
        return [0.0] * 384  # 기본 벡터 크기

async def generate_ai_response(env, query, context):
    """OpenAI API를 사용한 응답 생성 (선택사항)"""
    try:
        import fetch
        response = await fetch.fetch(
            "https://api.openai.com/v1/chat/completions",
            {
                "method": "POST",
                "headers": {
                    "Authorization": f"Bearer {env.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "당신은 고객 지원 전문가입니다. 제공된 컨텍스트를 바탕으로 정확하고 도움이 되는 답변을 제공합니다."
                        },
                        {
                            "role": "user",
                            "content": f"컨텍스트: {context}\n\n질문: {query}\n\n답변:"
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                })
            }
        )
        result = await response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenAI API 오류: {e}")
        return context  # 폴백: 원본 컨텍스트 반환

async def handle_reload(env, headers):
    """데이터 재로드 (CSV 파일을 D1에 로드)"""
    try:
        # CSV 파일은 GitHub에서 직접 읽거나, 
        # 별도의 데이터 로드 스크립트 필요
        # 여기서는 간단한 응답만 반환
        return Response.new(
            json.dumps({
                "message": "데이터 재로드는 별도의 스크립트로 실행해야 합니다. worker/scripts/load_data.py를 참고하세요."
            }),
            headers=headers
        )
    except Exception as e:
        return Response.new(
            json.dumps({"error": str(e)}),
            headers=headers,
            status=500
        )

