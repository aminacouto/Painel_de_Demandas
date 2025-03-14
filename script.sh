#!/bin/bash

echo "Inicializando o aplicativo LAD..."

# Garantir que o pip está atualizado
echo "Atualizando o pip..."
pip install --upgrade pip

# Instalando as dependências
echo "Instalando as bibliotecas necessárias..."
pip install Flask dash pandas matplotlib requests

echo "Instalação das bibliotecas concluída."

# Navegando para o diretório onde o app.py está localizado
echo "Navegando para o diretório do aplicativo..."
cd source  # Se o diretório for outro, ajuste conforme necessário

# Executando o aplicativo Dash
echo "Executando o aplicativo..."
python3 app.py