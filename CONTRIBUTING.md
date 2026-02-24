# Guia de Contribuição - B3_Portfolio

Obrigado por considerar contribuir com o B3_Portfolio! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Processo de Development](#processo-de-development)
- [Padrões de Código](#padrões-de-código)
- [Commits Semânticos](#commits-semânticos)
- [Pull Requests](#pull-requests)
- [Testes](#testes)
- [Documentação](#documentação)

## 📜 Código de Conduta

Este projeto segue o [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Ao participar, espera-se que você mantenha esse código.

### Comportamento Esperado

- ✅ Seja respeitoso e inclusivo
- ✅ Aceite críticas construtivas graciosamente
- ✅ Foque no que é melhor para a comunidade
- ✅ Mostre empatia com outros membros da comunidade

### Comportamento Inaceitável

- ❌ Uso de linguagem ou imagens sexualizadas
- ❌ Comentários insultuosos ou depreciativos (trolling)
- ❌ Assédio público ou privado
- ❌ Publicar informações privadas de outros sem permissão

## 🤝 Como Contribuir

### Reportando Bugs

Antes de criar um issue:

1. Verifique se o bug já foi reportado
2. Use a versão mais recente do código
3. Tente isolar o problema

Ao reportar, inclua:

- **Descrição clara** do problema
- **Passos para reproduzir** o bug
- **Comportamento esperado** vs **comportamento atual**
- **Screenshots** se aplicável
- **Versões** (Python, Node.js, OS)
- **Logs de erro** completos

### Sugerindo Melhorias

Para sugerir novas features:

1. Abra um issue com o label `enhancement`
2. Descreva claramente a funcionalidade desejada
3. Explique **por que** essa feature seria útil
4. Forneça exemplos de uso
5. Considere alternativas e trade-offs

### Primeira Contribuição?

Issues marcados com `good first issue` são ideais para iniciantes:

- Pequenos em escopo
- Bem documentados
- Bom para aprender o código base

## 🛠️ Processo de Development

### 1. Fork e Clone

```bash
# Fork o repositório via GitHub

# Clone seu fork
git clone https://github.com/SEU-USUARIO/b3_portfolio.git
cd b3_portfolio

# Adicione o upstream
git remote add upstream https://github.com/accolombini/b3_portfolio.git
```

### 2. Configure o Ambiente

```bash
# Python
python -m venv b3
source b3/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependências de desenvolvimento

# Frontend
cd frontend
npm install

# Docker
docker-compose up -d
```

### 3. Crie uma Branch

```bash
# Sempre crie a partir de develop
git checkout develop
git pull upstream develop
git checkout -b feature/minha-nova-feature
```

### 4. Desenvolva com TDD

```python
# 1. Escreva o teste primeiro
def test_calculate_sharpe():
    result = calculate_sharpe(returns=[0.1, 0.2, 0.15])
    assert result > 0

# 2. Execute (deve falhar)
pytest tests/test_analysis.py::test_calculate_sharpe

# 3. Implemente
def calculate_sharpe(returns: list[float], risk_free_rate: float = 0.0) -> float:
    # Implementação
    pass

# 4. Refatore
# Melhore o código mantendo testes verdes
```

### 5. Commit

```bash
git add .
git commit -m "feat(analysis): add Sharpe ratio calculation"
```

### 6. Push e PR

```bash
git push origin feature/minha-nova-feature
# Crie Pull Request via GitHub
```

## 📝 Padrões de Código

### Python

```python
# Use type hints
from typing import Optional, List

def process_portfolio(
    assets: List[dict],
    risk_tolerance: float = 0.5
) -> Optional[Portfolio]:
    """
    Process portfolio assets and return optimized allocation.

    Args:
        assets: List of asset dictionaries with ticker, quantity, price
        risk_tolerance: Risk tolerance level (0.0 to 1.0)

    Returns:
        Optimized Portfolio object or None if optimization fails

    Raises:
        ValueError: If risk_tolerance is out of range
    """
    if not 0 <= risk_tolerance <= 1:
        raise ValueError("Risk tolerance must be between 0 and 1")

    # Implementation
    pass

# Use Pydantic para validação
from pydantic import BaseModel, Field, validator

class AssetCreate(BaseModel):
    ticker: str = Field(..., min_length=4, max_length=10)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

    @validator('ticker')
    def ticker_must_be_uppercase(cls, v):
        return v.upper()

# Use logging estruturado
import structlog

logger = structlog.get_logger(__name__)

def risky_operation():
    try:
        result = perform_calculation()
        logger.info("calculation_success", result=result)
    except Exception as e:
        logger.error("calculation_failed", error=str(e))
        raise
```

### TypeScript

```typescript
// Use interfaces e tipos
interface Portfolio {
  id: string;
  name: string;
  assets: Asset[];
  createdAt: Date;
  updatedAt: Date;
}

type PortfolioStatus = "active" | "archived" | "deleted";

// Use async/await
async function fetchPortfolio(id: string): Promise<Portfolio> {
  try {
    const response = await api.get<Portfolio>(`/portfolios/${id}`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch portfolio:", error);
    throw new Error("Portfolio not found");
  }
}

// Use React Hooks
import { useState, useEffect, useCallback } from "react";

function usePortfolio(id: string) {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const loadPortfolio = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchPortfolio(id);
      setPortfolio(data);
      setError(null);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadPortfolio();
  }, [loadPortfolio]);

  return { portfolio, loading, error, reload: loadPortfolio };
}
```

### Formatação

**Backend (Python):**

```bash
# Antes de commitar
black .
isort .
ruff check .
mypy .
```

**Frontend (TypeScript):**

```bash
# Antes de commitar
npm run lint:fix
npm run format
```

## 📤 Commits Semânticos

Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/):

### Formato

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

### Tipos

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `test`: Adiciona ou modifica testes
- `chore`: Tarefas de build, dependências, etc.
- `perf`: Melhoria de performance
- `ci`: Mudanças em CI/CD

### Exemplos

```bash
# Feature
git commit -m "feat(analysis): add Sortino ratio calculation"

# Bug fix
git commit -m "fix(portfolio): correct allocation percentage rounding"

# Breaking change
git commit -m "feat(api)!: change portfolio endpoint response format

BREAKING CHANGE: Portfolio response now includes risk_metrics field"

# Múltiplas linhas
git commit -m "refactor(scanner): improve asset filtering logic

- Optimize database queries
- Add caching layer
- Update tests

Closes #123"
```

## 🔀 Pull Requests

### Checklist

Antes de submeter:

- [ ] ✅ Código segue os padrões do projeto
- [ ] ✅ Testes unitários adicionados/atualizados
- [ ] ✅ Todos os testes passando (`pytest` / `npm test`)
- [ ] ✅ Cobertura de código mantida (>80%)
- [ ] ✅ Linting sem erros (`ruff` / `biome check`)
- [ ] ✅ Documentação atualizada
- [ ] ✅ Commits seguem padrão semântico
- [ ] ✅ Branch atualizada com develop
- [ ] ✅ Sem conflitos de merge
- [ ] ✅ PR description clara e completa

### Template PR

```markdown
## Descrição

[Descreva brevemente as mudanças]

## Tipo de Mudança

- [ ] 🐛 Bug fix
- [ ] ✨ Nova feature
- [ ] 💥 Breaking change
- [ ] 📝 Documentação
- [ ] ♻️ Refatoração
- [ ] ✅ Testes

## Motivação e Contexto

[Por que essa mudança é necessária? Qual problema resolve?]

Closes #[issue-number]

## Como Foi Testado?

[Descreva os testes realizados]

- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Teste manual

## Screenshots (se aplicável)

[Adicione screenshots]

## Checklist

- [ ] Código revisado
- [ ] Testes adicionados
- [ ] Documentação atualizada
- [ ] Commits semânticos
```

## 🧪 Testes

### Backend

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_analysis.py
pytest tests/test_analysis.py::test_sharpe_ratio

# Com output
pytest -v -s
```

### Frontend

```bash
# Executar testes
npm test

# Com cobertura
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Cobertura Mínima

- **Backend**: 80%
- **Frontend**: 70%

## 📚 Documentação

### Docstrings (Python)

```python
def calculate_efficient_frontier(
    returns: pd.DataFrame,
    num_portfolios: int = 10000,
    risk_free_rate: float = 0.0
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the efficient frontier using Monte Carlo simulation.

    This function generates random portfolio allocations and calculates
    their expected returns and volatilities to construct the efficient
    frontier based on Modern Portfolio Theory (Markowitz).

    Args:
        returns: DataFrame with historical returns for each asset
        num_portfolios: Number of random portfolios to simulate
        risk_free_rate: Risk-free rate for Sharpe ratio calculation

    Returns:
        Tuple containing:
            - portfolio_returns: Array of portfolio returns
            - portfolio_volatilities: Array of portfolio volatilities
            - portfolio_weights: Array of portfolio weights

    Raises:
        ValueError: If returns DataFrame is empty or has NaN values
        TypeError: If num_portfolios is not an integer

    Examples:
        >>> returns = pd.DataFrame({
        ...     'PETR4': [0.01, 0.02, -0.01],
        ...     'VALE3': [0.015, 0.01, 0.02]
        ... })
        >>> rets, vols, weights = calculate_efficient_frontier(returns)
        >>> print(f"Max Sharpe: {rets[np.argmax(rets/vols)]}")

    See Also:
        calculate_sharpe_ratio: Calculate Sharpe ratio for a portfolio
        optimize_portfolio: Find optimal portfolio allocation

    References:
        - Markowitz, H. (1952). Portfolio Selection. Journal of Finance.
        - Sharpe, W. (1964). Capital Asset Prices: A Theory of Market
          Equilibrium under Conditions of Risk.
    """
    pass
```

### JSDoc (TypeScript)

````typescript
/**
 * Fetch portfolio data from API
 *
 * @param portfolioId - Unique identifier for the portfolio
 * @param includeMetrics - Whether to include risk/return metrics
 * @returns Promise resolving to Portfolio object
 * @throws {PortfolioNotFoundError} If portfolio doesn't exist
 * @throws {NetworkError} If API request fails
 *
 * @example
 * ```typescript
 * const portfolio = await fetchPortfolio('abc123', true);
 * console.log(portfolio.assets.length);
 * ```
 */
async function fetchPortfolio(
  portfolioId: string,
  includeMetrics: boolean = false,
): Promise<Portfolio> {
  // Implementation
}
````

## 🎯 Áreas que Precisam de Ajuda

Estamos especialmente procurando contribuições em:

1. **Integrações de Dados**
   - Novos provedores de dados
   - Melhoria de scraping ético
   - Validação de dados

2. **Algoritmos Financeiros**
   - Novos indicadores
   - Otimizações de performance
   - Modelos de Machine Learning

3. **Frontend**
   - Componentes de visualização
   - UX/UI improvements
   - Acessibilidade

4. **Testes**
   - Aumentar cobertura
   - Testes de integração
   - Testes E2E

5. **Documentação**
   - Tutoriais
   - Exemplos de uso
   - Tradução

## 📞 Contato

- **Issues**: [GitHub Issues](https://github.com/accolombini/b3_portfolio/issues)
- **Discussions**: [GitHub Discussions](https://github.com/accolombini/b3_portfolio/discussions)
- **Email**: [Seu email]

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma [MIT License](LICENSE) do projeto.

---

**Obrigado por contribuir! 🙏**
