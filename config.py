"""Configurações da aplicação."""

import os
#from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuração de cores para o tema
COLORS = {
    "background": "#192734",
    "text": "white",
    "bar1": "#2c6e9e",
    "bar2": "#e74c3c",
    "link": "#007bff",
    "gray": "gray",
}

# Configurações do GitHub
GITHUB_REPO = os.getenv("GITHUB_REPO", "aminacouto/projeto_dashboard")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
#para dados simulados
YEAR = int(os.getenv("YEAR", "2026"))
#para dados reais
#YEAR = int(os.getenv("YEAR", str(datetime.now().year)))

# Configurações da aplicação
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8050"))

# Padrões
LABEL_FILTER = "_USER"
MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
TITLE_PATTERN = r"\[(.*?)\]"
