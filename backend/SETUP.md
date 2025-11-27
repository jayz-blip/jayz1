# 백엔드 설정 가이드

## 오류: ModuleNotFoundError 해결

`ModuleNotFoundError: No module named 'fastapi'` 오류가 발생하면 다음 단계를 따라하세요.

## 단계별 설치

### 1단계: 가상환경 생성 (이미 완료됨)

```bash
python -m venv venv
```

### 2단계: 가상환경 활성화

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

활성화되면 CMD 창 앞에 `(venv)`가 표시됩니다:
```
(venv) C:\Users\malgn\Desktop\malgpt\backend>
```

### 3단계: 패키지 설치

```bash
pip install -r requirements.txt
```

이 과정은 몇 분 걸릴 수 있습니다.

### 4단계: 백엔드 실행

```bash
python main.py
```

---

## 전체 명령어 (한 번에)

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 백엔드 실행
python main.py
```

---

## 문제 해결

### pip가 없다는 오류

```bash
python -m ensurepip --upgrade
```

### 설치가 너무 느릴 때

```bash
# 업그레이드 먼저
python -m pip install --upgrade pip

# 그 다음 설치
pip install -r requirements.txt
```

### 특정 패키지 설치 오류

개별적으로 설치:
```bash
pip install fastapi
pip install uvicorn
pip install pandas
# ...
```

