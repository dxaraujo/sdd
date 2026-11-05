---
name: sdd-desenvolver
description: "Skill do papel Dev no fluxo sdd — começa ou retoma uma fatia já registrada no backlog (FT-031, DF ou IB do backlog, tarefa [DEV]), em qualquer trilha. É o ponto de compromisso: confere a Definition of Ready, o responsável, a sprint aberta (fora dela, puxada ou encaixe pela sdd-planejamento) e o WIP; grava a fatia iniciada na base (backlog e sprint, com push), cria a branch (sugere o nome) e a pasta .kiro/specs/ com o status.md, assume a [DEV] no EWM (com confirmação) e encaminha pela fase: pesquisar → plano → implementar → PR. Com o PR aprovado (aceita no HITL; a [APR] concluída no AFK), faz o merge, grava a fatia pronta na base com as lições e os créditos e conclui a [DEV]. Pedido novo vai para a sdd-triar; [REV], [VER], [ESP] e os itens de Sustentação (AT-, IM-…) têm skill própria (o hub sdd-iniciar encaminha). Use em \"vamos trabalhar na FT-031\", \"pegar a [DEV] da FT-031\", \"corrigir o defeito 4567\", \"próxima fatia\", \"retomar a FT-031\", \"mergeia a FT-031\", \"o PR da FT-031 foi aprovado\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.7"
---

# sdd-desenvolver — Compromisso e início do código

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-desenvolver/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Começar é um compromisso: daqui em diante a fatia consome a capacidade do time e o lead time corre. Por isso esta
skill só começa o que já está registrado e planejado; a entrada de trabalho novo é da **`sdd-triar`**. É a skill do
papel **Dev**: grava `iniciada` na base e assume a `[DEV]` da fatia (Passo 4), encaminha cada fase para a skill dela
(Passo 5) e, no merge do PR aprovado, grava `pronta` na base e encerra a `[DEV]` (Passo 6). Revisão (`[REV]`),
verificação (`[VER]`), especificação (`[ESP]`) e os itens `AT-`, `IM-`… da Sustentação (`[ATD]`, `[IMPL]`…) têm
skill própria; a fatia de Manutenção (`FT-`) é deste papel. Na dúvida sobre o item, o hub **`sdd-iniciar`** diz qual.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — O que chegou

**Ordem de consulta** para qualquer id (`FT-031`, número do EWM) — vale a primeira fonte que achar, e nunca se
inventa dado de work item: (1) o `status.md` da fatia nas branches (atual, worktrees, remotas) e na base, pela regra
A base prevalece do [status-template.md](references/status-template.md); (2) o `backlog.md` da base (ids locais e a
coluna `elm`); (3) o EWM (`elm_ler_wi`), se a sessão tem o MCP `elm`; (4) perguntar à pessoa. O EWM e a pessoa só
completam dados: id que não está em (1) nem (2) não está registrado → `sdd-triar`. A `fase` do `status.md` decide
se o papel pode começar.

| Entrada | Como ler |
|---|---|
| `FT-nnn` | `<produto>/backlog.md` e a ficha da fatia (coluna `ficha`; de épico, também o PRD que ela cobre) |
| número do EWM (DF, IB) | a linha do `backlog.md` com esse id na coluna `elm`, depois do rótulo (`DF [4567](…)`, `IB [612010](…)`; registrado sem o MCP, `DF 4567`); linha de épico ou da `## Sustentação` → as linhas abaixo |
| tarefa `[DEV] FT-nnn` | a fatia do pai |
| "próxima fatia" | a `planejada` de maior prioridade da sprint aberta (empate: a mais acima na tabela) sem `status.md` em nenhuma branch (o `especificada` conta como sem); nenhuma → a `elegivel` do topo do backlog, também sem `status.md` em branch ou worktree (puxada) |
| `[REV]`, `[VER]`, `EP-nn`/`[ESP]`, item de Sustentação pelo tipo de id (`AT-nnn`, `IM-nnn`…: o IB `[AT-nnn]` ou a tarefa `[ATD]`, `[IMPL]`…) | não é deste papel → "use `sdd-iniciar <item>`" e pare (a fatia de Manutenção, `FT-nnn`, é deste papel) |
| pedido em texto, ou id que não está no backlog | não está registrado → "use `sdd-triar`" e pare |

