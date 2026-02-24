# Prompt — Zerar erros Pylance no projeto

Leia o CLAUDE.md antes de começar.

## Contexto

O VSCode está mostrando 259+ erros Pylance em múltiplos arquivos,
todos criados pelo Claude Code. O objetivo é zerar completamente
o painel PROBLEMS — erros e warnings.

## Abordagem — duas etapas em sequência

---

### Etapa 1 — Diagnóstico completo (faça isso ANTES de qualquer correção)

Execute no terminal:
```bash
cd /Volumes/Mac_XV/projetos/b3_portfolio
workon b3
python -m pyright --outputjson 2>/dev/null | python -m json.tool | grep '"file"' | sort | uniq -c | sort -rn
```

Se pyright não estiver instalado:
```bash
pip install pyright
python -m pyright --stats 2>&1 | tail -20
```

PARE e mostre o output completo — quantos erros por arquivo.
Aguardar minha confirmação antes de continuar.

---

### Etapa 2 — Correção sistemática

#### 2A — Criar pyrightconfig.json na raiz do projeto

O pandas, numpy e requests têm limitações conhecidas de stubs de tipo
que geram falsos positivos no Pylance. Criar o arquivo:
`/Volumes/Mac_XV/projetos/b3_portfolio/pyrightconfig.json`

Conteúdo:
```json
{
  "pythonVersion": "3.12",
  "pythonPlatform": "Darwin",
  "venvPath": "/Volumes/Mac_XV/virtualenvs",
  "venv": "b3",
  "typeCheckingMode": "standard",
  "reportUnknownMemberType": "none",
  "reportUnknownVariableType": "none",
  "reportUnknownArgumentType": "none",
  "reportMissingTypeStubs": "none",
  "reportAttributeAccessIssue": "warning",
  "reportReturnType": "error",
  "reportIndexIssue": "warning",
  "exclude": [
    "**/node_modules",
    "**/__pycache__",
    "**/migrations",
    "b3/**"
  ]
}
```

Importante: `typeCheckingMode: "standard"` (não "strict") é o correto
para projetos com pandas/numpy — o modo strict gera centenas de falsos
positivos por limitações dos stubs dessas bibliotecas.

Após criar o arquivo: reabrir o VSCode ou aguardar o Pylance recarregar
(pode levar 10-30 segundos). Verificar quantos erros restaram.
PARE e informe o número. Aguardar confirmação.

#### 2B — Corrigir erros remanescentes nos arquivos Python

Para cada arquivo que ainda tiver erros após o pyrightconfig.json:

1. Listar os erros reais (não os de pandas/numpy já suprimidos)
2. Corrigir apenas erros genuínos:
   - Tipos de retorno incorretos (`reportReturnType`)
   - Variáveis sem tipo onde o tipo é claramente inferível
   - Imports não utilizados
   - Erros de lógica de tipos reais
3. NÃO suprimir erros com `# type: ignore` — corrigir o código

Para o padrão específico `str.contains()` do pandas que ainda aparecer:
```python
# Antes (gera erro Pylance)
mask = df["col"].str.contains("termo", na=False)

# Depois (tipagem explícita)
mask: pd.Series = df["col"].str.contains("termo", na=False)  # type: pd.Series[bool]
```

Ou usar cast:
```python
from typing import cast
mask = cast(pd.Series, df["col"].str.contains("termo", na=False))
```

Após corrigir cada arquivo: rodar pyright naquele arquivo específico
para confirmar zero erros antes de passar para o próximo.

#### 2C — Verificação final

```bash
python -m pyright 2>&1 | tail -5
```

O resultado deve mostrar: `0 errors, 0 warnings`

PARE e mostre o output final. Aguardar minha confirmação.

---

## Restrições
- PARE após cada etapa e aguarde confirmação
- NÃO usar `# type: ignore` em massa — é contornar, não resolver
- NÃO alterar lógica de negócio — apenas anotações de tipo
- Se um erro não tiver solução limpa: reportar e aguardar instrução
- Fazer commit apenas após minha aprovação do resultado final
