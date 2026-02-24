# B3_Portfolio — Sistema de Análise de Portfólio de Investimentos

## Objetivo
Sistema modular para análise, balanceamento e otimização de carteira de
investimentos focado em ativos brasileiros. Analisa 3 ativos existentes,
varre o mercado autonomamente e recomenda 2-3 novos ativos. Não realiza
trading — apenas análise e relatórios.

## Stack
- **Backend:** Python 3.12.5 + FastAPI — virtualenv chamado `b3`
- **Frontend:** React 18 + TypeScript + Vite + Biome (linter/formatter)
- **Banco de dados:** PostgreSQL 16 (Docker)
- **Cache/Queue:** Redis 7 (Docker) + Celery para tarefas assíncronas
- **ORM/Migrations:** SQLAlchemy 2.0 + Alembic
- **Testes:** pytest (backend) + Vitest (frontend)
- **Dados:** yfinance, requests + BeautifulSoup (scraping ético CVM/Tesouro)

## Estrutura do Projeto
```
b3_portfolio/
├── services/
│   ├── api-gateway/     # Porta 8000 — roteamento e JWT auth
│   ├── portfolio/       # Porta 8001 — CRUD ativos e balanceamento MPT
│   ├── analysis/        # Porta 8002 — cálculo de todos os indicadores
│   ├── scanning/        # Porta 8003 — varredura autônoma de mercado
│   ├── projection/      # Porta 8004 — Monte Carlo, ARIMA, fronteira eficiente
│   └── reporting/       # Porta 8005 — geração de relatórios JSON/CSV/PDF
├── frontend/            # React/TypeScript — porta 5173
├── common/              # Código compartilhado entre serviços
├── config/              # Configurações de ambiente
├── docs/                # Documentação técnica
├── Projeto/             # Documentos de projeto (não versionados)
├── docker-compose.yml   # Infraestrutura (PRÓXIMA TAREFA — ainda não criado)
├── requirements.txt     # Dependências Python produção
├── requirements-dev.txt # Dependências Python desenvolvimento
├── Makefile             # Automação de tarefas
└── CLAUDE.md            # Este arquivo
```

## Carteira Atual (3 ativos)
1. Fundos de Investimento RF LP High
2. Tesouro Direto LFT 01.03.2031-210100-LFT
3. LCA BB Prefixada

## Indicadores a Implementar
**Risco/Retorno:** β (Beta), α (Alfa >0), Sharpe, Treynor, Sortino, R², Correlação, VaR, CVaR
**Fundamentalistas:** P/E, P/B (P/VP), EV/EBITDA, ROE, ROA, Margem Líquida
**Liquidez/Endividamento:** Liquidez Corrente, Liquidez Seca, D/E
**Simulações:** Monte Carlo (10k iterações), ARIMA (projeções 2 anos), MPT/Fronteira Eficiente (Markowitz)
**Referência:** IBOVESPA (^BVSP) — histórico 5 anos + projeção 2 anos

## Ambiente
- Projeto: `/Volumes/Mac_XV/projetos/b3_portfolio`
- Virtualenv: `/Volumes/Mac_XV/virtualenvs/b3` (SSD externo)
- Ativar: `workon b3`
- NUNCA usar `source b3/bin/activate` — o env não está na raiz do projeto

## Comandos
```bash
# Ambiente
workon b3                       # Ativar virtualenv (está no SSD externo)
make install                    # Instalar todas as dependências
make docker-up                  # Subir PostgreSQL + Redis
make docker-down                # Derrubar containers

# Desenvolvimento
make backend-dev                # API Gateway porta 8000
make frontend-dev               # Frontend porta 5173
cd frontend && npm run dev      # Frontend direto

# Qualidade
make test                       # Todos os testes
make lint                       # Verificar código
make format                     # Formatar código
make ci                         # Pipeline CI local

# Docker (quando docker-compose.yml existir)
docker-compose up -d            # Sobe infra completa
docker-compose down             # Derruba tudo
```

## Regras Obrigatórias — LEIA ANTES DE ESCREVER QUALQUER CÓDIGO

