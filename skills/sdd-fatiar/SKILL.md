---
name: sdd-fatiar
description: "Quebra um PRD aprovado do fluxo sdd em fatias verticais (tracer bullets) — cada fatia atravessa todas as camadas, entrega um comportamento verificável de ponta a ponta, cita as histórias e cenários que cobre, as dependências (bloqueada por), o tamanho (P/M/G, nunca maior) e o modo de autonomia (AFK: o agente faz sozinho até o PR · HITL: precisa de uma pessoa no meio). Grava o backlog em <produto>/backlog.md, conduz o GATE do backlog e deixa as tarefas do EWM para quando as fatias entram na sprint; no refinamento, divide, junta e cancela fatias e cancela o épico. Use em \"fatiar o PRD\", \"quebrar em histórias\", \"gerar o backlog\", \"criar os itens de backlog\", \"PRD para issues\", \"refinar o backlog\", \"cancelar o EP-05\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.8"
---

# sdd-fatiar — PRD → fatias verticais

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-fatiar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Entrada: o PRD aprovado — `Fase: aprovado` no `status.md` do épico, na base (`<produto>/epicos/<EP>-<slug>/`, com o
`prd.md`; no refinamento, `fatiado`, ou `aprovado` depois de uma mudança no PRD). Saída: fatias no
`<produto>/backlog.md` (formato em [references/backlog.md](references/backlog.md)) e a ficha de cada uma (`<produto>/fatias/FT-<nnn>-<slug>.md`, formato
"padrão de épico" da [`sdd-triar`](../sdd-triar/references/ficha.md)).

Fatiar é decisão de uma pessoa (o GATE do backlog): chamada em modo autônomo (`AUTONOMO=true`, pelo loop ou por um
agente sem pessoa na conversa) → "PRD, backlog e itens de Sustentação (`AT-`, `IM-`…) nunca são AFK — fatie numa
sessão com o P.O." e pare.

## O que é uma boa fatia

- **Vertical (tracer bullet):** atravessa entrada → regra → dado → saída. "Criar a tabela", "fazer o DAO" ou
  "tela sem backend" **não** são fatias. A primeira fatia de um épico é a mais fina que prova o caminho inteiro
  (um cenário feliz, ponta a ponta); as seguintes engrossam.
- **Verificável sozinha:** tem cenários de aceite do PRD (`HF-01 · 1.1, 1.2`) que passam ao fim dela.
- **Cabe numa janela de contexto nova:** um agente pesquisa, planeja e implementa a fatia sem perder o fio, e uma
  pessoa revisa o PR numa sentada. Tamanho `P` (horas), `M` (≈ 1 dia), `G` (2–3 dias); maior que `G` → divida.
- **Nem fina demais:** doze fatias para uma mudança de três linhas é o erro mais comum. Teste de cada fatia:
  *"o que dá para demonstrar quando ela terminar?"* — se a resposta é "nada visível", junte com a vizinha.
- **Critério falsificável:** cada cenário coberto falha hoje, na base (diga a observação que mostra isso). Cenário
  que já passa não prova nada; cenário que só outra fatia consegue fazer passar está na fatia errada.
- **Preparação antes:** se a mudança exige mexer em código compartilhado, a primeira fatia deixa a mudança fácil
  (prefactoring) e a seguinte faz a mudança. Refatoração larga: expandir → migrar em lotes → contrair.
- **Independente quando der:** dependência só quando uma fatia precisa de algo que outra entrega (`bloqueada-por`).
- **Autonomia declarada:**
  - `AFK` — critérios claros, padrão conhecido no código, backpressure forte (testes e verificação automatizáveis),
    sem decisão de produto ou de UX no caminho: o agente pode ir do plano ao PR sem pessoa (a pessoa revisa o PR).
  - `HITL` — tem decisão de design, UX, integração nova, dado sensível ou risco alto: uma pessoa acompanha o plano e
    a implementação.
  - Tipo de trabalho novo no projeto começa `HITL`; vira `AFK` depois que fatias parecidas chegaram ao PR sem
    correção humana (a `sdd-aprender` mostra isso na retrospectiva).
  - O modo do fatiamento é uma **proposta** para a fatia, que ainda não tem responsável. O modo final é gravado
    quando ela ganha responsável (seleção da sprint ou encaixe, na `sdd-planejamento`), pela senioridade de quem
    implementa: Júnior → sempre `HITL`; Pleno → estes critérios; Sênior → `AFK` por padrão (`HITL` só com motivo
    forte, registrado).

