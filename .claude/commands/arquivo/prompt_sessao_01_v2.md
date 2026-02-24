# Prompt — Sessão 01: IBOVESPA + Comparação com Carteira Atual (v2)

Cole este prompt integralmente no Claude Code (VSCode).

---

Leia o CLAUDE.md na raiz do projeto antes de qualquer coisa e confirme
que entendeu as regras obrigatórias.

## Tarefa

Criar um módulo exploratório dentro de `services/analysis/` chamado
`ibovespa_analysis.py` com seus respectivos testes em
`services/analysis/tests/test_ibovespa_analysis.py`.

Siga TDD: escreva os testes primeiro, rode para confirmar que falham,
depois implemente o código para fazê-los passar.

---

## O que este módulo deve fazer

### 1. Buscar histórico do IBOVESPA
- Ticker: `^BVSP`
- Período desejado: últimos 5 anos a partir da data de hoje
- Fonte: yfinance
- Retornar DataFrame com colunas: Date, Close, Daily_Return
- Se o período real retornado for menor que 5 anos, registrar no log
  qual período foi obtido — não é erro, apenas informação

### 2. Projeção do IBOVESPA para 2 anos
- Usar ARIMA via statsmodels
- Input: série histórica de retornos diários obtida no passo anterior
- Output: DataFrame com colunas: Date, Projected_Close, CI_Lower_95, CI_Upper_95
- Tentar auto_arima (pmdarima) para seleção de parâmetros; se pmdarima
  não estiver instalado, usar (1,1,1) documentando a escolha no log
- Se pmdarima não estiver no requirements.txt, adicioná-lo antes de usar

### 3. Buscar dados dos 3 ativos da carteira

**Regra geral para todos os ativos:**
- Tentar buscar o máximo de histórico disponível — não fixar em 5 anos
- Se o histórico for menor que 5 anos, usar o que existe e registrar
  no log: qual período foi obtido e por quê é menor
- NUNCA simular dados faltantes, NUNCA hardcodar valores
- Se uma fonte falhar, tentar a próxima fonte da cadeia definida abaixo
- Registrar em log qual fonte foi usada para cada ativo

---

#### Ativo 1 — Fundos de Investimento RF LP High

**Atenção:** fundos brasileiros NÃO têm ticker no yfinance. A fonte
correta é a CVM Dados Abertos.

Cadeia de busca (tentar nesta ordem):
1. **CVM Dados Abertos** — buscar pelo nome do fundo na API:
   `https://dados.cvm.gov.br/api/fundo/doc/`
   Endpoint de cotas diárias:
   `https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/`
   - Buscar o CNPJ pelo nome "RF LP HIGH" ou similar
   - Baixar o arquivo CSV de cotas do período disponível
   - Coluna relevante: `VL_QUOTA` (valor da cota diária)
2. Se a CVM não retornar resultado identificável: registrar no log
   *"Fundo RF LP High não localizado na CVM por nome — necessário
   fornecer CNPJ manualmente"* e usar como proxy o **CDI acumulado**
   (série 12 do Banco Central:
   `https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json`)

---

#### Ativo 2 — Tesouro Direto LFT 01.03.2031-210100

**Atenção:** títulos do Tesouro Direto também não têm ticker no yfinance.

Cadeia de busca (tentar nesta ordem):
1. **Tesouro Direto API** — preços e taxas históricos:
   `https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/component/publicarea/PortfolioTesouroDiretoComponent/bd/bdTd.json`
   Ou via endpoint direto:
   `https://api.tesouro.gov.br/api/v1/titulos/precos-e-taxas-do-tesouro`
   - Buscar pelo nome: "Tesouro SELIC" ou "LFT"
   - Coluna relevante: preço unitário diário
2. Se o endpoint falhar: usar como proxy a **taxa SELIC acumulada**
   (série 432 do Banco Central:
   `https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json`)
   - Registrar no log que proxy foi usado

---

#### Ativo 3 — LCA BB Prefixada

**Atenção:** LCAs do Banco do Brasil não têm ticker público em nenhuma
fonte de dados de mercado.

Cadeia de busca (tentar nesta ordem):
1. **yfinance** — tentar ticker `BBAS3.SA` como referência do emissor
   (Banco do Brasil), apenas para ter uma referência do emissor
2. Como a LCA em si não tem dados públicos de cota: usar como proxy o
   **IRF-M** (índice de renda fixa prefixada)
   - Ticker yfinance: não disponível diretamente
   - Usar CDI como proxy com spread fixo NÃO — isso seria hardcode
   - Usar série do Banco Central: ANBIMA divulga IRF-M, verificar se
     há endpoint disponível em `https://api.anbima.com.br/`
   - Se ANBIMA não estiver acessível: usar CDI (série 12, Banco Central)
     como fallback documentando claramente no log
3. Registrar no log qual proxy foi usado e a limitação: *"LCA BB
   Prefixada não possui dados públicos de cota — proxy utilizado: [X]"*

---

### 4. Normalização para comparação
- Identificar a **data mais antiga comum** entre todas as séries que
  retornaram dados válidos
- Normalizar todas as séries para **base 100** nessa data
- Fórmula: `valor_normalizado = (valor / valor_na_data_base) * 100`
- Séries com histórico mais curto entram na comparação a partir da
  sua própria data inicial, não da data comum — exibir isso no gráfico
- Registrar no log: data base usada para cada série

### 5. Gráfico comparativo
- Gerar gráfico com matplotlib — 2 subplots:
  - **Subplot 1:** histórico disponível — IBOVESPA + 3 ativos/proxies
    normalizados (base 100). Legenda deve indicar quando um proxy foi
    usado: ex. "LFT (proxy: SELIC)"
  - **Subplot 2:** projeção IBOVESPA 2 anos com intervalo de confiança 95%
- Salvar em: `services/analysis/outputs/ibovespa_comparison.png`
- Criar o diretório `outputs/` se não existir

---

## Restrições absolutas (do CLAUDE.md)
- NUNCA simule dados — se não encontrar, logue e use o próximo da cadeia
- NUNCA hardcode valores de taxas, cotações, datas ou spreads
- NUNCA assuma que uma API está disponível sem testar a chamada real
- NUNCA tente adivinhar o CNPJ de um fundo — se não encontrar, sinalize
- Se qualquer etapa da cadeia de busca falhar completamente, o código
  deve encerrar aquela busca com log claro do motivo — não contornar
- TDD obrigatório: teste primeiro, código depois

---

## Estrutura esperada de arquivos
```
services/analysis/
├── ibovespa_analysis.py           ← módulo principal
├── outputs/                       ← criado automaticamente
│   └── ibovespa_comparison.png
└── tests/
    └── test_ibovespa_analysis.py
```

## Dependências disponíveis (requirements.txt)
yfinance, pandas, numpy, statsmodels, matplotlib, requests,
beautifulsoup4, structlog

Se pmdarima for necessário e não estiver no requirements.txt,
adicioná-lo antes de usar.

---

## Ao finalizar, reportar obrigatoriamente:
1. Resultado dos testes (pytest) — passou/falhou e por quê
2. Para cada um dos 4 ativos (IBOVESPA + 3 da carteira):
   - Fonte usada (real ou proxy)
   - Período obtido (data inicial → data final)
   - Quantidade de registros
3. Data base usada para normalização
4. Caminho do gráfico gerado
5. Qualquer falha de acesso a APIs — com o erro real, não contornado
