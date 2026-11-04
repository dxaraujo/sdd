---
name: sdd-consolidar
description: "Fecha uma fatia pronta do fluxo sdd (PR mergeado e registrado na base pelo Dev) — processo de produto, do P.O. ou do SM (analista de negócio) no agente sdd-produto, na tarefa [GB] Gerenciamento do backlog (horas só do SM; os créditos num comentário nela): lê o campo Drift de negócio do status.md (marcado pela revisão e pela verificação) e, com drift, leva o PRD ou a ficha a nova versão; manda para o ELM pelo MCP elm, numa confirmação, os requisitos, a regra da ficha as-built, a especificação técnica as-built (escrita pelo Dev no PR), os casos de teste (criados pelo agente no ETM, um por cenário verificado) e a conclusão do item de backlog; leva os ADRs do PR para a pasta de ADRs, corrige o glossário, marca a fatia concluida no backlog e na sprint, registra as lições (sdd-aprender) e diz o que vem a seguir no épico. Use em \"PR mergeado\", \"fecha a FT-031\", \"consolidar\", \"concluir a fatia\", \"a fatia foi entregue\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.5"
---

# sdd-consolidar — Documentação viva depois do merge

O plano da fatia (`research`, `design`, `tasks`) é andaime: cumpriu o papel quando o código chegou à base. O que
fica valendo é a documentação oficial no ELM — e ela tem de descrever o que **foi** construído. Esta skill fecha a
distância entre os dois.

**Processo de produto:** quem consolida é o **P.O. ou o SM** (analista de negócio), no agente **`sdd-produto`**, e
a tarefa é a **`[GB] Gerenciamento do backlog`** (a `GB` da primeira linha de `## Sustentação` do `backlog.md`;
dono = o SM). A consolidação não repete a revisão nem a verificação: o drift de negócio já vem marcado por elas no
`status.md`; os ADRs já vêm escritos no PR.

