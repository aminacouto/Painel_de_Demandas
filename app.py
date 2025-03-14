import requests
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from flask import Flask

# Configurações
GITHUB_REPO = "aminacouto/lad"  # Substitua pelo seu repositório
GITHUB_TOKEN = "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"  # Opcional para repositórios privados
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# URL da API do GitHub
URL = f"https://api.github.com/repos/{GITHUB_REPO}/issues"

# Faz a requisição
response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    issues = response.json()
    
    # Criando uma lista com os dados relevantes
    data = []
    for issue in issues:
        data.append({
            "ID": issue["number"],
            "Título": issue["title"],
            "Status": issue["state"],
            "Criado em": issue["created_at"][:10],  # Apenas a data (YYYY-MM-DD)
            "Labels": ", ".join([label["name"] for label in issue["labels"]])
        })
    
    # Converte para um DataFrame
    df = pd.DataFrame(data)

    # Filtrar demandas específicas (exemplo: erros de usuário)
    filtro = df["Labels"].str.contains("user", na=False)
    demandas_erro = df[filtro]

    # Converter as datas para datetime
    df["Criado em"] = pd.to_datetime(df["Criado em"])
    demandas_erro["Criado em"] = pd.to_datetime(demandas_erro["Criado em"])

    # Função para plotar o gráfico para um determinado mês
    def plot_month(month_offset):
        # Calculando o primeiro e o último dia do mês com o offset
        latest_date = df["Criado em"].max()
        target_month = latest_date - pd.DateOffset(months=month_offset)
        start_of_month = target_month.replace(day=1)
        end_of_month = (start_of_month + pd.DateOffset(months=1)) - pd.DateOffset(days=1)

        # Filtrando as demandas para o mês específico
        df_month = df[(df["Criado em"] >= start_of_month) & (df["Criado em"] <= end_of_month)]
        demandas_erro_month = df_month[df_month["Labels"].str.contains("user", na=False)]

        # Contagem de demandas por dia
        total_por_dia = df_month.groupby("Criado em").size()
        erros_por_dia = demandas_erro_month.groupby("Criado em").size()

        # Gráfico de Pizza
        pie_data = {
            "labels": ["Outras Demandas", "Demandas de Erro de Usuário"],
            "values": [len(df_month) - len(demandas_erro_month), len(demandas_erro_month)],
            "type": "pie",
            "marker": {"colors": ["lightblue", "red"]}
        }

        # Gráfico de barras (Evolução das demandas no tempo)
        bar_data = [
            go.Bar(x=total_por_dia.index, y=total_por_dia.values, name="Total de Demandas", marker={"color": "lightblue"}),
            go.Bar(x=erros_por_dia.index, y=erros_por_dia.values, name="Erros de Usuário", marker={"color": "red"})
        ]

        return pie_data, bar_data, start_of_month.strftime('%B %Y')

    # Função para plotar o gráfico de barras comparativo anual
    def plot_yearly_comparison():
        # Agrupar por mês e contar as demandas
        df['Month'] = df['Criado em'].dt.to_period('M')
        monthly_counts = df.groupby('Month').size()
        monthly_error_counts = demandas_erro.groupby(demandas_erro['Criado em'].dt.to_period('M')).size()

        # Gráfico de barras comparativo anual
        bar_yearly_data = [
            go.Bar(x=monthly_counts.index.astype(str), y=monthly_counts.values, name="Total de Demandas", marker={"color": "lightblue"}),
            go.Bar(x=monthly_error_counts.index.astype(str), y=monthly_error_counts.values, name="Erros de Usuário", marker={"color": "red"})
        ]

        return bar_yearly_data

    # Inicializar o servidor Flask
    server = Flask(__name__)

    # Inicializar o app Dash
    app = dash.Dash(__name__, server=server)

    # Layout do Dash
    app.layout = html.Div([
        html.H1("Análise de Demandas do Repositório", style={"text-align": "center", "color": "#f9b050"}),

        # Título do gráfico anual
        html.H2("Gráfico Anual", style={"text-align": "center", "color": "white"}),

        # Gráfico de barras comparativo anual
        dcc.Graph(id="yearly-bar-chart", style={"backgroundColor": "#f0f2f5"}),

        # Texto do mês
        html.Div(id="month-name", 
                 style={"text-align": "center", "color": "white", "font-size": "20px", "margin-top": "20px"}),

        # Controles para mudar o mês
        html.Div([
            html.Button("←Mês anterior", id="prev-month", n_clicks=0, 
                    style={"background-color": "#f9b050", "color": "black", "border": "none", "padding": "10px", "font-weight": "bold"}),
            html.Button("Próximo mês→", id="next-month", n_clicks=0, 
                    style={"background-color": "#f9b050", "color": "black", "border": "none", "padding": "10px", "font-weight": "bold"})
        ], style={"text-align": "center", "margin-top": "20px"}),

        # Gráficos lado a lado
        html.Div([
            dcc.Graph(id="pie-chart", style={"width": "48%", "display": "inline-block", "backgroundColor": "#f0f2f5"}),
            dcc.Graph(id="bar-chart", style={"width": "48%", "display": "inline-block", "backgroundColor": "#f0f2f5"})
        ])
    ], style={"backgroundColor": "#0e1b26", "padding": "10px 40px"})

    # Callback para atualizar os gráficos e o nome do mês
    @app.callback(
        [Output("yearly-bar-chart", "figure"),
         Output("pie-chart", "figure"),
         Output("bar-chart", "figure"),
         Output("month-name", "children")],
        [Input("prev-month", "n_clicks"),
         Input("next-month", "n_clicks")]
    )
    def update_graphs(prev_month_clicks, next_month_clicks):
        current_month_offset = next_month_clicks - prev_month_clicks
        pie_data, bar_data, month_name = plot_month(current_month_offset)
        bar_yearly_data = plot_yearly_comparison()
        
        # Retornando os gráficos com os dados atualizados
        return {"data": bar_yearly_data}, {"data": [pie_data]}, {"data": bar_data}, f"Mês: {month_name}"

    if __name__ == "__main__":
        app.run_server(debug=True)
else:
    print("Erro ao acessar o GitHub:", response.status_code)
