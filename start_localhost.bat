@echo off
title FoodieAtlas Local Server
cd /d "E:\Foodieatlas_HTML"
echo Starting local server on http://localhost:8000 ...
start "" "http://localhost:8000"
python -m http.server 8000
pause
