#!/bin/bash
# Cloudflare Pages 빌드 스크립트
# Python 설치를 건너뛰고 Node.js만 사용

set -e

echo "Node.js 버전:"
node --version

echo "npm 버전:"
npm --version

echo "의존성 설치 중..."
npm install

echo "빌드 중..."
npm run build

echo "빌드 완료!"

