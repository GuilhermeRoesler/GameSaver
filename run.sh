#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Python nao encontrado. Instale Python 3.6+ em https://python.org"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    "$PYTHON" -m venv venv
fi

source venv/bin/activate

echo "Instalando dependencias..."
python -m pip install -r requirements.txt -q

echo "Iniciando GameSaver..."
python -m gamesaver
