# Prompt — Sessão 02-A: Dados Históricos e Retornos Anuais

Cole este prompt integralmente no Claude Code (VSCode).
Leia o CLAUDE.md antes de começar e confirme as regras.

---

## Escopo desta sessão — APENAS isto, nada mais

Reescrever do zero o arquivo `services/analysis/ibovespa_analysis.py`.
**Não gerar gráfico. Não gerar projeção. Não gerar ARIMA.**
Entregar apenas: dados históricos corretos + tabela de retornos anuais.

A projeção e o gráfico serão feitos em sessão separada,
DEPOIS que os dados históricos forem validados pelo usuário.

---

## Entregáveis obrigatórios

### 1. Dados históricos do IBOVESPA
- Ticker: `^BVSP` via yfinance
- Período: 5 anos completos (verificar que retornou ao menos 1.200 registros)
- Se retornar menos que 1.200 registros: logar aviso com período real obtido
- Coluna de retorno diário: `Daily_Return = Close.pct_change()`

### 2. Dados dos 3 ativos da carteira
Mesma cadeia de busca da sessão anterior — o que mudou é a validação:

**Ativo 1 — FI RF LP High**
- Cadeia: CVM Dados Abertos → CDI acumulado (BCB série 12)
- Se usar proxy CDI: a taxa diária da série 12 vem em % ao dia
  (ex: 0.047 significa 0,047% ao dia)
- Acumulação CORRETA: `index[t] = index[t-1] * (1 + rate[t]/100)`
  Começando com index[0] = 100.0
- VALIDAÇÃO OBRIGATÓRIA: após acumular, calcular retorno anual implícito
  médio. Se CDI diário ~0.047%, o retorno anual deve ser ~12-13%.
  Se o resultado for absurdo (>100% ao ano ou <1% ao ano),
  PARAR e reportar o erro — não prosseguir

**Ativo 2 — LFT 2031**
- Cadeia: API Tesouro → SELIC acumulada (BCB série 432)
- Mesma validação: SELIC diária ~0.040-0.050%, retorno anual ~10-13%

**Ativo 3 — LCA BB Prefixada**
- Cadeia: ANBIMA IRF-M → CDI acumulado (BCB série 12)
- Mesma validação aplicada

### 3. Cálculo de retornos anuais
Para IBOVESPA e cada ativo, calcular:
- Retorno de cada ano calendário completo disponível (2021, 2022, 2023, 2024)
- Retorno do ano corrente até a data mais recente disponível (2025/2026)
- Retorno acumulado total do período disponível
- Fórmula retorno anual: `(valor_final_ano / valor_inicial_ano - 1) * 100`

### 4. Tabela comparativa — saída obrigatória
Imprimir no terminal E salvar em:
`services/analysis/outputs/retornos_anuais.csv`

Formato da tabela:
```
Ativo           | Fonte        | Período          | 2021  | 2022  | 2023  | 2024  | 2025* | Acumulado
IBOVESPA        | yfinance     | 2021-xx → 2026-xx | x.x%  | x.x%  | x.x%  | x.x%  | x.x%  | x.x%
FI RF LP High   | CDI (proxy)  | 2021-xx → 2026-xx | x.x%  | x.x%  | x.x%  | x.x%  | x.x%  | x.x%
LFT 2031        | SELIC(proxy) | 2021-xx → 2026-xx | x.x%  | x.x%  | x.x%  | x.x%  | x.x%  | x.x%
LCA BB Pref.    | CDI (proxy)  | 2021-xx → 2026-xx | x.x%  | x.x%  | x.x%  | x.x%  | x.x%  | x.x%
* ano corrente parcial
```

### 5. Validação de sanidade — OBRIGATÓRIA antes de encerrar
Após calcular os retornos, verificar automaticamente:

- CDI/SELIC: retorno anual entre 8% e 15% para anos 2021-2025
  (faixa realista da taxa brasileira no período)
- IBOVESPA: retorno anual entre -20% e +40%
  (faixa realista considerando volatilidade histórica)
- Se QUALQUER valor estiver fora dessa faixa:
  PARAR, reportar qual valor falhou na validação e o motivo
  NÃO gerar o CSV com dados inválidos

---

## Estrutura de arquivos
```
services/analysis/
├── ibovespa_analysis.py      ← reescrever do zero
├── outputs/
│   └── retornos_anuais.csv   ← novo entregável
└── tests/
    └── test_ibovespa_analysis.py  ← atualizar testes
```

## TDD obrigatório
Escrever testes ANTES do código para:
1. `test_accumulate_rate_correct_scale`: taxa 0.047% ao dia por 252 dias
   deve resultar em índice entre 110 e 115 (não em milhões)
2. `test_annual_return_ibovespa`: retorno anual calculado deve ser float
   entre -100% e +200%
3. `test_sanity_check_cdi`: retorno anual CDI deve estar entre 8% e 15%
   para os anos disponíveis

## Restrições absolutas (CLAUDE.md)
- NÃO gerar gráfico nesta sessão
- NÃO gerar projeção ARIMA nesta sessão
- NUNCA simular dados ou hardcodar taxas
- Se a validação de sanidade falhar: reportar e parar — não contornar
- Se uma API falhar: usar próximo da cadeia e logar claramente

## Ao finalizar, reportar obrigatoriamente
1. Resultado dos testes pytest
2. A tabela de retornos anuais impressa no terminal
3. Confirmação de que a validação de sanidade passou para todos os ativos
4. Caminho do CSV gerado
5. Qualquer falha — com erro real, não contornado
