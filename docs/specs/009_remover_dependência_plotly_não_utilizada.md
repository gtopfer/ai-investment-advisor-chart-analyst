# Especificação de Feature: Remover dependência plotly não utilizada

## 1. Contexto & Valor de Negócio
- **Como um(a)** desenvolvedor mantenedor
- **Eu quero** `requirements.txt` sem plotly enquanto a UI usa `st.bar_chart`
- **Para que** a instalação fique mais leve e o débito técnico documentado seja eliminado

## 2. Requisitos & Restrições
- **R1**: `plotly` removido de `requirements.txt` (e de qualquer requirements auxiliar se listado).
- **R2**: Nenhum módulo da aplicação importa plotly.
- **R3**: Gráficos existentes continuam via Streamlit (`st.bar_chart` ou equivalente já em uso).
- **R4**: `.ai/technical-spec.md` atualizado (risco/stack plotly) e `docs/CHANGELOG.md` com impacto.

## 3. Expectativas de UI/UX
- Há interface de usuário? **Não** (sem mudança visual planejada).

### Definition of Done — UX
- [x] N/A justificado

## 4. Checklist Técnico / Notas
- Precisa de banco: Não
- Novos pacotes: Não (remoção)
- Segurança: N/A

## 5. Definition of Ready (DoR)
- [x] Claro
- [x] Dependências N/A
- [x] Sem perguntas em aberto

## 6. Definition of Done (DoD)
- [ ] R1–R4 atendidos
- [ ] Testes verdes; review APROVADO
