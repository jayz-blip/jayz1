#!/bin/bash
echo "빌드 확인 스크립트"
echo "=================="

# 빌드 실행
echo "빌드 실행 중..."
npm run build

# 빌드 결과 확인
echo ""
echo "빌드 결과 확인:"
if [ -d "dist" ]; then
  echo "✓ dist 디렉토리 생성됨"
  
  if [ -f "dist/index.html" ]; then
    echo "✓ index.html 파일 존재"
    echo ""
    echo "index.html 내용 확인:"
    head -20 dist/index.html
  else
    echo "✗ index.html 파일 없음"
  fi
  
  echo ""
  echo "dist 디렉토리 내용:"
  ls -la dist/
else
  echo "✗ dist 디렉토리 없음"
  exit 1
fi

