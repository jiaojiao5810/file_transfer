@echo off
title File Transfer Server
echo Checking dependencies...

REM ��װ flask �� psutil�����δ��װ��
python -c "import flask, psutil" 2>nul || (
    echo Installing dependencies...
    pip install flask psutil
)

echo Starting file transfer server...
python file_transfer.py

pause
