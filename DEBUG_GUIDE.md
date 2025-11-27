# 오류 로그 확인 가이드

## 백엔드 로그 확인 (CMD 창)

백엔드를 실행한 CMD 창에서 바로 로그를 확인할 수 있습니다.

### 1. 백엔드 실행 시 로그 확인

```bash
cd backend
python main.py
```

**확인할 로그:**
- ✅ "데이터 로딩 중..."
- ✅ "원글 데이터: X개 로드됨"
- ✅ "댓글 데이터: X개 로드됨"
- ✅ "총 X개 문서 벡터화 중..."
- ✅ "데이터 로딩 완료!"
- ✅ "Uvicorn running on http://0.0.0.0:8000"
- ❌ 오류 메시지 (빨간색 텍스트)

### 2. API 요청 로그 확인

질문을 보낼 때마다 CMD 창에 다음과 같은 로그가 나타납니다:
- 요청 정보
- 오류 메시지 (있는 경우)

### 3. 더 자세한 로그를 원할 때

백엔드 코드에 로깅을 추가할 수 있습니다. `backend/main.py`를 수정:

```python
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"받은 질문: {request.message}")
        response, sources = rag_system.query(request.message)
        logger.info(f"응답 생성 완료, 소스 개수: {len(sources) if sources else 0}")
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 프론트엔드 로그 확인

### 1. 브라우저 개발자 도구

1. **F12 키** 또는 **우클릭 → 검사** 클릭
2. **Console** 탭 선택
3. 오류 메시지 확인 (빨간색으로 표시됨)

### 2. Network 탭에서 API 요청 확인

1. 개발자 도구 → **Network** 탭
2. 질문 전송
3. `/api/chat` 요청 클릭
4. **Response** 탭에서 서버 응답 확인
5. **Headers** 탭에서 요청/응답 헤더 확인

### 3. 프론트엔드 코드에 로깅 추가

`src/App.jsx`의 `handleSend` 함수에 로깅 추가:

```javascript
const handleSend = async () => {
  if (!input.trim() || loading) return

  const userMessage = {
    role: 'user',
    content: input,
    timestamp: new Date()
  }

  setMessages(prev => [...prev, userMessage])
  const question = input
  setInput('')
  setLoading(true)

  try {
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    console.log('API URL:', API_URL);
    console.log('전송할 질문:', question);
    
    const response = await axios.post(`${API_URL}/api/chat`, {
      message: question
    })
    
    console.log('서버 응답:', response.data);

    const assistantMessage = {
      role: 'assistant',
      content: response.data.response,
      sources: response.data.sources,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, assistantMessage])
  } catch (error) {
    console.error('오류 상세 정보:', error);
    console.error('오류 응답:', error.response);
    console.error('오류 메시지:', error.message);
    
    const errorMessage = {
      role: 'assistant',
      content: `오류가 발생했습니다: ${error.message}`,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, errorMessage])
  } finally {
    setLoading(false)
  }
}
```

---

## 일반적인 오류와 해결 방법

### 1. "Connection refused" 또는 "Network Error"

**원인**: 백엔드가 실행되지 않음

**해결**:
- 백엔드 CMD 창 확인
- `python main.py` 실행 확인
- `http://localhost:8000`에서 실행 중인지 확인

### 2. "Failed to fetch" 또는 CORS 오류

**원인**: CORS 설정 문제

**해결**:
- 백엔드의 `allow_origins=["*"]` 확인
- 프론트엔드 URL이 올바른지 확인

### 3. "데이터가 로드되지 않았습니다"

**원인**: CSV 파일을 찾을 수 없음

**해결**:
- CSV 파일이 프로젝트 루트에 있는지 확인
- 백엔드 로그에서 "원글 데이터: X개 로드됨" 메시지 확인

### 4. "Internal Server Error"

**원인**: 백엔드 처리 중 오류

**해결**:
- 백엔드 CMD 창에서 오류 메시지 확인
- `rag_system.py`의 오류 확인

---

## 실시간 로그 모니터링

### Windows PowerShell에서

```powershell
# 백엔드 로그를 파일로 저장
python backend/main.py > backend.log 2>&1

# 다른 터미널에서 실시간 확인
Get-Content backend.log -Wait -Tail 50
```

### 로그 파일로 저장

백엔드 실행 시:
```bash
python main.py > ../backend.log 2>&1
```

그러면 `backend.log` 파일에 모든 로그가 저장됩니다.

---

## 디버깅 팁

1. **단계별 확인**
   - 백엔드가 실행 중인지 확인 (`http://localhost:8000` 접속)
   - 프론트엔드가 실행 중인지 확인 (`http://localhost:3000` 접속)
   - 브라우저 콘솔에서 오류 확인

2. **API 직접 테스트**
   ```bash
   # PowerShell에서
   curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{\"message\":\"테스트\"}'
   ```

3. **백엔드 상태 확인**
   - 브라우저에서 `http://localhost:8000` 접속
   - `{"message":"사내용 채팅 AI API","status":"running"}` 응답 확인

