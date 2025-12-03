from js import Response
import json

async def on_fetch(request, env):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
    }
    
    return Response.new(
        json.dumps({"message": "OK", "status": "working"}),
        headers=headers
    )

