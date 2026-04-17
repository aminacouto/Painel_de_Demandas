#!/bin/bash

echo "=========================================="
echo "Painel de Demandas - Setup"
echo "=========================================="

# Verificar se .env existe
if [ ! -f .env ]; then
    echo ""
    echo "Arquivo .env não encontrado. Criando a partir de .env.example..."
    cp .env.example .env
    echo "✓ Arquivo .env criado"
else
    echo "✓ Arquivo .env já existe"
fi

echo ""
echo "Por favor, insira seu token do GitHub:"
read -p "Token: " GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠ Aviso: Nenhum token fornecido. A aplicação funcionará com acesso limitado."
else
    # Atualizar .env com o token
    if grep -q "^GITHUB_TOKEN=" .env; then
        sed -i.bak "s/^GITHUB_TOKEN=.*/GITHUB_TOKEN=$GITHUB_TOKEN/" .env
    else
        echo "GITHUB_TOKEN=$GITHUB_TOKEN" >> .env
    fi
    echo "✓ Token salvo em .env"
fi

echo ""
echo "Instalando dependências..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependências instaladas com sucesso"
else
    echo "✗ Erro ao instalar dependências"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup concluído!"
echo "Executando a aplicação..."
echo "=========================================="
echo ""

python app.py