Fatia com `status.md` da especificação ([status-template.md](references/status-template.md)): `especificando` →
"use `sdd-especificar FT-<nnn>`" e pare; `especificada` → é **começo**, não retomada: Passos 2–4 na branch dela
(troque para ela, como abaixo), sem os itens 1, 3 e 4 do Passo 4 (revisor, verificador, branch e pasta vieram da
especificação; o item 4 só cria o `.config.kiro`) e, no item 5, a `[DEV]` já existe (assumir); a DoR se confere pela ficha da branch; o `status.md` vai a
`pesquisando`, com `fatia iniciada (sdd-desenvolver)` no Histórico.

Fatia já iniciada (tem pasta em `.kiro/specs/` nesta branch, em worktrees ou em branches remotas —
`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`) → leia o `status.md` e **retome**: Passo 4, item 5
(assumir: já minha e em andamento → `ja_estava`, nada a fazer; já fechada → o `precondicao` do item 5) e Passo 5,
sem repetir o Passo 3; `pronta` ou `concluida` na base → só o Passo 5. `iniciada` no `backlog.md` sem `status.md` em nenhuma branch (a sessão parou
entre o registro e a branch) → só o `responsavel` da linha retoma, pelo Passo 4 a partir do item 3, depois de
conferir a `iniciada` em `origin/<base>` (`git show origin/<base>:<produto>/backlog.md`; só no local → antes, o push
do item 2, variante do Dev); outra pessoa →
"iniciada por <login> em <data do commit `<FT> iniciar`>, sem branch publicada" e pare. `dividida` ou `cancelada`
no `backlog.md` → nada a retomar: diga isso (a `obs` aponta a substituta) e pare. Branch
diferente da atual → pergunte se troca (alterações locais não commitadas → avise e pare; nunca ofereça descartar,
`stash` ou `reset`). **Branch aberta numa worktree** (`git worktree list` mostra `.kiro/local/wt/<ft>` com ela —
fatia do `sdd-loop`): não troque, o `git switch` falha; trabalhe na worktree — comandos com
`cd .kiro/local/wt/<ft> && <comando>`, arquivos pelo caminho `.kiro/local/wt/<ft>/<caminho>` — e passe isso à
próxima skill. Vale para todas as skills de papel que precisam da branch da fatia.

**Troca AFK → HITL** (fatia em `bloqueada (de: <fase>)` com `aguardando troca para HITL`, ou com `Modo: AFK` no
`status.md` e `HITL` no `backlog.md`): leia a base sem trocar de branch — `git fetch` e `git show origin/<base>:<produto>/backlog.md` e
`…/sprints/<pai>/sprint-<nn>.md`. A troca só vale registrada lá pelo P.O. (ou SM): `modo` `HITL` no backlog e a
Observação `modo: AFK → HITL (…)` na linha da fatia. Registrada → mostre, com o revisor e o verificador das colunas
Revisor e Verificador da linha da sprint (a Troca de modo grava ali; o Histórico não é a fonte), e, com "sim", grave
no `status.md` `Modo: HITL`, os ids da `[REV]` e da `[VER]` (campo ELM, da coluna "Tarefa ELM"), `Bloqueio: —` e a
fase de origem (`planejando`); commit e push. A `[DEV]` é retomada por
`elm_transicao(<id>, "assumir")` (já minha e em andamento → nada a fazer; já fechada → Passo 4, item 5). Siga no HITL: `sdd-plano` Passo 5, com o GATE pela
senioridade. Recusada (Observação `modo: AFK mantido`) → `Bloqueio: —`, fase de origem, segue no AFK. Nenhuma das duas → diga
que a troca é do P.O. (`sdd-planejamento`, Troca de modo) e pare. Na troca, o Dev
não grava na base nem cria ou cancela tarefa. **HITL → AFK nunca:** `Modo: HITL` no `status.md` e `AFK` no backlog →
avise a divergência ao P.O. e siga no HITL.

## Passo 2 — Trilha

A trilha vem do registro, não de uma triagem nova: a coluna `trilha` da linha da fatia no `backlog.md` (de épico,
sempre **padrão**). Ao ler o item, a trilha registrada não serve (a "rápida" tem regra de negócio nova)
→ pare e devolva à `sdd-triar` para refazer a triagem.

