# Node.js 설치 가이드

## 오류: npm이 인식되지 않음

이 오류는 Node.js가 설치되지 않았거나 PATH에 추가되지 않았을 때 발생합니다.

## 해결 방법

### 방법 1: Node.js 설치 확인

PowerShell에서:
```powershell
node --version
```

**결과가 나오면**: Node.js가 설치되어 있습니다. PATH 문제일 수 있습니다.
**오류가 나면**: Node.js를 설치해야 합니다.

### 방법 2: Node.js 설치

1. **Node.js 공식 사이트 접속**
   - https://nodejs.org 접속
   - **LTS 버전** 다운로드 (권장)

2. **설치**
   - 다운로드한 `.msi` 파일 실행
   - 기본 설정으로 설치 (Next 클릭)
   - **중요**: "Add to PATH" 옵션이 체크되어 있는지 확인

3. **PowerShell 재시작**
   - 설치 후 PowerShell을 완전히 종료
   - 새 PowerShell 창 열기

4. **확인**
   ```powershell
   node --version
   npm --version
   ```
   
   둘 다 버전이 나오면 성공!

### 방법 3: PATH 수동 추가 (이미 설치되어 있는 경우)

1. **Node.js 설치 경로 확인**
   ```powershell
   where.exe node
   ```
   
   일반적인 경로:
   - `C:\Program Files\nodejs\`
   - `C:\Users\사용자명\AppData\Roaming\npm\`

2. **환경 변수에 추가**
   - Windows 검색에서 "환경 변수" 검색
   - "시스템 환경 변수 편집" 클릭
   - "환경 변수" 버튼 클릭
   - "Path" 선택 → "편집"
   - "새로 만들기" 클릭
   - Node.js 경로 추가 (예: `C:\Program Files\nodejs\`)
   - 확인 클릭
   - PowerShell 재시작

---

## 빠른 설치 (Chocolatey 사용)

Chocolatey가 설치되어 있다면:

```powershell
choco install nodejs-lts
```

---

## 설치 후 확인

```powershell
# Node.js 버전 확인
node --version

# npm 버전 확인
npm --version

# 둘 다 버전이 나오면 성공!
```

---

## 설치 후 프론트엔드 실행

```powershell
cd C:\Users\malgn\Desktop\malgpt
npm install
npm run dev
```

---

## 문제 해결

### 여전히 npm이 인식되지 않으면

1. **PowerShell 완전히 종료 후 재시작**
2. **컴퓨터 재시작** (가장 확실한 방법)
3. **설치 경로 확인**: `C:\Program Files\nodejs\`에 `node.exe`와 `npm.cmd`가 있는지 확인

### 다른 PowerShell 창에서 시도

새 PowerShell 창을 열어서 다시 시도해보세요.

