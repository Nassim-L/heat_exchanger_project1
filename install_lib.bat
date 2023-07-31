@echo off

REM Create virtual environment
python -m venv .venv

IF %ERRORLEVEL% NEQ 0 (
  echo Error: Failed to create virtual environment.
  goto :end
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

IF %ERRORLEVEL% NEQ 0 (
  echo Error: Failed to activate virtual environment.
  goto :end
)

REM Install required packages
pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
  echo Error: Failed to install required packages.
  goto :end
)

echo Environment created and packages installed successfully.
goto :end

:end
pause