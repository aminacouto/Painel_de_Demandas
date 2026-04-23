"""Aplicação principal do Painel de Demandas."""

import logging
import sys

import dash
from flask import Flask

from callbacks import register_callbacks
from components import create_main_layout
from config import DEBUG, HOST, PORT, MONTH_ORDER, GITHUB_REPO, GITHUB_TOKEN, LABEL_FILTER, TITLE_PATTERN, YEAR
from data_processor import DataProcessor
from github_client import GitHubClient

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── Inicialização no escopo global (obrigatório para o gunicorn) ───────────────

logger.info("Iniciando Dashboard")

github_client = GitHubClient(repo=GITHUB_REPO, token=GITHUB_TOKEN)
issues = github_client.fetch_all_issues()

if not issues:
    logger.error("Nenhuma issue encontrada. Verifique suas credenciais ou repositório.")
    sys.exit(1)

processor = DataProcessor(
    year=YEAR,
    label_filter=LABEL_FILTER,
    title_pattern=TITLE_PATTERN,
)

flask_server = Flask(__name__)
app = dash.Dash(__name__, server=flask_server)
app.layout = create_main_layout(all_months=MONTH_ORDER)

register_callbacks(app=app, issues=issues, processor=processor)

# Expõe o servidor Flask — o gunicorn chama `app:server`
server = app.server

# ── Execução local ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info(f"Iniciando servidor em http://{HOST}:{PORT}")
    app.run(debug=DEBUG, host=HOST, port=PORT)