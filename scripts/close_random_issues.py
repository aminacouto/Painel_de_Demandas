"""Script para fechar issues aleatórias de um repositório GitHub."""

from __future__ import annotations

import logging
import os
import random
from typing import Any

import requests
from dotenv import find_dotenv, load_dotenv


def configure_logging() -> None:
    """Configura o logging padrão para saída no terminal."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_env_variables() -> tuple[str, str]:
    """Carrega as variáveis de ambiente necessárias do arquivo .env."""
    dotenv_path = find_dotenv(usecwd=True)
    if not dotenv_path:
        raise FileNotFoundError("Arquivo .env não encontrado no diretório atual ou acima.")

    load_dotenv(dotenv_path)
    github_token = os.environ.get("GITHUB_TOKEN")
    github_repo = os.environ.get("GITHUB_REPO")

    if not github_token:
        raise ValueError("A variável de ambiente GITHUB_TOKEN não está definida.")
    if not github_repo:
        raise ValueError("A variável de ambiente GITHUB_REPO não está definida.")
    if "/" not in github_repo:
        raise ValueError("GITHUB_REPO deve estar no formato 'owner/repo'.")

    return github_token, github_repo


def fetch_open_issues(session: requests.Session, repo: str) -> list[dict[str, Any]]:
    """Busca todas as issues abertas do repositório, ignorando pull requests."""
    issues: list[dict[str, Any]] = []
    page = 1
    url = f"https://api.github.com/repos/{repo}/issues"

    while True:
        params = {"state": "open", "per_page": 100, "page": page}
        response = session.get(url, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            logging.error("Erro ao buscar issues na página %d: %s", page, error)
            raise

        page_issues = response.json()
        if not isinstance(page_issues, list):
            logging.error("Resposta inesperada ao buscar issues: %s", page_issues)
            raise ValueError("Resposta da API do GitHub não estava no formato esperado.")

        filtered_issues = [issue for issue in page_issues if "pull_request" not in issue]
        issues.extend(filtered_issues)

        if len(page_issues) < params["per_page"]:
            break

        page += 1

    logging.info("Foram encontradas %d issues abertas (excluindo PRs).", len(issues))
    return issues


def select_random_issues(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Seleciona aleatoriamente entre 20% e 40% das issues fornecidas."""
    total = len(issues)
    if total == 0:
        logging.info("Nenhuma issue aberta encontrada para selecionar.")
        return []

    percent = random.uniform(0.40, 0.80)
    count = max(1, int(round(total * percent)))
    count = min(count, total)
    selected = random.sample(issues, count)

    logging.info(
        "Selecionando %d/%d issues (%.1f%%) para fechar.",
        count,
        total,
        100 * count / total,
    )
    return selected


def close_issue(session: requests.Session, repo: str, issue_number: int) -> bool:
    """Fecha uma issue específica no GitHub usando PATCH para alterar o estado."""
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    payload = {"state": "closed"}
    response = session.patch(url, json=payload)

    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        logging.error("Falha ao fechar issue #%d: %s - %s", issue_number, error, response.text)
        return False

    logging.info("Issue #%d fechada com sucesso.", issue_number)
    return True


def main() -> None:
    """Ponto de entrada para o script que fecha issues aleatórias do repositório."""
    configure_logging()
    github_token, github_repo = load_env_variables()

    with requests.Session() as session:
        session.headers.update(
            {
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "close-random-issues-script",
            }
        )

        try:
            open_issues = fetch_open_issues(session, github_repo)
        except Exception as error:
            logging.error("Não foi possível recuperar as issues abertas: %s", error)
            return

        selected_issues = select_random_issues(open_issues)
        closed_count = 0

        for issue in selected_issues:
            issue_number = issue.get("number")
            if not isinstance(issue_number, int):
                logging.warning("Issue inválida encontrada e ignorada: %s", issue)
                continue

            if close_issue(session, github_repo, issue_number):
                closed_count += 1

        logging.info("Processo concluído. Total de issues fechadas: %d.", closed_count)


if __name__ == "__main__":
    main()
