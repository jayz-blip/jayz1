# PowerShell에서 백엔드 실행하기

## 현재 오류

```
ModuleNotFoundError: No module named 'fastapi'
```

이 오류는 가상환경을 활성화하지 않았거나 패키지가 설치되지 않았을 때 발생합니다.

## 해결 방법

### 1단계: 가상환경 활성화

PowerShell에서:

```powershell
venv\Scripts\Activate.ps1
```

**또는:**

```powershell
.\venv\Scripts\Activate.ps1
```

활성화되면 앞에 `(venv)`가 표시됩니다:
```
(venv) PS C:\Users\malgn\Desktop\malgpt\backend>
```

### 2단계: PowerShell 실행 정책 오류가 나면

만약 "실행할 수 없습니다" 오류가 나면:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

그 다음 다시 활성화:
```powershell
.\venv\Scripts\Activate.ps1
```

### 3단계: 패키지 설치

```powershell
pip install -r requirements.txt
```

### 4단계: 백엔드 실행

```powershell
python main.py
```

---

## 전체 명령어 순서

```powershell
# 1. 백엔드 폴더로 이동 (이미 있으면 생략)
cd C:\Users\malgn\Desktop\malgpt\backend

# 2. 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 3. 패키지 설치 (처음 한 번만)
pip install -r requirements.txt

# 4. 백엔드 실행
python main.py
```

---

## 빠른 확인

가상환경이 활성화되었는지 확인:
- 앞에 `(venv)`가 표시되어야 합니다
- 없으면 가상환경이 활성화되지 않은 것입니다