Entrada: fatia `pronta` — o Dev responsável mergeou o PR aprovado e, conferido o merge, gravou `Fase: pronta` no
`status.md` da **base** (Passo 6 da `sdd-desenvolver`; merge por fora do sdd: a sincronização da sprint,
[elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §9). Leia a fase dali (`git fetch` e `git show
origin/<base>:.kiro/specs/<ft>-<slug>/status.md`), com o `status` da linha no `backlog.md` da base: `concluida` em
qualquer um dos dois → diga "já consolidada em <data>" e pare — nada se repete (ADR, lições, glossário, CT, ELM).
Sem `pronta` na base (PR aberto, ou mergeado sem o registro) → não consolide: mande o Dev ao Passo 6 da
`sdd-desenvolver` (o merge e o registro do merge são dele; mergeado por fora do sdd → "sincroniza a sprint") e
pare. Tudo aqui é gravado na **base**, pelo bloco
[Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base) (a troca e o `pull --ff-only` vêm antes de
qualquer passo).

## Passo 1 — Drift de negócio

Leia o campo **Drift de negócio** do `status.md` — marcado pela revisão (`sdd-revisar`, rubrica C: achado aceito
ou decisão técnica que muda comportamento visível) e pela verificação (`sdd-verificar`: cenário ajustado). Não
releia o `design.md` nem o `verificacao.md` atrás de drift: isso já foi julgado.

- `sim — <motivo>` → mostre o motivo e leve o PRD a nova versão pela `sdd-prd` (mudança depois de aprovado) — na
  fatia sem épico, a ficha, pela `sdd-triar` — **antes** de publicar (Passo 2).
- `não` → nada no PRD nem na ficha.
- vazio (`—`) → pergunte a quem revisou ou verificou (Histórico) e grave a resposta no campo; não procure você;
  sem REV nem VER no Histórico (fatia `pronta` pela sincronização, `merge do PR <link> por fora do sdd`) → pergunte
  ao Dev responsável (o dono da `[DEV]`) e grave a resposta no campo.

## Passo 2 — ELM (com o MCP `elm`; senão registre pendências)

Numa confirmação só, nesta ordem, como diz [references/elm-publicar.md](references/elm-publicar.md) (os casos de teste precisam dos ids dos requisitos):
- *requisitos* — publicar/atualizar o que ainda não foi (publicação `no-merge` no `sdd.md`, ou a nova versão do
  Passo 1);
- *regra da ficha* (fatia padrão sem épico com regra nova ou alterada) — gerar o conceito OKF da regra as-built
  em `.kiro/specs/<ft>-<slug>/elm/` (formato do `okf-elm.md` da `sdd-prd`; alteração → a partir do artefato do
  bundle), mostrar e, com o `verified` humano, publicar como os requisitos;
- *especificação técnica* — se a linha ET do `sdd.md` diz `as-built no merge`: a ET **as-built** chegou escrita
  pelo Dev no PR (`elm/ET-<slug>.md`) e foi julgada com o código (rubrica C15); você não a escreve nem a reescreve.
  O `verified` humano é de quem aprovou o código: `{ by: human:<login>, at: <data da aprovação> }` do revisor
  (`revisao-codigo-<N>.md` APROVADO, HITL) ou do Dev Sênior da `[APR] Aprovar PR` (AFK), com `status: stable`.
  Sem a ET no PR → `ELM pendente [ET FT-<nnn> escrever]` para o Dev, que a entrega num PR curto;
- *casos de teste* — um por cenário verificado (`verificacao.md`/`CT.csv`); ids no `verificacao.md` e no
  `status.md`;
- *tarefas* — a consolidação **não** lança horas nem conclui `[DEV]`, `[REV]`, `[VER]` ou `[APR]`: cada skill de
  papel concluiu a sua (a `[DEV]` no merge, a `[REV]` ao aprovar, a `[VER]` ao aceitar, a `[APR]` na aprovação do
  plano ou do PR; no AFK não há `[REV]` nem `[VER]`). Tarefa da fatia ainda aberta → mostre qual e de quem, e
  registre `ELM pendente [<chave>]: concluir <tarefa> (<login>)`, que a pessoa faz na sessão dela;
- *backlog* — concluir o IB da fatia (e o do épico, na última fatia — Passo 4). Tarefa concluída sem horas não
  trava: a virada aponta. A consolidação é **pré-condição dos ritos de fechamento** da sprint (review, retrospectiva,
  virada): fatia `pronta` sem ela para o rito, salvo decisão do P.O.;
- *horas* — só o SM lança as da consolidação na `[GB] Gerenciamento do backlog`: `elm_lancar_horas(id, horas)`
  (lança, não conclui — a `[GB]` é contínua). O P.O. nunca lança horas, nem quando também é o SM.
- *créditos* — em toda consolidação, do P.O. ou do SM, os créditos desta sessão
  ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4) vão, no Passo 4, num comentário na `[GB]`
  (`elm_comentar(<id da [GB]>, "Créditos consolidação FT-<nnn>: <créditos> (sessão <sessão>, <login>, <AAAA-MM-DD>)")`,
  com "sim") e na seção **Créditos de gestão** do `sprint-<nn>.md` aberto (Atividade `consolidação FT-<nnn>`), no
  commit do Passo 4. `## Sustentação` sem a `GB` → indique o modo inicial da `sdd-planejamento` (ou crie-a pelo
  [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §2, com "sim"); sem ela, grave só a linha em
  Créditos de gestão. Falha no comentário → `ELM pendente [GB <id> créditos]` no lugar das pendências da `[GB]`
  ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4), não no `status.md`.

