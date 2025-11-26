import os
import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Optional
import re
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

load_dotenv()

class RAGSystem:
    def __init__(self):
        self.embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        db_path = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=db_path
        ))
        self.collection = None
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_openai = bool(self.openai_api_key)
        
        # 데이터 로드 및 벡터화
        self.load_data()
    
    def clean_html(self, text: str) -> str:
        """HTML 태그 제거 및 텍스트 정리"""
        if pd.isna(text) or text == "":
            return ""
        soup = BeautifulSoup(str(text), 'html.parser')
        text = soup.get_text()
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def load_data(self):
        """CSV 파일 로드 및 벡터 DB에 저장"""
        print("데이터 로딩 중...")
        
        # 기존 컬렉션 삭제 및 재생성
        try:
            self.client.delete_collection("ppm_knowledge")
        except:
            pass
        
        self.collection = self.client.create_collection(
            name="ppm_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
        
        documents = []
        metadatas = []
        ids = []
        
        # 원글 데이터 로드
        try:
            csv_path_original = os.path.join(os.path.dirname(__file__), "..", "20251125_PPM학습용데이터_원글.csv")
            df_original = pd.read_csv(csv_path_original, encoding='utf-8')
            print(f"원글 데이터: {len(df_original)}개 로드됨")
            
            for idx, row in df_original.iterrows():
                content = self.clean_html(row.get('content', ''))
                subject = self.clean_html(row.get('subject', ''))
                name = row.get('name', '')
                
                if content and len(content) > 10:  # 최소 길이 체크
                    text = f"제목: {subject}\n내용: {content}"
                    if name:
                        text = f"[{name}] {text}"
                    
                    documents.append(text)
                    metadatas.append({
                        "type": "원글",
                        "name": str(name),
                        "subject": str(subject)[:100],
                        "id": str(row.get('id', ''))
                    })
                    ids.append(f"original_{row.get('id', idx)}")
        except Exception as e:
            print(f"원글 데이터 로드 오류: {e}")
        
        # 댓글 데이터 로드
        try:
            csv_path_comment = os.path.join(os.path.dirname(__file__), "..", "20251125_PPM학습용데이터_댓글.csv")
            df_comment = pd.read_csv(csv_path_comment, encoding='utf-8')
            print(f"댓글 데이터: {len(df_comment)}개 로드됨")
            
            for idx, row in df_comment.iterrows():
                content = self.clean_html(row.get('content', ''))
                name = row.get('name', '')
                writer = row.get('writer', '')
                
                if content and len(content) > 10:
                    text = f"답변: {content}"
                    if name:
                        text = f"[{name}] {text}"
                    if writer:
                        text = f"{text} (작성자: {writer})"
                    
                    documents.append(text)
                    metadatas.append({
                        "type": "댓글",
                        "name": str(name),
                        "writer": str(writer),
                        "id": str(row.get('id', ''))
                    })
                    ids.append(f"comment_{row.get('id', idx)}")
        except Exception as e:
            print(f"댓글 데이터 로드 오류: {e}")
        
        # 벡터화 및 저장 (배치 처리)
        print(f"총 {len(documents)}개 문서 벡터화 중...")
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_metas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            embeddings = self.embedding_model.encode(batch_docs, show_progress_bar=False)
            
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=batch_docs,
                metadatas=batch_metas,
                ids=batch_ids
            )
            print(f"진행률: {min(i+batch_size, len(documents))}/{len(documents)}")
        
        print("데이터 로딩 완료!")
    
    def reload_data(self):
        """데이터 재로드"""
        self.load_data()
    
    def get_openai_response(self, query: str, context: str) -> str:
        """OpenAI API를 사용한 응답 생성"""
        if not self.use_openai:
            return None
        
        try:
            client = openai.OpenAI(api_key=self.openai_api_key)
            prompt = f"""다음은 고객 지원 질문과 답변 데이터베이스입니다. 
사용자의 질문에 대해 제공된 컨텍스트를 바탕으로 정확하고 도움이 되는 답변을 작성해주세요.

컨텍스트:
{context}

사용자 질문: {query}

답변 (친절하고 전문적인 톤으로, 한국어로 작성):"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 고객 지원 전문가입니다. 제공된 컨텍스트를 바탕으로 정확하고 도움이 되는 답변을 제공합니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API 오류: {e}")
            return None
    
    def get_local_response(self, query: str, context: str) -> str:
        """로컬 모델을 사용한 응답 생성 (간단한 템플릿 기반)"""
        # 가장 관련성 높은 답변을 찾아서 반환
        lines = context.split('\n\n')
        if lines:
            # 첫 번째 가장 관련성 높은 답변 사용
            best_match = lines[0]
            if "답변:" in best_match:
                answer = best_match.split("답변:")[-1].strip()
                return answer[:500]  # 길이 제한
            elif "내용:" in best_match:
                answer = best_match.split("내용:")[-1].strip()
                return answer[:500]
        
        return "죄송합니다. 관련된 정보를 찾을 수 없습니다. 좀 더 구체적으로 질문해 주시면 도움을 드릴 수 있습니다."
    
    def query(self, query: str, top_k: int = 3) -> Tuple[str, List[dict]]:
        """질문에 대한 답변 생성"""
        # 쿼리 벡터화
        query_embedding = self.embedding_model.encode([query])[0]
        
        # 유사한 문서 검색
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        # 컨텍스트 구성
        context_parts = []
        sources = []
        
        if results['documents'] and len(results['documents'][0]) > 0:
            for i, doc in enumerate(results['documents'][0]):
                context_parts.append(doc)
                if results['metadatas'] and len(results['metadatas'][0]) > i:
                    sources.append({
                        "content": doc[:200] + "...",
                        "metadata": results['metadatas'][0][i]
                    })
        
        context = "\n\n".join(context_parts)
        
        # 응답 생성
        if self.use_openai:
            response = self.get_openai_response(query, context)
            if not response:
                response = self.get_local_response(query, context)
        else:
            response = self.get_local_response(query, context)
        
        return response, sources

