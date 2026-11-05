---
name: sdd-iniciar
description: "Hub de início do fluxo sdd — recebe um work item já registrado (FT-031, EP-03, AT-012, IM-003, DF ou IB que o backlog conhece, tarefa [DEV] [REV] [APR] [VER] [ESP] [GB] [ATD] [IMPL] [BD] [INF] [OPE] [EXT]) ou \"minha próxima tarefa\", descobre o tipo e diz qual skill de papel usar: sdd-desenvolver (Dev), sdd-revisar (Revisor e [APR]), sdd-verificar (QA), sdd-especificar (Especificador), sdd-atender (Atendimento), sdd-executar (demais categorias da Sustentação), sdd-implementar (fatia AFK verificada: abrir o PR), sdd-consolidar (fatia pronta: PR mergeado) ou sdd-planejamento (troca de modo, sprint); pedido novo ou item fora do backlog vai para a sdd-triar. Use em \"iniciar\", \"começar\", \"pegar a task 123\", \"vamos trabalhar na FT-031\", \"iniciar o AT-012\", \"minha próxima tarefa\", \"o que eu pego agora?\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.7"
---

# sdd-iniciar — Hub: qual skill faz este item

Cada tarefa do EWM tem um papel e uma skill dona, que pode ser chamada direto por quem tem o papel. Esta skill
descobre o tipo do item e diz qual é: não confere compromisso, não cria branch e não mexe no EWM — a skill do papel
faz isso, começando por assumir a própria tarefa (`elm_transicao(<id>, "assumir")`).

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — Identificar o item

**Ordem de consulta** — vale a primeira fonte que achar, e nunca se inventa dado de work item: (1) `status.md` nas
branches (atual, worktrees, remotas: `git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`) e na base, pela regra
A base prevalece do [`status-template.md`](../sdd-desenvolver/references/status-template.md); (2) o `backlog.md`
da base (ids locais e as colunas `origem` e `elm`, inclusive as `### <Categoria>` da `## Sustentação`); (3) o EWM
(`elm_ler_wi`), se a sessão tem o MCP `elm` (o título da tarefa traz o tipo: `[DEV] FT-031 …`); (4) perguntar à
pessoa. Id que não está em (1) nem (2) não está registrado. Fatia `concluida`, `dividida` ou `cancelada` no
`backlog.md` → mostre a situação (e a `obs`) e pare: o `status.md` de uma branch não vale.

**Número do EWM** (DF, IB): quem decide é o tipo do id local da linha que o tem na coluna `elm` (`FT-`, `EP-`, `AT-`,
`IM-`…), não o tipo do work item. O IB `Sustentação`, `Manutenção` ou de uma categoria não é item de trabalho:
diga o que ele é e peça o item.

## Passo 2 — Encaminhar

| Item informado | Skill | Papel / agente |
|---|---|---|
| pedido em texto, ou id que não está no backlog | **`sdd-triar`** | P.O. / `sdd-produto` |
| `EP-nn`, tarefa `[ESP]` (de épico ou de fatia) | **`sdd-especificar`** | Especificador / `sdd-produto` |
| `FT-nnn` (de épico ou de Manutenção), tarefa `[DEV]`, "próxima fatia" | **`sdd-desenvolver`** | Dev / `sdd-codificador` |
| tarefa `[REV]` | **`sdd-revisar`** (rubrica C sobre o PR) | Revisor / `sdd-revisor` |
| tarefa `[APR] FT-nnn Aprovar plano` | **`sdd-revisar`** (seção "Aprovação do plano — a `[APR]`") | Aprovador (Dev Sênior) / `sdd-revisor` |
| tarefa `[APR] FT-nnn Aprovar PR` | **`sdd-revisar`** (seção "Aprovação do PR — a `[APR]`") | Aprovador (Dev Sênior) / `sdd-revisor` |
| tarefa `[VER]` | **`sdd-verificar`** | Verificador (QA) / `sdd-verificador` |
| `AT-nnn`, tarefa `[ATD]` | **`sdd-atender`** | quem atende / `sdd-produto` |
| `IM-`, `BD-`, `IN-`, `OP-`, `EX-nnn` (as demais categorias da tabela **Sustentação** do `sdd.md`), tarefa `[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]` | **`sdd-executar`** | quem faz / `sdd-produto` |
| fatia `nova` no `backlog.md` (não passa na DoR: `obs` `falta: …`), ou `status.md` em `especificando` | **`sdd-especificar`** (a `[ESP] FT-nnn`, na branch da fatia) | Especificador / `sdd-produto` |
| `status.md` em `especificada` (especificação concluída, `[DEV]` criada) | **`sdd-desenvolver`** (começa na branch dela) | Dev / `sdd-codificador` |
| fatia `iniciada` no `backlog.md` sem `status.md` em nenhuma branch (a sessão parou entre o registro e a branch) | **`sdd-desenvolver`** (retomada pelo Passo 4 — só o `responsavel` da linha retoma) | Dev responsável / `sdd-codificador` |
| fatia em `verificada` (AFK) | **`sdd-implementar`** (Passo 5 — abrir o PR) | Dev / `sdd-codificador` |
| fatia em `aceita` (HITL), ou em `aguardando-aprovacao-pr` (AFK) com a `[APR] Aprovar PR` concluída — qualquer item dela, menos a `[APR]` | **`sdd-desenvolver`** (Passo 6 — merge do PR aprovado) | Dev responsável / `sdd-codificador` |
| fatia em `aguardando-aprovacao-pr` (AFK) sem a `[APR] Aprovar PR` concluída | **`sdd-revisar`** (seção "Aprovação do PR — a `[APR]`") | Aprovador (Dev Sênior) / `sdd-revisor` |
| fatia em `bloqueada` com `aguardando troca para HITL` | **`sdd-planejamento`** (Troca de modo, na base); feita a troca, o Dev retoma pela **`sdd-desenvolver`** | P.O. ou SM / `sdd-produto` · Dev / `sdd-codificador` |
| fatia `pronta` (na base) | **`sdd-consolidar`** (processo de produto, na `[GB]`) | P.O. ou SM / `sdd-produto` |
| tarefa `[GB] Gerenciamento do backlog` | pedido de sprint (planejar, ritos, "sincroniza a sprint") → **`sdd-planejamento`**; senão, fatias `pronta` → **`sdd-consolidar`** (uma por vez); nenhuma → **`sdd-triar`** | SM (o dono) ou P.O. / `sdd-produto` |

