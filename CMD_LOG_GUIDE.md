# CMD 창에서 오류 메시지 확인 가이드

## 기본 확인 방법

### 1. 백엔드 실행 중인 CMD 창 확인

백엔드를 실행한 CMD 창을 그대로 보면 됩니다!

```bash
cd backend
python main.py
```

**실행하면 다음과 같은 로그가 나타납니다:**

#### 정상 실행 시:
```
데이터 로딩 중...
원글 데이터: 1234개 로드됨
댓글 데이터: 5678개 로드됨
총 6912개 문서 벡터화 중...
진행률: 100/6912
...
진행률: 6900/6912
데이터 로딩 완료!
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 질문을 보낼 때:
```
2025-11-27 00:45:30 - __main__ - INFO - 📩 받은 질문: 담당자 변경 방법
2025-11-27 00:45:32 - __main__ - INFO - ✅ 응답 생성 완료 (소스 개수: 3)
```

#### 오류 발생 시:
```
2025-11-27 00:45:30 - __main__ - ERROR - ❌ 오류 발생: 'NoneType' object has no attribute 'query'
Traceback (most recent call last):
  File "C:\Users\malgn\Desktop\malgpt\backend\main.py", line 40, in chat
    response, sources = rag_system.query(request.message)
  ...
```

---

## 오류 메시지 읽는 방법

### 1. 오류 타입 확인

CMD 창에서 빨간색으로 표시되는 부분을 찾으세요:

```
ERROR - ❌ 오류 발생: [오류 내용]
```

### 2. 오류 위치 확인

`Traceback` 다음에 나오는 내용:
```
File "C:\Users\malgn\Desktop\malgpt\backend\main.py", line 40, in chat
```
- 파일 경로와 줄 번호를 알려줍니다
- 어떤 함수에서 오류가 났는지 알려줍니다

### 3. 오류 원인 확인

마지막 줄의 오류 메시지:
```
'NoneType' object has no attribute 'query'
```
- 이것이 실제 오류 원인입니다

---

## CMD 창에서 로그를 더 잘 보는 방법

### 방법 1: CMD 창 크기 조절

1. CMD 창 제목 표시줄 우클릭
2. **속성** 클릭
3. **레이아웃** 탭에서:
   - 화면 버퍼 크기 높이: `9999` (스크롤 가능)
   - 창 크기 높이: `50` (더 많이 보이게)

### 방법 2: 스크롤해서 이전 로그 확인

- CMD 창에서 **마우스 휠**로 위로 스크롤
- 또는 **상단 바**를 드래그해서 위로 올리기

### 방법 3: 로그를 파일로 저장

백엔드 실행 시 로그를 파일로 저장:

```bash
cd backend
python main.py > ../backend.log 2>&1
```

그러면 `backend.log` 파일에 모든 로그가 저장됩니다.

**로그 파일 확인:**
```bash
# 다른 CMD 창에서
type backend.log
# 또는 메모장으로 열기
notepad backend.log
```

### 방법 4: 실시간으로 로그 파일 보기 (PowerShell)

```powershell
# PowerShell에서
Get-Content backend.log -Wait -Tail 50
```

이렇게 하면 로그가 실시간으로 업데이트되면서 보입니다.

---

## 일반적인 오류 메시지와 의미

### 1. `ModuleNotFoundError: No module named 'xxx'`
**의미**: 필요한 패키지가 설치되지 않음
**해결**: `pip install -r requirements.txt` 실행

### 2. `FileNotFoundError: [Errno 2] No such file or directory: 'xxx.csv'`
**의미**: CSV 파일을 찾을 수 없음
**해결**: CSV 파일이 프로젝트 루트에 있는지 확인

### 3. `'NoneType' object has no attribute 'xxx'`
**의미**: None 값에 대해 메서드를 호출하려고 함
**해결**: 변수가 제대로 초기화되었는지 확인

### 4. `Connection refused` 또는 `[Errno 111] Connection refused`
**의미**: 포트가 이미 사용 중이거나 서버가 실행되지 않음
**해결**: 
- 다른 프로그램이 8000번 포트를 사용하는지 확인
- `netstat -ano | findstr :8000` 으로 확인

### 5. `chromadb.errors.InvalidCollectionException`
**의미**: ChromaDB 컬렉션이 없거나 손상됨
**해결**: `chroma_db` 폴더 삭제 후 재실행

---

## 오류 메시지 복사하는 방법

### 방법 1: 마우스로 선택

1. CMD 창에서 오류 메시지 부분을 **마우스로 드래그**해서 선택
2. **Enter 키**를 누르면 클립보드에 복사됨
3. 메모장이나 채팅창에 **Ctrl+V**로 붙여넣기

### 방법 2: 전체 화면 복사

1. CMD 창에서 **우클릭**
2. **모두 선택** 클릭
3. **Enter 키**로 복사
4. 메모장에 붙여넣기

---

## 디버깅 팁

### 1. 오류가 발생하면

1. **CMD 창의 오류 메시지 전체를 복사**
2. 특히 다음 정보를 확인:
   - 오류 타입 (ERROR, WARNING 등)
   - 오류 메시지 (마지막 줄)
   - 파일 경로와 줄 번호
   - Traceback 전체 내용

### 2. 백엔드가 시작되지 않을 때

```
ERROR:    [Errno 10048] Only one usage of each socket address
```

**의미**: 8000번 포트가 이미 사용 중
**해결**: 
```bash
# 포트 사용 중인 프로세스 확인
netstat -ano | findstr :8000

# 프로세스 종료 (PID는 위 명령어 결과에서 확인)
taskkill /PID [PID번호] /F
```

### 3. 데이터 로딩이 안 될 때

```
원글 데이터 로드 오류: [오류 내용]
댓글 데이터 로드 오류: [오류 내용]
```

**확인 사항**:
- CSV 파일이 프로젝트 루트에 있는지
- 파일 이름이 정확한지
- 파일 인코딩이 UTF-8인지

---

## 빠른 체크리스트

오류가 발생했을 때 확인할 것:

- [ ] 백엔드 CMD 창에서 오류 메시지 확인
- [ ] 오류 메시지 전체 복사
- [ ] 오류 타입 확인 (ERROR, Exception 등)
- [ ] 파일 경로와 줄 번호 확인
- [ ] Traceback 전체 내용 확인
- [ ] 브라우저 콘솔도 확인 (F12)

---

## 예시: 실제 오류 확인하기

1. **백엔드 실행**
   ```bash
   cd backend
   python main.py
   ```

2. **브라우저에서 질문 보내기**

3. **CMD 창 확인**
   - 질문이 보이면: `📩 받은 질문: ...`
   - 오류가 있으면: `❌ 오류 발생: ...`
   - 성공하면: `✅ 응답 생성 완료`

4. **오류 메시지 복사해서 공유**

이렇게 하면 문제를 빠르게 해결할 수 있습니다!

