# Painel de Demandas

O **Painel de Demandas** é uma aplicação web interativa desenvolvida com Dash para análise e monitoramento de demandas a partir de *issues* do GitHub.

🔗 **Acesse a aplicação:**  
[https://dashboard-ihqb.onrender.com/](https://dashboard-ihqb.onrender.com/)

---

## 📊 Sobre o projeto

A aplicação consome dados diretamente da API do GitHub e transforma *issues* em informações visuais, permitindo acompanhar o volume e a categorização das demandas ao longo do tempo.

O objetivo é facilitar a tomada de decisão e dar visibilidade sobre as demandas mais relevantes.

---

## 🚀 Funcionalidades

- 📈 **Gráfico comparativo anual**  
  Visualização da quantidade de demandas abertas e demandas especiais por mês

- 🥧 **Gráfico de pizza**  
  Distribuição das demandas especiais por categoria (*labels*)

- 📋 **Lista de demandas**  
  Exibição detalhada com link direto para cada issue no GitHub

- 📅 **Filtro por mês**  
  Permite análise específica ou visão geral dos dados

---

## 🧠 Como funciona

1. As *issues* são coletadas via API do GitHub  
2. Os dados são processados e organizados  
3. As demandas especiais são identificadas por *labels*  
4. Os dados são exibidos em gráficos interativos com Dash/Plotly  

---

## 🛠️ Tecnologias utilizadas

- Python  
- Dash  
- Plotly  
- Pandas  
- GitHub API  

---

## 🏗️ Arquitetura

O projeto segue uma estrutura modular:

- `github_client.py`: integração com a API do GitHub  
- `data_processor.py`: tratamento e organização dos dados  
- `graph_generator.py`: geração dos gráficos  
- `components.py`: componentes visuais  
- `callbacks.py`: interatividade  
- `app.py`: inicialização da aplicação  

---

## ✨ Destaques técnicos

- Código modular e organizado  
- Separação clara de responsabilidades  
- Uso de variáveis de ambiente  
- Tipagem com type hints  
- Tratamento de erros e logging  

---

## 🎯 Objetivo

Este projeto foi desenvolvido com foco em:

- Praticar integração com APIs  
- Trabalhar com visualização de dados  
- Aplicar boas práticas de organização de código  
- Construir uma aplicação web interativa com Python  
