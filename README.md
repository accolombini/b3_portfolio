# B3_Portfolio

[![Python](https://img.shields.io/badge/Python-3.12.5-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3.1-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4.5-blue.svg)](https://www.typescriptlang.org/)
[![Biome](https://img.shields.io/badge/Biome-1.9.4-60a5fa.svg)](https://biomejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()

> **Sistema modular de análise e gerenciamento de portfólio de investimentos focado em ativos brasileiros (B3)**

## Índice

- [Descrição](#descrição)
- [Status do Projeto](#status-do-projeto)
- [Recursos Principais](#recursos-principais)
  - [Indicadores Financeiros](#indicadores-financeiros-calculados)
  - [Microservices](#microservices-independentes)
  - [Frontend](#frontend)
  - [Fontes de Dados](#fontes-de-dados)
  - [Metodologia de Análise](#metodologia-de-análise)
- [Tecnologias](#tecnologias)
- [Qualidade e Segurança](#qualidade-e-segurança)
- [Roadmap de Desenvolvimento](#roadmap-de-desenvolvimento)
- [Riscos e Mitigações](#riscos-e-mitigações)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Práticas de Desenvolvimento](#práticas-de-desenvolvimento)
- [Testes](#testes)
- [Arquitetura](#arquitetura)
- [Sobre o Biome](#sobre-o-biome)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Contribuição](#contribuição)
- [FAQ](#faq-perguntas-frequentes)
- [Recursos Adicionais](#recursos-adicionais)
- [Documentação Adicional](#documentação-adicional)
- [Licença](#licença)

---

## Descrição

O **B3_Portfolio** é um sistema modular de análise e gerenciamento de portfólio de investimentos, focado em ativos brasileiros (ex.: ações listadas na B3, fundos registrados na CVM, títulos públicos e LCAs).

O projeto:

- Analisa um portfólio inicial com 3 ativos:
  - **Fundos de Investimento RF LP High**
  - **Tesouro Direto 01.03.2031-210100-LFT**
  - **LCA BB LCA PREFIXADA**
- Realiza varreduras para sugerir **2–3 novos investimentos**.
- Calcula indicadores financeiros e de risco (ex.: **Alfa, Beta, Sharpe, Treynor, Sortino, R², Correlação, P/E, ROE**, etc.).
- Faz **projeções de 2 anos** com base em **histórico de 5 anos**.
- Executa **simulações Monte Carlo** e **otimização** via **Teoria Moderna de Portfólio (MPT)**, incluindo **Fronteira Eficiente**.

O sistema foi desenhado com **arquitetura de microservices** para escalabilidade e resiliência, usando **ferramentas open-source e gratuitas** (sem custos).

> ⚠️ **Aviso importante / Disclaimers (CVM):**
> Este projeto é **educacional e experimental**. **Não constitui recomendação, consultoria, sugestão ou aconselhamento** de investimento.
> Use por sua conta e risco e inclua **disclaimers regulatórios** apropriados (ex.: CVM) em qualquer material derivado.

---

## 🚀 Quick Start

```bash
# 1. Clone o repositório
git clone https://github.com/accolombini/b3_portfolio.git
cd b3_portfolio

# 2. Configure o ambiente Python
python -m venv b3
source b3/bin/activate  # Linux/Mac | b3\Scripts\activate (Windows)

# 3. Instale tudo com Make (recomendado)
make install  # Instala todas as dependências

# Ou manualmente:
pip install -r requirements.txt
cd frontend && npm install

# 4. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# 5. Inicie a infraestrutura
make docker-up  # ou docker-compose up -d

# 6. Execute os testes
make test       # Testa backend e frontend

# 7. Inicie o desenvolvimento
make backend-dev   # Terminal 1: API Gateway (porta 8000)
make frontend-dev  # Terminal 2: Frontend (porta 5173)
```

### 🛠️ Comandos Úteis (Makefile)

```bash
make help          # Ver todos os comandos disponíveis
make install       # Instalar todas as dependências
make test          # Rodar todos os testes
make lint          # Verificar qualidade do código
make format        # Formatar código automaticamente
make docker-up     # Iniciar PostgreSQL e Redis
make clean         # Limpar arquivos temporários
make ci            # Rodar pipeline CI localmente
```

> 💡 **Dica**: Use `make help` para ver todos os comandos disponíveis!

---

## 📸 Screenshots

> 🚧 **Em desenvolvimento**: Screenshots serão adicionados conforme os componentes forem implementados.

**Planejado:**

- 📊 Dashboard principal com overview do portfólio
- 📈 Gráficos de performance e fronteira eficiente
- 🔍 Interface de varredura e sugestões de ativos
- 📑 Geração de relatórios PDF

---

## ✨ Features Chave

| Feature                      | Descrição                                  | Status          |
| ---------------------------- | ------------------------------------------ | --------------- |
| 📊 **Análise de Portfólio**  | Gerenciamento de 3+ ativos brasileiros     | ✅ Planejado    |
| 📈 **Indicadores Avançados** | Alfa, Beta, Sharpe, Sortino, R², VaR, CVaR | ✅ Planejado    |
| 🎲 **Monte Carlo**           | 10.000 simulações para projeções de 2 anos | ✅ Planejado    |
| 🔍 **Scanning Inteligente**  | Varredura B3 com sugestões de 2-3 ativos   | ✅ Planejado    |
| 📉 **Fronteira Eficiente**   | Otimização MPT (Markowitz)                 | ✅ Planejado    |
| 📑 **Relatórios**            | Exportação em JSON, CSV e PDF              | ✅ Planejado    |
| 🔒 **Zero Vulnerabilidades** | Frontend auditado e seguro                 | ✅ Implementado |
| ⚡ **Performance**           | Biome (100x mais rápido que ESLint)        | ✅ Implementado |
| 🐳 **Dockerizado**           | Deploy simplificado com Docker Compose     | 🔄 Em progresso |
| 🧪 **TDD**                   | Cobertura de testes com pytest e Vitest    | 🔄 Em progresso |

---

## Status do Projeto

📅 **Última atualização**: 17 de fevereiro de 2026

### Fase Atual: **Planejamento e Setup Inicial (Fase 2)**

✅ **Concluído:**

- Estrutura de diretórios dos microservices
- Configuração do frontend (React/TypeScript/Vite/Biome)
- Arquivo `requirements.txt` com dependências Python
- Documentação arquitetural na pasta `Projeto/`
- Migração para Biome (linter/formatter moderno)
- Zero vulnerabilidades no frontend

🔄 **Em Progresso:**

- Configuração do Docker Compose para PostgreSQL e Redis
- Implementação do API Gateway
- Setup de migrações com Alembic

📋 **Próximos Passos:**

- Implementação dos microservices (Portfolio, Analysis, Scanning, Projection, Reporting)
- Desenvolvimento dos componentes frontend
- Integração com fontes de dados (yfinance, CVM, Tesouro)
- Testes unitários e de integração
- Deploy e monitoramento

---

## Recursos principais

### Indicadores Financeiros Calculados

#### Indicadores de Risco e Retorno

- **Alfa (α)**: Retorno excedente em relação ao benchmark (objetivo: α > 0)
- **Beta (β)**: Sensibilidade do ativo em relação ao mercado (IBOVESPA)
- **Índice de Sharpe**: Retorno ajustado ao risco (quanto maior, melhor)
- **Índice de Treynor**: Retorno em excesso por unidade de risco sistemático
- **Índice de Sortino**: Similar ao Sharpe, mas considera apenas downside risk
- **R² (R-quadrado)**: Percentual de variação explicada pelo mercado (0-100%)
- **Correlação**: Relação linear entre ativos (-1 a +1)
- **VaR (Value at Risk)**: Perda máxima esperada com determinada confiança
- **CVaR (Conditional VaR)**: Perda média além do VaR

#### Indicadores Fundamentalistas

- **P/E (Price-to-Earnings)**: Preço da ação dividido pelo lucro por ação
- **P/B (Price-to-Book)**: Índice preço/valor patrimonial
- **EV/EBITDA**: Valor da empresa / lucros operacionais
- **ROE (Return on Equity)**: Retorno sobre patrimônio líquido
- **ROA (Return on Assets)**: Retorno sobre ativos
- **Margem Líquida**: Lucro líquido / receita total
- **D/E (Debt-to-Equity)**: Índice de endividamento
- **Liquidez Corrente**: Ativo circulante / passivo circulante
- **Liquidez Seca**: (Ativo circulante - estoques) / passivo circulante

### Microservices independentes

- **API Gateway**: Roteamento e autenticação.
- **Portfolio Service**: Gerenciamento de ativos e balanceamento.
- **Analysis Service**: Cálculos de risco/retorno e indicadores fundamentalistas.
- **Scanning Service**: Varredura e sugestão de novos ativos.
- **Projection Service**: Simulações Monte Carlo, ARIMA e MPT.
- **Reporting Service**: Geração de relatórios (JSON/CSV/PDF).

#### Detalhes dos Serviços

**Portfolio Service**

- CRUD de ativos do portfólio
- Cálculo de composição e alocação
- Balanceamento via Teoria Moderna de Portfólio (MPT)
- Rebalanceamento periódico
- Histórico de transações

**Analysis Service**

- Cálculo de todos os indicadores de risco/retorno
- Análise fundamentalista (P/E, ROE, etc.)
- Comparação com benchmarks (IBOVESPA, CDI)
- Matriz de correlação entre ativos
- Análise de concentração de risco

**Scanning Service**

- Varredura diária de ativos brasileiros (B3)
- Aplicação de filtros (liquidez, setor, indicadores)
- Scoring e ranking de oportunidades
- Sugestão de 2-3 novos ativos
- Alertas de oportunidades

**Projection Service**

- Simulações Monte Carlo (10.000 iterações)
- Projeções ARIMA para 2 anos
- Otimização de fronteira eficiente (Markowitz)
- Maximização de Sharpe Ratio
- Cenários (otimista, pessimista, realista)

**Reporting Service**

- Relatórios em JSON, CSV e PDF
- Gráficos (Matplotlib) de performance
- Dashboard consolidado
- Exportação de dados históricos
- Relatórios periódicos automatizados

### Frontend

- Interface reativa em **React/TypeScript** com **Vite**
- Dashboards e gráficos (ex.: **Chart.js**)
- Linting e formatação com **Biome** (linter/formatter moderno, ultra-rápido e sem vulnerabilidades)

### Fontes de Dados

#### APIs e Bibliotecas

- **yfinance**: Cotações históricas e em tempo real de ações da B3, IBOVESPA, índices setoriais
- **Banco Central do Brasil API**: Taxa SELIC, CDI, IPCA
- **CVM (Dados Abertos)**: Fundos de investimento, informes regulatórios
- **Tesouro Direto**: Preços e taxas de títulos públicos

#### Web Scraping Ético

- **BeautifulSoup + requests**: Coleta complementar respeitando robots.txt
- **Rate limiting**: Respeito aos limites de requisições
- **Caching**: Redis para evitar requisições desnecessárias

#### Dados Históricos

- **Período de análise**: 5 anos de dados históricos
- **Frequência**: Dados diários (ajustados para dividendos/splits)
- **Validação**: Múltiplas fontes quando possível
- **Atualização**: Diária para dados de mercado

### Tecnologias

#### Backend

- 🐍 **Python 3.12.5** - Linguagem principal
- ⚡ **FastAPI 0.110.0** - Framework web assíncrono
- 🗄️ **PostgreSQL** - Banco de dados relacional
- 📦 **Redis** - Cache e message broker
- 🔄 **Celery** - Processamento assíncrono
- 🧪 **pytest** - Framework de testes

#### Frontend

- ⚛️ **React 18.3.1** - Biblioteca UI
- 📘 **TypeScript 5.4.5** - Tipagem estática
- ⚡ **Vite 7.3.1** - Build tool ultra-rápido
- 🎨 **Chart.js 4.4.1** - Visualização de dados
- 🔧 **Biome 1.9.4** - Linter/Formatter moderno
- 🧪 **Vitest 4.0.18** - Framework de testes

#### Dados e Análise

- 📊 **Pandas 2.2.1** - Manipulação de dados
- 🔢 **NumPy 1.26.4** - Computação numérica
- 📈 **yfinance 0.2.37** - Dados de mercado
- 🧮 **SciPy 1.12.0** - Algoritmos científicos
- 📉 **Statsmodels 0.14.1** - Modelos estatísticos
- 📊 **Matplotlib 3.8.3** - Visualização

#### DevOps e Infraestrutura

- 🐳 **Docker** - Containerização
- 🔧 **Docker Compose** - Orquestração local
- 🔄 **Alembic 1.13.1** - Migrações de banco
- 📝 **structlog 24.1.0** - Logging estruturado

### Qualidade e Segurança

- ✅ **Zero vulnerabilidades** no frontend (`npm audit`)
- 🔒 **Dependências mínimas** (149 pacotes vs. 370+ com ESLint)
- ⚡ **Build otimizado** com Vite
- 🧪 **Cobertura de testes** com pytest e Vitest

### Metodologia de Análise

#### Teoria Moderna de Portfólio (MPT)

- **Fronteira Eficiente**: Combinações ótimas de risco/retorno
- **Modelo de Markowitz**: Otimização quadrática para minimizar risco
- **Índice de Sharpe**: Seleção do portfólio com melhor retorno ajustado
- **Diversificação**: Redução de risco não-sistemático
- **Rebalanceamento**: Manutenção de alocação target

#### Simulações Monte Carlo

- **10.000 iterações** para cada cenário
- **Distribuições**: Normal, Log-normal, t-Student
- **Correlações**: Matriz de covariância histórica
- **Intervalos de confiança**: 95% e 99%
- **Stress testing**: Cenários extremos

#### Modelos de Projeção

- **ARIMA**: Previsões de séries temporais
- **Regressão Linear**: Relação com benchmarks
- **Médias Móveis**: Identificação de tendências
- **Volatilidade GARCH**: Modelagem de volatilidade variável

### Restrições e Princípios

- ✅ Somente ferramentas **free** (open-source / gratuitas)
- ✅ **Sem mocks/hardcodes** para lógica crítica de negócio
- ✅ **Foco em precisão** e dados reais
- ✅ **TDD** (Test-Driven Development) obrigatório
- ✅ **Código limpo** e bem documentado
- ✅ **Conformidade regulatória** (CVM)

---

## Roadmap de Desenvolvimento

### Fase 1: Planejamento ✅ (Concluída)

- Definição de escopo e arquitetura
- Seleção de tecnologias
- Documentação inicial
- **Duração**: 1 semana

### Fase 2: Setup de Infraestrutura 🔄 (Em Progresso)

- Docker Compose (PostgreSQL, Redis)
- Configuração de ambientes
- CI/CD inicial
- **Duração**: 2 semanas

### Fase 3: Desenvolvimento de Microservices 📋 (Próxima)

- API Gateway com autenticação JWT
- Portfolio Service com CRUD e MPT
- Analysis Service com todos os indicadores
- Scanning Service com varredura B3
- Projection Service com Monte Carlo
- Reporting Service
- **Duração**: 4 semanas

### Fase 4: Integrações 📋 (Planejada)

- Integração yfinance e dados B3
- Web scraping CVM e Tesouro Direto
- Celery para tarefas assíncronas
- **Duração**: 3 semanas

### Fase 5: Frontend 📋 (Planejada)

- Componentes React + TypeScript
- Dashboards com Chart.js
- Interface de análise e relatórios
- **Duração**: 3 semanas

### Fase 6: Testes e Validação 📋 (Planejada)

- Testes unitários (pytest, Vitest)
- Testes de integração
- Validação de indicadores
- Simulações reais
- **Duração**: 2 semanas

### Fase 7: Deploy e Monitoramento 📋 (Planejada)

- Deploy em produção
- Monitoramento e logs
- Documentação final
- **Duração**: 1 semana

**Tempo Total Estimado**: 16 semanas (2-4 meses em ritmo part-time)

---

## Riscos e Mitigações

### Riscos Técnicos

| Risco                           | Impacto | Probabilidade | Mitigação                                          |
| ------------------------------- | ------- | ------------- | -------------------------------------------------- |
| Dados imprecisos ou incompletos | Alto    | Média         | Validação com múltiplas fontes; fallbacks          |
| Complexidade de microservices   | Médio   | Alta          | Docker Compose simplificado; documentação clara    |
| Performance de simulações       | Médio   | Baixa         | Celery para processamento assíncrono; cache Redis  |
| Limitação de APIs gratuitas     | Alto    | Média         | Rate limiting; caching agressivo; múltiplas fontes |

### Riscos Regulatórios

| Risco                     | Impacto | Probabilidade | Mitigação                                       |
| ------------------------- | ------- | ------------- | ----------------------------------------------- |
| Não conformidade com CVM  | Alto    | Baixa         | Disclaimers claros; sem recomendações diretas   |
| Problemas de web scraping | Médio   | Média         | Respeito a robots.txt; rate limiting; fallbacks |

### Riscos de Negócio

| Risco                  | Impacto | Probabilidade | Mitigação                                     |
| ---------------------- | ------- | ------------- | --------------------------------------------- |
| Mudanças no mercado    | Médio   | Alta          | Sistema adaptável; parâmetros configuráveis   |
| Obsolescência de dados | Baixo   | Média         | Atualização diária; alertas de desatualização |

---

## Requisitos

- Python **3.12.5**
- Node.js **LTS** (v20+)
- Docker e Docker Compose
- Git
- **Mínimo 8GB RAM** (para simulações Monte Carlo)
- **2GB espaço em disco** (dados históricos + containers)

---

## Instalação

### 1) Clone do repositório

```bash
git clone https://github.com/accolombini/b3_portfolio.git
cd b3_portfolio
```

### 2) Adicionar remoto (se necessário)

```bash
git remote add origin https://github.com/accolombini/b3_portfolio.git
git remote -v
```

### 3) Ambiente virtual Python

Crie e ative um ambiente virtual chamado `b3`:

```bash
python -m venv b3
source b3/bin/activate  # Linux/Mac
# ou b3\Scripts\activate no Windows
```

Instale dependências:

```bash
pip install -r requirements.txt
```

### 4) Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/portfolio_db
REDIS_URL=redis://localhost:6379/0
```

### 5) Dependências do frontend

```bash
cd frontend
npm install
```

> O projeto frontend usa **Biome** para linting e formatação, garantindo código limpo e sem vulnerabilidades de segurança.

### 6) Subir infraestrutura com Docker

> Ajuste o `docker-compose.yml` conforme a topologia real de serviços do repositório.

```bash
docker-compose up -d
```

### 7) Migrações (por serviço)

Exemplo no **Portfolio Service**:

```bash
cd services/portfolio
alembic upgrade head
```

---

## Uso

### 1) Rodar microservices localmente

Exemplo: **API Gateway**

```bash
cd services/api-gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Repita para os demais serviços em portas **8001+** (ajuste conforme o projeto).

### 2) Rodar o frontend

```bash
cd frontend
npm run dev
```

Acesse em `http://localhost:5173` (proxy para o Gateway).

### 3) Comandos disponíveis no frontend

```bash
npm run dev         # Iniciar servidor de desenvolvimento
npm run build       # Build para produção (TypeScript + Vite)
npm run preview     # Preview do build de produção
npm run test        # Executar testes com Vitest
npm run lint        # Verificar código com Biome
npm run lint:fix    # Corrigir problemas automaticamente
npm run format      # Formatar código
```

---

## API Endpoints

Todos os endpoints são acessados através do **API Gateway** (porta 8000).

### Autenticação

```bash
# Login
POST /api/auth/login
Content-Type: application/json
{
  "username": "user@example.com",
  "password": "senha123"
}

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}

# Usar token em requisições
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Portfolio Service

```bash
# Listar portfólio
GET /api/portfolios
GET /api/portfolios/{id}

# Criar/atualizar portfólio
POST /api/portfolios
PUT /api/portfolios/{id}

# Adicionar ativo
POST /api/portfolios/{id}/assets
{
  "ticker": "PETR4",
  "quantity": 100,
  "purchase_price": 28.50
}

# Balanceamento MPT
POST /api/portfolios/{id}/rebalance
{
  "target_return": 0.15,
  "risk_tolerance": "moderate"
}
```

### Analysis Service

```bash
# Calcular indicadores de risco/retorno
POST /api/analyze/metrics
{
  "portfolio_id": "abc123",
  "benchmark": "IBOV",
  "period": "5y"
}

# Response
{
  "alpha": 0.023,
  "beta": 1.15,
  "sharpe": 1.42,
  "treynor": 0.089,
  "sortino": 1.68,
  "r_squared": 0.87,
  "var_95": -0.032,
  "cvar_95": -0.045
}

# Análise fundamentalista
GET /api/analyze/fundamentals/{ticker}

# Correlação entre ativos
POST /api/analyze/correlation
{
  "tickers": ["PETR4", "VALE3", "ITUB4"]
}
```

### Scanning Service

```bash
# Buscar sugestões de novos ativos
GET /api/scan/suggestions?sectors=energia,financeiro&min_liquidity=1000000

# Response
{
  "suggestions": [
    {
      "ticker": "EGIE3",
      "name": "Engie Brasil",
      "sector": "Energia",
      "score": 8.5,
      "reasons": ["Alto dividend yield", "P/E atrativo", "Crescimento constante"]
    }
  ]
}

# Alertas de oportunidades
GET /api/scan/alerts

# Executar varredura manual
POST /api/scan/run
```

### Projection Service

```bash
# Simulação Monte Carlo
POST /api/project/simulate
{
  "portfolio_id": "abc123",
  "iterations": 10000,
  "years": 2,
  "confidence_levels": [0.95, 0.99]
}

# Response
{
  "mean_return": 0.157,
  "median_return": 0.143,
  "std_dev": 0.089,
  "confidence_intervals": {
    "95": {"min": -0.023, "max": 0.312},
    "99": {"min": -0.067, "max": 0.389}
  },
  "scenarios": {...}
}

# Projeção ARIMA
POST /api/project/forecast
{
  "ticker": "PETR4",
  "periods": 24,
  "model": "arima"
}

# Fronteira Eficiente
POST /api/project/efficient-frontier
{
  "tickers": ["PETR4", "VALE3", "ITUB4"],
  "num_portfolios": 10000
}
```

### Reporting Service

```bash
# Gerar relatório PDF
POST /api/reports/generate
{
  "portfolio_id": "abc123",
  "format": "pdf",
  "sections": ["summary", "performance", "risk", "projections"]
}

# Download relatório
GET /api/reports/{report_id}/download

# Listar relatórios
GET /api/reports?portfolio_id=abc123
```

### Health Check

```bash
# Verificar saúde dos serviços
GET /health
GET /api/portfolio/health
GET /api/analysis/health
GET /api/scanning/health
GET /api/projection/health
GET /api/reporting/health
```

---

## Práticas de Desenvolvimento

### Test-Driven Development (TDD)

1. **Red**: Escreva um teste que falha

   ```python
   def test_calculate_sharpe_ratio():
       portfolio = create_test_portfolio()
       sharpe = calculate_sharpe_ratio(portfolio)
       assert sharpe > 0
   ```

2. **Green**: Implemente o mínimo para passar

   ```python
   def calculate_sharpe_ratio(portfolio):
       # Implementação mínima
       return portfolio.excess_return / portfolio.std_dev
   ```

3. **Refactor**: Melhore o código mantendo testes verdes

   ```python
   def calculate_sharpe_ratio(portfolio, risk_free_rate=0.0):
       """
       Calcula o índice de Sharpe.

       Args:
           portfolio: Portfolio object
           risk_free_rate: Taxa livre de risco (padrão: 0.0)

       Returns:
           float: Sharpe ratio
       """
       excess_return = portfolio.returns.mean() - risk_free_rate
       std_dev = portfolio.returns.std()

       if std_dev == 0:
           return 0.0

       return excess_return / std_dev
   ```

### Code Review Checklist

- [ ] Testes unitários passando (`pytest`)
- [ ] Cobertura de código > 80%
- [ ] Linting sem erros (`biome check` / `ruff check`)
- [ ] Documentação atualizada (docstrings, README)
- [ ] Sem credenciais ou dados sensíveis
- [ ] Logs estruturados adicionados
- [ ] Validação de inputs (Pydantic)
- [ ] Tratamento de erros adequado
- [ ] Performance verificada (sem N+1 queries)
- [ ] Commits semânticos e descritivos

### Padrões de Código

#### Python

```python
# Use type hints
def calculate_return(prices: list[float], dividends: list[float] = None) -> float:
    """Calculate total return including dividends."""
    ...

# Use Pydantic para validação
from pydantic import BaseModel, validator

class AssetCreate(BaseModel):
    ticker: str
    quantity: int
    price: float

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

# Use logging estruturado
import structlog

logger = structlog.get_logger()
logger.info("portfolio_created", portfolio_id=portfolio.id, assets=len(portfolio.assets))
```

#### TypeScript (Frontend)

```typescript
// Use interfaces para tipos
interface Portfolio {
  id: string;
  name: string;
  assets: Asset[];
  created_at: Date;
}

// Use async/await
async function fetchPortfolio(id: string): Promise<Portfolio> {
  const response = await api.get(`/portfolios/${id}`);
  return response.data;
}

// Use React Hooks
function usePortfolio(id: string) {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPortfolio(id)
      .then(setPortfolio)
      .finally(() => setLoading(false));
  }, [id]);

  return { portfolio, loading };
}
```

### Estrutura de Branches

```bash
main          # Produção (só merge de release)
  └─ develop  # Desenvolvimento (só merge de feature)
      └─ feature/portfolio-rebalancing  # Nova funcionalidade
      └─ feature/monte-carlo-simulation
      └─ hotfix/fix-sharpe-calculation  # Correção urgente
      └─ release/v1.0.0                 # Preparação para release
```

### Workflow de Desenvolvimento

1. **Criar branch** do develop

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nova-funcionalidade
   ```

2. **Desenvolver** com TDD
   - Escrever testes
   - Implementar código
   - Refatorar

3. **Commit** frequente e semântico

   ```bash
   git add .
   git commit -m "feat(analysis): add Sortino ratio calculation"
   ```

4. **Push** e criar **Pull Request**

   ```bash
   git push origin feature/nova-funcionalidade
   ```

5. **Code Review** e aprovação

6. **Merge** no develop

7. **Deploy** automático (CI/CD)

---

## Testes

### Backend (Python)

Rode `pytest` em cada serviço:

```bash
pytest
```

### Frontend (TypeScript)

```bash
cd frontend
npm run test    # Testes com Vitest
npm run lint    # Verificação de código com Biome
```

> Sugestão: padronize `Makefile` por serviço com alvos como `test`, `lint`, `format`, `run`, etc.

---

## Sobre o Biome

O projeto utiliza **Biome** (anteriormente Rome) como ferramenta de linting e formatação para o frontend. Biome oferece:

- 🚀 **Performance**: 100x mais rápido que ESLint
- 🔒 **Segurança**: Zero vulnerabilidades (sem ajv, sem dependências complexas)
- 🛠️ **Tudo em um**: Linter + Formatter integrados
- 📦 **Leve**: Reduz drasticamente o número de dependências
- ⚙️ **Configuração simples**: Arquivo único `biome.json`

### Configuração

O projeto está configurado em [`frontend/biome.json`](frontend/biome.json) com:

- Regras recomendadas ativadas
- Suporte para React e TypeScript
- Formatação consistente (100 caracteres por linha, single quotes, etc.)
- Importações organizadas automaticamente

---

## Contribuição

Contribuições são bem-vindas! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) antes de submeter Pull Requests.

### Processo Rápido

- Use branches para features:
  ```bash
  git checkout -b feature/novo-servico
  ```
- Siga **TDD**: escreva testes antes do código.
- **Frontend**: Execute `npm run lint:fix` e `npm run format` antes de commitar.
- Commits semânticos:
  - `feat: adiciona endpoint X`
  - `fix: corrige cálculo do indicador Y`
  - `docs: atualiza README`
  - `style: formata código com Biome`
- Pull requests com descrição clara e testes passando.

### Áreas que Precisam de Ajuda

- 🔌 Integrações de dados (novos provedores, validação)
- 📊 Algoritmos financeiros (novos indicadores, ML)
- 🎨 Frontend (componentes, UX/UI, acessibilidade)
- 🧪 Testes (cobertura, integração, E2E)
- 📚 Documentação (tutoriais, exemplos)

---

## Licença

**MIT License**. Veja `LICENSE` para detalhes.

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/portfolio_db
DATABASE_TEST_URL=postgresql://postgres:postgres@localhost:5432/portfolio_test_db

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_TEST_URL=redis://localhost:6379/1

# JWT Authentication
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (se necessário)
# ALPHAVANTAGE_API_KEY=your-api-key-here

# Environment
ENVIRONMENT=development  # development | staging | production

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO  # DEBUG | INFO | WARNING | ERROR

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

> ⚠️ **Importante**: Nunca commite o arquivo `.env` no Git. Use `.env.example` como template.

---

## Documentação adicional

### Arquivos do Projeto

- 📘 [README.md](README.md) - Documentação principal (você está aqui!)
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Guia de contribuição detalhado
- 📝 [CHANGELOG.md](CHANGELOG.md) - Histórico de mudanças e versões
- ⚙️ [.env.example](.env.example) - Template de variáveis de ambiente
- 🛠️ [Makefile](Makefile) - Automação de tarefas de desenvolvimento
- 🔧 [.pre-commit-config.yaml](.pre-commit-config.yaml) - Hooks de pré-commit
- 📦 [requirements.txt](requirements.txt) - Dependências Python (produção)
- 🧪 [requirements-dev.txt](requirements-dev.txt) - Dependências Python (desenvolvimento)
- 📄 [LICENSE](LICENSE) - Licença MIT

### Documentos Técnicos (Pasta `Projeto/`)

> ⚠️ **Nota**: A pasta `Projeto/` não é versionada no Git por conter documentos em progresso.

Disponível localmente:

- `Draft_Projeto.docx` - Especificações detalhadas do projeto
- `Visao_Geral_Projeto.docx` - Visão executiva e objetivos
- `Arquitetura_Sistema_Análise_Portfolio.docx` - Diagramas e fluxos de dados
- `Prompts_Projeto.docx` - Prompts para desenvolvimento sequencial
- `novos_chats.json` - Estrutura de dados e configuração do projeto

---

## Arquitetura

### Visão Geral

O B3_Portfolio utiliza uma **arquitetura de microservices** com os seguintes componentes:

```text
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React/Vite)                    │
│              Charts, Dashboards, Authentication              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (FastAPI)                    │
│         JWT Auth, Rate Limiting, Request Routing            │
└─┬─────────┬──────────┬───────────┬──────────┬──────────────┘
  │         │          │           │          │
  │ Port    │ Port     │ Port      │ Port     │ Port
  │ 8001    │ 8002     │ 8003      │ 8004     │ 8005
  ▼         ▼          ▼           ▼          ▼
┌─────┐ ┌─────┐   ┌─────┐    ┌─────┐    ┌─────┐
│Port │ │Anal │   │Scan │    │Proj │    │Rept │
│folio│ │ysis │   │ning │    │ection│   │ορting│
└──┬──┘ └──┬──┘   └──┬──┘    └──┬──┘    └──┬──┘
   │       │          │          │          │
   ├───────┴──────────┴──────────┘          │
   │                                         │
   ▼                                         ▼
┌─────────────────┐                    ┌────────┐
│   PostgreSQL    │                    │ Redis  │
│  (Dados Persist)│                    │(Cache) │
└─────────────────┘                    └────┬───┘
                                             │
                                             ▼
                                        ┌────────┐
                                        │ Celery │
                                        │Workers │
                                        └────────┘
                                             │
                                             ▼
                                        [yfinance]
                                        [CVM APIs]
                                        [Tesouro]
```

### Comunicação Entre Serviços

- **Frontend ↔ Gateway**: REST API / WebSockets
- **Gateway ↔ Services**: REST API interna
- **Services ↔ Database**: SQLAlchemy ORM
- **Services ↔ Redis**: Cache e message broker
- **Celery Workers**: Tarefas assíncronas (scan, projections)

### Fluxo de Dados

1. **Usuário** acessa o frontend e faz login
2. **Frontend** envia requisição ao **API Gateway** com JWT token
3. **Gateway** valida token e roteia para o serviço apropriado
4. **Serviço** processa requisição:
   - Consulta banco de dados (PostgreSQL)
   - Consulta cache (Redis) se disponível
   - Dispara tarefas assíncronas (Celery) se necessário
   - Busca dados externos (yfinance, CVM, etc.)
5. **Serviço** retorna resposta ao Gateway
6. **Gateway** agrega respostas e retorna ao Frontend
7. **Frontend** renderiza dados para o usuário

### Escalabilidade

- **Horizontal**: Cada microservice pode escalar independentemente
- **Vertical**: Otimização de queries e algoritmos
- **Cache**: Redis para reduzir latência e carga no DB
- **Async**: Celery para tarefas pesadas (Monte Carlo, varreduras)
- **Load Balancing**: Nginx/Traefik (futuro)

### Segurança

- 🔐 **Autenticação**: JWT tokens com expiração
- 🔒 **Autorização**: RBAC (Role-Based Access Control)
- 🛡️ **Rate Limiting**: Proteção contra abuso de API
- 🔑 **Secrets Management**: Variáveis de ambiente (.env)
- 📊 **Audit Logs**: Registro de ações críticas
- 🚫 **Input Validation**: Pydantic models em todos os endpoints
- 🌐 **CORS**: Configuração restrita para frontend
- 🔐 **HTTPS**: Obrigatório em produção

### Monitoramento e Observabilidade (Planejado)

- **Logs Estruturados**: structlog para análise
- **Métricas**: Prometheus + Grafana
- **Tracing**: OpenTelemetry para debugging
- **Health Checks**: Endpoints `/health` em todos os serviços
- **Alertas**: Notificações para falhas críticas

---

## Estratégia de Continuidade

### Documentação

Todos os documentos técnicos estão organizados em:

- **`Projeto/`**: Documentação arquitetural (não versionada)
  - `Draft_Projeto.docx`: Especificações detalhadas
  - `Visao_Geral_Projeto.docx`: Visão executiva
  - `Arquitetura_Sistema_Análise_Portfolio.docx`: Diagramas e fluxos
  - `Prompts_Projeto.docx`: Prompts para desenvolvimento sequencial
  - `novos_chats.json`: Estrutura de dados do projeto

### Versionamento

- **Git**: Controle de versão completo
- **Semantic Versioning**: `MAJOR.MINOR.PATCH`
- **Branches**: `main`, `develop`, `feature/*`, `hotfix/*`
- **Tags**: Para releases importantes

### Backup

- **Código**: GitHub (repositório remoto)
- **Documentação**: Pasta `Projeto/` com backup local
- **Banco de Dados**: Scripts de backup automático (planejado)

### Continuidade da Conversa

Para retomar o projeto em novos chats:

1. Anexar `novos_chats.json` para contexto completo
2. Referenciar README.md para estado atual
3. Consultar pasta `Projeto/` para detalhes técnicos
4. Usar prompts sequenciais do `Prompts_Projeto.docx`

---

---

## FAQ (Perguntas Frequentes)

### Geral

**P: Este sistema pode ser usado para trading real?**
R: Não. Este é um projeto **educacional e experimental**. Não constitui recomendação de investimento. Sempre consulte profissionais qualificados antes de investir.

**P: Preciso pagar por APIs ou dados?**
R: Não. O projeto usa apenas ferramentas gratuitas (yfinance, APIs públicas do governo). Alguns serviços têm rate limits, que respeitamos com cache.

**P: Qual a precisão dos indicadores calculados?**
R: Os indicadores são calculados com metodologias reconhecidas (Sharpe, Sortino, MPT), mas dependem da qualidade dos dados históricos. Sempre valide com múltiplas fontes.

**P: Posso usar com ações internacionais?**
R: O foco é em ativos brasileiros (B3), mas o yfinance suporta ações globais. Adaptações podem ser necessárias.

### Técnico

**P: Por que microservices em vez de monolito?**
R: Para escalabilidade, manutenibilidade e separação de responsabilidades. Cada serviço pode ser desenvolvido, testado e escalado independentemente.

**P: Quanto tempo levam as simulações Monte Carlo?**
R: Com 10.000 iterações, aproximadamente 2-5 segundos por portfolio (depende do hardware e número de ativos). Processamento é assíncrono via Celery.

**P: Como funcionam os disclaimers da CVM?**
R: O sistema sempre indica que não constitui recomendação de investimento. É puramente analítico e educacional.

**P: Posso contribuir com o projeto?**
R: Sim! Veja a seção [Contribuição](#contribuição) para entender o processo de Pull Requests e padrões de código.

**P: Como atualizar dados históricos?**
R: Execute o serviço de Scanning que atualiza dados diariamente. Também pode disparar manualmente via endpoint `/api/scan/run`.

### Deploy e Infraestrutura

**P: Onde posso fazer deploy?**
R: Qualquer cloud provider com suporte a Docker (AWS ECS, Google Cloud Run, Azure Container Instances) ou VPS tradicional.

**P: Qual o custo de infraestrutura?**
R: Zero para desenvolvimento local. Em produção, estimativa de $10-30/mês em VPS básico (2GB RAM, 1 vCPU).

**P: Como fazer backup dos dados?**
R: Use `pg_dump` para PostgreSQL e export do Redis. Recomendamos backups diários automatizados.

---

## Recursos Adicionais

### Documentação Técnica

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)
- [Celery Documentation](https://docs.celeryproject.org/)

### Finanças e Investimentos

- [Modern Portfolio Theory (Markowitz)](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
- [CVM - Comissão de Valores Mobiliários](https://www.gov.br/cvm/)
- [B3 - Brasil, Bolsa, Balcão](http://www.b3.com.br/)
- [Tesouro Direto](https://www.tesourodireto.com.br/)

### Python para Finanças

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)
- [SciPy Documentation](https://scipy.org/)
- [Statsmodels Documentation](https://www.statsmodels.org/)

### Livros Recomendados

- "A Random Walk Down Wall Street" - Burton Malkiel
- "Python for Finance" - Yves Hilpisch
- "Advances in Financial Machine Learning" - Marcos López de Prado
- "Trading and Exchanges" - Larry Harris

---

## 📦 Versão e Histórico

**Versão Atual**: `0.1.0` (Em Desenvolvimento)

Para ver todas as mudanças e versões anteriores, consulte o [CHANGELOG.md](CHANGELOG.md).

### Roadmap de Versões

- **v0.1.0** ✅ - Setup inicial e documentação (Atual)
- **v0.2.0** 🔄 - API Gateway e infraestrutura base
- **v0.3.0** 📋 - Portfolio e Analysis Services
- **v0.4.0** 📋 - Scanning e Projection Services
- **v0.5.0** 📋 - Reporting Service e Frontend
- **v1.0.0** 📋 - Primeira release estável

---

## Contato e Suporte

- **Autor**: Angelo Cesar (@accolombini / @colo6567)
- **GitHub**: [github.com/accolombini/b3_portfolio](https://github.com/accolombini/b3_portfolio)
- **Issues**: [GitHub Issues](https://github.com/accolombini/b3_portfolio/issues)

---

## Licença

**MIT License**. Veja `LICENSE` para detalhes.

---

**Última atualização**: 17 de fevereiro de 2026

---

> ⚠️ **Aviso Importante / Disclaimers (CVM):**
> Este projeto é **puramente educacional e experimental**. **Não constitui recomendação, consultoria ou aconselhamento de investimento**. Os resultados são baseados em dados históricos e simulações, que não garantem desempenho futuro. Use por sua conta e risco. Sempre inclua **disclaimers regulatórios** (ex.: CVM) em aplicações derivadas e consulte profissionais qualificados para decisões financeiras reais.

---

## Agradecimentos

Obrigado a todos os desenvolvedores e mantenedores das bibliotecas open-source que tornam este projeto possível:

- FastAPI, Uvicorn, Starlette
- React, Vite, TypeScript
- Pandas, NumPy, SciPy, Statsmodels
- PostgreSQL, Redis, Celery
- Biome (linter/formatter)
- yfinance e todas as fontes de dados públicas

**Happy Coding! 🚀📈**
