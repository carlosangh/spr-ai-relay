@echo off
echo Configurando ambiente do SPR...

python -m venv .venv
call .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

echo Ambiente configurado!
echo Abra o arquivo .env e confira suas API Keys.

pause