| Trilha | Caminho depois daqui |
|---|---|
| **padrão** | pesquisa → plano → **GATE do plano** → implementação → PR → revisão → verificação (AFK: revisão e verificação antes do PR) |
| **rápida** | pesquisa curta → `bugfix.md` + `tasks.md` (o teste que reproduz primeiro) → implementação → PR → revisão → verificação (AFK: antes do PR) |

## Passo 3 — Compromisso

Vale para todas as trilhas. Tudo conferido **antes** de gravar na base, criar branch ou mexer no EWM; falhou um item
→ diga qual e o caminho, e não comece.

1. **Definition of Ready** da trilha — a do formato do backlog
   ([../sdd-fatiar/references/backlog.md](../sdd-fatiar/references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-elegivel),
   mais os itens próprios do `acordos.md`): a fatia está `elegivel` ou `planejada` e ainda passa (confira agora).
   - Falhou → `sdd-especificar FT-<nnn>`: a fatia `nova` é especificada na `[ESP]` dela, que encaminha à
     `sdd-entrevistar`, à `sdd-triar` (ficha, sem épico) ou à `sdd-fatiar` (refinamento).
2. **Responsável.** A coluna `responsavel` do `backlog.md` é outra pessoa → pergunte se ela sabe; trocar é do
   planejamento, não grave aqui. Quem vai implementar é **Júnior** (`senioridade` no `equipe.json`) e a fatia é
   `AFK` → não comece: avise que Júnior implementa sempre em HITL e mande para a **`sdd-planejamento`** (o modo sai
   da senioridade de quem implementa).
3. **Sprint.** Nada começa sem item planejado: é na tarefa da sprint que as horas são lançadas. A
   fatia está `planejada` na sprint aberta (`sprint` do `backlog.md` = a chave do `sprint-<nn>.md` com
   `**Situação:** aberta`, como `2026/Sprint 03`)? Não está → **puxe** (fluxo puxado, a sprint é cadência): se ela
   é a `elegivel` do topo — nenhuma `elegivel` ou `planejada` de prioridade maior esperando (empate: a mais acima na
   tabela), dentro ou fora da sprint — e o WIP do item 4 tem folga, ela entra na sprint aberta sem cerimônia: a
   linha nasce na sprint com a `iniciada` (Observação `puxada`), e as tarefas vão para a iteração da sprint (Passo 4:
   a que já existe move; só nasce a que falta). Fura a fila ou estoura o WIP → **Encaixe**: a decisão é do P.O., pela
   **`sdd-planejamento`** (seção Encaixe); sem a decisão registrada, não comece. Nenhuma sprint aberta
   (planejamento ainda não feito) → não é encaixe: ofereça a `sdd-planejamento` e não comece.
4. **WIP** (`<produto>/acordos.md`; sem o arquivo, 2 fatias esperando pessoa). Conte as fatias em
   `aguardando-aprovacao-plano`, `pr-aberto`, `em-revisao`, `em-verificacao`, `aceita`, `verificada` e
   `aguardando-aprovacao-pr` nos `status.md` das branches, pela regra A base prevalece do
   [status-template.md](references/status-template.md) (`pronta` ou `concluida` na base não conta), como a
   `sdd-status`. No limite, ou com PR
   parado há mais tempo que o acordo (padrão 1 dia) → mostre quais e recomende destravar antes (aprovar o plano,
   revisar o PR). A pessoa pode seguir mesmo assim: `WIP excedido: <motivo>` vai no Histórico do `status.md` ao
   criá-lo (Passo 4).
5. **Registro publicado.** A linha da fatia, a ficha e o encaixe já estão em `origin/<base>`
   (`git grep -q '<FT>' origin/<base> -- <produto>/backlog.md`)? Só no local → peça o push
   antes: a branch nasce de `origin/<base>`, e um id que ainda não chegou lá pode mudar. Repositório sem remoto
   (ou base nunca publicada) → não há o que conferir: a branch nasce da base local; diga isso e siga.
6. **Dono do item pai** (com o MCP `elm`): o item da fatia no EWM — o IB, ou o item de origem (`DF`/`IB` da coluna
   `elm`) — tem dono (`elm_ler_wi`)? O `assumir` da `[DEV]` com `iniciar_pai` (Passo 4) o exige. Sem dono → peça
   ao P.O. que se ponha como dono (o item é dele: [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md)
   §3) e não comece; `elm` `pendente` ou id sem link (`DF 4567`) → o Passo 4 cria ou completa o item, já com o
   P.O. como dono.

