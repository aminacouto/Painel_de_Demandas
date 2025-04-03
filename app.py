import requests
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objs as go
from flask import Flask
from datetime import datetime
import re  
import os
from dash.dependencies import Input, Output

# Configuração de cores para o tema
COLORS = {
    "background": "#192734",
    "text": "white",
    "bar1": "#2c6e9e", 
    "bar2": "#e74c3c", 
    "link": "#007bff",
    "gray": "gray",
}

# Configurações
GITHUB_REPO = "LAD-PUCRS/LAD-Management"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
YEAR = 2025 # Defina o ano desejado

def fetch_all_issues():
    issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/issues?state=all&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS) 

        if response.status_code != 200:
            print("Erro ao acessar o GitHub:", response.status_code)
            return []

        data = response.json()

        if not data:  # Se não há mais issues, para de buscar
            break

        issues.extend(data)
        page += 1  # Vai para a próxima página

    return issues

# Buscar todas as issues
issues = fetch_all_issues()

# Verifica se há issues
if not issues:
    print("Nenhuma issue encontrada. Verifique suas credenciais ou repositório.")
    exit()

# Lista com os dados relevantes
data = []
for issue in issues:
    data.append({
        "ID": issue["number"],
        "Título": issue["title"],
        "Status": issue["state"],
        "Criado em": issue["created_at"][:10],
        "Labels": ", ".join([label["name"] for label in issue["labels"]]),
        "URL": issue["html_url"]  
    })

# Converte para um DataFrame
df = pd.DataFrame(data)
df["Criado em"] = pd.to_datetime(df["Criado em"])

# Filtrar dados para o ano especificado
df = df[df["Criado em"].dt.year == YEAR].copy()

# Criar coluna de mês
df["Month"] = df["Criado em"].dt.strftime('%b')  

# Filtrar demandas com label "_USER"
demandas_erro = df[df["Labels"].str.contains("_USER", na=False)].copy()

# Gráfico anual
def plot_monthly_comparison():
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_counts = df["Month"].value_counts()
    monthly_error_counts = demandas_erro["Month"].value_counts()
    months_with_data = [m for m in month_order if m in monthly_counts.index]
    monthly_counts = monthly_counts.reindex(months_with_data)
    monthly_error_counts = monthly_error_counts.reindex(months_with_data, fill_value=0)

    return {
        "data": [
            go.Bar(
                x=monthly_counts.index,
                y=monthly_counts.values,
                name="Demandas Abertas no mês",
                marker={"color": COLORS["bar1"]},
                text=monthly_counts.values,
                width=0.6,
                hovertemplate="<b>Mês:</b> %{x}<br><b>Demandas Abertas:</b> %{y}<extra></extra>"
            ),
            go.Bar(
                x=monthly_counts.index,
                y=monthly_error_counts.values,
                name="Erros de Usuário",
                marker={"color": COLORS["bar2"]},
                text=monthly_error_counts.values,
                width=0.6,
                hovertemplate="<b>Mês:</b> %{x}<br><b>Erros de Usuário:</b> %{y}<extra></extra>"
            )
        ],
        "layout": go.Layout(
            xaxis={"title": "Mês", "color": COLORS["text"]},
            yaxis={"title": "Quantidade de Demandas Abertas", "color": COLORS["text"]},
            barmode="overlay",
            plot_bgcolor=COLORS["background"],
            paper_bgcolor=COLORS["background"],
            font={"color": COLORS["text"]},
            hovermode="closest",
        )
    }

# Extrair nomes dos grupos das demandas de label "_USER"
def extract_names_from_titles(df):
    pattern = re.compile(r"\[(.*?)\]")
    return [match.group(1) for title in df["Título"] if (match := pattern.search(title))]

# Função para plotar o gráfico de pizza por mês
def plot_pie_chart(month):
    # Filtrar demandas de erro pelo mês fornecido
    filtered_data = demandas_erro[demandas_erro["Month"] == month]
    names = extract_names_from_titles(filtered_data)
    if names:
        name_counts = pd.Series(names).value_counts()
        return [go.Pie(labels=name_counts.index, values=name_counts.values, hole=0.3)]
    return []  # Retorna um gráfico vazio se não houver dados para o mês

# Inicializar o servidor Flask
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Lista fixa com todos os meses do ano
all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Obter o mês atual 
current_month = datetime.now().strftime('%b')

