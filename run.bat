@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON=python"
) else (
    where py >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON=py -3"
    ) else (
        echo Python nao encontrado. Instale Python 3.6+ em https://python.org
        pause
        exit /b 1
    )
)

if not exist "venv" (
    echo Criando ambiente virtual...
    %PYTHON% -m venv venv
    if errorlevel 1 (
        echo Falha ao criar o ambiente virtual.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo Instalando dependencias...
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo Iniciando GameSaver...
python -m gamesaver
if errorlevel 1 pause

endlocal