## Passo 4 — `iniciada` na base, branch, pasta e `[DEV]`

Nesta ordem: a `iniciada` chega à base antes da branch — é ela que diz ao time (e a um segundo Dev) que a fatia
começou.

1. **Revisor e verificador** — só na fatia **HITL puxada** (não passou pelo planejamento: a sprint não tem revisor
   nem verificador para ela). Pergunte quem revisa e quem verifica (sugira pelo `equipe.json`: papéis,
   `senioridade` e `horas-revisao-semana`): o revisor é um **Dev Sênior** ativo que não é quem implementa — quem
   implementa é o único Sênior ativo → ele mesmo, com `revisor único`; o verificador nunca é quem implementa.
2. **`iniciada` na base** — pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base),
   variante do Dev: no `backlog.md`, `status` `iniciada` e, se estava `—`, `responsavel` = quem implementa; no
   `sprint-<nn>.md` aberto, Status `iniciada` na linha da fatia. **Puxada:** também a `sprint` (a chave da sprint
   aberta) no backlog, e a linha nasce na seção Fatias da sprint com quem implementa, Status `iniciada`, o revisor
   e o verificador do item 1 (AFK: `—`), Tarefa ELM `—` (a consolidação completa) e a Observação `puxada` (mais
   `revisor único`, se for o caso). Commit `<FT> iniciar`. A branch só nasce com o push conferido (sem remoto:
   Passo 3, item 5). Push recusado → o bloco desfaz o commit de registro e para: rode de novo (outra pessoa pode
   ter iniciado a fatia — Passo 1).
3. **Branch** — sugira e **aguarde**:
   ```
   Branch sugerida: <prefixo do sdd.md><ft>-<slug>   (ex.: feature/ft-031-bloquear-conta)
   Confirma, ou informe outro nome:
   ```
   Confirmado → `git fetch` e `git switch -c <branch> origin/<base>` (já com a `iniciada`).
4. **Pasta** `.kiro/specs/<ft>-<slug>/` com `status.md` de [references/status-template.md](references/status-template.md)
   e o `.config.kiro` da spec do Kiro (`specType` `feature` na trilha padrão, `bugfix` na rápida — formato em
   [../sdd-plano/references/plano-templates.md](../sdd-plano/references/plano-templates.md)).
5. **Assumir a `[DEV]`** (com o MCP `elm`; nunca sem "sim") — `elm_transicao(<id da [DEV]>, "assumir",
   iniciar_pai: true)`, com `estimativa_h` se faltar (regras: [elm.md](../sdd/references/elm.md)). O item de backlog continua do P.O.
   **Já fechada** (`precondicao` "já concluída: reabra antes": alguém a fechou à mão) → mostre o estado; PR da fatia
   mergeado (`gitlab_listar_mrs(origem=<branch>, estado=merged)`; sem o MCP, a pessoa diz) → **Passo 6**, do item 5;
   senão, com "sim", `elm_transicao(<id>, "reabrir")` e de novo o `assumir`.
   Tarefa ainda fora da sprint (puxada, encaixe aprovado agora ou publicação que falhou no planejamento) → antes, o
   IB (ou o item de origem) sai do backlog do EWM para a iteração da sprint (`elm_atualizar_wi(id, iteracao)`; `elm`
   `pendente` → crie-o; id sem link, como `DF 4567` → complete o que a triagem não fez, como a publicação da sprint)
   e, na fatia que saiu de uma sprint sem começar (as tarefas ficaram no backlog do EWM), cada tarefa que já existe
   move na chamada dela, com o dono e a estimativa do papel — `elm_atualizar_wi([id], iteracao, dono, estimativa_h)`:
   a `[DEV]` com quem implementa, a `[REV]` e a `[VER]` com o revisor e o verificador da linha —; só nasce o papel
   que falta, conferido com `elm_listar_wi(pai = IB)`, sem contar a tarefa descartada nem a que tem pendência de
   cancelamento aberta ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md), topo e §3–4; pai sempre
   definido):

   | Fatia | Tarefas | Pai |
   |---|---|---|
   | de épico (padrão) | `[DEV]` `[REV]` `[VER]` | IB da fatia, filho do épico |
   | sem épico, com item de origem (DF, IB) | `[DEV]` `[REV]` `[VER]` | o próprio item de origem, sob a Manutenção — **sem IB novo** |
   | sem épico, pedido em texto | `[DEV]` `[REV]` `[VER]` | IB `[FT-nnn]`, filho da Manutenção |

   Fatia **AFK**: só a `[DEV]`, em qualquer linha — revisão e verificação são subagentes, sem tarefa; a `[REV]` e a
   `[VER]` da fatia HITL que volta AFK não movem: `elm_transicao(<id>, "cancelar")`, no mesmo "sim"; sem o MCP, com
   `precondicao` ou erro → `ELM pendente [<tipo> <id> cancelar]` no `status.md` (elm-sprint.md, topo). Fatia **HITL puxada**: a `[REV]` e
   a `[VER]` vão para o revisor e o verificador da linha da sprint (item 1).

   Grave os ids das tarefas, as que moveram inclusive, no campo ELM do `status.md` (`DEV <id> · REV <id> · VER <id>`)
   e, se o item nasceu ou foi completado aqui, o dele (`IB <id>` ou `DF <id>`) — é por ele que as horas acham a
   tarefa; a `sdd-consolidar` os leva à coluna `elm` do backlog e à Tarefa ELM da sprint. Sem o MCP `elm`:
   `ELM pendente [DEV FT-<nnn> assumir]` no `status.md`.