# Layout do Dash
app.layout = html.Div([
    html.H1(f"Análise de Demandas {YEAR}", className="h1-title"),

    html.H3("Comparativo: Total de Demandas vs. Erros de Usuário", className="h3-subtitle"),
    dcc.Graph(
        id="monthly-bar-chart",
        figure=plot_monthly_comparison(), 
    ),

    html.Div([
        html.Div([
            html.H3("Distribuição de Erros de Usuário por Grupo", className="h3-subtitle"),

            # Dropdown para selecionar o mês
            html.Div(
                [
                    dcc.Dropdown(
                        id="month-dropdown",
                        options=[{"label": "Visão Geral", "value": "all"}] + [{"label": month, "value": month} for month in all_months],
                        value=current_month,
                        className="dropdown-style"
                    )
                ], className="dropdown-container"
            ), 

            # Gráfico de pizza
            dcc.Graph(
                id="pie-chart",
            )
        ], className="pie-chart-container"),

        # Lista de demandas com links para o GitHub
        html.Div([
            html.H3("Lista de Demandas Relacionadas a Erros de Usuário", className="h3-subtitle"),

            # dcc.Store para armazenar os dados filtrados
            dcc.Store(id="filtered-demands-store"),

            html.Ul(id="demand-list", className="demand-list")
        ], className="demand-list-container")
    ], className="flex-container")
], className="container")

# Callback para atualizar o gráfico de pizza
@app.callback(
    Output("pie-chart", "figure"),
    [Input("month-dropdown", "value")]
)
def update_pie_chart(selected_month):
    if selected_month == "all":
        # Use todos os meses
        filtered_data = demandas_erro
    else:
        # Filtrar pelo mês selecionado
        filtered_data = demandas_erro[demandas_erro["Month"] == selected_month]

    names = extract_names_from_titles(filtered_data)
    if names:
        name_counts = pd.Series(names).value_counts()
        total_demandas = name_counts.sum()  # Calcula o total de demandas

        return {
            "data": [
                go.Pie(
                    labels=name_counts.index,
                    values=name_counts.values,
                    hole=0.3,
                    textinfo="percent+value",
                    hovertemplate="<b>Grupo:</b> %{label}<br><b>Quantidade:</b> %{value}<br><b>Percentual:</b> %{percent}<extra></extra>"
                )
            ],
            "layout": go.Layout(
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["background"],
                font={"color": COLORS["text"]},
                annotations=[
                    {
                        "text": f"Total: {total_demandas}",
                        "font": {"size": 16, "color": COLORS["text"]},
                        "showarrow": False,
                        "xref": "paper",
                        "yref": "paper",
                        "x": 0.5,
                        "y": 0.5,
                    }
                ]
            )
        }
    return {
        "data": [],
        "layout": go.Layout(
            annotations=[
                {
                    "text": "Nenhuma demanda especial registrada no mês selecionado",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 20, "color": COLORS["gray"] },
                }
            ],
            showlegend=False,
            xaxis={"visible": False},
            yaxis={"visible": False},
            plot_bgcolor=COLORS["background"],
            paper_bgcolor=COLORS["background"],
        )
    }

# Callback para atualizar a lista de demandas com base no mês selecionado
@app.callback(
    [Output("filtered-demands-store", "data"),
     Output("demand-list", "children")],
    [Input("month-dropdown", "value")]
)
def update_demand_list(selected_month):
    if selected_month == "all":
        # Use todos os meses
        filtered_data = demandas_erro
    else:
        # Filtrar pelo mês selecionado
        filtered_data = demandas_erro[demandas_erro["Month"] == selected_month]

    if filtered_data.empty:  # Verifica se não há dados
        return [], [html.Li("Nenhuma demanda especial registrada no mês selecionado", style={"color": COLORS["gray"], "font-size": "16px", "text-align": "center"})]

    # Atualizar a lista de demandas
    demand_list = [
        html.Li(
            html.A(
                title, 
                href=url, 
                target="_blank", 
                className="demand-list-a",  
                title="Clique para abrir no GitHub"
            ),
            className="demand-list-li"  
        )
        for title, url in zip(filtered_data["Título"], filtered_data["URL"])
    ]
    return filtered_data.to_dict("records"), demand_list

if __name__ == "__main__":
    app.run(debug=True)
else:
    print("Erro ao acessar o GitHub")
