"""Processamento e tratamento de dados de issues."""

import calendar
import logging
import re
from typing import List, Dict, Any, Pattern

import pandas as pd

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processador de dados de issues do GitHub."""

    def __init__(self, year: int, label_filter: str, title_pattern: str):
        """
        Inicializa o processador de dados.

        Args:
            year: Ano para filtrar issues
            label_filter: Label para filtrar demandas especiais
            title_pattern: Padrão regex para extrair nomes de títulos
        """
        self.year = year
        self.label_filter = label_filter
        self.title_pattern: Pattern = re.compile(title_pattern)

    def process_issues(self, issues: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Converte issues em DataFrame processado.

        Args:
            issues: Lista de issues do GitHub

        Returns:
            DataFrame processado e filtrado
        """
        if not issues:
            logger.warning("Nenhuma issue fornecida")
            return pd.DataFrame()

        # Converte para lista de dicionários usando a data simulada quando presente
        data = [
            {
                "ID": issue["number"],
                "Título": issue["title"],
                "Status": issue["state"],
                "Criado em": self._extract_simulated_date(issue),
                "Labels": ", ".join([label["name"] for label in issue["labels"]]),
                "URL": issue["html_url"],
            }
            for issue in issues
        ]

        df = pd.DataFrame(data)

        if df.empty:
            logger.warning("DataFrame vazio após processamento")
            return df

        # Converte data
        df["Criado em"] = pd.to_datetime(df["Criado em"])

        # Filtra por ano
        df = df[df["Criado em"].dt.year == self.year].copy()

        if df.empty:
            logger.warning(f"Nenhuma issue encontrada para o ano {self.year}")
            return df

        # Adiciona coluna de mês usando abreviações fixas em inglês para evitar dependência de localidade
        df["Month"] = df["Criado em"].dt.month.map(lambda month: calendar.month_abbr[month])

        logger.info(f"Processadas {len(df)} issues para o ano {self.year}")

        return df

    def get_special_demands(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filtra demandas especiais pelo label.

        Args:
            df: DataFrame original

        Returns:
            DataFrame com demandas especiais
        """
        special_demands = df[df["Labels"].str.contains(self.label_filter, na=False, regex=True)].copy()
        logger.info(f"Encontradas {len(special_demands)} demandas especiais")
        return special_demands

    def extract_names_from_titles(self, df: pd.DataFrame) -> List[str]:
        """
        Extrai nomes entre colchetes dos títulos.

        Args:
            df: DataFrame com títulos

        Returns:
            Lista de nomes extraídos
        """
        names = []
        for title in df["Título"]:
            match = self.title_pattern.search(title)
            if match:
                names.append(match.group(1))

        return names

    def _extract_simulated_date(self, issue: Dict[str, Any]) -> str:
        """
        Extrai a data simulada do corpo da issue.

        Se a issue contiver uma linha no formato "Data simulada: YYYY-MM-DD",
        essa data é utilizada. Caso contrário, usa a data de criação real.

        Args:
            issue: Dicionário da issue.

        Returns:
            str: Data no formato YYYY-MM-DD.
        """
        body = issue.get("body", "") or ""
        match = re.search(r"Data simulada:\s*(\d{4}-\d{2}-\d{2})", body)
        if match:
            return match.group(1)
        return issue["created_at"][:10]

