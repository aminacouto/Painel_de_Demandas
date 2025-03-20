#!/bin/bash

echo "Configuração do Token do GitHub para LAD Issues"

# Solicita ao usuário o token do GitHub
read -sp "Digite seu GitHub Token e pressione [ENTER]: " USER_TOKEN
echo

# Verifica se o usuário realmente digitou algo
if [[ -z "$USER_TOKEN" ]]; then
    echo "Nenhum token foi inserido. Tente novamente."
    exit 1
fi

# Adiciona o token ao ~/.bashrc (evita duplicação)
if grep -q "export GITHUB_TOKEN=" ~/.bashrc; then
    echo "O token já está configurado. Atualizando..."
    sed -i '/export GITHUB_TOKEN=/d' ~/.bashrc  # Remove linha antiga, se existir
fi

echo "export GITHUB_TOKEN=\"$USER_TOKEN\"" >> ~/.bashrc
echo "Token salvo com sucesso no ~/.bashrc"

# Aplica as mudanças na mesma sessão
source ~/.bashrc
echo "Configuração aplicada. Você pode usar o token agora!"