@echo off
cd /d "%~dp0"
if not exist node_modules\ (
  echo Installing frontend packages. First run may take a few minutes...
  call npm install
  if errorlevel 1 goto failed
)
call npm run dev
goto end
:failed
echo Frontend dependency installation failed. Check the error above.
pause
exit /b 1
:end
pause
