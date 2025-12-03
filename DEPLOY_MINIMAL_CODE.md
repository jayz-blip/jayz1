# 최소한의 코드로 배포 가이드

## 🎯 목적

가장 간단한 코드로 배포하여 Workers가 기본적으로 작동하는지 확인합니다.

## ✅ 배포 방법

### 1단계: Cloudflare 대시보드 접속

1. **https://dash.cloudflare.com/** 접속
2. 로그인

### 2단계: Workers 프로젝트로 이동

1. **Workers & Pages** → **Workers**
2. **`chatbot-api`** 프로젝트 클릭

### 3단계: 코드 편집

1. **"배포"** (Deployment) 탭 클릭
2. **"</> 코드 편집"** 버튼 클릭

### 4단계: 최소한의 코드 붙여넣기

**`worker/src/worker_minimal.py`** 파일의 전체 내용을 복사하여 붙여넣기:

```python
from js import Response
import json

async def on_fetch(request, env):
    """최소한의 핸들러"""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json",
    }
    
    # OPTIONS 처리
    if request.method == "OPTIONS":
        return Response.new(None, headers=headers, status=204)
    
    # 모든 요청에 대해 간단한 응답
    return Response.new(
        json.dumps({
            "message": "Workers 정상 작동 중",
            "status": "ok",
            "path": str(request.url) if hasattr(request, 'url') else "unknown"
        }),
        headers=headers
    )
```

### 5단계: 저장 및 배포

1. **"저장 및 배포"** (Save and Deploy) 클릭
2. 배포 완료 대기 (1-2분)

## 🧪 테스트

배포 후:

1. **브라우저에서 접속**:
   - `https://chatbot-api.jayz-407.workers.dev/api/chat`
   - JSON 응답이 표시되어야 합니다

2. **응답 확인**:
   ```json
   {
     "message": "Workers 정상 작동 중",
     "status": "ok",
     "path": "..."
   }
   ```

### 성공하면
- ✅ Workers 자체는 정상 작동
- ✅ 문제는 기존 코드에 있음
- ✅ 단계적으로 기능 추가 가능

### 실패하면
- ❌ Workers 환경 설정 문제
- ❌ wrangler.toml 설정 문제
- ❌ 로그 확인 필수

## 🔍 실패 시 할 일

1. **로그 확인** (필수!)
   - "관찰 가능성" 탭 → "이벤트" 확인
   - 오류 메시지 복사

2. **wrangler.toml 확인**:
   - `main = "src/worker.py"` 확인
   - 배포 시 `worker_minimal.py`를 사용하도록 변경 필요할 수 있음

---

**이 코드로 배포하면 최소한의 응답은 받을 수 있어야 합니다!**

**배포 후 결과를 알려주세요!**