## Passo 1 — Rascunho

1. Leia o PRD inteiro e o `decisoes.md`. Releia o código das fatias que mexem
   em módulos existentes (subagente `sdd-pesquisador`, se houver) — a fatia tem de ser possível no código real.
2. Monte a lista:

```
| FT | Título (comportamento, linguagem do negócio) | Cobre | Bloqueada por | Tam. | Modo |
|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas inválidas | HF-01 · 1.1, 1.2 · REG-01 | — | M | AFK |
| FT-032 | Desbloquear automaticamente após 30 min | HF-01 · 1.3 · REG-02 | FT-031 | P | AFK |
| FT-033 | Avisar o usuário do bloqueio por e-mail | HF-02 · 2.1–2.3 | FT-031 | M | HITL (texto do e-mail) |
```

3. Confira a **cobertura**: todo cenário de todas as histórias do PRD aparece em exatamente uma fatia (cenário
   compartilhado → a primeira que o entrega). Cenário sem fatia ou fatia sem cenário → corrija antes de mostrar.
4. Confira o **ponta a ponta**: ao menos uma fatia (a primeira) atravessa do gatilho do PRD (agendamento, chamada,
   tela, arquivo de entrada) até a saída que o ator observa (arquivo, resposta, tela, registro). Cobertura completa
   com fatias que só entregam peças internas (classificador, DAO, regra isolada) **não** passa: falta a fatia que
   liga as peças ao gatilho — acrescente-a (ou engrosse a primeira) antes de mostrar.

## Passo 2 — Perguntar à pessoa (uma vez, com a tabela)

```
🍰 EP-<nn> — <n> fatias · <a> AFK · <h> HITL · tamanhos <P/M/G>
<tabela>
Cobertura: <c>/<c> cenários · Ponta a ponta (tracer bullet): FT-<…> — <gatilho> → <saída observável>
- A granularidade está boa? (muito grossa / muito fina)
- As dependências estão certas?
- Alguma fatia deveria ser HITL/AFK ao contrário?
```

Ajuste e repita até "ok". Esse "ok" é o **GATE do backlog** (P.O. ou time no refinamento) — e não vale sem a
fatia ponta a ponta.

## Passo 3 — Gravar

Na **base**, pelo bloco [Gravar na base](references/backlog.md#gravar-na-base):

1. `backlog.md`: uma linha por fatia no fim de `## Fatias`, na ordem do rascunho (que respeita as dependências), com
   `origem` `EP-<nn>`, a `prioridade` do épico, `elm` (item 4) e `status` `elegivel` se passa na **Definition of
   Ready** ([references/backlog.md](references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-elegivel)) ou
   `nova` com `obs` `falta: <o quê>`. Ids `FT-<nnn>` sequenciais no projeto, **nunca reaproveitados**. O `status` do
   épico não muda (a `[ESP]` e a Especificação `concluida` são da `sdd-especificar`).
2. **Fichas** das fatias (`<produto>/fatias/FT-<nnn>-<slug>.md`, formato "padrão de épico"): Objetivo, Cobre (links
   para os cenários do PRD, sem copiar) e Como verificar; a coluna `ficha` aponta para elas.
3. `status.md` do épico: `Fase: fatiado`.
4. **EWM** (com ELM, com "sim"): um IB por fatia sob o épico, no backlog do EWM e no estado inicial ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3,
   `iteracao = backlog`); os ids vão para a coluna `elm` (`IB [<id>](<url>)`). Sem o MCP `elm` → `pendente`.
5. Commit (padrão do `sdd.md`): `backlog.md`, fichas, `status.md` do épico.

## Passo 4 — Próximos passos (na mesma resposta)

- Primeiro fatiamento do épico, ou refinamento com a linha da Especificação ainda `iniciada` → "use
  `sdd-especificar EP-<nn>`": ela conclui a `[ESP]`.
- Com ELM: os IBs das fatias já estão no backlog do EWM; entrar na sprint só muda o "Planejado para"
  ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3).
- **`sdd-planejamento`** — encaixar as fatias na sprint.
- Para começar uma fatia já: "vamos trabalhar na FT-031" (`sdd-desenvolver`, ou o hub `sdd-iniciar`).

