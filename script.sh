#!/bin/bash

echo "Inicializando o aplicativo LAD..."

# Instalando as dependências
echo "Instalando as bibliotecas necessárias..."
pip install Flask dash pandas matplotlib requests

# Executando o aplicativo Dash
echo "Executando o aplicativo..."
python3 app.py
