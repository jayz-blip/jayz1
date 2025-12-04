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

app = FastAPI(title="사내용 채팅 AI", version="1.0.0", lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG 시스템 지연 초기화 (메모리 절약)
rag_system = None
_initialization_started = False

def get_rag_system():
    """RAG 시스템 지연 로딩"""
    global rag_system, _initialization_started
    if rag_system is None:
        logger.info("🔄 RAG 시스템 초기화 중...")
        rag_system = RAGSystem()
        logger.info("✅ RAG 시스템 초기화 완료")
    return rag_system

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 시작/종료 시 실행되는 lifespan 이벤트"""
    # 서버 시작 시
    import asyncio
    logger.info("🚀 서버 시작 - 백그라운드에서 모델 로딩 시작...")
    
    async def warm_up():
        try:
            # 백그라운드에서 모델 로드
            await asyncio.to_thread(get_rag_system)
            logger.info("✅ 모델 warm-up 완료")
        except Exception as e:
            logger.error(f"⚠️ 모델 warm-up 실패 (첫 요청 시 로드됨): {e}", exc_info=True)
    
    # 백그라운드 태스크로 실행 (요청을 블로킹하지 않음)
    asyncio.create_task(warm_up())
    
    yield  # 서버 실행 중
    
    # 서버 종료 시 (필요한 경우)
    logger.info("🛑 서버 종료 중...")

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
        
        # RAG 시스템 지연 로딩
        rag = get_rag_system()
        
        # 고객사 근황 조회인지 먼저 확인
        company_status = rag.query_company_status(request.message)
        if company_status:
            response, sources = company_status
            logger.info(f"✅ 고객사 근황 조회 완료")
            return ChatResponse(response=response, sources=sources)
        
        # 일반 쿼리 처리
        response, sources = rag.query(request.message)
        logger.info(f"✅ 응답 생성 완료 (소스 개수: {len(sources) if sources else 0})")
        logger.info(f"📝 응답 내용 (처음 100자): {response[:100]}...")
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ 오류 발생: {error_msg}", exc_info=True)
        # 에러 메시지에서 ANSI 색상 코드 제거
        clean_error = error_msg.replace('\x1B[91m', '').replace('\x1B[0m', '')
        raise HTTPException(status_code=500, detail=clean_error)

@app.post("/api/reload")
async def reload_data():
    try:
        rag = get_rag_system()
        rag.reload_data()
        return {"message": "데이터가 성공적으로 다시 로드되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Render는 환경 변수 PORT를 자동으로 제공하므로 0.0.0.0에 바인딩
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

