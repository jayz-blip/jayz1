# 환경 변수 설정 가이드

## 📍 환경 변수는 두 곳에 설정해야 합니다!

### 1️⃣ Cloudflare Workers (`chatbot-api`) - 백엔드용

**설정 위치**: Workers 프로젝트 (`chatbot-api`)

**설정해야 할 환경 변수**:
- `OPENAI_API_KEY` (선택사항): OpenAI API 키

**설정 방법**:

#### 방법 1: Cloudflare 대시보드에서 설정 (권장)

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com

2. **Workers & Pages** → **Workers** 클릭

3. **`chatbot-api` 프로젝트 선택**

4. **Settings** → **Variables** 클릭

5. **Add variable** 클릭
   - **Variable name**: `OPENAI_API_KEY`
   - **Value**: 실제 OpenAI API 키
   - **Encrypt** 체크 (보안)

6. **Save** 클릭

#### 방법 2: wrangler 명령어로 설정

```powershell
# worker 폴더에서
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler secret put OPENAI_API_KEY
```

실행하면 API 키를 입력하라는 프롬프트가 나타납니다.

---

### 2️⃣ Cloudflare Pages (프론트엔드) - 프론트엔드용

**설정 위치**: Pages 프로젝트 (예: `jayz1`)

**설정해야 할 환경 변수**:
- `BACKEND_URL`: Workers URL (예: `https://chatbot-api.your-subdomain.workers.dev`)

**설정 방법**:

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com

2. **Workers & Pages** → **Pages** 클릭

3. **프로젝트 선택** (예: `jayz1`)

4. **Settings** → **Environment variables** 클릭

5. **Add variable** 클릭
   - **Variable name**: `BACKEND_URL`
   - **Value**: Workers URL (예: `https://chatbot-api.your-subdomain.workers.dev`)
   - **Environment**: Production, Preview, Development 모두 선택 가능

6. **Save** 클릭

7. **중요**: 환경 변수를 추가한 후 **재배포**가 필요할 수 있습니다.

---

## 📋 환경 변수 정리

### Workers (`chatbot-api`) 프로젝트
| 변수명 | 설명 | 필수 여부 |
|--------|------|----------|
| `OPENAI_API_KEY` | OpenAI API 키 | 선택사항 |

### Pages (프론트엔드) 프로젝트
| 변수명 | 설명 | 필수 여부 |
|--------|------|----------|
| `BACKEND_URL` | Workers URL | **필수** |

---

## 🔍 Workers URL 찾기

Workers URL을 모르겠다면:

1. **Cloudflare 대시보드** → **Workers & Pages** → **Workers**
2. **`chatbot-api` 프로젝트** 클릭
3. 상단에 표시된 URL 복사

또는 배포 시 표시된 URL을 사용하세요.

---

## ⚠️ 중요 사항

1. **Workers 환경 변수**: 백엔드(Workers)에서 사용
2. **Pages 환경 변수**: 프론트엔드(Pages)에서 사용
3. **`BACKEND_URL`은 Pages 프로젝트에 설정해야 합니다!**
4. 환경 변수 추가 후 재배포가 필요할 수 있습니다.

---

## 🚀 빠른 설정 순서

### 1단계: Workers 환경 변수 설정 (선택사항)

```powershell
# worker 폴더에서
cd C:\Users\malgn\Desktop\malgpt\worker
npx wrangler secret put OPENAI_API_KEY
```

### 2단계: Pages 환경 변수 설정 (필수)

1. Cloudflare 대시보드 → Pages → 프로젝트 선택
2. Settings → Environment variables
3. `BACKEND_URL` 추가 (Workers URL 입력)

---

**`BACKEND_URL`은 Pages 프로젝트에 설정하세요! Workers가 아닙니다! 🎯**

