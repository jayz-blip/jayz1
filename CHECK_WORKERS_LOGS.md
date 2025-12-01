# Workers 로그 확인 가이드

## 🔍 Workers 로그 확인 방법

Workers가 Error 1101을 발생시키고 있으므로, 로그를 확인해야 정확한 원인을 알 수 있습니다.

## 📋 로그 확인 단계

### 1단계: Cloudflare 대시보드 접속

1. **Cloudflare 대시보드 접속**
   - https://dash.cloudflare.com

2. **Workers & Pages** → **Workers** 클릭

3. **`chatbot-api` 프로젝트** 클릭

### 2단계: 관찰 가능성 탭 확인

1. **"관찰 가능성"** (Observability) 탭 클릭

2. **로그 확인**:
   - 실시간 로그 (Real-time Logs)
   - 오류 로그 (Error Logs)
   - 추적 정보 (Traces)

### 3단계: 오류 로그 찾기

1. **최근 오류 메시지 확인**
2. **오류 발생 시간 확인**
3. **오류 메시지 복사**

## 🔍 확인할 정보

로그에서 다음 정보를 찾으세요:

1. **오류 메시지**:
   - 예: `AttributeError`, `TypeError`, `KeyError` 등
   - 정확한 오류 메시지

2. **Traceback**:
   - 오류 발생 위치
   - 함수 호출 스택

3. **요청 정보**:
   - 요청 URL
   - 요청 메서드
   - 요청 본문

## 📋 로그 예시

로그에서 다음과 같은 정보를 볼 수 있습니다:

```
Error: AttributeError: 'str' object has no attribute 'pathname'
Traceback:
  File "worker.py", line 36, in on_fetch
    path = url_obj.pathname
```

또는:

```
Error: D1 database binding not found
```

## 🚀 로그 확인 후

로그의 오류 메시지를 알려주시면:
1. 정확한 문제 파악
2. 코드 수정
3. 재배포

---

**가장 먼저 Workers 로그를 확인하세요!**

**"관찰 가능성" 탭에서 오류 메시지를 찾아 알려주세요!**

