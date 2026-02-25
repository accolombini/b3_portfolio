# Prompt — Sessão 02-A: Tabela de Retornos Anuais (v2)

Cole este prompt integralmente no Claude Code (VSCode).
Leia o CLAUDE.md antes de começar e confirme as regras.

---

## Escopo desta sessão — APENAS isto, nada mais

Adicionar ao arquivo EXISTENTE `services/analysis/ibovespa_analysis.py`
o módulo de cálculo de retornos anuais.

NÃO reescrever o arquivo do zero — ele já tem correções importantes:
- Bug double-scaling CDI corrigido
- Bug série 432 (SELIC % ao ano) corrigido com parâmetro rate_type
- 9 testes passando
Preservar tudo isso. Apenas ADICIONAR novas funções.

NÃO gerar gráfico. NÃO gerar projeção. NÃO gerar ARIMA.
Entregar apenas: tabela de retornos anuais validada.

---

## Entregáveis obrigatórios

### 1. Adicionar target no Makefile
Antes de qualquer código Python, adicionar em
`/Volumes/Mac_XV/projetos/b3_portfolio/Makefile`:

```makefile
analise-retornos: ## Gera tabela de retornos anuais e imprime no terminal
	workon b3 && python -m services.analysis.ibovespa_analysis retornos
```

PARE e confirme que o Makefile foi atualizado. Aguardar confirmação.

### 2. Função de retornos anuais
Adicionar função `calculate_annual_returns` em ibovespa_analysis.py:

- Input: DataFrame com colunas Date e Value (ou Close)
- Output: dict com chaves 2021, 2022, 2023, 2024, 2025 (parcial),
  acumulado
- Fórmula: `(valor_ultimo_dia_ano / valor_primeiro_dia_ano - 1) * 100`
- Se o ano não tiver dados completos: calcular com o disponível e
  marcar como parcial no output
- Se o ano não tiver dados: retornar None para aquela chave —
  NUNCA simular ou interpolar

### 3. Função de tabela comparativa
Adicionar função `generate_returns_table` que:
- Chama fetch_ibovespa_history() para IBOVESPA
- Chama fetch_portfolio_assets() para os 3 ativos
- Chama calculate_annual_returns() para cada série
- Retorna DataFrame com a tabela comparativa
- Salva em: services/analysis/outputs/retornos_anuais.csv
- Imprime no terminal formatado

### 4. Validação de sanidade com faixas corretas por ano
Atenção: a SELIC variou muito no período — validar por faixa correta:

| Ano  | SELIC/CDI esperado | IBOVESPA esperado |
|------|-------------------|-------------------|
| 2021 | 2% a 10%          | -20% a +40%       |
| 2022 | 10% a 14%         | -20% a +40%       |
| 2023 | 12% a 14%         | -20% a +40%       |
| 2024 | 10% a 13%         | -20% a +40%       |
| 2025 | 12% a 15%         | -20% a +40%       |

Se QUALQUER valor estiver fora da faixa do seu ano:
PARAR, reportar e aguardar instrução — NÃO gerar CSV com dados inválidos.

### 5. Ponto de entrada CLI
Adicionar no bloco `if __name__ == "__main__"` um handler para
argumento "retornos":
```python
if len(sys.argv) > 1 and sys.argv[1] == "retornos":
    table = generate_returns_table()
    print(table.to_string())
```

---

## TDD obrigatório
Escrever testes ANTES do código para:

1. `test_calculate_annual_returns_completo`: dado um DataFrame com
   dados de 2021 a 2024, retornar dict com 4 retornos anuais float
2. `test_calculate_annual_returns_parcial`: dado DataFrame com dados
   só até junho de um ano, marcar aquele ano como parcial
3. `test_calculate_annual_returns_ano_ausente`: se não houver dados
   de um ano, retornar None — não simular
4. `test_sanity_check_2021_selic_baixa`: retorno CDI de 2021 deve
   estar entre 2% e 10% (SELIC estava em 2% em jan/2021)
5. `test_sanity_check_2022_selic_alta`: retorno CDI de 2022 deve
   estar entre 10% e 14%

Rodar pytest — confirmar que os 5 novos testes FALHAM.
PARE e mostre output do pytest. Aguardar confirmação antes de implementar.

---

## Sequência de execução com paradas obrigatórias

1. Atualizar Makefile → PARE, mostrar diff, aguardar confirmação
2. Escrever testes → rodar pytest → PARE, mostrar falhas, aguardar
3. Implementar calculate_annual_returns → rodar pytest → PARE, mostrar
4. Implementar generate_returns_table → rodar pytest → PARE, mostrar
5. Rodar `make analise-retornos` → PARE, mostrar tabela completa
6. Validação de sanidade → PARE, mostrar resultado, aguardar aprovação
7. SÓ após aprovação: salvar CSV e reportar conclusão

---

## Restrições absolutas (CLAUDE.md)
- NÃO reescrever ibovespa_analysis.py do zero
- NÃO gerar gráfico nesta sessão
- NÃO gerar projeção nesta sessão
- NUNCA simular dados, interpolar ou hardcodar taxas
- NUNCA encadear etapas sem confirmação entre elas
- Se validação de sanidade falhar: parar e reportar — não contornar

## Ao finalizar, reportar obrigatoriamente
1. Todos os testes passando (número total, não só os novos)
2. Tabela de retornos impressa no terminal via `make analise-retornos`
3. Confirmação que validação de sanidade passou com faixas por ano
4. Caminho do CSV gerado
5. Qualquer falha com erro real — não contornado
