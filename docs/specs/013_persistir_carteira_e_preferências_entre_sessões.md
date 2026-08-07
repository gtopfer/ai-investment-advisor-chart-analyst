# Especificação de Feature: Persistir carteira e preferências entre sessões

## 1. Contexto & Valor de Negócio
- **Como um(a)** usuário recorrente do dashboard
- **Eu quero** reabrir o app e encontrar minha carteira e preferências de filtro
- **Para que** eu não precise reimportar/reconfigurar a cada visita

## 2. Requisitos & Restrições
- **R1**: Persistência **no browser** (decisão 2026-08-01): sobrevive a F5/reload no mesmo navegador/origem. Sem backend de conta.
- **R2**: Persistir no mínimo:
  - texto/posições da **carteira atual** (`portfolio_text` / equivalente)
  - preferências: **classes**, **universo**, **estratégia**, **capital** (aporte)
- **R3**: Opcional no mesmo pacote se barato: `period`, limiar de rebalance (SPEC-015), modo valor/qtd da carteira.
- **R4**: Ação de **limpar dados salvos** (reset para defaults do app).
- **R5**: Se não houver dados salvos, comportamento atual (defaults).
- **R6**: Não persistir senha de IA nem chaves de API.
- **Restrição**: Streamlit — preferir mecanismo suportado (ex. `st.query_params` / component localStorage / `st.session_state` + rehydrate documentado). Architect escolhe a API estável do Streamlit em uso.
- **Fora de escopo**: multi-dispositivo, conta cloud, criptografia forte de dados sensíveis (carteira é local).

## 3. Expectativas de UI/UX
- **Há interface de usuário?** Sim
- Caption discreta “Preferências salvas neste navegador” + botão “Limpar dados salvos”
- Sem modal agressivo no primeiro load

### Definition of Done — UX
- [ ] Reset e feedback de “limpo”
- [ ] Microcopy
- [ ] design-premises
- [ ] Aceite UX

## 4. Checklist Técnico / Notas
- Banco: Não
- Pacotes: só se Architect exigir component leve; preferir std Streamlit
- Segurança: não gravar `AI_ACCESS_PASSWORD` / API keys

## 5. Definition of Ready (DoR)
- [x] Browser/local
- [x] Campos mínimos definidos
- [x] Sem conta

## 6. Definition of Done (DoD)
- [ ] R1–R6 atendidos
- [ ] Testes do round-trip serialização (onde testável sem browser real)
- [ ] CHANGELOG; review APROVADO
