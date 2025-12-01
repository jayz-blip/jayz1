# Workers 로그 활성화 가이드

## 🔍 문제

**Workers 로그가 "사용 안 함" (Disabled) 상태입니다.**

로그를 확인하려면 먼저 로그를 활성화해야 합니다.

## ✅ 해결 방법

### 방법 1: wrangler.toml에 설정 추가 (권장)

`wrangler.toml` 파일에 다음을 추가했습니다:

```toml
[observability]
enabled = true
```

이제 Workers를 재배포하면 로그가 활성화됩니다.

### 방법 2: Cloudflare 대시보드에서 활성화

1. **Cloudflare 대시보드** → **Workers & Pages** → **Workers**
2. **`chatbot-api` 프로젝트** 클릭
3. **"관찰 가능성"** (Observability) 탭 클릭
4. **"Workers 로그"** 옆의 **연필 아이콘** 클릭
5. **활성화** (Enable) 선택
6. **저장**

## 🚀 다음 단계

### 1단계: Workers 재배포

`wrangler.toml`을 수정했으니 Workers를 재배포해야 합니다:

```powershell
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler deploy
```

### 2단계: 로그 활성화 확인

재배포 후:
1. **Cloudflare 대시보드** → **Workers & Pages** → **Workers**
2. **`chatbot-api` 프로젝트** 클릭
3. **"관찰 가능성"** 탭 클릭
4. **"Workers 로그"** 상태 확인:
   - ✅ **"사용 중"** (Enabled): 정상
   - ❌ **"사용 안 함"** (Disabled): 여전히 비활성화

### 3단계: 로그 확인

로그가 활성화되면:
1. **"관찰 가능성"** 탭에서 **로그 확인**
2. **최근 오류 메시지 확인**
3. **오류 메시지 복사**

## 📋 체크리스트

- [ ] `wrangler.toml`에 `[observability] enabled = true` 추가 완료
- [ ] Workers 재배포
- [ ] 로그 활성화 확인
- [ ] 로그에서 오류 메시지 확인

## 🔍 로그가 여전히 보이지 않으면

### 방법 1: Tail Worker 사용

1. **"관찰 가능성"** 탭에서
2. **"Tail Worker"** → **"연결"** 버튼 클릭
3. **실시간 로그 확인**

### 방법 2: Logpush 사용

1. **"관찰 가능성"** 탭에서
2. **"Logpush"** → **"사용"** 버튼 클릭
3. **로그 설정**

---

**Workers를 재배포하면 로그가 활성화됩니다!**

**재배포 후 로그를 확인하세요!**

