"""
CSV 데이터를 D1 데이터베이스에 로드하는 스크립트
로컬에서 실행하여 데이터를 D1에 저장합니다.
"""
import pandas as pd
import json
import re
import os
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def clean_html(text):
    """HTML 태그 제거 및 텍스트 정리"""
    if pd.isna(text) or text == "":
        return ""
    # 간단한 HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', str(text))
    # 여러 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_simple_embedding(text):
    """
    간단한 해시 기반 임베딩 생성 (실제로는 Cloudflare AI Workers 사용 권장)
    실제 배포 시에는 Cloudflare AI Workers로 임베딩을 생성해야 합니다.
    """
    # 간단한 예시: 텍스트를 해시 기반 벡터로 변환
    # 실제로는 Cloudflare AI Workers API를 호출해야 함
    import hashlib
    hash_obj = hashlib.md5(text.encode())
    hash_hex = hash_obj.hexdigest()
    # 384차원 벡터로 변환 (예시)
    vector = [int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, min(384, len(hash_hex)), 2)]
    while len(vector) < 384:
        vector.append(0.0)
    return vector[:384]

async def load_data_to_d1():
    """CSV 데이터를 D1에 로드"""
    print("데이터 로딩 시작...")
    
    documents = []
    
    # 원글 데이터 로드
    try:
        csv_path_original = project_root / "20251125_PPM학습용데이터_원글.csv"
        if csv_path_original.exists():
            df_original = pd.read_csv(csv_path_original, encoding='utf-8')
            print(f"원글 데이터: {len(df_original)}개 로드됨")
            
            for idx, row in df_original.iterrows():
                content = clean_html(row.get('content', ''))
                subject = clean_html(row.get('subject', ''))
                name = row.get('name', '')
                
                if content and len(content) > 10:
                    text = f"제목: {subject}\n내용: {content}"
                    if name:
                        text = f"[{name}] {text}"
                    
                    metadata = {
                        "type": "원글",
                        "name": str(name),
                        "subject": str(subject)[:100],
                        "id": str(row.get('id', ''))
                    }
                    
                    # 임베딩 생성 (실제로는 Cloudflare AI Workers 사용)
                    embedding = generate_simple_embedding(text)
                    
                    documents.append({
                        "id": f"original_{row.get('id', idx)}",
                        "content": text,
                        "metadata": json.dumps(metadata, ensure_ascii=False),
                        "embedding": json.dumps(embedding)
                    })
        else:
            print(f"원글 CSV 파일을 찾을 수 없습니다: {csv_path_original}")
    except Exception as e:
        print(f"원글 데이터 로드 오류: {e}")
    
    # 댓글 데이터 로드
    try:
        csv_path_comment = project_root / "20251125_PPM학습용데이터_댓글.csv"
        if csv_path_comment.exists():
            df_comment = pd.read_csv(csv_path_comment, encoding='utf-8')
            print(f"댓글 데이터: {len(df_comment)}개 로드됨")
            
            for idx, row in df_comment.iterrows():
                content = clean_html(row.get('content', ''))
                name = row.get('name', '')
                writer = row.get('writer', '')
                
                if content and len(content) > 10:
                    text = f"답변: {content}"
                    if name:
                        text = f"[{name}] {text}"
                    if writer:
                        text = f"{text} (작성자: {writer})"
                    
                    metadata = {
                        "type": "댓글",
                        "name": str(name),
                        "writer": str(writer),
                        "id": str(row.get('id', ''))
                    }
                    
                    # 임베딩 생성
                    embedding = generate_simple_embedding(text)
                    
                    documents.append({
                        "id": f"comment_{row.get('id', idx)}",
                        "content": text,
                        "metadata": json.dumps(metadata, ensure_ascii=False),
                        "embedding": json.dumps(embedding)
                    })
        else:
            print(f"댓글 CSV 파일을 찾을 수 없습니다: {csv_path_comment}")
    except Exception as e:
        print(f"댓글 데이터 로드 오류: {e}")
    
    print(f"총 {len(documents)}개 문서 준비됨")
    
    # D1에 저장하는 코드는 wrangler CLI를 사용해야 함
    # 또는 Cloudflare API를 직접 호출
    print("\nD1에 데이터를 저장하려면 다음 명령어를 사용하세요:")
    print("wrangler d1 execute chatbot-db --local --file=insert_data.sql")
    print("\n또는 Cloudflare API를 사용하여 프로그래밍 방식으로 저장할 수 있습니다.")
    
    # SQL 파일 생성
    sql_file = project_root / "worker" / "scripts" / "insert_data.sql"
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write("-- D1 데이터베이스에 문서 삽입\n")
        f.write("-- 먼저 테이블을 생성해야 합니다:\n")
        f.write("""
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    metadata TEXT,
    embedding TEXT
);

-- 기존 데이터 삭제
DELETE FROM documents;

""")
        for doc in documents:
            # SQL injection 방지
            content_escaped = doc["content"].replace("'", "''")
            f.write(f"INSERT INTO documents (id, content, metadata, embedding) VALUES ('{doc['id']}', '{content_escaped}', '{doc['metadata']}', '{doc['embedding']}');\n")
    
    print(f"\nSQL 파일이 생성되었습니다: {sql_file}")
    print(f"총 {len(documents)}개 문서가 포함되어 있습니다.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_data_to_d1())