## Refinamento (backlog já existe)

"Refinar o backlog", "a FT-033 está grande demais", "faltou uma fatia", "cancelar o EP-05" — fatia de Manutenção é da
`sdd-triar`. Cada mudança vai ao `backlog.md` e, com a fatia numa sprint, à linha dela no `sprint-<nn>.md`, no mesmo
commit, pelas [Situações](references/backlog.md#situações). Épico na Fase `aprovado` com fatias já no backlog (o PRD
mudou depois do fatiamento) → o GATE do refinamento grava `Fase: fatiado` no `status.md` do épico, no mesmo commit.
- **Dividir:** a original fica `dividida`, com `obs` `substituida-por FT-x, FT-y`; as novas entram no fim de
  `## Fatias`, `nova`, com `obs` `desmembrada de FT-<nnn>`, a `origem` e a `prioridade` dela, a cobertura repartida,
  as dependências e uma ficha cada. No EWM:
  [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3, "Fatia dividida".
- **Juntar:** só entre fatias não iniciadas (`nova`, `elegivel`, `planejada`); a absorvida fica `cancelada`, com `obs`
  `substituida-por FT-<a que fica>`, e a que fica herda a cobertura dela.
- **Cancelar** uma fatia não iniciada: `cancelada`, com o motivo na `obs`. Era a última não terminal de um épico com
  fatia `concluida` → no mesmo commit, o épico `concluido` no backlog, Fase `concluido` no `status.md` do épico e o
  IB do épico concluído (como no Passo 4 da `sdd-consolidar`).
- **No EWM**, a fatia `cancelada` (inclusive a absorvida pelo juntar) tem o IB (e, se não foi iniciada, as tarefas)
  cancelado: `elm_transicao(<id>, "cancelar")`, um por id, com "sim". Na falha (sem o MCP, `precondicao`, erro) →
  `ELM pendente [FT-<nnn> cancelar]` no rodapé da ficha da fatia, onde moram as pendências da fatia não iniciada,
  `dividida` ou `cancelada`.
- **Dividir ou cancelar depois de `iniciada`** (juntar, nunca): conclua as tarefas abertas da fatia com as horas já
  lançadas (`elm_transicao(<id>, "concluir")`, com "sim"; sem o MCP, `ELM pendente` no rodapé da ficha) e avise o Dev
  para fechar o PR.
- **Cancelar o épico** (decisão do P.O.), numa gravação: `Fase: cancelado` no `status.md` do épico (se já está na
  base); no backlog, o épico `cancelado` (motivo na `obs`) e as fatias não iniciadas `cancelada`; na sprint, a linha
  da Especificação não concluída `cancelada`; a `[ESP]` aberta conclui com as horas já lançadas, e o IB do épico
  cancela como o das fatias (na falha, `ELM pendente [EP-<nn> cancelar]`, onde moram as do épico —
  [pendências](../sdd/references/elm.md#pendências)). As fatias `iniciada` em diante não mudam aqui: mostre-as ao
  P.O. (cancelar uma iniciada é o item acima).
- **Nova fatia:** no fim de `## Fatias`, como no Passo 3 (item 1; o IB nasce no backlog do EWM pelo item 4).
- **Fatia nova com cenário novo** exige PRD alterado antes (`sdd-prd`, mudança depois de aprovado).
- **Definition of Ready** ([critérios](references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-elegivel)): a
  cada refinamento, grave `elegivel` nas `nova` que passam; a `elegivel` ou `planejada` que deixou de passar volta a
  `nova` com `falta:` — a `planejada` sai da sprint pela [Volta](references/backlog.md#situações) (no EWM, o IB e as
  tarefas voltam ao backlog, o IB no estado inicial: [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3).

## Regras

- Nunca crie fatia por camada técnica ou por papel ("especificar X", "testar X") — o trabalho de todos os papéis
  na mesma fatia é a mesma fatia.
- Nunca altere fatia `pronta` ou `concluida` (já na base). Mudança de comportamento entregue = fatia nova.
- Tamanho não é promessa de prazo: é o sinal de que a fatia cabe num PR revisável.
- Não invoque nem simule outra skill além das que os passos mandam chamar (subagente pesquisador): depois
  do GATE do backlog, diga os próximos passos (Passo 4) e pare.
