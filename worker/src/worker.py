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
    try:
        # request.url 처리 - 안전한 방식
        from js import URL
        try:
            # request.url이 문자열인 경우
            if isinstance(request.url, str):
                url_str = request.url
            else:
                # request.url이 객체인 경우
                url_str = str(request.url)
            
            url_obj = URL.new(url_str)
            path = url_obj.pathname
        except Exception as url_error:
            # URL 파싱 실패 시 기본값 사용
            path = "/"
            print(f"URL parsing error: {url_error}")
        
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
                json.dumps({"error": "Not Found", "path": path}),
                headers=headers,
                status=404
            )
    except Exception as e:
        import traceback
        try:
            error_msg = str(e)
            traceback_str = ''.join(traceback.format_exc())
            error_response = {
                "error": error_msg,
                "traceback": traceback_str
            }
            return Response.new(
                json.dumps(error_response),
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                status=500
            )
        except Exception as inner_e:
            # 최후의 폴백
            return Response.new(
                json.dumps({"error": f"Internal error: {str(inner_e)}"}),
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
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
        
        # D1에서 모든 문서 가져오기 (안전한 방식)
        try:
            if not hasattr(env, 'DB') or env.DB is None:
                return Response.new(
                    json.dumps({
                        "response": "D1 데이터베이스가 연결되지 않았습니다.",
                        "sources": []
                    }),
                    headers=headers,
                    status=500
                )
            
            # 성능 최적화: 필요한 컬럼만 선택하고 LIMIT 적용
            result = await env.DB.prepare(
                "SELECT id, content, metadata, embedding FROM documents WHERE content IS NOT NULL AND content != '' LIMIT 500"
            ).all()
        except Exception as db_error:
            return Response.new(
                json.dumps({
                    "response": f"D1 데이터베이스 오류: {str(db_error)}",
                    "sources": []
                }),
                headers=headers,
                status=500
            )
        
        if not result.results:
            return Response.new(
                json.dumps({
                    "response": "죄송합니다. 아직 데이터가 로드되지 않았습니다. /api/reload를 먼저 호출해주세요.",
                    "sources": []
                }),
                headers=headers
            )
        
        # 유사도 계산 및 정렬 (안전한 방식)
        # 성능 최적화: 최대 500개만 처리
        similarities = []
        max_docs = min(500, len(result.results))
        for i, doc in enumerate(result.results[:max_docs]):
            try:
                # embedding 파싱
                doc_embedding = None
                if doc.embedding:
                    try:
                        if isinstance(doc.embedding, str):
                            doc_embedding = json.loads(doc.embedding)
                        elif isinstance(doc.embedding, (list, tuple)):
                            doc_embedding = list(doc.embedding)
                        else:
                            doc_embedding = None
                    except:
                        doc_embedding = None
                
                if doc_embedding and isinstance(doc_embedding, (list, tuple)):
                    # query_embedding도 리스트로 변환
                    query_emb = list(query_embedding) if isinstance(query_embedding, (list, tuple)) else query_embedding
                    doc_emb = list(doc_embedding)
                    
                    similarity = cosine_similarity(query_emb, doc_emb)
                    
                    # metadata 파싱
                    metadata = {}
                    if doc.metadata:
                        try:
                            if isinstance(doc.metadata, str):
                                metadata = json.loads(doc.metadata)
                            elif isinstance(doc.metadata, dict):
                                metadata = doc.metadata
                        except:
                            metadata = {}
                    
                    similarities.append({
                        "similarity": float(similarity),
                        "content": str(doc.content) if doc.content else "",
                        "metadata": metadata
                    })
            except Exception as doc_error:
                # 문서 처리 실패 시 건너뛰기
                print(f"Document processing error: {doc_error}")
                continue
        
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
        
        # 소스 정보 구성 (안전한 방식)
        sources = []
        for result in top_results:
            try:
                # metadata가 dict인지 확인
                metadata = result.get("metadata", {})
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except:
                        metadata = {}
                elif not isinstance(metadata, dict):
                    metadata = {}
                
                source_item = {
                    "content": str(result.get("content", ""))[:200] + "..." if len(str(result.get("content", ""))) > 200 else str(result.get("content", "")),
                    "metadata": metadata,
                    "similarity": float(result.get("similarity", 0.0))
                }
                sources.append(source_item)
            except Exception as source_error:
                # 소스 항목 생성 실패 시 건너뛰기
                print(f"Source item error: {source_error}")
                continue
        
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
        # AI Workers 바인딩 확인
        if not hasattr(env, 'AI') or env.AI is None:
            raise Exception("AI Workers 바인딩이 없습니다")
        
        # Cloudflare AI Workers 사용
        # @cf/baai/bge-small-en-v1.5 사용 (더 작고 빠른 모델)
        response = await env.AI.run(
            "@cf/baai/bge-small-en-v1.5",
            {"text": text}
        )
        
        # 응답 형식에 따라 임베딩 추출 (안전한 방식)
        try:
            if isinstance(response, dict):
                if "data" in response:
                    embeddings = response["data"]
                    if isinstance(embeddings, (list, tuple)) and len(embeddings) > 0:
                        embedding = embeddings[0]
                        if isinstance(embedding, (list, tuple)):
                            return list(embedding)
                elif "embeddings" in response:
                    embeddings = response["embeddings"]
                    if isinstance(embeddings, (list, tuple)) and len(embeddings) > 0:
                        embedding = embeddings[0]
                        if isinstance(embedding, (list, tuple)):
                            return list(embedding)
                elif "shape" in response and "data" in response:
                    # NumPy 배열 형식일 수 있음
                    data = response["data"]
                    if isinstance(data, (list, tuple)):
                        return list(data)
            elif isinstance(response, (list, tuple)) and len(response) > 0:
                embedding = response[0]
                if isinstance(embedding, (list, tuple)):
                    return list(embedding)
        except Exception as parse_error:
            print(f"Embedding parse error: {parse_error}")
        
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

