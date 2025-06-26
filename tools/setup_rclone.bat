@echo off
REM =========================================
REM  Pulse • SPR • Configuração do rclone  (AWS – São Paulo)
REM =========================================

REM --- carrega as variáveis do profile.env ---
for /f "usebackq delims=" %%i in ("%~dp0profile.env") do set %%i

REM --- remove o remote antigo (se existir) ---
rclone config delete spr >NUL 2>&1

REM --- cria o remote correto ---
rclone config create spr s3 provider=AWS env_auth=false ^
  region=sa-east-1

echo.
echo Remote "spr" criado (AWS S3 sa-east-1) com sucesso.
echo Teste com:
echo   rclone ls spr:
echo.
pause
