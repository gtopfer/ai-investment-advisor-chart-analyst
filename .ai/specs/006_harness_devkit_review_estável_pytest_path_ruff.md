# Especificação de Feature: [HOTFIX] Harness ./devkit review estável (pytest path + ruff)

## 1. Contexto & Valor de Negócio
- **Como um(a)** operador / time
- **Eu quero** que `./devkit review` passe no ambiente de desenvolvimento do projeto
- **Para que** o gate Developer/QA do DevKit novo seja utilizável

## 2. Requisitos & Restrições
- **R1**: Com o venv do projeto ativo, `./devkit review` termina **APROVADO** (exit 0) na baseline atual de testes.
- **R2**: A suíte pytest descobre módulos locais (`analysis`, `app`, etc.) **sem** exigir export manual de `PYTHONPATH` (ex.: `pytest.ini` / `pythonpath`).
- **R3**: O linter **não** falha o review por regras aplicadas ao script CLI `./devkit` (excluir ou não incluir como alvo de produção).
- **R4**: O linter **inclui** pacotes de aplicação (`analysis/`, `allocator/`, `ui/`, `llm/`, `portfolio/`, `config/`, `data_fetcher/`, `models/`, `utils/`, além de `app.py` e `tests/`).
- **R5**: CHANGELOG registra hotfix + auditoria de gates pulados (PM/UX/Architect).

## 0. HOTFIX — Auditoria de gates pulados
- **Motivo**: Review REPROVADO bloqueia fluxo do kit; correção de tooling/harness.
- **Gates pulados**: PM estendido, UX, Architect
- **UI**: N/A

## 3. Expectativas de UI/UX
- Há interface de usuário? **Não** (hotfix de tooling)

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- Artefatos esperados: `pytest.ini` e/ou ajuste `ruff.toml`; possível ajuste pontual no `./devkit` local (`cmd_review`)
- Sem mudança de regra de negócio de investimento

## 5. Definition of Ready (DoR)
- [x] Claro
- [x] Dependências: venv + requirements-dev
- [x] Aceite para executar como hotfix

## 6. Definition of Done (DoD)
- [x] R1–R5 atendidos
- [x] `./devkit review` APROVADO
- [x] Auditoria no CHANGELOG
