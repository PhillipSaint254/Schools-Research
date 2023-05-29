@echo off

REM Check if all dependencies are installed
cd C:\Users\ABC\Desktop\work_auto_tools\enrollment_and_analysis

for /f "usebackq delims=" %%i in ("requirements.txt") do (
    REM Check if the requirement is already installed
    pip show %%i > nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Installing %%i...
        start /wait pip install %%i
    )
)

REM Start Django Server
start cmd /k "cd C:\Users\ABC\Desktop\work_auto_tools\enrollment_and_analysis && python manage.py runserver 8000"

REM Start React Server
cd C:\Users\ABC\Desktop\work_auto_tools\enrollment_and_analysis\frontend
start cmd /c "npm start"
