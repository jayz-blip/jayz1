# Cloudflare Pages 수동 재배포 가이드

## 🚀 수동 재배포 방법

### 방법 1: Cloudflare 대시보드에서 재배포 (가장 쉬움)

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com

2. **Pages** → **프로젝트 선택**
   - 왼쪽 메뉴에서 "Workers & Pages" 클릭
   - "Pages" 탭 클릭
   - 프로젝트 선택 (예: `jayz1`)

3. **"배포" (Deployments) 탭 클릭**
   - 상단 메뉴에서 "배포" 또는 "Deployments" 클릭

4. **최신 배포 찾기**
   - 최상단에 최신 배포가 표시됨
   - 상태 확인:
     - ✅ **성공**: 녹색 체크 표시
     - ⏳ **진행 중**: 노란색 진행 표시
     - ❌ **실패**: 빨간색 X 표시

5. **재배포 실행**
   - 최신 배포의 **"..." (더보기) 메뉴** 클릭
   - **"재배포" (Redeploy)** 또는 **"Retry deployment"** 선택
   - 또는 **"새 배포" (Create deployment)** 버튼 클릭

### 방법 2: Git 커밋으로 자동 재배포

Cloudflare Pages는 Git 저장소와 연결되어 있으면 자동으로 재배포됩니다:

1. **작은 변경사항 커밋**
   ```powershell
   git commit --allow-empty -m "Trigger redeploy"
   git push origin main
   ```

2. **자동 재배포 대기**
   - Cloudflare Pages가 자동으로 변경사항을 감지
   - 새로운 배포 시작

### 방법 3: GitHub에서 재배포 트리거

1. **GitHub 저장소 접속**
   - https://github.com/jayz-blip/jayz1

2. **Actions 탭 클릭** (있는 경우)
   - 또는 Cloudflare Pages가 자동으로 감지

3. **수동으로 웹훅 트리거** (필요시)
   - GitHub → Settings → Webhooks
   - Cloudflare Pages 웹훅 확인

## 📋 재배포 확인 방법

### 1. 배포 상태 확인

1. **Cloudflare Pages** → **프로젝트** → **"배포" (Deployments) 탭**
2. **최신 배포 확인**:
   - 상태: 성공/실패/진행 중
   - 시간: 배포 시작/완료 시간
   - 커밋: 어떤 커밋에서 배포되었는지

### 2. 배포 완료 대기

- 배포는 보통 **2-5분** 정도 소요됩니다
- 배포가 완료되면 상태가 "성공"으로 변경됩니다

### 3. 배포 완료 후 테스트

1. **Cloudflare Pages URL 접속**
   - 예: `https://jayz1.pages.dev`

2. **채팅 기능 테스트**
   - 메시지 전송
   - 응답 확인

3. **브라우저 캐시 삭제** (필요시)
   - Ctrl + Shift + Delete
   - 캐시 삭제 후 새로고침

## ⚠️ 주의사항

### 환경 변수 변경 후

- 환경 변수를 변경하면 **자동으로 재배포가 시작됩니다**
- 재배포가 완료될 때까지 **몇 분 대기**해야 합니다
- 배포 상태는 "배포" 탭에서 확인할 수 있습니다

### 재배포 중

- 재배포 중에는 이전 버전이 계속 작동합니다
- 재배포가 완료되면 새 버전으로 자동 전환됩니다

## 🔍 배포 상태 확인

### 성공적인 배포

- 상태: ✅ **성공** (녹색)
- 메시지: "Deployment successful"
- URL: 정상 작동

### 실패한 배포

- 상태: ❌ **실패** (빨간색)
- 메시지: 오류 메시지 표시
- 로그: 배포 로그 확인 가능

## 🚀 빠른 재배포 방법

**가장 간단한 방법**:
1. Cloudflare Pages → 프로젝트 → "배포" 탭
2. 최신 배포의 "..." 메뉴 클릭
3. "재배포" 선택

또는:

```powershell
git commit --allow-empty -m "Trigger redeploy"
git push origin main
```

---

**환경 변수를 저장하면 자동으로 재배포가 시작됩니다!**

**배포 상태는 "배포" 탭에서 확인하세요.**

