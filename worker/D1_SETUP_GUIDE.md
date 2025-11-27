# D1 데이터베이스 설정 가이드

## 문제 해결: 파일 경로 오류

`wrangler` 명령어는 **반드시 `worker` 폴더에서 실행**해야 합니다.

## 올바른 실행 방법

### 1단계: worker 폴더로 이동

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
```

### 2단계: D1 스키마 생성

**로컬 테스트용** (로컬 D1 데이터베이스):
```powershell
npx wrangler d1 execute chatbot-db --local --file=scripts/setup_d1.sql
```

**프로덕션용** (실제 Cloudflare D1):
```powershell
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

### 3단계: 데이터 로드

먼저 CSV 데이터를 SQL 파일로 변환:

```powershell
# 프로젝트 루트에서
cd C:\Users\malgn\Desktop\malgpt
python worker/scripts/load_data.py
```

그 다음 D1에 데이터 삽입:

```powershell
# worker 폴더에서
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
```

## 주의사항

1. **항상 `worker` 폴더에서 실행**: `wrangler` 명령어는 `wrangler.toml` 파일이 있는 폴더에서 실행해야 합니다.

2. **로컬 vs 프로덕션**:
   - `--local`: 로컬 개발용 (테스트)
   - 없음: 실제 Cloudflare D1 (프로덕션)

3. **npx 사용**: 로컬에 설치된 `wrangler`를 사용하려면 `npx wrangler`를 사용하세요.

## 빠른 명령어 모음

```powershell
# 1. worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 2. 스키마 생성 (프로덕션)
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql

# 3. 데이터 로드 (프로젝트 루트에서)
cd C:\Users\malgn\Desktop\malgpt
python worker/scripts/load_data.py

# 4. 데이터 삽입 (worker 폴더에서)
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
```

