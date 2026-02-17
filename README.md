# B3_Portfolio

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

## Recursos principais

### Microservices independentes

- **API Gateway**: Roteamento e autenticação.
- **Portfolio Service**: Gerenciamento de ativos e balanceamento.
- **Analysis Service**: Cálculos de risco/retorno e indicadores fundamentalistas.
- **Scanning Service**: Varredura e sugestão de novos ativos.
- **Projection Service**: Simulações Monte Carlo, ARIMA e MPT.
- **Reporting Service**: Geração de relatórios (JSON/CSV/PDF).

### Frontend

- Interface reativa em **React/TypeScript** com **Vite**
- Dashboards e gráficos (ex.: **Chart.js**)

### Integrações e dados

- Dados de mercado: **yfinance** (IBOVESPA, tickers).
- Coletas específicas: **requests/BeautifulSoup** (ex.: Tesouro.gov.br, CVM).

### Tecnologias

- **Python 3.12.5** + **FastAPI**
- **Node.js** (LTS)
- **PostgreSQL** e **Redis** via **Docker**
- **Celery** para tarefas assíncronas
- **TDD** com **pytest**

### Restrições

- Somente ferramentas **free** (open-source / gratuitas).
- **Sem mocks/hardcodes** para lógica crítica de negócio.
- **Foco em precisão** e **TDD**.

---

## Requisitos

- Python **3.12.5**
- Node.js **LTS**
- Docker e Docker Compose
- Git

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

### 5) Dependências do frontend (se aplicável)

```bash
cd frontend
npm install
```

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

---

## Exemplos de endpoints (via Gateway)

- `GET /api/portfolios` — Lista portfólio.
- `POST /api/analyze/metrics` — Cálculos de indicadores.
- `GET /api/scan/suggestions` — Sugestões de ativos.
- `POST /api/project/simulate` — Projeções Monte Carlo.

---

## Testes

Rode `pytest` em cada serviço:

```bash
pytest
```

> Sugestão: padronize `Makefile` por serviço com alvos como `test`, `lint`, `format`, `run`, etc.

---

## Contribuição

- Use branches para features:
  ```bash
  git checkout -b feature/novo-servico
  ```
- Siga **TDD**: escreva testes antes do código.
- Commits semânticos:
  - `feat: adiciona endpoint X`
  - `fix: corrige cálculo do indicador Y`
  - `docs: atualiza README`
- Pull requests com descrição clara e testes passando.

---

## Licença

**MIT License**. Veja `LICENSE` para detalhes.

---

## Documentação adicional

Consulte a pasta `Projeto/` (**não versionada no Git**) para documentos como:

- `Draft_Projeto.docx`
- `Visao_Geral_Projeto.docx`
- Diagramas de arquitetura

---

## Arquitetura (visão rápida)

```text
[Frontend React/Vite]
        |
        v
   [API Gateway]
        |
        +--> [Portfolio Service] ----> [PostgreSQL]
        |
        +--> [Analysis Service]  ----> [PostgreSQL]
        |
        +--> [Scanning Service]  ----> [PostgreSQL]
        |
        +--> [Projection Service] ---> [Redis] ---> [Celery Workers]
        |
        +--> [Reporting Service] ---> (JSON/CSV/PDF)
```

### Visão geral da arquitetura inicialmente sugerida

![Diagrama de arquitetura do B3_Portfolio](Figuras/arquitetura.png)

> ⚠️ **Aviso Importante / Disclaimers (CVM):**
> Este projeto é **puramente educacional e experimental**. **Não constitui recomendação, consultoria ou aconselhamento de investimento**. Os resultados são baseados em dados históricos e simulações, que não garantem desempenho futuro. Use por sua conta e risco. Sempre inclua **disclaimers regulatórios** (ex.: CVM) em aplicações derivadas e consulte profissionais qualificados para decisões financeiras reais.
