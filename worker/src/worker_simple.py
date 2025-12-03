"""
간단한 테스트용 Workers 코드
문제를 단계적으로 해결하기 위한 최소 버전
"""
from js import Response
import json

async def on_fetch(request, env):
    """Cloudflare Workers 요청 핸들러 - 간단한 테스트 버전"""
    try:
        # CORS 헤더
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Content-Type": "application/json",
        }
        
        # request.method 안전하게 가져오기
        try:
            method = request.method
        except:
            method = "GET"
        
        # OPTIONS 요청 처리
        if method == "OPTIONS":
            return Response.new(None, headers=headers, status=204)
        
        # request.url 처리
        try:
            from js import URL
            if isinstance(request.url, str):
                url_str = request.url
            else:
                url_str = str(request.url)
            url_obj = URL.new(url_str)
            path = url_obj.pathname
        except Exception as url_error:
            path = "/"
        
        # 루트 경로
        if path == "/" and method == "GET":
            return Response.new(
                json.dumps({
                    "message": "사내용 채팅 AI API",
                    "status": "running",
                    "version": "simple-test"
                }),
                headers=headers
            )
        
        # /api/chat 엔드포인트
        if path == "/api/chat":
            if method == "GET":
                return Response.new(
                    json.dumps({
                        "message": "사내용 채팅 AI API",
                        "endpoint": "/api/chat",
                        "method": "POST",
                        "description": "이 엔드포인트는 POST 요청만 지원합니다.",
                        "test": "GET 요청은 정상 작동합니다"
                    }),
                    headers=headers
                )
            elif method == "POST":
                # 간단한 POST 응답 (D1, AI Workers 사용 안 함)
                try:
                    body_text = await request.text()
                    if body_text:
                        try:
                            body = json.loads(body_text)
                            message = body.get("message", "")
                        except:
                            message = ""
                    else:
                        message = ""
                    
                    return Response.new(
                        json.dumps({
                            "response": f"테스트 응답: '{message}' 메시지를 받았습니다. Workers는 정상 작동 중입니다.",
                            "sources": [],
                            "test_mode": True
                        }),
                        headers=headers
                    )
                except Exception as post_error:
                    return Response.new(
                        json.dumps({
                            "error": f"POST 처리 오류: {str(post_error)}",
                            "test_mode": True
                        }),
                        headers=headers,
                        status=500
                    )
            else:
                return Response.new(
                    json.dumps({"error": "Method not allowed"}),
                    headers=headers,
                    status=405
                )
        
        # 404
        return Response.new(
            json.dumps({
                "error": "Not Found",
                "path": path,
                "available_endpoints": ["/", "/api/chat"]
            }),
            headers=headers,
            status=404
        )
        
    except Exception as e:
        import traceback
        try:
            error_msg = str(e)
            traceback_str = ''.join(traceback.format_exc())
            return Response.new(
                json.dumps({
                    "error": error_msg,
                    "traceback": traceback_str[:1000],
                    "test_mode": True
                }),
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                status=500
            )
        except Exception as inner_e:
            return Response.new(
                json.dumps({
                    "error": f"Internal error: {str(inner_e)}",
                    "test_mode": True
                }),
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                status=500
            )

