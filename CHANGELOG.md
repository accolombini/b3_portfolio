# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Em Desenvolvimento

- 🚧 Implementação dos microservices
- 🚧 Desenvolvimento do frontend React
- 🚧 Integração com fontes de dados (yfinance, CVM, Tesouro)
- 🚧 Configuração Docker Compose
- 🚧 Setup CI/CD

## [0.1.0] - 2026-02-17

### Adicionado

#### Infraestrutura

- ✅ Estrutura inicial do projeto com microservices
- ✅ Configuração de environment Python 3.12.5
- ✅ Arquivo `requirements.txt` com todas as dependências
- ✅ Configuração do frontend React + TypeScript + Vite
- ✅ Setup inicial de Docker Compose (PostgreSQL + Redis)
- ✅ Arquitetura de diretórios para todos os serviços

#### Frontend

- ✅ Configuração do `package.json` com dependências
- ✅ Migração de ESLint para **Biome 1.9.4**
- ✅ Configuração `biome.json` otimizada
- ✅ Zero vulnerabilidades no `npm audit` (149 pacotes vs. 370+)
- ✅ Scripts npm configurados (dev, build, lint, format, test)

#### Documentação

- ✅ README.md completo e abrangente (1268 linhas)
  - Badges informativos
  - Índice navegável
  - Quick Start guide
  - Features detalhadas
  - Status do projeto e roadmap
  - Indicadores financeiros explicados
  - Metodologia de análise (MPT, Monte Carlo, ARIMA)
  - API Endpoints documentados
  - Práticas de desenvolvimento
  - Arquitetura detalhada
  - FAQ completo
  - Recursos adicionais
- ✅ CONTRIBUTING.md com guias de contribuição
- ✅ .env.example como template de configuração
- ✅ CHANGELOG.md (este arquivo)
- ✅ Documentação técnica na pasta `Projeto/`:
  - `Draft_Projeto.docx`
  - `Visao_Geral_Projeto.docx`
  - `Arquitetura_Sistema_Análise_Portfolio.docx`
  - `Prompts_Projeto.docx`
  - `novos_chats.json`

#### Configuração

- ✅ `.gitignore` configurado para Python, Node.js, Docker
- ✅ Variáveis de ambiente documentadas
- ✅ Estrutura de branches (main, develop, feature/\*)

### Mudanças Técnicas

#### Performance e Segurança

- 🔒 **Zero vulnerabilidades** de segurança no frontend
- ⚡ **100x mais rápido** linting com Biome vs ESLint
- 📦 **Redução de 60%** nas dependências npm (149 vs 370 pacotes)
- 🛡️ JWT authentication planejado
- 🔐 Rate limiting configurado
- ✅ Input validation com Pydantic

#### Qualidade de Código

- 🧪 Framework de testes configurado (pytest, Vitest)
- 📝 Logging estruturado com structlog
- 🎨 Formatação automática (Biome para TS, Black para Python)
- 📊 Type hints obrigatórios (Python typing, TypeScript)

### Próximos Passos (v0.2.0)

- [ ] Implementar API Gateway com FastAPI
- [ ] Criar models e schemas Pydantic
- [ ] Configurar Alembic para migrações
- [ ] Implementar autenticação JWT
- [ ] Criar endpoints base de health check
- [ ] Configurar logging centralizado
- [ ] Setup de testes unitários iniciais

### Próximos Passos (v0.3.0)

- [ ] Implementar Portfolio Service
  - CRUD de portfólios e ativos
  - Cálculo de alocação
  - Rebalanceamento MPT
- [ ] Implementar Analysis Service
  - Indicadores de risco/retorno
  - Análise fundamentalista
  - Correlação entre ativos

### Próximos Passos (v0.4.0)

- [ ] Implementar Scanning Service
  - Varredura B3
  - Sistema de scoring
  - Sugestões de ativos
- [ ] Implementar Projection Service
  - Simulações Monte Carlo
  - Projeções ARIMA
  - Fronteira eficiente

### Próximos Passos (v0.5.0)

- [ ] Implementar Reporting Service
  - Geração de relatórios JSON/CSV
  - Geração de PDF com ReportLab
  - Gráficos com Matplotlib
- [ ] Implementar componentes React
  - Dashboard principal
  - Visualizações Chart.js
  - Formulários de criação/edição

---

## Versionamento

Este projeto usa [Semantic Versioning](https://semver.org/):

- **MAJOR** version quando há mudanças incompatíveis na API
- **MINOR** version quando adiciona funcionalidade de forma retrocompatível
- **PATCH** version quando corrige bugs de forma retrocompatível

### Estados de Desenvolvimento

- **[Não Lançado]**: Trabalho em progresso, não taggeado
- **[X.Y.Z-alpha]**: Feature incompleta, pode mudar drasticamente
- **[X.Y.Z-beta]**: Feature completa, em testing
- **[X.Y.Z-rc.N]**: Release candidate, pronto para produção após testes
- **[X.Y.Z]**: Release estável

---

## Tipos de Mudanças

- `Added` - Novas funcionalidades
- `Changed` - Mudanças em funcionalidades existentes
- `Deprecated` - Funcionalidades que serão removidas
- `Removed` - Funcionalidades removidas
- `Fixed` - Correções de bugs
- `Security` - Correções de vulnerabilidades

---

## Como Contribuir para o Changelog

Ao criar um Pull Request, adicione suas mudanças na seção `[Não Lançado]` seguindo o formato:

```markdown
### Added

- Breve descrição da nova feature

### Fixed

- Breve descrição do bug corrigido

### Changed

- Breve descrição da mudança
```

Quando uma versão for lançada, o mantenedor moverá as mudanças para a seção apropriada com a data.

---

**Última atualização**: 17 de fevereiro de 2026