Sem o MCP `elm` nesta sessão ou com falha → `ELM pendente [<chave>]: <ação>` no Histórico do `status.md`
([pendências](../sdd/references/elm.md#pendências)). Depois da publicação, a `sdd-sync` traz o publicado ao bundle (e
pergunta se indexa; a busca local também indexa o que mudou, em segundo plano).

## Passo 3 — Conhecimento que dura

- **ADRs:** o Dev os escreveu no PR (`.kiro/specs/<ft>-<slug>/adr/`, uma por decisão "Vira ADR? sim" do
  `design.md`) e o Dev Sênior os julgou na revisão ou na `[APR]`. Leve cada um para a pasta de ADRs do `sdd.md`
  (próximo número da pasta, `origem FT-<nnn>`), sem reescrever o conteúdo; a cópia da pasta da fatia fica como
  registro do PR. Pasta de ADRs "não há" → ficam só na pasta da fatia.
- **Glossário:** termos que o código novo introduziu ou renomeou — e os `termo pendente` do `decisoes.md` da
  fatia — estão no glossário? Faltando ou divergente → corrija o glossário (com "ok") ou abra a correção do código
  como fatia.

O lint do conhecimento (contradições entre glossário, ADRs, bundle e steering) não é por fatia: é da
retrospectiva do épico ou da sprint (`sdd-aprender`).

## Passo 4 — Fechar

- Na **base** (já nela desde a Entrada; commit direto — várias fatias podem ir no mesmo commit de
  consolidação): `status.md` da fatia com `Fase: concluida` e data; no `backlog.md`, `status` `concluida`,
  `concluida-em` e os ids do campo ELM do `status.md` (o item e as tarefas) que a coluna `elm` ainda não tem, no
  lugar de `pendente` ou do id sem link (com o tipo antes: `REV [<id>](<url>)`); na linha da fatia no `sprint-<nn>.md` aberto, Status `concluida`, os ids que faltam na
  Tarefa ELM (`DEV <id> · REV <id>`…) e Créditos = a soma da seção **Créditos** do `status.md` da base (com as
  linhas que o Dev gravou com a `pronta`) — o `creditos` do `backlog.md` é da virada da sprint; ADRs e glossário do
  Passo 3.
- Fatia puxada: a linha dela na sprint (Observação `puxada`) e a `sprint` no backlog já vêm do `iniciar`
  (`sdd-desenvolver` Passo 4) — aqui, só a Tarefa ELM, como acima; ela conta na vazão da sprint.
- Última fatia do épico concluída (as demais `concluida`, `dividida` ou `cancelada`) → épico `concluido` no
  `backlog.md` e Fase `concluido` no `status.md` do épico, no mesmo commit, e, com ELM, o IB do épico no EWM
  concluído ([conclusão](references/elm-publicar.md#conclusão-do-ib-e-do-épico), na mesma confirmação do Passo 2; sem o MCP → `ELM pendente
  [EP-<nn> concluir]` no rodapé do PRD); sugira a retrospectiva do épico (`sdd-aprender`), com o lint do
  conhecimento. Épico `cancelado` não conclui: fica `cancelado` no `backlog.md`, na Fase e no EWM.
- **`sdd-aprender`** modo registrar para cada linha das **Lições candidatas** que o Dev gravou com a `pronta`
  (`status.md` da base): transcreva sem reclassificar — os fatos e a causa são de quem recebeu a correção — e grave
  o L-nnn na linha. Causa `—` ou `nenhuma` → nada a registrar.
- Créditos da sessão (Passo 2, *créditos*): o comentário na `[GB]` e a linha em Créditos de gestão.
- Commit (padrão do `sdd.md`, `<id> consolidar`) com `status.md`, `backlog.md`, `sprint-<nn>.md` e o que mudou.

## Passo 5 — Próximo

```
✅ FT-<nnn> concluída — <título>
ELM: <publicado (requisitos · ET · CT <ids>) | pendente: …> · Drift de negócio: <não | PRD v1.1 | ficha v2>
Créditos: <x.xx> (<n> sessões · power sdd <versões>)
Épico EP-<nn>: <c>/<t> fatias · próxima: FT-<…> (<planejada | elegivel> · <AFK|HITL>, desbloqueada agora)
Lições: <n> registradas
```

## Regras

- Não apague a pasta da fatia: ela é o registro de como a mudança foi feita (o ELM é o registro do que o sistema
  faz).
- Toda escrita no ELM só com confirmação ([regras](../sdd/references/elm.md#regras-de-toda-escrita)).
- Não escreve código: a correção que o glossário ou o drift pedirem no código vira fatia.
- Não invoque nem simule outra skill além das que os passos mandam chamar (`sdd-prd` ou `sdd-triar` no
  drift; `sdd-aprender` modo registrar): termine com o Passo 5 e pare.
