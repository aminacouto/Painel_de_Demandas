"""Geração de gráficos para o dashboard."""

import logging
from typing import Dict, List, Any

import pandas as pd
import plotly.graph_objs as go

from config import COLORS

logger = logging.getLogger(__name__)


class GraphGenerator:
    """Gerador de gráficos Plotly."""

    @staticmethod
    def create_monthly_comparison(
        df: pd.DataFrame,
        special_demands: pd.DataFrame,
        month_order: List[str],
    ) -> Dict[str, Any]:
        """
        Cria gráfico de comparação mensal.

        Args:
            df: DataFrame com todas as issues
            special_demands: DataFrame com demandas especiais
            month_order: Ordem dos meses

        Returns:
            Dicionário com dados e layout do gráfico
        """
        monthly_counts = df["Month"].value_counts()
        monthly_error_counts = special_demands["Month"].value_counts()
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
                    hovertemplate="<b>Mês:</b> %{x}<br><b>Demandas Abertas:</b> %{y}<extra></extra>",
                ),
                go.Bar(
                    x=monthly_counts.index,
                    y=monthly_error_counts.values,
                    name="Erros de Usuário",
                    marker={"color": COLORS["bar2"]},
                    text=monthly_error_counts.values,
                    width=0.6,
                    hovertemplate="<b>Mês:</b> %{x}<br><b>Erros de Usuário:</b> %{y}<extra></extra>",
                ),
            ],
            "layout": go.Layout(
                xaxis={"title": "Mês", "color": COLORS["text"]},
                yaxis={"title": "Quantidade de Demandas Abertas", "color": COLORS["text"]},
                barmode="overlay",
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["background"],
                font={"color": COLORS["text"]},
                hovermode="closest",
            ),
        }

    @staticmethod
    def create_pie_chart(
        labels: List[str],
        values: List[int],
    ) -> Dict[str, Any]:
        """
        Cria gráfico de pizza.

        Args:
            labels: Rótulos para o gráfico
            values: Valores para cada rótulo

        Returns:
            Dicionário com dados e layout do gráfico
        """
        total = sum(values)

        return {
            "data": [
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.3,
                    textinfo="percent+value",
                    hovertemplate="<b>Grupo:</b> %{label}<br><b>Quantidade:</b> %{value}<br><b>Percentual:</b> %{percent}<extra></extra>",
                ),
            ],
            "layout": go.Layout(
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["background"],
                font={"color": COLORS["text"]},
                annotations=[
                    {
                        "text": f"Total: {total}",
                        "font": {"size": 16, "color": COLORS["text"]},
                        "showarrow": False,
                        "xref": "paper",
                        "yref": "paper",
                        "x": 0.5,
                        "y": 0.5,
                    }
                ],
            ),
        }

    @staticmethod
    def create_empty_pie_chart() -> Dict[str, Any]:
        """
        Cria gráfico de pizza vazio (sem dados).

        Returns:
            Dicionário com layout vazio
        """
        return {
            "data": [],
            "layout": go.Layout(
                annotations=[
                    {
                        "text": "Nenhuma demanda especial registrada no mês selecionado",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {"size": 20, "color": COLORS["gray"]},
                    }
                ],
                showlegend=False,
                xaxis={"visible": False},
                yaxis={"visible": False},
                plot_bgcolor=COLORS["background"],
                paper_bgcolor=COLORS["background"],
            ),
        }