6. Commit pequeno do `status.md` e do `.config.kiro` e, com "sim", push da branch — publicada, quem retoma (e a
   `sdd-status`) acha o `status.md`.

## Passo 5 — Encaminhar

```
🚦 FT-<nnn> — <título>   ·   trilha <…> · modo <AFK|HITL> · fase <…>
Origem: <EP-nn — título | Manutenção> · Cobre: <… | ficha C1–Cn> · Branch: <…> · Pasta: .kiro/specs/<ft>-<slug>/
Próximo: <skill>
```

| Fase | Próxima skill |
|---|---|
| `pesquisando`, `planejando`, `aguardando-aprovacao-plano` | `sdd-plano` (que começa pela `sdd-pesquisar`) |
| `implementando`, `revisando`, `retrabalho (de: …)` | `sdd-implementar` |
| `verificando` | `sdd-verificar` (AFK) |
| `verificada` | AFK: `sdd-implementar` (Passo 5 — abrir o PR) |
| `pr-aberto`, `em-revisao` | HITL: com o revisor — `[REV]` pela `sdd-revisar` |
| `em-verificacao` | HITL: com o verificador — `[VER]` pela `sdd-verificar` |
| `aceita` | HITL: Dev — **Passo 6** desta skill (merge do PR aprovado e conclusão da `[DEV]`) |
| `aguardando-aprovacao-pr` | AFK: com o Dev Sênior da `[APR] Aprovar PR` — pela `sdd-revisar` (Aprovação do PR); `[APR]` concluída → Dev, **Passo 6** desta skill |
| `pronta` (na base) | `[DEV]` ainda aberta → **Passo 6**, do item 7; senão nada para o Dev: a consolidação é do P.O. ou do SM — `sdd-consolidar` (agente `sdd-produto`); `concluida` → já consolidada |
| `bloqueada (de: <fase>)` | mostre o motivo e a pergunta; resolvido → volta à skill da fase de origem. `aguardando troca para HITL` → a troca é do P.O. (`sdd-planejamento`, Troca de modo); registrada, a Troca AFK → HITL do Passo 1 |

Modo AFK e várias fatias padrão ou rápida planejadas na sprint → ofereça o **`sdd-loop`** (o agente leva cada uma até
o PR). Uma fatia só, com as receitas instaladas (`.kiro/workflows/sdd-*`) → diga que a pessoa pode dispará-las no
chat ("rode o workflow `sdd-planejar-fatia` com fatia FT-<nnn>"; AFK, depois `sdd-entregar-fatia`) — quem dispara
receita é sempre a pessoa, nunca uma skill ou agente.

Diga a próxima e **pare**: nunca invoque nem simule a skill da fase — ela começa na própria invocação. A
exceção é o merge (`aceita`, ou `aguardando-aprovacao-pr` com a `[APR]` concluída): o Passo 6 é desta skill.

