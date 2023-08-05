@echo off
set "VIRTUAL_ENV=%cd%\.venv"
set "VIRTUAL_ENV_PYTHON=%VIRTUAL_ENV%\Scripts\python.exe"
@echo on

%VIRTUAL_ENV_PYTHON% "%VIRTUAL_ENV%\Scripts\pip.exe" %*