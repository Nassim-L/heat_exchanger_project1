mode con: cols=120 lines=9999
@echo off

REM Activate virtual environment
call .venv\Scripts\activate.bat

IF %ERRORLEVEL% NEQ 0 (
  echo Error: Failed to activate virtual environment.
  goto :end
)

REM Run Python script
python heat_exchanger_beta.py

IF %ERRORLEVEL% NEQ 0 (
  echo Error: Failed to run Python script.
  goto :end
)

echo Python script completed successfully.
goto :end

:end
echo.
echo Closing window in 10 seconds...
ping -n 10 127.0.0.1 > nul
exit