## Passo 6 — Encerrar a `[DEV]`: merge do PR aprovado

A fatia chegou a `aceita` (HITL) ou a `aguardando-aprovacao-pr` (AFK): o merge, o registro na base e a conclusão da
`[DEV]` são do Dev responsável, aqui. Também o PR já mergeado por fora, pela UI do GitLab (a `sdd-consolidar` manda
para cá quando falta a `Fase: pronta` na base): siga do item 5 — a `pronta` só com o merge conferido —, e sem a
aprovação registrada (abaixo) o aviso do item 9 diz isso. **Já registrado?** `git fetch` e o `status.md` da fatia em
`origin/<base>` com `Fase: pronta` ou `concluida` → o merge já foi registrado — aqui ou pela sincronização
([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §9), que também grava `pronta` pela evidência do merge
feito por fora, com Créditos e lições `—`: com a `[DEV]` ainda aberta, siga do item 7; senão, diga isso e pare. Vale
a aprovação **registrada**, nunca a dita na conversa ("o PR foi aprovado", "pode mergear"; o P.O. não aprova PR):
- **HITL:** revisão `APROVADO` e verificação `ACEITO` registradas (é o que leva a fatia a `aceita`);
- **AFK:** a `[APR] FT-<nnn> Aprovar PR` está **concluída** e tem o comentário `PR aprovado, sha <sha>` (`elm_ler_wi(<id>,
  comentarios: true)`, só leitura). Sem o MCP `elm` → a linha `PR aprovado por <login>, sha <sha>` que o
  aprovador entregou. Sem a aprovação → avise que o PR espera a leitura do Dev Sênior e pare.

1. **Leia o PR:** `gitlab_obter_mr` pelo `iid` do link no `status.md`. Tem de estar aberto, sem WIP/Draft e sem
   conflito. `merged` → vá ao item 5; `closed` ou WIP → avise e pare. **Conflito** com a base → `fase: retrabalho
   (de: <aceita | aguardando-aprovacao-pr>)` e, no Histórico, a linha `conflito no merge` com os arquivos (é por ela
   que a `sdd-implementar`, no Passo 0, separa este caso das mudanças pedidas na `[APR]`, que gravam a mesma fase);
   commit, push e conferência (itens 1–3 da Entrega do Passo 5 da [`sdd-implementar`](../sdd-implementar/SKILL.md))
   e pare: a `sdd-implementar` atualiza a branch, e a mudança passa de novo pela revisão.
2. **Commit aprovado:** o `sha` do PR = `git rev-parse origin/<branch>` e é o commit que foi aprovado — HITL: o da
   entrega da verificação (o último commit que mudou o `verificacao.md`, `git log -1 --format=%H -- <pasta da fatia>/verificacao.md`, e nele o veredito `ACEITO` — não depende do padrão de mensagem do projeto); AFK: o `sha` do
   comentário da `[APR]`. Commit depois da aprovação → só vale se a base só trouxe registros: o aprovado segue na
   história do PR (`git branch -r --contains <sha aprovado>` lista `origin/<branch>`; o `git merge-base` cai na
   negação do `git merge` dos agentes) e `git diff --name-only <sha aprovado>
   <sha do PR>` cabe no critério do item 1 do Passo 5 da `sdd-implementar` (a branch atualizada por merge da base,
   como em projeto com merge fast-forward ou semi-linear no GitLab); senão, não mergeie: a mudança volta à revisão.
   Branch rebaseada (botão Rebase do GitLab) também volta: o `sha` aprovado some (HITL: o commit da verificação
   reescrito, com data de commit diferente da de autoria) — o sdd atualiza a branch por merge da base.
3. **Resumo e confirmação:**
   ```
   🔀 Merge FT-<nnn> — <título>
   PR !<iid> <origem> → <destino> · sha <curto> · aprovado: <REV APROVADO + VER ACEITO | por <login>>
   Mergear? (sim/não)
   ```
4. **Merge:** `gitlab_mesclar_mr(iid, sha=<sha do PR, conferido no item 2>, remover_origem=true)` — o Kiro também
   confirma; a branch não guarda mais nada (o `status.md` chega à base com o merge, e o registro é lá: item 6). Sem
   o MCP, sem permissão de merge ou recusa do GitLab (conflito → item 1) → a pessoa faz o merge na UI do GitLab, sem
   o botão Rebase (item 2), e diz "mergeado".
5. **Confira:** `gitlab_obter_mr(iid)` (ou `gitlab_listar_mrs(origem=<branch>, estado=merged)`) com estado `merged`
   — inclusive no merge pela UI. Sem o MCP → `git fetch` e `git diff origin/<base> <branch> -- <arquivos que a fatia
   mudou>` vazio (a branch local: a remota sai no merge). Não mergeado → pare.
6. **Registro do merge na base** — pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base),
   variante do Dev; o `status.md` já chegou à base com o merge:
   - **Lições candidatas** no `status.md` — antes de fechar a `[DEV]`: liste as correções humanas que a fatia
     recebeu (tabela Retrabalho; Achados abertos de origem PR ou GATE do plano; bloqueio resolvido por uma pessoa;
     "não é assim" no Histórico) e, com a pessoa, grave uma linha por correção: feito × certo, onde estava o certo e
     a causa proposta (tabela de causas da [`sdd-aprender`](../sdd-aprender/SKILL.md)). Correção sem lição
     (ambiente, digitação) → causa `—`; nenhuma correção → `nenhuma`. O `licoes.md` é da base: quem o grava é a
     consolidação.
   - `Fase: pronta`; no Histórico, `merge do PR <link> por <login>` (AFK: antes, `PR aprovado por <login>, sha <sha>`,
     do comentário da `[APR]` ou a linha que o aprovador entregou); sem o MCP `elm`, também `ELM pendente [<chave>]:
     lançar <h>h e concluir [DEV] FT-<nnn>` e, no AFK, a `ELM pendente [APR FT-<nnn> concluir]: …` que o aprovador
     entregou.
   - **Créditos** na seção Créditos ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4): os desta
     sessão; no AFK, a linha da `[APR]` que veio no comentário `PR aprovado` (ou que o aprovador entregou); e a
     sessão do loop, que só fecha o consumo no fim do turno — o script a lista como sem registro: com o "sim",
     `rateio 1/<n>` pelas fatias do lote.
   - `pronta` na linha da fatia no `backlog.md` e na da sprint dela.

   Commit `<FT> registrar merge` só com o `status.md`, o `backlog.md` e o `sprint-<nn>.md`; push com a conferência.
   Na branch, nada: antes do merge, um commit nela mudaria o `sha` aprovado.
