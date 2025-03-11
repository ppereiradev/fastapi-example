#!/bin/bash

# Sai imediatamente se algum comando falhar
set -e

# Define o caminho do ambiente virtual
VENV_DIR="/venv"

# Cria o ambiente virtual se ainda não existir
if [ ! -d "$VENV_DIR" ]; then
    python -m venv "$VENV_DIR"
fi

# Ativar o ambiente virtual automaticamente para shells interativos
echo "source $VENV_DIR/bin/activate" >> /root/.bashrc
echo "source $VENV_DIR/bin/activate" >> /root/.profile

# Ativa o ambiente virtual
source "$VENV_DIR/bin/activate"

# Atualiza pip
pip install --upgrade pip

# Instala os pacotes apropriados com base na variável DEBUG
if [ "$ENVIRONMENT" = "dev" ]; then
    pip install -r /home/requirements-dev.txt
else
    pip install -r /home/requirements.txt
fi

tail -f /dev/null
