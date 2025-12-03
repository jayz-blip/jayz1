# 자동 배포 가이드

## ⚠️ 현재 상황

Node.js가 설치되어 있지 않아 명령어로 배포할 수 없습니다.

## ✅ Cloudflare 대시보드에서 직접 배포

### 단계별 가이드

1. **Cloudflare 대시보드 접속**:
   - https://dash.cloudflare.com/
   - 로그인

2. **Workers 프로젝트로 이동**:
   - 왼쪽 메뉴에서 **"Workers & Pages"** 클릭
   - **"Workers"** 탭 클릭
   - **`chatbot-api`** 프로젝트 클릭

3. **코드 편집**:
   - 상단 탭에서 **"배포"** (Deployment) 클릭
   - 오른쪽 상단의 **"</> 코드 편집"** 버튼 클릭
   - 또는 **"Quick edit"** 버튼 클릭

4. **코드 붙여넣기**:
   - **`DEPLOY_CODE_HERE.txt`** 파일을 열기
   - 전체 코드 복사 (===== 사이의 코드만)
   - Cloudflare 에디터에 붙여넣기
   - 기존 코드를 모두 삭제하고 새 코드로 교체

5. **저장 및 배포**:
   - 오른쪽 상단의 **"저장 및 배포"** (Save and Deploy) 버튼 클릭
   - 또는 **Ctrl+S** (Windows) / **Cmd+S** (Mac)
   - 배포 완료 대기 (1-2분)

6. **배포 확인**:
   - 배포 완료 메시지 확인
   - **"방문"** (Visit) 버튼 클릭하여 테스트

## 🧪 테스트

배포 후:

1. **브라우저에서 접속**:
   - `https://chatbot-api.jayz-407.workers.dev/api/chat`
   - JSON 응답이 표시되어야 합니다

2. **응답 확인**:
   ```json
   {
     "message": "Workers 정상 작동 중",
     "status": "ok",
     "path": "/api/chat",
     "method": "GET"
   }
   ```

## 📋 체크리스트

- [ ] Cloudflare 대시보드 접속
- [ ] chatbot-api 프로젝트 선택
- [ ] 코드 편집 버튼 클릭
- [ ] DEPLOY_CODE_HERE.txt에서 코드 복사
- [ ] 에디터에 붙여넣기
- [ ] 저장 및 배포
- [ ] 배포 완료 확인
- [ ] 테스트

## 💡 중요 팁

1. **코드 복사 시 주의**:
   - `=====` 표시는 복사하지 마세요
   - Python 코드만 복사하세요

2. **기존 코드 삭제**:
   - 기존 코드를 모두 삭제하고 새 코드로 교체하세요

3. **저장 확인**:
   - 저장 후 배포가 자동으로 시작됩니다
   - 배포 완료까지 1-2분 소요됩니다

---

**지금 바로 Cloudflare 대시보드에서 배포하세요!**

**`DEPLOY_CODE_HERE.txt` 파일의 코드를 복사하여 붙여넣으세요!**

