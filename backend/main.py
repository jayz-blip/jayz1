from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
from dotenv import load_dotenv
from rag_system import RAGSystem

load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="사내용 채팅 AI", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG 시스템 초기화
rag_system = RAGSystem()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[dict]] = None

@app.get("/")
async def root():
    return {"message": "사내용 채팅 AI API", "status": "running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"📩 받은 질문: {request.message}")
        
        # 고객사 근황 조회인지 먼저 확인
        company_status = rag_system.query_company_status(request.message)
        if company_status:
            response, sources = company_status
            logger.info(f"✅ 고객사 근황 조회 완료")
            return ChatResponse(response=response, sources=sources)
        
        # 일반 쿼리 처리
        response, sources = rag_system.query(request.message)
        logger.info(f"✅ 응답 생성 완료 (소스 개수: {len(sources) if sources else 0})")
        logger.info(f"📝 응답 내용 (처음 100자): {response[:100]}...")
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        logger.error(f"❌ 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reload")
async def reload_data():
    try:
        rag_system.reload_data()
        return {"message": "데이터가 성공적으로 다시 로드되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Render는 환경 변수 PORT를 자동으로 제공하므로 0.0.0.0에 바인딩
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

