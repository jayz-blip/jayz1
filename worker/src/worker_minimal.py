"""
최소한의 Workers 코드 - 모든 경로에 응답 반환
"""
from js import Response
import json

async def on_fetch(request, env):
    """최소한의 핸들러 - 모든 요청에 응답"""
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
        
        # OPTIONS 처리
        if method == "OPTIONS":
            return Response.new(None, headers=headers, status=204)
        
        # request.url 안전하게 가져오기
        try:
            from js import URL
            if isinstance(request.url, str):
                url_str = request.url
            else:
                url_str = str(request.url)
            url_obj = URL.new(url_str)
            path = url_obj.pathname
        except:
            path = "/"
        
        # 모든 경로에 대해 응답 반환 (hung 방지)
        response_data = {
            "message": "Workers 정상 작동 중",
            "status": "ok",
            "path": path,
            "method": method
        }
        
        # 즉시 응답 반환 (await 없이)
        return Response.new(
            json.dumps(response_data),
            headers=headers
        )
        
    except Exception as e:
        # 오류 발생 시에도 응답 반환 (hung 방지)
        return Response.new(
            json.dumps({
                "error": str(e),
                "status": "error"
            }),
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            status=500
        )

