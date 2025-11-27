# D1 스키마 생성 성공! 🎉

## ✅ 완료된 작업

로컬 D1 데이터베이스에 스키마가 성공적으로 생성되었습니다!

```
🚣 2 commands executed successfully.
```

## 📋 다음 단계

### 1단계: 원격(프로덕션) D1에도 스키마 생성

로컬에서 성공했으니 이제 실제 Cloudflare D1에도 스키마를 생성해야 합니다:

```powershell
# worker 폴더에서
npx wrangler d1 execute chatbot-db --remote --file=scripts/setup_d1.sql
```

**중요**: `--remote` 플래그를 추가하면 실제 Cloudflare D1 데이터베이스에 적용됩니다.

### 2단계: CSV 데이터 로드

```powershell
# 프로젝트 루트로 이동
cd C:\Users\malgn\Desktop\malgpt

# CSV 데이터를 SQL 파일로 변환
python worker/scripts/load_data.py
```

이 명령어는:
- CSV 파일을 읽어서
- 임베딩을 생성하고
- `worker/scripts/insert_data.sql` 파일을 생성합니다

### 3단계: 로컬 D1에 데이터 삽입 (테스트)

```powershell
# worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 로컬 D1에 데이터 삽입 (테스트용)
npx wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
```

### 4단계: 원격(프로덕션) D1에 데이터 삽입

```powershell
# worker 폴더에서
npx wrangler d1 execute chatbot-db --remote --file=scripts/insert_data.sql
```

**주의**: 데이터가 많으면 시간이 걸릴 수 있습니다.

### 5단계: Workers 배포

```powershell
# worker 폴더에서
npx wrangler deploy
```

배포 성공 시 Workers URL이 표시됩니다.

### 6단계: Cloudflare Pages 환경 변수 설정

1. Cloudflare Pages → Settings → Environment variables
2. `BACKEND_URL`: Workers URL 입력

### 7단계: 테스트 🎉

Cloudflare Pages URL에서 채팅 테스트!

---

## 🔍 로컬 vs 원격

- **로컬 (`--file=...`)**: 개발/테스트용 로컬 D1
- **원격 (`--remote --file=...`)**: 실제 Cloudflare D1 (프로덕션)

**프로덕션 배포 시에는 반드시 `--remote` 플래그를 사용하세요!**

---

## 📋 빠른 명령어 모음

```powershell
# 1. 원격 D1 스키마 생성
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler d1 execute chatbot-db --remote --file=scripts/setup_d1.sql

# 2. CSV 데이터 로드 (프로젝트 루트에서)
cd C:\Users\malgn\Desktop\malgpt
python worker/scripts/load_data.py

# 3. 원격 D1에 데이터 삽입 (worker 폴더에서)
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler d1 execute chatbot-db --remote --file=scripts/insert_data.sql

# 4. Workers 배포
npx wrangler deploy
```

---

**좋습니다! 이제 원격 D1에도 스키마를 생성하고 데이터를 로드하세요! 🚀**

