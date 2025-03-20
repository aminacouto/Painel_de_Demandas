#!/bin/bash

echo "Inicializando o aplicativo LAD..."

# Executa o script de configuração do token
echo "Configurando o Token do GitHub..."
bash setup_token.sh

# Instalando as dependências
echo "Instalando as bibliotecas necessárias..."
pip install Flask dash pandas matplotlib requests

# Navegando para o diretório onde o app.py está localizado
echo "Navegando para o diretório do aplicativo..."
cd source  # Se o diretório for outro, ajuste conforme necessário

# Executando o aplicativo Dash
echo "Executando o aplicativo..."
python3 app.py