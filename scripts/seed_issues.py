"""
Script para gerar issues de teste no GitHub.

Este script cria automaticamente issues fake em um repositório GitHub
para popular um dashboard de demandas com dados realistas.
"""

import os
import random
from datetime import datetime, timedelta
from typing import List, Optional

import requests
from dotenv import load_dotenv


# Carregar variáveis de ambiente
load_dotenv()

# Configurações
GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO: str = os.getenv("GITHUB_REPO", "")
API_BASE_URL: str = "https://api.github.com"

# Listas para geração aleatória
TITLES: List[str] = [
    "Problema na VM de testes",
    "Falha no backup",
    "Instabilidade na rede",
    "Atualização de servidor",
    "Erro de acesso remoto",
    "Manutenção preventiva",
    "Falha no sistema de monitoramento",
    "Problema de conectividade VPN",
    "Atualização de software",
    "Erro no banco de dados",
    "Problema de performance",
    "Falha na sincronização",
    "Erro de autenticação",
    "Manutenção de hardware",
    "Problema de segurança",
    "Falha no serviço web",
    "Atualização de firmware",
    "Erro no sistema de logs",
    "Problema de armazenamento",
    "Falha na replicação",
]

LABELS: List[str] = [
    "_USER",
    "infraestrutura",
    "rede",
    "manutenção",
]

GROUPS: List[str] = [f"Grupo{i}" for i in range(1, 21)]


def generate_random_title() -> str:
    """
    Gera um título aleatório para a issue.

    Returns:
        str: Título selecionado aleatoriamente da lista.
    """
    return random.choice(TITLES)


def generate_random_labels() -> List[str]:
    """
    Gera uma lista aleatória de labels para a issue.

    Returns:
        List[str]: Lista com 1-3 labels selecionadas aleatoriamente.
    """
    num_labels = random.randint(1, 3)
    return random.sample(LABELS, num_labels)


def generate_random_date() -> str:
    """
    Gera uma data aleatória no ano de 2026.

    Returns:
        str: Data no formato YYYY-MM-DD.
    """
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")


def create_issue(title: str, body: str, labels: List[str]) -> Optional[dict]:
    """
    Cria uma issue no repositório GitHub.

    Args:
        title (str): Título da issue.
        body (str): Corpo da issue.
        labels (List[str]): Lista de labels.

    Returns:
        Optional[dict]: Resposta da API ou None se erro.
    """
    url = f"{API_BASE_URL}/repos/{GITHUB_REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "title": title,
        "body": body,
        "labels": labels,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar issue '{title}': {e}")
        return None


def main() -> None:
    """
    Executa a criação de issues de teste.
    """
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("Erro: GITHUB_TOKEN e GITHUB_REPO devem estar definidos no arquivo .env")
        return

    num_issues = random.randint(100, 200)
    print(f"Criando {num_issues} novas issues de teste...")

    created_count = 0

    for i in range(num_issues):
        group = random.choice(GROUPS)
        title = f"[{group}] {generate_random_title()}"
        labels = generate_random_labels()
        simulated_date = generate_random_date()

        body = f"Descrição: Issue de teste gerada automaticamente.\n\nData simulada: {simulated_date}"

        issue = create_issue(title, body, labels)
        if issue:
            created_count += 1
            print(f"Issue {i+1}/{num_issues} criada: {title}")
        else:
            print(f"Falha ao criar issue {i+1}/{num_issues}")

    print(f"\nProcesso concluído. {created_count} issues criadas com sucesso.")


if __name__ == "__main__":
    main()