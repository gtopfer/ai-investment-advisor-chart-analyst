# Especificação de Feature: Unificar parse de carteira (app + portfolio)

## 1. Contexto & Valor de Negócio
- **Como um(a)** desenvolvedor mantenedor
- **Eu quero** uma única implementação de parse de ticker/valor para texto da sidebar e import CSV/TXT
- **Para que** regras de normalização não divirjam e a manutenção seja em um só lugar

## 2. Requisitos & Restrições
- **R1**: `parse_current_portfolio` (texto multilinha da sidebar) e o parse TXT do import usam a **mesma** lógica de valor numérico e validação de ticker.
- **R2**: Comportamento aceito pelos testes atuais de rebalance/crypto/import permanece (mesmos formatos: `TICKER,VALOR` / `:` / `;`, R$, vírgula/ponto, `#` comentário).
- **R3**: Normalização de ticker (`normalize_ticker`) continua aplicada em todos os caminhos de entrada.
- **R4**: Não há duas cópias de `_parse_numeric_value` no repositório.
- **Restrição**: Sem mudança de UX/layout; sem novos formatos de arquivo neste escopo.

## 3. Expectativas de UI/UX (se aplicável)
- Há interface de usuário? **Não** — apenas refatoração de lógica de parse (comportamento observável idêntico).

### Definition of Done — UX
- [x] N/A justificado (sem mudança de interface)

## 4. Checklist Técnico / Notas
- Precisa de mudança no banco de dados: Não
- Novos pacotes/dependências: Não
- Módulo canônico esperado: `portfolio/import_portfolio.py` (ou util compartilhado no mesmo pacote)
- `app.py` delega ao módulo de carteira

## 5. Definition of Ready (DoR)
- [x] Problema e resultado claros
- [x] Dependências externas N/A
- [x] Sem perguntas em aberto

## 6. Definition of Done (DoD)
- [ ] R1–R4 atendidos
- [ ] Suíte de testes (incl. parse) verde
- [ ] CHANGELOG atualizado
- [ ] `./devkit review` APROVADO