### Proibições absolutas — nunca faça isso
- **NUNCA use mocks** para dados financeiros, cotações, indicadores ou qualquer lógica de negócio
- **NUNCA use hardcodes** — nenhum valor financeiro, ticker, taxa ou parâmetro fixo no código
- **NUNCA simule dados** — se um dado real não estiver disponível, sinalize e aguarde instrução
- **NUNCA tente adivinhar** valores, comportamentos ou regras de negócio não especificados — pergunte
- **NUNCA assuma** que uma integração funciona sem testá-la com dados reais
- **NUNCA pule etapas de TDD** — teste primeiro, código depois, sem exceções
- **NUNCA commite .env** — usar exclusivamente .env.example como template
- **NUNCA use ferramentas pagas** — custo zero é requisito, não preferência

### Obrigações
- **TDD obrigatório:** escreva o teste antes do código de produção — sempre, sem exceção
- **Dados reais:** usar yfinance, APIs públicas (CVM, Tesouro, Banco Central) — sem substitutos
- **Modular:** cada serviço é independente; não crie acoplamento entre serviços além do gateway
- **Pergunte antes de assumir:** diante de qualquer ambiguidade, pare e questione
- **Commits semânticos:** feat/fix/docs/refactor/test/chore
- **Branches:** main (produção) → develop → feature/*
- **Ferramentas free** apenas — custo zero

## Disciplina de Sessões de Desenvolvimento
- Cada sessão tem UM entregável verificável — nunca misturar dados + gráfico + projeção
- Dados históricos devem ser validados com sanidade econômica ANTES de qualquer visualização
- Validação de sanidade obrigatória para proxies de renda fixa:
  CDI/SELIC diário ~0.040-0.050% → retorno anual esperado 8-15%
  Se resultado fora dessa faixa: PARAR e reportar — nunca contornar
- Projeções só começam depois que dados históricos forem aprovados pelo usuário
- Sessão 02-A entrega: tabela retornos_anuais.csv validada
- Sessão 02-B entrega: gráfico comparativo + projeção

## Slash Commands Disponíveis
Prompts de sessão ficam em `.claude/commands/` e são executados digitando `/nome`:
- `/sessao-01-ibovespa` — versão inicial substituída pela 02-A
- `/sessao-02a-dados` — dados históricos + tabela retornos anuais validada (sem gráfico, sem projeção)

## Status Atual (24/02/2026) — Fase 2 em andamento

### Concluído
✅ Fase 1: documentação, arquitetura, requirements, README, estrutura de pastas
✅ Frontend configurado com Biome (zero vulnerabilidades)
✅ services/analysis/ibovespa_analysis.py — versão inicial criada
✅ Bug de double-scaling do CDI corrigido (linha 335)
✅ Testes: 6/6 passando para TestAccumulateRateToIndex

### Bug pendente — CORRIGIR ANTES DE QUALQUER OUTRA COISA
🐛 _fetch_lft_2031 passa série BCB 432 (SELIC em % ao ANO, ex: 13.75)
   para _accumulate_rate_to_index que espera % ao DIA — escala errada.
   Correção: adicionar parâmetro rate_type na função.
   Se rate_type="annual_pct": taxa_diaria = (1 + rate/100)^(1/252) - 1
   Se rate_type="daily_pct": usar rate/100 diretamente (CDI série 12)
   Arquivo: services/analysis/ibovespa_analysis.py

### Próxima tarefa após correção do bug
📋 Gerar tabela de retornos anuais validada (sem gráfico, sem projeção)
   Entregável: services/analysis/outputs/retornos_anuais.csv
   Critério de aprovação:
   - CDI/SELIC: retorno anual entre 8% e 15% para 2021-2025
   - IBOVESPA: retorno anual entre -20% e +40%

### Sequência de desenvolvimento
1. Corrigir bug série 432 — AQUI AGORA
2. Gerar tabela retornos_anuais.csv validada
3. Gráfico comparativo + projeção (só após validação da tabela)
4. docker-compose.yml + infraestrutura
5. Demais microservices e frontend

## Fontes de Dados
- **yfinance** — cotações históricas B3, IBOVESPA, fundos
- **Tesouro.gov.br** — preços e taxas títulos públicos (scraping via requests)
- **CVM Dados Abertos** — fundos de investimento (scraping via BeautifulSoup)
- **Banco Central API** — taxa SELIC, CDI, IPCA
- Respeitar robots.txt, rate limiting e usar cache Redis para evitar requisições redundantes

## Disclaimer
Sistema educacional e experimental. Não constitui recomendação de
investimento. Incluir disclaimers CVM em todos os relatórios gerados.
