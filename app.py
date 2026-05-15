"""Aplicação principal do Painel de Demandas."""

import logging
import re
import sys

import dash
from flask import Flask

from callbacks import register_callbacks
from components import create_main_layout
from config import DEBUG, HOST, PORT, MONTH_ORDER, SPECIAL_LABELS, GITHUB_REPO, GITHUB_TOKEN, LABEL_FILTER, TITLE_PATTERN, YEAR
from data_processor import DataProcessor
from github_client import GitHubClient


def extract_special_labels(issues):
    labels = []
    seen = set()
    for issue in issues:
        for label in issue.get("labels", []):
            name = label.get("name", "").strip()
            if name and re.search(LABEL_FILTER, name, flags=re.IGNORECASE):
                normalized = name
                if normalized not in seen:
                    labels.append(normalized)
                    seen.add(normalized)
    return labels or SPECIAL_LABELS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── Inicialização no escopo global (obrigatório para o gunicorn) ───────────────

logger.info("Iniciando Dashboard")

github_client = GitHubClient(repo=GITHUB_REPO, token=GITHUB_TOKEN)
initial_issues = github_client.fetch_all_issues()

if not initial_issues:
    logger.warning("Nenhuma issue encontrada na inicialização. Continuando com issues vazias.")
    initial_issues = []

processor = DataProcessor(
    year=YEAR,
    label_filter=LABEL_FILTER,
    title_pattern=TITLE_PATTERN,
)

special_labels = extract_special_labels(initial_issues)

flask_server = Flask(__name__)
app = dash.Dash(__name__, server=flask_server)
app.layout = create_main_layout(all_months=MONTH_ORDER, special_labels=special_labels)

register_callbacks(app=app, initial_issues=initial_issues, processor=processor)

# Expõe o servidor Flask — o gunicorn chama `app:server`
server = app.server

# ── Execução local ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info(f"Iniciando servidor em http://{HOST}:{PORT}")
    app.run(debug=DEBUG, host=HOST, port=PORT)