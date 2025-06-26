@echo off
cd /d C:\SPR
REM Cria ou atualiza .gitignore com padräes essenciais
echo .venv> .gitignore
echo __pycache__>
echo outputs/>
echo logs/>
echo *.bin>
echo *.nc>
echo *.zip>
echo *.exe>
echo .env>
REM Inicializa git se nao existir
if not exist ".git" (
git init
git branch -M main
git remote add origin https://github.com/carlosangh/spr-ai-relay.git
REM Remove do git cache os arquivos/pastas que devem ser ignorados
git rm -r --cached .venv >nul 2>&
git rm -r --cached outputs >nul 2>&
git rm -r --cached logs >nul 2>&
git rm --cached *.bin >nul 2>&
git rm --cached *.nc >nul 2>&
git rm --cached *.zip >nul 2>&
git rm --cached *.exe >nul 2>&
git rm --cached .env >nul 2>&
REM Adiciona tudo limpo
git add .
REM Comita as mudancas
git commit -m "?? Clean push: remove arquivos pesados e prepara para deploy"
REM Push forcado para o branch main
git push -u origin main --force
pause
