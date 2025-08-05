@echo off
title File Transfer Server
echo Checking dependencies...

REM 安装 flask 和 psutil（如果未安装）
python -c "import flask, psutil" 2>nul || (
    echo Installing dependencies...
    pip install flask psutil
)

echo Starting file transfer server...
python file_transfer.py

pause
