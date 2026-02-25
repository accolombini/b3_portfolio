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

## Visão do Sistema — Pergunta Central
"Meu portfólio está performando bem em relação ao mercado,
e o que posso adicionar para melhorar?"

### Módulo 1 — Análise Histórica
Gráfico normalizado base 100 — todos no mesmo plano:
- IBOVESPA (referência), 3 ativos atuais, índices adicionais
  (SELIC, dólar, ouro — avaliar quais agregam clareza)
- Período: 5 anos histórico real

### Módulo 2 — Projeção 2 Anos
- Modelos: ARIMA + Prophet + regressão polinomial com votação
- Precisão calculada via backtest — exibida explicitamente
- Gráfico: três linhas limpas Pessimista/Base/Otimista com probabilidade
- ZERO nuvens de dispersão

### Módulo 3 — Varredura Autônoma B3 (Scanning Service)
- Varre todos os ativos da B3 de forma autônoma
- Aplica: Alfa, Beta, Sharpe, Treynor, Sortino, R², VaR, CVaR,
  P/E, P/B, EV/EBITDA, ROE, ROA, Margem Líquida, D/E, Liquidez
- Identifica autonomamente os 3 melhores candidatos
- Critério: maximizar desempenho do portfólio vs IBOVESPA

### Módulo 4 — Otimização MPT/Markowitz (Portfolio Service)
- Input: 3 ativos atuais + 3 novos = 6 ativos
- Calcula alocação percentual ótima via fronteira eficiente
- Objetivo: Sharpe máximo
- Output: "X% ativo A, Y% ativo B, Z% ativo C..."

## Makefile — Execução Modular (OBRIGATÓRIO)
Cada módulo deve ter um target no Makefile. O usuário executa, analisa
o output no terminal e decide se continua. Targets obrigatórios:
  make analise-ibovespa    — busca histórico IBOVESPA e imprime resumo
  make analise-retornos    — gera retornos_anuais.csv e imprime tabela
  make analise-projecao    — roda projeção e imprime cenários
  make pipeline-completa   — executa toda a sequência em ordem
  make analise-status      — mostra o que já foi gerado
Cada target: ativar workon b3, executar módulo, imprimir resultado,
retornar exit code 0 se OK ou 1 se falhou.
NUNCA encadear próxima etapa automaticamente — usuário decide quando avançar.

## Metodologia de Projeção (DEFINITIVA)
Abordagem: múltiplos modelos com votação
- Modelos: ARIMA + Prophet + regressão polinomial
- Cenário BASE: mediana ponderada onde os três convergem
- Cenário OTIMISTA: limite superior do modelo mais otimista
- Cenário PESSIMISTA: limite inferior do modelo mais conservador
- Probabilidade de cada cenário: calculada — NÃO arbitrária, NÃO hardcoded
Gráfico — formato OBRIGATÓRIO:
- ZERO nuvens de dispersão
- Três linhas nomeadas: Pessimista / Base / Otimista
- Probabilidade explícita em cada label: "Base (58%)"
- Conecta ao último ponto histórico real

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
✅ services/analysis/ibovespa_analysis.py — criado e corrigido
✅ Bug double-scaling CDI corrigido (linha 335)
✅ Bug série 432 corrigido — SELIC % ao ano convertida para diária
✅ Pylance zerado — 0 errors, 0 warnings, 0 informations
✅ Testes: 9/9 passando (TDD aplicado)
✅ 36 arquivos commitados e pushados para repositório remoto
✅ Validação de sanidade: CDI 11.4% a.a., SELIC 11.5% a.a. ✅

### Próxima tarefa — AQUI AGORA
📋 Sessão 02-A: tabela de retornos anuais validada
   Comando: /sessao-02a-dados
   Entregável: services/analysis/outputs/retornos_anuais.csv
   Critério: CDI/SELIC entre 8-15% a.a., IBOVESPA entre -20% e +40%
   SEM gráfico, SEM projeção nesta sessão

### Sequência de desenvolvimento
1. ✅ Corrigir bugs série 432 e double-scaling
2. ✅ Zerar Pylance
3. Sessão 02-A: tabela retornos_anuais.csv validada ← AQUI AGORA
4. Sessão 02-B: gráfico comparativo + projeção ARIMA
5. docker-compose.yml + infraestrutura
6. Demais microservices e frontend

## Fontes de Dados
- **yfinance** — cotações históricas B3, IBOVESPA, fundos
- **Tesouro.gov.br** — preços e taxas títulos públicos (scraping via requests)
- **CVM Dados Abertos** — fundos de investimento (scraping via BeautifulSoup)
- **Banco Central API** — taxa SELIC, CDI, IPCA
- Respeitar robots.txt, rate limiting e usar cache Redis para evitar requisições redundantes

## Disclaimer
Sistema educacional e experimental. Não constitui recomendação de
investimento. Incluir disclaimers CVM em todos os relatórios gerados.
