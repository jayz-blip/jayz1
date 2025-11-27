-- D1 데이터베이스 데이터 확인 쿼리

-- 전체 문서 개수 확인
SELECT COUNT(*) as total_documents FROM documents;

-- 문서 타입별 개수 확인
SELECT 
    json_extract(metadata, '$.type') as document_type,
    COUNT(*) as count
FROM documents
GROUP BY json_extract(metadata, '$.type');

-- 샘플 데이터 확인 (처음 5개)
SELECT 
    id,
    substr(content, 1, 100) as content_preview,
    json_extract(metadata, '$.type') as type
FROM documents
LIMIT 5;

