# Wrangler CLI 설치 가이드

## 사전 준비: Node.js 설치

Wrangler CLI는 Node.js가 필요합니다. 먼저 Node.js가 설치되어 있는지 확인하세요.

### Node.js 설치 확인

PowerShell에서:
```powershell
node --version
npm --version
```

**버전이 나오면**: Node.js가 설치되어 있습니다. 다음 단계로 진행하세요.
**오류가 나면**: Node.js를 먼저 설치해야 합니다.

---

## Node.js 설치 (필요한 경우)

### 방법 1: 공식 사이트에서 설치 (권장)

1. **Node.js 공식 사이트 접속**
   - https://nodejs.org 접속
   - **LTS 버전** 다운로드 (왼쪽 버튼, 권장)
   - 예: `node-v20.x.x-x64.msi`

2. **설치 실행**
   - 다운로드한 `.msi` 파일 더블클릭
   - "Next" 클릭하여 기본 설정으로 설치
   - **중요**: "Add to PATH" 옵션이 체크되어 있는지 확인

3. **PowerShell 재시작**
   - 설치 완료 후 PowerShell을 완전히 종료
   - 새 PowerShell 창 열기

4. **설치 확인**
   ```powershell
   node --version
   npm --version
   ```
   
   둘 다 버전이 나오면 성공!

### 방법 2: Chocolatey 사용 (선택사항)

Chocolatey가 설치되어 있다면:

```powershell
choco install nodejs-lts
```

---

## Wrangler CLI 설치

### 1단계: 전역 설치

PowerShell에서:

```powershell
npm install -g wrangler
```

**설치 시간**: 1-2분 정도 소요됩니다.

### 2단계: 설치 확인

```powershell
wrangler --version
```

버전이 나오면 설치 성공!

예시 출력:
```
wrangler 3.x.x
```

---

## Wrangler 로그인

### 1단계: 로그인 명령어 실행

```powershell
wrangler login
```

### 2단계: 브라우저에서 인증

1. 명령어 실행 시 브라우저가 자동으로 열립니다
2. Cloudflare 계정으로 로그인
3. "Allow" 클릭하여 권한 부여

### 3단계: 로그인 확인

```powershell
wrangler whoami
```

로그인된 계정 정보가 표시되면 성공!

---

## 설치 문제 해결

### 문제 1: npm이 인식되지 않음

**원인**: Node.js가 설치되지 않았거나 PATH에 추가되지 않음

**해결**:
1. Node.js 재설치 (위의 Node.js 설치 방법 참고)
2. PowerShell 재시작
3. 컴퓨터 재시작 (필요한 경우)

### 문제 2: 권한 오류 (EACCES)

**오류 메시지**:
```
npm ERR! Error: EACCES: permission denied
```

**해결 방법 1: 관리자 권한으로 실행**
1. PowerShell을 관리자 권한으로 실행
2. 다시 설치 시도

**해결 방법 2: npm 전역 경로 변경**
```powershell
# npm 전역 경로 확인
npm config get prefix

# 전역 경로를 사용자 폴더로 변경
npm config set prefix "$env:APPDATA\npm"

# PATH에 추가 (PowerShell 프로필에 추가)
$env:Path += ";$env:APPDATA\npm"
```

### 문제 3: 설치가 너무 느림

**해결**:
```powershell
# npm 레지스트리를 한국 미러로 변경
npm config set registry https://registry.npmmirror.com

# 설치
npm install -g wrangler

# 원래대로 복구 (선택사항)
npm config set registry https://registry.npmjs.org
```

### 문제 4: wrangler 명령어가 인식되지 않음

**원인**: PATH에 npm 전역 경로가 추가되지 않음

**해결**:
1. npm 전역 경로 확인:
   ```powershell
   npm config get prefix
   ```

2. 출력된 경로를 환경 변수 PATH에 추가:
   - Windows 검색에서 "환경 변수" 검색
   - "시스템 환경 변수 편집" 클릭
   - "환경 변수" 버튼 클릭
   - "Path" 선택 → "편집"
   - "새로 만들기" 클릭
   - npm 전역 경로 추가 (예: `C:\Users\사용자명\AppData\Roaming\npm`)
   - 확인 클릭
   - PowerShell 재시작

---

## 설치 확인 체크리스트

설치가 완료되었는지 확인:

- [ ] `node --version` 실행 시 버전 표시
- [ ] `npm --version` 실행 시 버전 표시
- [ ] `npm install -g wrangler` 실행 성공
- [ ] `wrangler --version` 실행 시 버전 표시
- [ ] `wrangler login` 실행 성공
- [ ] `wrangler whoami` 실행 시 계정 정보 표시

---

## 다음 단계

Wrangler CLI 설치가 완료되면:

1. **D1 스키마 생성**
   ```powershell
   cd worker
   wrangler d1 execute chatbot-db --file=scripts/setup_d1.sql
   ```

2. **데이터 로드**
   ```powershell
   python scripts/load_data.py
   wrangler d1 execute chatbot-db --file=scripts/insert_data.sql
   ```

3. **Workers 배포**
   ```powershell
   npm install
   wrangler deploy
   ```

자세한 내용은 `worker/DEPLOY_STEPS.md` 참고!

