# Node.js 설치 후 다음 단계

## ⚠️ 중요: PowerShell 재시작 필요!

Node.js를 설치한 후 **반드시 PowerShell을 완전히 종료하고 다시 시작**해야 합니다.

## ✅ 확인 단계

### 1단계: PowerShell 재시작

1. **현재 PowerShell 창을 완전히 닫기**
2. **새 PowerShell 창 열기**
3. 다음 명령어로 확인:

```powershell
node --version
npm --version
```

**예상 결과**:
```
v20.x.x
10.x.x
```

### 2단계: worker 폴더로 이동

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
```

### 3단계: wrangler 설치 확인

```powershell
# 로컬에 설치되어 있는지 확인
npm list wrangler

# 없으면 설치
npm install
```

### 4단계: D1 스키마 생성

```powershell
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

## 📋 전체 명령어 (PowerShell 재시작 후)

```powershell
# 1. Node.js 확인
node --version
npm --version

# 2. worker 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\worker

# 3. wrangler 설치 (필요시)
npm install

# 4. D1 스키마 생성
npx wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
```

## 🔍 문제 해결

### Node.js가 여전히 인식되지 않는 경우

1. **설치 확인**:
   - Windows 검색에서 "Node.js" 검색
   - 설치되어 있는지 확인

2. **수동 PATH 추가** (필요시):
   ```powershell
   # Node.js 설치 경로 확인 (일반적으로)
   # C:\Program Files\nodejs
   
   # 환경 변수에 추가
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\nodejs", "User")
   ```

3. **설치 프로그램 재실행**:
   - Node.js 설치 프로그램 다시 실행
   - "Repair" 옵션 선택

## 🎯 다음 단계 (스키마 생성 후)

1. ✅ D1 스키마 생성
2. 📊 CSV 데이터 로드
3. 🚀 Workers 배포
4. 🔗 Cloudflare Pages 환경 변수 설정

---

**지금 바로 PowerShell을 재시작하고 위 명령어를 실행해보세요!**

