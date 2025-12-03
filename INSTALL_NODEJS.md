# Node.js 설치 가이드

## ❌ 현재 상태

**Node.js가 설치되어 있지 않습니다.**

Workers를 재배포하려면 Node.js가 필요합니다.

## ✅ Node.js 설치 방법

### 방법 1: 공식 웹사이트에서 다운로드 (권장)

1. **Node.js 공식 웹사이트 접속**:
   - https://nodejs.org/
   - 또는 https://nodejs.org/ko (한국어)

2. **LTS 버전 다운로드**:
   - "LTS" 버전 선택 (안정적인 버전)
   - 예: `v20.x.x` 또는 `v22.x.x`

3. **설치 프로그램 실행**:
   - 다운로드한 `.msi` 파일 실행
   - **중요**: 설치 중 **"Add to PATH"** 옵션 체크 필수!

4. **설치 완료 확인**:
   - PowerShell을 **완전히 종료**하고 다시 열기
   - 다음 명령어 실행:
     ```powershell
     node --version
     npm --version
     ```
   - 버전 번호가 표시되면 설치 완료!

### 방법 2: Chocolatey 사용 (고급 사용자)

```powershell
choco install nodejs-lts
```

## 🚀 설치 후 Workers 재배포

Node.js 설치가 완료되면:

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

## 📋 체크리스트

- [ ] Node.js 다운로드
- [ ] 설치 프로그램 실행
- [ ] "Add to PATH" 옵션 체크
- [ ] PowerShell 재시작
- [ ] `node --version` 확인
- [ ] `npm --version` 확인
- [ ] Workers 재배포

## 💡 팁

1. **PowerShell 재시작**: 설치 후 반드시 PowerShell을 완전히 종료하고 다시 열어야 합니다.

2. **PATH 확인**: 만약 `node` 명령어가 작동하지 않으면:
   - 환경 변수 PATH에 Node.js가 추가되었는지 확인
   - 또는 컴퓨터 재시작

3. **버전 확인**: 
   - `node --version`: Node.js 버전 확인
   - `npm --version`: npm 버전 확인

---

**Node.js를 설치한 후 Workers를 재배포하세요!**

