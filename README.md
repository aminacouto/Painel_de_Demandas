# Painel de Demandas

O **Painel de Demandas** é uma aplicação interativa desenvolvida com [Dash](https://dash.plotly.com/) para análise de demandas do laboratório. Ela utiliza a API do GitHub para acessar as issues de um repositório específico, permitindo visualizar gráficos comparativos, gráficos de pizza e uma lista com as demandas especiais, identificadas por Labels criadas no GitHub, com integração direta à plataforma.

---

## Funcionalidades

- **Gráfico Comparativo Anual**: Apresenta uma visão geral do total de demandas abertas e demandas especiais ao longo dos meses.
- **Gráfico de Pizza**: Exibe a distribuição percentual de demandas especiais separadas por grupo, facilitando a análise de categorias mais impactadas.
- **Lista de Demandas**: Mostra uma lista detalhada das demandas especiais, com links diretos para o GitHub.
- **Filtro por Mês**: Permite filtrar os dados por um mês específico ou visualizar informações de todos os meses, oferecendo flexibilidade na análise.

---

## Requisitos

- Python 3.8 ou superior
- Bibliotecas Python (veja `requirements.txt`)
- Token de acesso ao GitHub (para acessar dados de repositórios privados, se necessário)

---

## Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd nome-do-seu-projeto
```

### 2. Criar Arquivo de Configuração
```bash
cp .env.example .env
```

### 3. Adicionar Token do GitHub
Edite o arquivo `.env` e adicione seu token:
```
GITHUB_TOKEN=seu_token_aqui
```

### 4. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 5. Executar a Aplicação
```bash
python app.py
```

A aplicação será acessível em `http://127.0.0.1:8050`

---

## Geração de Token do GitHub

1. Acesse [GitHub Developer Settings](https://github.com/settings/tokens)
2. Clique em "Generate new token (classic)"
3. Dê um nome para o token (ex: LAD-Token)
4. Defina a data de expiração
5. Em Scopes, selecione `repo` (acesso a repositórios)
6. Clique em "Generate token"
7. Copie o token e adicione ao arquivo `.env`

**Nota:** O token não será visível novamente após geração. Armazene-o com segurança.

---

## Estrutura do Projeto

```
<nome-do-seu-projeto>/
├── app.py                 # Aplicação principal
├── config.py              # Configurações e variáveis de ambiente
├── github_client.py       # Cliente GitHub API
├── data_processor.py      # Processamento de dados
├── graph_generator.py     # Geração de gráficos
├── components.py          # Componentes Dash
├── callbacks.py           # Callbacks interativos
├── requirements.txt       # Dependências Python
├── .env.example           # Exemplo de variáveis de ambiente
├── .gitignore             # Arquivos ignorados pelo Git
├── script.sh              # Script de setup (Linux/macOS)
├── assets/
│   └── style.css          # Estilos CSS personalizados
└── README.md              # Este arquivo
```

---

## Variáveis de Ambiente

Configure no arquivo `.env`:

```env
# GitHub
GITHUB_REPO=aminacouto/lad
GITHUB_TOKEN=seu_token

# Aplicação
YEAR=2026
DEBUG=True
HOST=127.0.0.1
PORT=8050
```

---

## Arquitetura

### Separação de Responsabilidades

- **config.py**: Centraliza todas as configurações e constantes
- **github_client.py**: Gerencia comunicação com a API do GitHub
- **data_processor.py**: Processa e transforma dados em DataFrames
- **graph_generator.py**: Cria gráficos Plotly
- **components.py**: Define componentes visuais Dash
- **callbacks.py**: Implementa interatividade da interface
- **app.py**: Orquestra todos os módulos e inicia a aplicação

### Type Hints e Docstrings

Todos os módulos incluem:
- ✅ Type hints para argumentos e retornos
- ✅ Docstrings descritivas
- ✅ Logging apropriado
- ✅ Tratamento de erros robusto

---

## Melhorias Implementadas

### ✨ Refatorações

1. **Modularização**: Código separado em 8 módulos especializados
2. **Configuração Externa**: Variáveis de ambiente em `.env`
3. **Type Safety**: Anotações de tipo em todas as funções
4. **Logging**: Sistema de logs estruturado
5. **Tratamento de Erros**: Validações e exceções apropriadas
6. **Documentação**: Docstrings e comments claros
7. **Código Limpo**: Remoção de duplicação e variáveis globais
8. **Versionamento**: requirements.txt com versões fixas

### 📦 Arquivos Novos

- `.env.example`: Template de configuração
- `.gitignore`: Padrões de exclusão melhorados
- `requirements.txt`: Dependências do projeto
- Módulos especializados: github_client, data_processor, graph_generator, components, callbacks

---

## Desenvolvimento

### Executar em Modo Debug

```bash
export DEBUG=True
python app.py
```

### Ver Logs

```bash
# Linux/macOS
python app.py 2>&1 | tee app.log

# Windows
python app.py > app.log 2>&1
```

### Adicionar Novas Dependências

```bash
pip install nova-biblioteca
pip freeze > requirements.txt
```

---

## Troubleshooting

### Erro: "Nenhuma issue encontrada"
- Verifique se o token está correto
- Confirme se o repositório está correto em `GITHUB_TOKEN`
- Verifique a conectividade com a internet

### Erro: "ModuleNotFoundError"
- Instale as dependências: `pip install -r requirements.txt`
- Verifique se está usando o ambiente virtual correto

### Porta já em uso
- Mude a porta em `.env`: `PORT=8051`
- Ou encerre o processo usando a porta

---

## Suporte

Para questões ou sugestões, abra uma issue no repositório.

---

## Licença

Este projeto é fornecido como está. Consulte a licença do repositório para mais informações.