As linhas `fatia …` valem sobre as do item (`FT-nnn`, `[DEV]`…) e leem a fase pela regra A base prevalece (Passo 1).
Tarefa `[DEV]` ou de Sustentação já fechada no EWM encaminha igual: a `sdd-desenvolver`, a `sdd-atender` e a
`sdd-executar` mostram o estado e oferecem reabrir ou fechar o item
(a `[DEV]` com o PR mergeado, pelo Passo 6 da `sdd-desenvolver`; o item de Sustentação, `concluido`).

```
🔀 <item> — <título> · <tipo> · <fase do status.md | status do backlog>
Próximo: use `<skill> <item>`   (agente: <agente>)
```

Pedido em texto: `🔀 pedido não registrado — <resumo em uma linha>` · `Próximo: use sdd-triar`.

Responda com a instrução e **pare**: nunca invoque nem simule a skill do papel — ela começa na própria invocação.

## "Minha próxima tarefa"

1. Com o MCP `elm` e a sprint publicada: `elm_listar_wi(dono: "eu", iteracao: <a da sprint aberta>, tipo: "tarefa")`;
   sem ele, ou com `**Publicação no EWM:** pendente` no cabeçalho (nenhuma tool recebe a iteração dela antes da
   publicação — [elm.md](../sdd/references/elm.md), Regras de toda escrita, item 6): as linhas do `sprint-<nn>.md`
   aberto (Fatias, Especificação e as `### <Categoria>` da Sustentação) com `responsavel` = a pessoa (login do
   `sdd.md` ou `git config user.email`) — com o marcador, diga também "sprint não publicada no EWM → sincroniza a
   sprint (`sdd-planejamento`)".
2. Mostre as tarefas abertas (não concluídas) de **qualquer tipo**, na ordem de prioridade do `backlog.md` (`crítica`
   → `baixa`, `—` no fim; empate pela ordem da linha) — as que já estão em andamento primeiro (sem o MCP: fatia e
   especificação `iniciada`, item `em-andamento`):
   ```
   📋 Suas tarefas na sprint <pai>/Sprint <nn> (<login>)
   | # | Tarefa | Item | Estado | Skill |
   |---|---|---|---|---|
   | 1 | [DEV] 669412 | FT-034 Exportar relatório | Em Desenvolvimento | sdd-desenvolver |
   | 2 | [REV] 669401 | FT-031 Bloquear a conta | Novo | sdd-revisar |
   Qual? (número)
   ```
   Tarefa sem tipo do sdd no título (`[DEV]`, `[REV]`, `[APR]`, `[VER]`, `[ESP]`, `[GB]` e os prefixos da Sustentação não aparecem): mostre no fim, com
   Skill `— (fora do sdd)`; escolhida → diga que ela ainda não está na sprint e indique "sincroniza a sprint"
   (`sdd-planejamento`, P.O. ou SM), que a traz com o mesmo id — como item de Sustentação ou como tarefa de papel de
   uma fatia ou épico ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §9).
3. A pessoa escolhe → Passo 2 com o item escolhido. Nenhuma tarefa → diga e ofereça "próxima fatia"
   (`sdd-desenvolver`) ou a `sdd-status`.

## Regras

- Só encaminha: o compromisso (DoR, sprint, WIP), a branch e o EWM são da skill do papel.
- Nunca invente dados de work item; na dúvida entre dois tipos, pergunte.
