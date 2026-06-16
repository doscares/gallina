@echo off
call .venv\Scripts\activate
python -m PyInstaller main.spec --clean
pause
