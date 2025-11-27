# 원격 D1 스키마 생성 가이드

## 📍 어디서 실행하나요?

**현재 위치 (`worker` 폴더)에서 그대로 실행하시면 됩니다!**

## 🎯 명령어

현재 PowerShell이 `C:\Users\malgn\Desktop\malgpt\worker` 위치에 있다면:

```powershell
npx wrangler d1 execute chatbot-db --remote --file=scripts/setup_d1.sql
```

## 📋 전체 과정

### 1단계: 현재 위치 확인

```powershell
# 현재 위치 확인
Get-Location
```

**예상 결과**: `C:\Users\malgn\Desktop\malgpt\worker`

### 2단계: 원격 D1 스키마 생성

```powershell
# worker 폴더에서 (현재 위치)
npx wrangler d1 execute chatbot-db --remote --file=scripts/setup_d1.sql
```

**중요**:
- `--remote`: 실제 Cloudflare D1 데이터베이스에 적용
- `--file=scripts/setup_d1.sql`: SQL 파일 경로 (현재 폴더 기준)

### 3단계: 결과 확인

성공하면 다음과 같은 메시지가 표시됩니다:

```
🌀 Executing on remote database chatbot-db (07f05a1f-794b-4429-a91d-6191de544588):
🚣 2 commands executed successfully.
```

## 🔍 로컬 vs 원격 차이

### 로컬 (테스트용)
```powershell
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```
- 로컬 개발 환경에만 적용
- 실제 Cloudflare에는 영향 없음

### 원격 (프로덕션)
```powershell
npx wrangler d1 execute chatbot-db --remote --file=scripts/setup_d1.sql
```
- 실제 Cloudflare D1 데이터베이스에 적용
- 프로덕션 환경에 영향

## ⚠️ 주의사항

1. **반드시 `worker` 폴더에서 실행**: `wrangler.toml` 파일이 있는 폴더여야 합니다.

2. **파일 경로**: `scripts/setup_d1.sql`은 `worker` 폴더 기준 상대 경로입니다.

3. **원격 실행**: `--remote` 플래그를 사용하면 실제 Cloudflare에 적용되므로 신중하게 실행하세요.

## 📋 다음 단계

원격 스키마 생성 후:

1. CSV 데이터 로드
2. 원격 D1에 데이터 삽입
3. Workers 배포

---

**지금 바로 실행하세요!**

```powershell
npx wrangler d1 execute chatbot-db --remote --file=scripts/setup_d1.sql
```

