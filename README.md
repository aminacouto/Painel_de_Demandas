# LAD Issues Dashboard

O **LAD Issues Dashboard** é uma aplicação interativa desenvolvida com [Dash](https://dash.plotly.com/) para análise de demandas do laboratório. Ele utiliza a API do GitHub para acessar as issues de um repositório específico, permitindo visualizar gráficos comparativos, gráficos de pizza e uma lista com as demandas especiais, identificadas por Labels criadas no GitHub, com integração direta à plataforma.

---

## Funcionalidades

- **Gráfico Comparativo Anual**: Apresenta uma visão geral do total de demandas abertas e demandas especiais ao longo dos meses.
- **Gráfico de Pizza**: Exibe a distribuição percentual de demandas especiais separadas por grupo, facilitando a análise de categorias mais impactadas.
- **Lista de Demandas**: Mostra uma lista detalhada das demandas especiais, com links diretos para o GitHub.
- **Filtro por Mês**: Permite filtrar os dados por um mês específico ou visualizar informações de todos os meses, oferecendo flexibilidade na análise.

---

## Requisitos

- Python 3.8 ou superior
- Bibliotecas Python:
  - `dash`
  - `plotly`
  - `pandas`
  - `flask`
- Token de acesso ao GitHub (para acessar dados de repositórios privados, se necessário)

---

### Acesso ao LAD Issues no GitHub Codespaces

---

#### Criar um Token de Acesso no GitHub
1. Acesse GitHub Developer Settings.
2. Clique em "Generate new token" (ou "Generate new token (classic)", dependendo da versão).
3. Dê um nome para o token (por exemplo, LAD-Token).
4. Defina a data de expiração conforme necessário.
5. Em Scopes, selecione pelo menos:
- repo (acesso a repositórios privados, se necessário)
6. Clique em Generate token.
7. Copie o token gerado e guarde-o temporariamente (não será possível vê-lo novamente).

#### Adicionar o Token ao Codespaces
1. Criar um novo codespace.
2. No terminal do Codespace, execute o comando:  
   `bash script.sh`
3. O script solicitará que você insira o token de segurança gerado anteriormente.
4. Pressione Enter e aguarde o script ser finalizado.
   
**Importante:** O token ficará disponível enquanto o Codespace estiver ativo. Se um novo Codespace for aberto, será necessário adicionar novamente um token válido.
