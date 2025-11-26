-- D1 데이터베이스 스키마 생성
-- wrangler d1 execute chatbot-db --local --file=setup_d1.sql
-- 또는 프로덕션: wrangler d1 execute chatbot-db --file=setup_d1.sql

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    metadata TEXT,
    embedding TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_content ON documents(content);

-- 데이터 삭제 (필요시)
-- DELETE FROM documents;

