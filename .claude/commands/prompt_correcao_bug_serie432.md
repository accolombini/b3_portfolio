# Prompt — Correção Bug Série 432 (SELIC escala % ao ano)

Leia o CLAUDE.md antes de começar. Confirme que vê o bug pendente
documentado na seção "Bug pendente".

---

## Contexto do bug

Em `services/analysis/ibovespa_analysis.py`, a função
`_accumulate_rate_to_index` recebe taxas e acumula usando:
`index[t] = index[t-1] * (1 + rate/100)`

Essa fórmula está correta para a série BCB 12 (CDI), que retorna
taxa em **% ao dia** (ex: 0.047 = 0,047% ao dia).

Porém a série BCB 432 (SELIC), usada em `_fetch_lft_2031`, retorna
taxa em **% ao ano** (ex: 13.75 = 13,75% ao ano). Passar esse valor
diretamente para `_accumulate_rate_to_index` gera acumulação absurda.

---

## Correção exigida

### Passo 1 — TDD primeiro
Escrever os testes ANTES de alterar qualquer código de produção.
Adicionar em `tests/test_ibovespa_analysis.py`:

```python
def test_accumulate_daily_rate_cdi():
    """CDI: 0.047% ao dia por 252 dias deve resultar em ~113 (≈13% ao ano)"""
    # Criar série com taxa diária constante de 0.047
    dates = pd.date_range("2024-01-01", periods=252, freq="B")
    rate_df = pd.DataFrame({"Date": dates, "Rate": 0.047})
    result = _accumulate_rate_to_index(rate_df, rate_type="daily_pct")
    final = result["Value"].iloc[-1]
    assert 110 <= final <= 116, f"CDI acumulado esperado ~113, obtido {final:.2f}"

def test_accumulate_annual_rate_selic():
    """SELIC: 13.75% ao ano por 252 dias deve resultar em ~113.75"""
    dates = pd.date_range("2024-01-01", periods=252, freq="B")
    rate_df = pd.DataFrame({"Date": dates, "Rate": 13.75})
    result = _accumulate_rate_to_index(rate_df, rate_type="annual_pct")
    final = result["Value"].iloc[-1]
    assert 110 <= final <= 117, f"SELIC acumulado esperado ~113.75, obtido {final:.2f}"

def test_accumulate_wrong_type_raises():
    """rate_type inválido deve levantar ValueError"""
    dates = pd.date_range("2024-01-01", periods=5, freq="B")
    rate_df = pd.DataFrame({"Date": dates, "Rate": 0.047})
    with pytest.raises(ValueError):
        _accumulate_rate_to_index(rate_df, rate_type="invalid")
```

Rodar pytest — confirmar que os 3 testes FALHAM antes de implementar.
PARE e mostre o output do pytest. Aguardar minha confirmação antes
de continuar.

### Passo 2 — Implementar a correção
Modificar `_accumulate_rate_to_index` para aceitar `rate_type`:

```python
def _accumulate_rate_to_index(
    rate_df: pd.DataFrame,
    start_value: float = 100.0,
    rate_type: str = "daily_pct",  # "daily_pct" ou "annual_pct"
) -> pd.DataFrame:
```

Lógica interna:
- Se `rate_type == "daily_pct"`: usar `rate/100` diretamente (CDI série 12)
- Se `rate_type == "annual_pct"`: converter para diário primeiro:
  `taxa_diaria = (1 + rate/100) ** (1/252) - 1`
  Depois acumular: `index[t] = index[t-1] * (1 + taxa_diaria)`
- Se `rate_type` for outro valor: levantar `ValueError` com mensagem clara

### Passo 3 — Atualizar chamadas
- `_fetch_lft_2031`: passar `rate_type="annual_pct"` na chamada
- `_fetch_rf_lp_high` e `_fetch_lca_bb_prefixada`: passar
  `rate_type="daily_pct"` explicitamente (já funciona, mas deixar
  explícito para clareza)

### Passo 4 — Rodar testes novamente
Rodar pytest completo. PARE e mostrar output completo.
Aguardar minha confirmação antes de continuar.

### Passo 5 — Validação de sanidade com dados reais
Após testes passando, executar o módulo e imprimir APENAS isto:

```
=== VALIDAÇÃO DE ESCALA ===
CDI (série 12) — primeiros 3 valores de Rate: [x, x, x]
CDI acumulado — último valor do índice: x.xx
CDI retorno anual implícito médio: x.x%

SELIC (série 432) — primeiros 3 valores de Rate: [x, x, x]
SELIC acumulado — último valor do índice: x.xx
SELIC retorno anual implícito médio: x.x%
===========================
```

PARE após imprimir esses valores. NÃO gerar gráfico. NÃO continuar.
Aguardar minha aprovação dos números antes de qualquer outra ação.

---

## Restrições absolutas
- TDD: testes antes do código — sem exceção
- PARE após cada passo e aguarde confirmação
- Se os retornos anuais ficarem fora de 8-15%: reportar e parar
- Não alterar nada além de _accumulate_rate_to_index e suas chamadas
