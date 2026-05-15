"""Componentes visuais do Dash."""

from datetime import datetime
from typing import List

from dash import dcc, html

from config import COLORS


def create_title() -> html.Div:
    """Cria título principal com seletor de ano."""
    return html.Div(
        [
            html.H1("Análise de Demandas", className="h1-title"),
            html.Div(
                [
                    html.Label("Selecione o Ano:", htmlFor="year-dropdown"),
                    dcc.Dropdown(
                        id="year-dropdown",
                        options=[{"label": str(year), "value": year} for year in range(2020, 2027)],
                        value=2026,
                        clearable=False,
                        className="year-dropdown-style",
                    ),
                ],
                className="year-selector-container",
            ),
        ],
        className="title-with-selector",
    )


def create_monthly_chart(figure) -> dcc.Graph:
    """Cria gráfico de comparação mensal."""
    return dcc.Graph(
        id="monthly-bar-chart",
        figure=figure,
    )


def create_month_dropdown(all_months: List[str]) -> html.Div:
    """
    Cria dropdown para seleção de mês.

    Args:
        all_months: Lista de todos os meses

    Returns:
        Div contendo o dropdown
    """
    current_month = datetime.now().strftime("%b")

    return html.Div(
        [
            html.Label("Filtrar por Mês:", htmlFor="month-dropdown"),
            dcc.Dropdown(
                id="month-dropdown",
                options=[{"label": "Visão Geral", "value": "all"}]
                + [{"label": month, "value": month} for month in all_months],
                value="all",
                className="dropdown-style",
            )
        ],
        className="dropdown-container",
    )


def create_pie_chart() -> dcc.Graph:
    """Cria gráfico de pizza."""
    return dcc.Graph(id="pie-chart")


def create_status_comparison_chart() -> dcc.Graph:
    """Cria gráfico comparativo de demandas abertas e fechadas."""
    return dcc.Graph(id="status-comparison-chart")


def create_label_dropdown(labels: List[str]) -> html.Div:
    """
    Cria dropdown para seleção de label de demanda especial.

    Args:
        labels: Lista de labels especiais

    Returns:
        Div contendo o dropdown
    """
    return html.Div(
        [
            html.Label("Filtrar por Tipo de Demanda:", htmlFor="label-dropdown"),
            dcc.Dropdown(
                id="label-dropdown",
                options=[
                    {"label": "Todos", "value": "all"}
                ] + [
                    {
                        "label": label.upper() if label.lower() == "vm" else label if label.startswith("_") else label.title(),
                        "value": label,
                    }
                    for label in labels
                ],
                value="all",
                clearable=False,
                className="dropdown-style",
            ),
        ],
        className="dropdown-container",
    )


def create_pie_chart_section(all_months: List[str], special_labels: List[str]) -> html.Div:
    """
    Cria seção de gráfico de pizza com dropdowns.

    Args:
        all_months: Lista de todos os meses
        special_labels: Lista de labels de demandas especiais

    Returns:
        Div contendo a seção
    """
    return html.Div(
        [
            html.H3("Distribuição de Grupos de Demandas Especiais", className="h3-subtitle"),
            html.Div(
                [
                    create_month_dropdown(all_months),
                    create_label_dropdown(special_labels),
                ],
                className="filter-row",
            ),
            create_pie_chart(),
        ],
        className="pie-chart-container section-card",
    )


def create_status_comparison_section() -> html.Div:
    """Cria seção do gráfico comparativo de status de demandas."""
    return html.Div(
        [
            html.H3("Comparativo: Total Demandas Abertas vs. Fechadas", className="h3-subtitle"),
            create_status_comparison_chart(),
        ],
        className="status-comparison-container section-card",
    )


def create_demand_list_section() -> html.Div:
    """Cria seção de lista de demandas."""
    return html.Div(
        [
            html.H3("Lista de Demandas Especiais", className="h3-subtitle"),
            dcc.Store(id="filtered-demands-store"),
            html.Ul(id="demand-list", className="demand-list"),
        ],
        className="demand-list-container section-card",
    )


def create_main_layout(
    all_months: List[str],
    special_labels: List[str],
) -> html.Div:
    """
    Cria layout principal da aplicação.

    Args:
        all_months: Lista de todos os meses
        special_labels: Lista de labels de demandas especiais

    Returns:
        Div contendo o layout principal
    """
    return html.Div(
        [
            dcc.Store(id="raw-issues-store"),
            dcc.Store(id="processed-data-store"),
            # Intervalo de 5 minutos (300000 ms) para atualizar as issues
            dcc.Interval(id="issues-update-interval", interval=300000, n_intervals=0),
            create_title(),
            html.H3(
                "Comparativo: Total de Demandas vs. Demandas Especiais",
                className="h3-subtitle",
            ),
            dcc.Graph(id="monthly-bar-chart", className="chart-card"),
            html.Div(
                [
                    create_pie_chart_section(all_months, special_labels),
                    create_demand_list_section(),
                ],
                className="flex-container",
            ),
            create_status_comparison_section(),
        ],
        className="container",
    )
