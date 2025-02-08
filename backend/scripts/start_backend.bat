@echo off
echo Wolvox-WooCommerce Entegrasyonu başlatılıyor...
cd %~dp0\..
call venv\Scripts\activate
set PYTHONPATH=%PYTHONPATH%;%CD%\src

REM Install dependencies if needed
pip install -r requirements.txt

REM Run migrations
alembic upgrade head

REM Start the FastAPI application with uvicorn
uvicorn src.main:app --reload --port 8000

REM Deactivate virtual environment on exit
deactivate 

REM Start the FastAPI application with python
python src\main.py 