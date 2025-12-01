# 줄바꿈 문자 오류 해결

## 🔴 문제 발견!

**Network 탭 Response를 보니**:

```json
{
  "backendUrl": "https://chatbot-api.jayz-407.workers.dev\n",  ← 줄바꿈 문자!
  "apiUrl": "https://chatbot-api.jayz-407.workers.dev\n/api/chat"  ← 줄바꿈 문자!
}
```

**문제**: `backendUrl`에 줄바꿈 문자(`\n`)가 포함되어 있습니다!

이것이 Workers URL을 잘못된 형식으로 만들어서 Error 1101을 발생시키고 있습니다.

## ✅ 해결 방법

### 1단계: Cloudflare Pages 환경 변수 수정

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **`BACKEND_URL` 변수 클릭** (또는 편집)
3. **값 필드 확인**:
   - 현재: `https://chatbot-api.jayz-407.workers.dev` (줄바꿈 포함)
   - 수정: `https://chatbot-api.jayz-407.workers.dev` (줄바꿈 제거)

4. **값을 완전히 삭제하고 다시 입력**:
   - 전체 선택 (Ctrl + A)
   - 삭제
   - **정확히 입력**: `https://chatbot-api.jayz-407.workers.dev`
   - **마지막에 공백이나 줄바꿈이 없는지 확인**

5. **"저장" 버튼 클릭**

### 2단계: 값 확인

저장 후 다시 확인:
- ✅ 올바른 값: `https://chatbot-api.jayz-407.workers.dev`
- ❌ 잘못된 값: `https://chatbot-api.jayz-407.workers.dev\n` (줄바꿈 포함)

### 3단계: 재배포 대기

- 환경 변수를 저장하면 자동으로 재배포가 시작됩니다
- 배포 완료까지 **2-5분** 대기

### 4단계: 테스트

재배포 완료 후:
1. **브라우저 캐시 삭제** (Ctrl + Shift + Delete)
2. **페이지 새로고침** (Ctrl + F5)
3. **채팅 테스트**

## 🔍 줄바꿈이 생기는 이유

1. **복사/붙여넣기 시**: 줄바꿈이 포함될 수 있음
2. **여러 줄 입력**: 실수로 Enter 키를 눌렀을 수 있음
3. **텍스트 에디터**: 일부 에디터가 줄바꿈을 추가할 수 있음

## 📋 확인 체크리스트

- [ ] 환경 변수 값에서 줄바꿈 제거
- [ ] 값 끝에 공백이나 줄바꿈이 없는지 확인
- [ ] 정확한 값 입력: `https://chatbot-api.jayz-407.workers.dev`
- [ ] 저장
- [ ] 재배포 대기
- [ ] 테스트

## 🚀 빠른 해결

1. **Cloudflare Pages** → **Settings** → **Environment variables**
2. **`BACKEND_URL` 편집**
3. **전체 선택 후 삭제** (Ctrl + A → Delete)
4. **다시 입력**: `https://chatbot-api.jayz-407.workers.dev`
5. **저장**
6. **재배포 대기**

---

**이것이 문제의 원인입니다! 줄바꿈을 제거하면 해결될 것입니다! 🎯**

