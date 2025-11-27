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
        if top_results and top_results[0]["similarity"] > 0.1:  # 유사도 임계값 (낮춤)
            best_match = top_results[0]
            # 가장 관련성 높은 답변 사용
            response_text = best_match["content"]
            
            # 메타데이터에서 타입 확인하여 더 나은 응답 생성
            metadata = best_match.get("metadata", {})
            if metadata.get("type") == "댓글":
                # 댓글은 이미 답변 형식이므로 그대로 사용
                response_text = best_match["content"]
            else:
                # 원글의 경우 내용을 추출
                response_text = best_match["content"]
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
        # Cloudflare AI Workers 사용
        # @cf/baai/bge-small-en-v1.5 사용 (더 작고 빠른 모델)
        response = await env.AI.run(
            "@cf/baai/bge-small-en-v1.5",
            {"text": text}
        )
        
        # 응답 형식에 따라 임베딩 추출
        if isinstance(response, dict):
            if "data" in response:
                embeddings = response["data"]
                if isinstance(embeddings, list) and len(embeddings) > 0:
                    return embeddings[0]
            elif "embeddings" in response:
                embeddings = response["embeddings"]
                if isinstance(embeddings, list) and len(embeddings) > 0:
                    return embeddings[0]
        elif isinstance(response, list) and len(response) > 0:
            return response[0]
        
        # 기본 벡터 반환 (384차원)
        return [0.0] * 384
    except Exception as e:
        # 폴백: 간단한 해시 기반 벡터
        import hashlib
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        vector = [int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, min(384, len(hash_hex)), 2)]
        while len(vector) < 384:
            vector.append(0.0)
        return vector[:384]

async def generate_ai_response(env, query, context):
    """OpenAI API를 사용한 응답 생성 (선택사항)"""
    try:
        # fetch는 JavaScript에서 사용하는 것이므로 Python에서는 다른 방법 사용
        # Cloudflare Workers Python에서는 fetch를 직접 사용할 수 없으므로
        # 간단하게 컨텍스트를 반환하거나, Cloudflare AI Workers의 텍스트 생성 모델 사용
        return context  # 일단 원본 컨텍스트 반환
    except Exception as e:
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

