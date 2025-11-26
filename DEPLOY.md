# GitHub 업로드 가이드

## GitHub 레포지토리 생성 및 업로드

### 1. GitHub에서 새 레포지토리 생성
1. GitHub에 로그인
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 레포지토리 이름 입력 (예: `company-chatbot`)
4. Public 또는 Private 선택
5. "Create repository" 클릭

### 2. 로컬 저장소를 GitHub에 연결

터미널에서 다음 명령어 실행:

```bash
# 원격 저장소 추가 (YOUR_USERNAME과 YOUR_REPO_NAME을 실제 값으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 메인 브랜치 이름 설정 (필요한 경우)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3. 인증
- GitHub에서 Personal Access Token이 필요할 수 있습니다
- Settings → Developer settings → Personal access tokens → Tokens (classic)
- `repo` 권한으로 토큰 생성 후 사용

## 대안: GitHub CLI 사용

```bash
# GitHub CLI 설치 후
gh repo create company-chatbot --public --source=. --remote=origin --push
```

