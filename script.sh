#!/bin/bash

echo "Inicializando o aplicativo LAD..."

# Lendo o token do usuário
echo "Por favor, insira seu token do GitHub:"
read GITHUB_TOKEN

# Exportando o token como variável de ambiente
export GITHUB_TOKEN="$GITHUB_TOKEN"

# Instalando as dependências
echo "Instalando as bibliotecas necessárias..."
pip install Flask dash pandas matplotlib requests

# Executando o aplicativo Dash
echo "Executando o aplicativo..."
python3 app.py
