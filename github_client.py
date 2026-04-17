"""Cliente para comunicação com a API do GitHub."""

import logging
from typing import List, Dict, Any

import requests

logger = logging.getLogger(__name__)


class GitHubClient:
    """Cliente para buscar issues do GitHub."""

    def __init__(self, repo: str, token: str = ""):
        """
        Inicializa o cliente GitHub.

        Args:
            repo: Repositório no formato 'owner/repo'
            token: Token de autenticação (opcional)
        """
        self.repo = repo
        self.headers = {"Authorization": f"token {token}"} if token else {}
        self.base_url = "https://api.github.com"

    def fetch_all_issues(self) -> List[Dict[str, Any]]:
        """
        Busca todas as issues do repositório com paginação.

        Returns:
            Lista de issues do GitHub
        """
        issues = []
        page = 1

        while True:
            try:
                url = f"{self.base_url}/repos/{self.repo}/issues"
                params = {
                    "state": "all",
                    "per_page": 100,
                    "page": page,
                }

                response = requests.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=10,
                )
                response.raise_for_status()

                data = response.json()

                if not data:
                    logger.info(f"Todas as issues foram recuperadas ({len(issues)} total)")
                    break

                issues.extend(data)
                logger.debug(f"Página {page}: {len(data)} issues recuperadas")
                page += 1

            except requests.exceptions.RequestException as e:
                logger.error(f"Erro ao acessar GitHub: {e}")
                return []

        return issues
