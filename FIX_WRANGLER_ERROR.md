# Wrangler 파일 경로 오류 해결 방법

## 🔍 문제 분석

오류 메시지:
```
X [ERROR] Unable to read SQL text file "scripts/setup_d1.sql"
```

**원인**: 
1. `worker` 폴더에서 실행하지 않았거나
2. Node.js가 PATH에 추가되지 않았거나
3. PowerShell을 재시작하지 않았습니다

## ✅ 해결 방법

### 1단계: PowerShell 재시작 (필수!)

Node.js를 설치한 후 **반드시 PowerShell을 완전히 종료하고 다시 시작**해야 합니다.

1. 현재 PowerShell 창 닫기
2. 새 PowerShell 창 열기
3. 다음 명령어로 확인:
   ```powershell
   node --version
   npm --version
   ```

### 2단계: worker 폴더로 이동

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
```

### 3단계: 파일 경로 확인

```powershell
Test-Path scripts\setup_d1.sql
```

`True`가 나와야 합니다.

### 4단계: D1 스키마 생성

**방법 1: npx 사용 (권장)**
```powershell
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

**방법 2: npm run 스크립트 사용**
```powershell
npm run d1:prod -- --file=scripts/setup_d1.sql
```

**방법 3: 로컬 wrangler 사용**
```powershell
.\node_modules\.bin\wrangler.cmd d1 execute chatbot-db --file=scripts/setup_d1.sql
```

## 📋 전체 명령어 순서

```powershell
# 1. PowerShell 재시작 후
# 2. worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 3. Node.js 확인
node --version
npm --version

# 4. wrangler 설치 확인 (필요시)
npm install

# 5. D1 스키마 생성
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

## ⚠️ 주의사항

1. **반드시 `worker` 폴더에서 실행**: `wrangler.toml` 파일이 있는 폴더여야 합니다.

2. **절대 경로 사용 가능**:
   ```powershell
   npx wrangler d1 execute chatbot-db --file=C:\Users\malgn\Desktop\malgpt\worker\scripts\setup_d1.sql
   ```

3. **PowerShell 재시작**: Node.js 설치 후 반드시 재시작해야 PATH가 업데이트됩니다.

## 🔄 대안: 전역 설치

로컬 설치가 계속 문제가 되면 전역 설치를 시도하세요:

```powershell
npm install -g wrangler
wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

단, 이 경우에도 `worker` 폴더에서 실행해야 합니다.

