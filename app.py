import requests
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
from flask import Flask
from datetime import datetime
import re  
import os

# Configurações
GITHUB_REPO = "LAD-PUCRS/LAD-Management"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# API do GitHub
URL = f"https://api.github.com/repos/{GITHUB_REPO}/issues?state=all"
response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    issues = response.json()

    # Lista com os dados relevantes
    data = []
    for issue in issues:
        data.append({
            "ID": issue["number"],
            "Título": issue["title"],
            "Status": issue["state"],
            "Criado em": issue["created_at"][:10],
            "Labels": ", ".join([label["name"] for label in issue["labels"]])
        })

    # Converte para um DataFrame
    df = pd.DataFrame(data)
    df["Criado em"] = pd.to_datetime(df["Criado em"])

    # Filtrar dados para o ano atual
    current_year = datetime.now().year
    df = df[df["Criado em"].dt.year == current_year].copy()

    # Criar coluna de mês
    df["Month"] = df["Criado em"].dt.strftime('%b')  

    # Filtrar demandas de usuário
    demandas_erro = df[df["Labels"].str.contains("_USER", na=False)].copy()

    # Gráfico anual
    def plot_monthly_comparison():
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        # Contagem de demandas por mês
        monthly_counts = df["Month"].value_counts()
        # Contagem de erros por mês
        monthly_error_counts = demandas_erro["Month"].value_counts()
        # Filtrar apenas os meses que possuem dados
        months_with_data = [m for m in month_order if m in monthly_counts.index]
        # Reindexar para manter a ordem correta dos meses e preencher valores ausentes com 0
        monthly_counts = monthly_counts.reindex(months_with_data)
        monthly_error_counts = monthly_error_counts.reindex(months_with_data, fill_value=0)

        bar_monthly_data = [
            go.Bar(
                x=monthly_counts.index,
                y=monthly_counts.values,
                name="Total de Demandas",
                marker={"color": "lightblue"},
                text=monthly_counts.values,
                width=0.5  
            ),
            go.Bar(
                x=monthly_counts.index,
                y=monthly_error_counts.values,
                name="Erros de Usuário",
                marker={"color": "red"},
                text=monthly_error_counts.values,
                width=0.5  
            )
        ]

        return bar_monthly_data

    # Extrair nomes dos títulos das demandas usuário
    def extract_names_from_titles(df):
        pattern = re.compile(r"\[(.*?)\]")
        return [match.group(1) for title in df["Título"] if (match := pattern.search(title))]

    # Função para plotar o gráfico de pizza
    def plot_pie_chart():
        names = extract_names_from_titles(demandas_erro)
        if names:
            name_counts = pd.Series(names).value_counts()
            return [go.Pie(labels=name_counts.index, values=name_counts.values, hole=0.3)]
        return []  

    # Inicializar o servidor Flask
    server = Flask(__name__)

    # Inicializar o app Dash
    app = dash.Dash(__name__, server=server)

    # Layout do Dash
    app.layout = html.Div([
        html.H1("Análise de Demandas", style={"text-align": "center", "color": "#f9b050"}),

        html.H2("Gráfico Anual", style={"text-align": "center", "color": "white"}),
        dcc.Graph(
            id="monthly-bar-chart",
            figure={
                "data": plot_monthly_comparison(),
                "layout": go.Layout(
                    xaxis={"title": "Mês", "tickmode": "array", "tickvals": df["Month"].unique(), "tickfont": {"family": "Arial", "size": 12, "color": "black", "weight": "bold"}},
                    yaxis={"title": "Quantidade de Demandas", "tickmode": "linear", "dtick": 10},
                    barmode="overlay",
                    bargap=0.2,  
                    bargroupgap=0.1,
                    plot_bgcolor="#f0f0f0",
                    paper_bgcolor="#f0f0f0",
                    font={"color": "black"}
                )
            },
        
        ), 

        html.H2("Grupos de Usuários", style={"text-align": "center", "color": "white"}),
        dcc.Graph(
            id="pie-chart",
            figure={
                "data": plot_pie_chart(),
                "layout": go.Layout(
                    plot_bgcolor="#f0f0f0",
                    paper_bgcolor="#f0f0f0",
                    font={"color": "black"}
                )},
            style={"backgroundColor": "#f0f2f5"}
        )
    ], style={"padding": "0 40px", "height": "100%"})

    if __name__ == "__main__":
        app.run(debug=True)
else:
    print("Erro ao acessar o GitHub:", response.status_code)