7. **Conclusão da `[DEV]`** (depois do push do item 6): mostre as horas já lançadas (`elm_horas(<id>)`) e pergunte
   só o saldo → `elm_lancar_horas(<id>, <saldo>)` e `elm_transicao(<id>, "concluir")`, numa confirmação (`[DEV]` já
   fechada, do Passo 4, item 5 → só o saldo). Sem o MCP
   `elm`, a pendência já foi no item 6.
8. **Worktree do loop** (`.kiro/local/wt/<ft>`): depois do merge, `git worktree remove .kiro/local/wt/<ft>` —
   **sem `--force`**; os agentes não podem (negado a todos): entregue o comando e a pessoa o roda. Falhou por arquivos
   não rastreados ou alterados → mostre quais (evidência com dado real fica em `.kiro/local/verificacao/`, fora da
   worktree) e deixe a pessoa decidir; nunca force.
9. **Avise o P.O. ou o SM** de que a fatia está `pronta` para a consolidação (**`sdd-consolidar`**, no agente
   `sdd-produto`, com os créditos num comentário na `[GB]`; horas, só do SM) e **pare**: a consolidação não é do Dev.

## Regras

- Só começa o que está registrado e planejado: pedido novo ou item fora do backlog vai para a `sdd-triar`; fatia
  fora da sprint, para o encaixe.
- O EWM (ou a pessoa) é a fonte dos dados do item; o código, do comportamento atual; o `status.md`, da fase (regra A
  base prevalece).
- Toda troca/criação de branch, todo commit e push na base e toda alteração no EWM só com "sim". Na base, o Dev só
  grava a situação da fatia (`iniciada`, `pronta`) e o `status.md` dela depois do merge.
- Nunca invente dados de work item.
- Não invoque nem simule outra skill do fluxo: diga a próxima (Passo 5) e pare.
