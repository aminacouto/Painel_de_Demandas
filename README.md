# Painel de Demandas

O **Painel de Demandas** é uma aplicação web interativa desenvolvida com Dash para análise e monitoramento de demandas a partir de *issues* do GitHub.

🔗 **Acesse a aplicação:**  
[https://dashboard-ihqb.onrender.com/](https://dashboard-ihqb.onrender.com/)

---

## 📊 Sobre o projeto

A aplicação consome dados diretamente da API do GitHub e transforma *issues* em informações visuais, permitindo acompanhar o volume e a categorização das demandas ao longo do tempo.

O objetivo é facilitar a tomada de decisão e dar visibilidade às demandas mais relevantes por meio de gráficos interativos, filtros dinâmicos e visualizações organizadas.

---

## 🚀 Funcionalidades

- 📈 **Gráfico comparativo anual**  
  Exibe o total de demandas abertas por mês e destaca demandas especiais.

- 🥧 **Gráfico de pizza interativo**  
  Mostra a distribuição das demandas especiais por grupo, com filtros por mês e tipo de demanda.

- 📋 **Lista de demandas especiais**  
  Exibe os títulos das *issues* com link direto para o GitHub.

- 🧭 **Filtros avançados**  
  Permite filtrar por mês e por tipo de demanda especial (*labels* aplicados às *issues*).

- 📊 **Comparativo de status**  
  Visualização separada de demandas abertas e fechadas.

- 🧪 **Ambiente de demonstração**  
  O projeto utiliza geração automatizada de *issues* para simular cenários reais de demandas e manter o dashboard constantemente populado para testes e demonstrações.

---

## 🧠 Como funciona

1. As *issues* são coletadas via API do GitHub.  
2. Os dados são processados e organizados em um DataFrame.  
3. Demandas especiais são identificadas por *labels* configuráveis.  
4. O dashboard exibe gráficos interativos, filtros dinâmicos e listas navegáveis de *issues*.  

---

## 🧪 Geração automatizada de dados

Para manter o ambiente de demonstração sempre populado, o projeto utiliza um script responsável pela geração automatizada de *issues* via API do GitHub.

As *issues* simuladas incluem:

- títulos variados
- grupos distintos
- categorização por *labels*
- distribuição temporal simulada
- dados organizados para análise visual

Essa abordagem permite validar a arquitetura da aplicação, os filtros, os gráficos e o processamento dos dados em um ambiente controlado e reproduzível.

---

## 🛠️ Tecnologias utilizadas

- Python  
- Dash  
- Plotly  
- Pandas  
- GitHub API  
- Requests  

---

## 🏗️ Arquitetura

O projeto segue uma estrutura modular:

- `github_client.py`: integração com a API do GitHub  
- `data_processor.py`: processamento e organização dos dados  
- `graph_generator.py`: geração dos gráficos  
- `components.py`: componentes visuais  
- `callbacks.py`: interatividade da aplicação  
- `app.py`: inicialização da aplicação  

---

## ✨ Destaques técnicos

- Código modular e organizado  
- Separação clara de responsabilidades  
- Integração com API REST do GitHub  
- Uso de variáveis de ambiente  
- Tipagem com *type hints*  
- Tratamento de erros e logging  
- Geração automatizada de dados para testes e demonstração  

---

## 🎯 Objetivo

Este projeto foi desenvolvido com foco em:

- Praticar integração com APIs  
- Trabalhar com visualização de dados  
- Aplicar boas práticas de organização de código  
- Construir aplicações web interativas com Python  
- Simular fluxos reais de monitoramento e análise de demandas