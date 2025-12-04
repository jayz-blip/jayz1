import os
import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Optional, Dict
import re
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class RAGSystem:
    def __init__(self):
        # 모델과 데이터는 지연 로딩 (메모리 절약)
        self.embedding_model = None
        db_path = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=db_path
        ))
        self.collection = None
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_openai = bool(self.openai_api_key)
        
        # 원본 데이터프레임 저장 (고객사별 검색용)
        self.df_original = None
        self.df_comment = None
        
        # 초기화 완료 플래그
        self._initialized = False
    
    def _ensure_initialized(self):
        """필요 시 초기화 (지연 로딩)"""
        if not self._initialized:
            print("🔄 RAG 시스템 초기화 중...")
            # 모델 로드
            if self.embedding_model is None:
                print("📥 임베딩 모델 로딩 중...")
                self.embedding_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
                print("✅ 임베딩 모델 로딩 완료")
            
            # 데이터 로드 및 벡터화
            self.load_data()
            self._initialized = True
            print("✅ RAG 시스템 초기화 완료")
    
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
            self.df_original = pd.read_csv(csv_path_original, encoding='utf-8')
            print(f"원글 데이터: {len(self.df_original)}개 로드됨")
            
            for idx, row in self.df_original.iterrows():
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
            self.df_comment = pd.read_csv(csv_path_comment, encoding='utf-8')
            print(f"댓글 데이터: {len(self.df_comment)}개 로드됨")
            
            for idx, row in self.df_comment.iterrows():
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
        self._ensure_initialized()
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
    
    def extract_company_name(self, query: str) -> Optional[str]:
        """쿼리에서 고객사명 추출"""
        self._ensure_initialized()
        # 고객사명이 있는지 확인
        if self.df_original is not None:
            company_names = self.df_original['name'].unique().tolist()
            # 긴 이름부터 매칭 (부분 매칭 방지)
            company_names_sorted = sorted([str(c) for c in company_names if c], key=len, reverse=True)
            
            for company in company_names_sorted:
                if company and company in query:
                    return company
        return None
    
    def get_company_recent_inquiries(self, company_name: str, limit: int = 10) -> List[Dict]:
        """고객사별 최근 문의글과 답변 조회"""
        if self.df_original is None or self.df_comment is None:
            return []
        
        # 해당 고객사의 최근 문의글 조회
        company_inquiries = self.df_original[
            self.df_original['name'] == company_name
        ].copy()
        
        # 날짜순 정렬 (최신순)
        if 'reg_date' in company_inquiries.columns:
            company_inquiries = company_inquiries.sort_values('reg_date', ascending=False)
        
        results = []
        
        for idx, inquiry in company_inquiries.head(limit).iterrows():
            inquiry_id = str(inquiry.get('id', ''))
            inquiry_content = self.clean_html(inquiry.get('content', ''))
            inquiry_subject = self.clean_html(inquiry.get('subject', ''))
            inquiry_date = inquiry.get('reg_date', '')
            manager_id = inquiry.get('manager_id', '')
            writer = inquiry.get('writer', '')
            
            # 해당 문의글의 답변 조회 (post_id는 문자열로 변환해서 비교)
            replies = self.df_comment[
                (self.df_comment['name'] == company_name) & 
                (self.df_comment['post_id'].astype(str) == str(inquiry_id))
            ].copy()
            
            # 답변도 날짜순 정렬
            if 'reg_date' in replies.columns:
                replies = replies.sort_values('reg_date', ascending=False)
            
            reply_list = []
            for _, reply in replies.iterrows():
                reply_content = self.clean_html(reply.get('content', ''))
                reply_writer = reply.get('writer', '')
                reply_date = reply.get('reg_date', '')
                reply_list.append({
                    'content': reply_content,
                    'writer': reply_writer,
                    'date': reply_date
                })
            
            results.append({
                'id': inquiry_id,
                'subject': inquiry_subject,
                'content': inquiry_content,
                'date': inquiry_date,
                'writer': writer,
                'manager_id': manager_id,
                'replies': reply_list,
                'reply_count': len(reply_list)
            })
        
        return results
    
    def summarize_company_status(self, company_name: str, inquiries: List[Dict]) -> str:
        """고객사별 근황 요약"""
        if not inquiries:
            return f"{company_name}의 최근 문의 내역이 없습니다."
        
        # 최근 문의글들을 텍스트로 구성
        summary_text = f"{company_name}의 최근 문의 내역:\n\n"
        
        for i, inquiry in enumerate(inquiries[:5], 1):  # 최대 5개만
            summary_text += f"{i}. 문의 제목: {inquiry.get('subject', '[제목 없음]')}\n"
            summary_text += f"   문의 내용: {inquiry.get('content', '')[:200]}...\n"
            
            if inquiry.get('replies'):
                latest_reply = inquiry['replies'][0]
                summary_text += f"   답변 담당자: {latest_reply.get('writer', '미상')}\n"
                summary_text += f"   답변 내용: {latest_reply.get('content', '')[:150]}...\n"
                summary_text += f"   상태: 답변 완료 ({inquiry.get('reply_count', 0)}개 답변)\n"
            else:
                summary_text += f"   상태: 답변 대기 중\n"
            
            summary_text += "\n"
        
        # OpenAI를 사용해서 더 간결하게 요약
        if self.use_openai and self.openai_api_key:
            try:
                client = openai.OpenAI(api_key=self.openai_api_key)
                prompt = f"""다음은 {company_name}의 최근 고객 문의 및 답변 내역입니다. 
간략하게 요약해서 알려주세요. 각 문의에 대해 어떤 문의였는지, 담당자가 누구인지, 해결되었는지 여부를 간단히 정리해주세요.

{summary_text}

위 내용을 간략하게 요약해주세요 (3-5줄 정도):"""
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "당신은 고객 지원 현황을 요약하는 전문가입니다. 간결하고 명확하게 요약해주세요."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI 요약 오류: {e}")
                return summary_text
        
        return summary_text
    
    def query_company_status(self, query: str) -> Optional[Tuple[str, List[dict]]]:
        """고객사 근황 조회 전용 함수"""
        company_name = self.extract_company_name(query)
        
        if not company_name:
            return None
        
        # 고객사별 최근 문의 조회
        inquiries = self.get_company_recent_inquiries(company_name, limit=10)
        
        if not inquiries:
            return f"{company_name}의 최근 문의 내역을 찾을 수 없습니다.", []
        
        # 요약 생성
        summary = self.summarize_company_status(company_name, inquiries)
        
        # 소스 정보 구성
        sources = []
        for inquiry in inquiries[:3]:  # 상위 3개만 소스로
            sources.append({
                "content": f"문의: {inquiry.get('subject', '')}",
                "metadata": {
                    "type": "고객사 근황",
                    "name": company_name,
                    "id": inquiry.get('id', '')
                }
            })
        
        return summary, sources

