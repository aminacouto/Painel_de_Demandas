"""Callbacks da aplicação Dash."""

from typing import List, Dict, Any, Tuple

import pandas as pd
from dash import Output, Input
from dash import html

from config import COLORS, MONTH_ORDER
from data_processor import DataProcessor
from graph_generator import GraphGenerator


def register_callbacks(
    app,
    issues: List[Dict[str, Any]],
    processor: DataProcessor,
) -> None:
    """
    Registra todos os callbacks da aplicação.

    Args:
        app: Aplicação Dash
        issues: Lista bruta de issues do GitHub
        processor: Processador de dados
    """

    @app.callback(
        [
            Output("processed-data-store", "data"),
            Output("monthly-bar-chart", "figure"),
        ],
        Input("year-dropdown", "value"),
    )
    def update_data_by_year(selected_year: int) -> Tuple[Dict, Dict]:
        """
        Atualiza dados quando o ano é alterado.

        Args:
            selected_year: Ano selecionado

        Returns:
            Tupla com dados processados e figura do gráfico
        """
        # Criar novo processador com o ano selecionado
        new_processor = DataProcessor(
            year=selected_year,
            label_filter=processor.label_filter,
            title_pattern=processor.title_pattern,
        )

        # Reprocessar dados com o novo ano
        df = new_processor.process_issues(issues)

        if df.empty:
            # Retornar gráfico vazio se não houver dados
            empty_figure = {
                "data": [],
                "layout": {
                    "annotations": [
                        {
                            "text": f"Nenhuma issue encontrada para o ano {selected_year}",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {"size": 20, "color": COLORS["gray"]},
                        }
                    ],
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                    "plot_bgcolor": COLORS["background"],
                    "paper_bgcolor": COLORS["background"],
                },
            }
            return {}, empty_figure

        special_demands = new_processor.get_special_demands(df)

        # Gerar gráfico atualizado
        monthly_chart = GraphGenerator.create_monthly_comparison(
            df=df,
            special_demands=special_demands,
            month_order=MONTH_ORDER,
        )

        # Armazenar apenas os campos necessários para os callbacks
        processed_data = {
            "special_demands": special_demands[["Título", "URL", "Month"]].to_dict("records"),
            "year": selected_year,
        }

        return processed_data, monthly_chart

    @app.callback(
        Output("status-comparison-chart", "figure"),
        [Input("month-dropdown", "value"), Input("year-dropdown", "value")],
    )
    def update_status_comparison_chart(selected_month: str, selected_year: int) -> Dict[str, Any]:
        """
        Atualiza gráfico comparativo de demandas abertas e fechadas.

        Args:
            selected_month: Mês selecionado
            selected_year: Ano selecionado

        Returns:
            Figura do gráfico de status de demandas
        """
        new_processor = DataProcessor(
            year=selected_year,
            label_filter=processor.label_filter,
            title_pattern=processor.title_pattern,
        )

        df = new_processor.process_issues(issues)

        if df.empty:
            return {
                "data": [],
                "layout": {
                    "annotations": [
                        {
                            "text": "Nenhuma issue disponível para o período selecionado",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {"size": 18, "color": COLORS["gray"]},
                        }
                    ],
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                    "plot_bgcolor": COLORS["background"],
                    "paper_bgcolor": COLORS["background"],
                },
            }

        return GraphGenerator.create_status_comparison_chart(df=df, selected_month=selected_month)

    @app.callback(
        Output("pie-chart", "figure"),
        [Input("month-dropdown", "value"), Input("processed-data-store", "data"), Input("year-dropdown", "value")],
    )
    def update_pie_chart(selected_month: str, processed_data: Dict, selected_year: int) -> Dict[str, Any]:
        """
        Atualiza gráfico de pizza ao mudar o mês.

        Args:
            selected_month: Mês selecionado
            processed_data: Dados processados armazenados

        Returns:
            Figura do gráfico
        """
        if not processed_data:
            return GraphGenerator.create_empty_pie_chart()

        # Recuperar dados armazenados como registros JSON
        special_demands = pd.DataFrame(processed_data["special_demands"])

        if selected_month == "all":
            filtered_data = special_demands
        else:
            filtered_data = special_demands[special_demands["Month"] == selected_month]

        if filtered_data.empty:
            return GraphGenerator.create_empty_pie_chart()

        names = processor.extract_names_from_titles(filtered_data)

        if names:
            name_counts = pd.Series(names).value_counts()
            return GraphGenerator.create_pie_chart(
                labels=name_counts.index.tolist(),
                values=name_counts.values.tolist(),
            )

        return GraphGenerator.create_empty_pie_chart()

    @app.callback(
        [
            Output("filtered-demands-store", "data"),
            Output("demand-list", "children"),
        ],
        [Input("month-dropdown", "value"), Input("processed-data-store", "data"), Input("year-dropdown", "value")],
    )
    def update_demand_list(
        selected_month: str,
        processed_data: Dict,
        selected_year: int,
    ) -> Tuple[List[Dict[str, Any]], List[html.Li]]:
        """
        Atualiza lista de demandas ao mudar o mês.

        Args:
            selected_month: Mês selecionado
            processed_data: Dados processados armazenados

        Returns:
            Tupla com dados armazenados e elementos da lista
        """
        if not processed_data:
            return [], [
                html.Li(
                    "Carregando dados...",
                    style={
                        "color": COLORS["gray"],
                        "font-size": "16px",
                        "text-align": "center",
                    },
                )
            ]

        # Recuperar dados armazenados como registros JSON
        special_demands = pd.DataFrame(processed_data["special_demands"])

        if selected_month == "all":
            filtered_data = special_demands
        else:
            filtered_data = special_demands[special_demands["Month"] == selected_month]

        if filtered_data.empty:
            return [], [
                html.Li(
                    "Nenhuma demanda especial registrada no mês selecionado",
                    style={
                        "color": COLORS["gray"],
                        "font-size": "16px",
                        "text-align": "center",
                    },
                )
            ]

        # Atualizar a lista de demandas
        demand_list = [
            html.Li(
                html.A(
                    title,
                    href=url,
                    target="_blank",
                    className="demand-list-a",
                    title="Clique para abrir no GitHub",
                ),
                className="demand-list-li",
            )
            for title, url in zip(filtered_data["Título"], filtered_data["URL"])
        ]

        return filtered_data.to_dict("records"), demand_list

    @app.callback(
        Output("month-dropdown", "value"),
        Input("year-dropdown", "value"),
    )
    def update_month_on_year_change(selected_year: int) -> str:
        """
        Atualiza o mês selecionado para 'all' quando o ano muda.

        Args:
            selected_year: Ano selecionado

        Returns:
            Valor 'all' para o dropdown de mês
        """
        return "all"
