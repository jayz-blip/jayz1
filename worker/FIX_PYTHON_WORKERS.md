# Python Workers 호환성 플래그 오류 해결

## 🔍 문제

```
X [ERROR] The `python_workers` compatibility flag is required to use Python.
```

**원인**: Cloudflare Workers Python을 사용하려면 `wrangler.toml`에 호환성 플래그를 추가해야 합니다.

## ✅ 해결 방법

### 1단계: wrangler.toml 수정 완료

`compatibility_flags = ["python_workers"]`를 추가했습니다.

### 2단계: Wrangler 업데이트

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npm install --save-dev wrangler@4
```

또는:

```powershell
npm install --save-dev wrangler@latest
```

### 3단계: D1 스키마 생성 재시도

```powershell
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

## 📋 전체 명령어 순서

```powershell
# 1. worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 2. Wrangler 업데이트
npm install --save-dev wrangler@4

# 3. D1 스키마 생성
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

## ⚠️ 주의사항

- Wrangler 4.x는 Python Workers를 지원합니다
- `compatibility_flags = ["python_workers"]`가 `wrangler.toml`에 있어야 합니다
- 업데이트 후 `npx wrangler`를 사용하세요

