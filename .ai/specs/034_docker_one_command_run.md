# Especificação de Feature: Docker one-command run

> **Prioridade:** P3 · **Backlog melhoria 2026-08-01** · Status inicial `draft` (PM)

## 1. Contexto & Valor de Negócio
- **Como um(a)** novo usuário
- **Eu quero** subir com Docker
- **Para que** não precise montar venv manual

## 2. Requisitos & Restrições
- **R1**: Dockerfile (Python slim + deps).
- **R2**: docker-compose opcional com porta 8501 e env_file.
- **R3**: README: comando único; passar GROQ_API_KEY etc.
- **R4**: Fluxo local sem Docker permanece documentado.
- **Dependências:** SPEC-023
- **Desbloqueia / relacionada:** —
- **Fora de escopo:** K8s Helm chart.

## 3. Expectativas de UI/UX (se aplicável)
- **Há interface de usuário?** Não — Infra
- Prioridade: **P3**

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- Dockerfile; .dockerignore; compose.
- Banco de dados: Não (salvo se Architect excepcionar)
- Novos pacotes: só se justificado na tech-spec
- Segurança: não persistir/logar API keys nem senha de IA

## 5. Definition of Ready (DoR)
- [x] Problema e valor claros (auditoria de melhorias)
- [x] Prioridade e dependências registradas
- [ ] Decisões finas de produto (se restarem) fechadas no chat PM antes do approve
- [x] Critérios de aceite testáveis nos requisitos

## 6. Definition of Done (DoD)
- [ ] Todos os requisitos da §2 atendidos
- [ ] Testes automatizados cobrem caminhos críticos
- [ ] `docs/CHANGELOG.md` + link em `docs/README.md` / backlog
- [ ] `./devkit review` APROVADO
- [ ] Tech-spec §9 se houver decisão arquitetural
