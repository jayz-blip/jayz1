# 문제 해결 가이드

## 오류: ERR_CONNECTION_REFUSED

이 오류는 **백엔드가 실행되지 않았거나** 연결할 수 없을 때 발생합니다.

### 해결 방법

#### 1단계: 백엔드가 실행 중인지 확인

**새 CMD 창을 열고** 다음 명령어 실행:

```bash
cd C:\Users\malgn\Desktop\malgpt\backend
venv\Scripts\activate
python main.py
```

**정상 실행 시 다음과 같은 메시지가 나타납니다:**
```
데이터 로딩 중...
원글 데이터: X개 로드됨
댓글 데이터: X개 로드됨
데이터 로딩 완료!
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 2단계: 백엔드가 실행 중인지 테스트

브라우저에서 다음 URL 접속:
```
http://localhost:8000
```

다음과 같은 응답이 보여야 합니다:
```json
{"message":"사내용 채팅 AI API","status":"running"}
```

#### 3단계: 포트가 사용 중인지 확인

다른 CMD 창에서:
```bash
netstat -ano | findstr :8000
```

결과가 나오면 포트가 사용 중입니다. 결과가 없으면 백엔드가 실행되지 않은 것입니다.

---

## 백엔드 실행 체크리스트

- [ ] 가상환경이 활성화되었는가? (`(venv)` 표시 확인)
- [ ] `python main.py` 명령어를 실행했는가?
- [ ] "Uvicorn running on http://0.0.0.0:8000" 메시지가 보이는가?
- [ ] `http://localhost:8000` 접속 시 응답이 오는가?

---

## 단계별 실행 가이드

### 터미널 1: 백엔드 실행

```bash
# 1. 프로젝트 폴더로 이동
cd C:\Users\malgn\Desktop\malgpt\backend

# 2. 가상환경 활성화
venv\Scripts\activate

# 3. 백엔드 실행
python main.py
```

**이 창은 그대로 두세요!** 백엔드가 계속 실행되어야 합니다.

### 터미널 2: 프론트엔드 실행 (이미 실행 중이면 생략)

```bash
# 프로젝트 루트로 이동
cd C:\Users\malgn\Desktop\malgpt

# 프론트엔드 실행
npm run dev
```

---

## 일반적인 문제

### 문제 1: 포트 8000이 이미 사용 중

**오류 메시지:**
```
ERROR:    [Errno 10048] Only one usage of each socket address
```

**해결:**
```bash
# 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8000

# 프로세스 종료 (PID는 위 명령어 결과에서 확인)
taskkill /PID [PID번호] /F
```

### 문제 2: 백엔드가 바로 종료됨

**원인**: 데이터 로딩 중 오류 발생

**해결**: CMD 창의 오류 메시지를 확인하고 공유해주세요.

### 문제 3: 가상환경이 활성화되지 않음

**확인:**
```bash
# 가상환경 활성화
venv\Scripts\activate

# (venv)가 앞에 표시되는지 확인
(venv) C:\Users\malgn\Desktop\malgpt\backend>
```

---

## 빠른 테스트

1. **백엔드 실행 확인**
   - 브라우저에서 `http://localhost:8000` 접속
   - `{"message":"사내용 채팅 AI API","status":"running"}` 응답 확인

2. **프론트엔드에서 테스트**
   - `http://localhost:3000` 접속
   - 질문 입력 후 전송

---

## 여전히 안 되면

1. **백엔드 CMD 창의 오류 메시지 확인**
2. **브라우저 콘솔(F12)의 오류 메시지 확인**
3. **두 오류 메시지를 모두 공유해주세요**

