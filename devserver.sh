#!/bin/sh
source .venv/bin/activate

# Define a porta 8080 como padrão se $PORT não estiver definida
export PORT=${PORT:-8080}

echo "Iniciando servidor na porta $PORT..."
python -u -m flask --app app run -p $PORT --debug