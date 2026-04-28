#!/bin/bash
# 確保環境安裝好必要的套件 (這裡我們使用簡單的 Node.js 處理靜態生成)
echo "Installing/Updating dependencies..."
npm install

echo "Generating site content..."
# 執行我們的網站生成腳本 (稍後會建立)
node scripts/generate_site.js

echo "Build complete."
python3 /home/hermes/fetch_care_trends.py
