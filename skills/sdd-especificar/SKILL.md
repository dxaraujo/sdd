---
name: sdd-especificar
description: "Skill do papel Especificador no fluxo sdd — conduz a especificação de um épico (EP-nn) ou de uma fatia nova (FT-nnn que não passa na DoR, de épico ou de Manutenção) a partir da tarefa [ESP]: assume a [ESP] no EWM (o épico fica iniciado na base), monta a pasta de trabalho local fora do git (.kiro/local/especificacao/), encaminha pela Fase do status.md do épico (sdd-entrevistar → sdd-prd → GATE do PRD → sdd-fatiar), leva o PRD aprovado para a base, conclui a [ESP] depois do GATE do backlog e, no fim de cada sessão com o cliente, registra o levantamento na [ESP] (comentário + anexos .md com a última versão de cada artefato) e lança as horas da sessão. Outra máquina retoma baixando os anexos. Na fatia nova, a [ESP] FT-nnn: cria a branch e o status.md (fase especificando), atualiza a ficha e o status.md, encaminha o que falta (sdd-entrevistar, sdd-prd) e, na conclusão, planeja a fatia na sprint e cria a [DEV] (e a [REV] e a [VER] só no HITL, pela senioridade de quem implementa); a sdd-desenvolver começa dali. Use em \"especificar o EP-03\", \"especificar a FT-003\", \"pegar a [ESP] do EP-03\", \"retomar a especificação\", \"fechar a sessão de especificação\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.5"
---

# sdd-especificar — Especificação de épico e de fatia nova

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-especificar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

A especificação de um épico é trabalho junto ao cliente — levantamento de regras e definições — que dura várias
sessões antes do GATE do PRD. Ele fica registrado na tarefa `[ESP]` do EWM, não na base: até o GATE, a base só
recebe a situação do épico (Passo 2); o resto vai com o PRD aprovado. Esta skill é a do papel **Especificador**; o
épico chega `novo` ou `elegivel` pela `sdd-triar` e `planejado` (com a `[ESP]`) pela `sdd-planejamento`.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — O que chegou

| Entrada | Como ler |
|---|---|
| `EP-nn` ou `[ESP] EP-nn` | linha do épico em `## Épicos` do `backlog.md` da base; a `[ESP]` pela coluna `elm` (`ESP <id>`) ou pela Tarefa ELM da seção Especificação do `sprint-<nn>.md` |
| `FT-nnn` `nova` no `backlog.md`, `[ESP] FT-nnn` ou `status.md` em `especificando` | → [Fatia `nova`](#fatia-nova--a-esp-da-fatia) |
| `FT-nnn` com `status.md` em `especificada` | especificação concluída → "use `sdd-desenvolver FT-<nnn>`" e pare |
| `FT-nnn` em outra situação, `[DEV]`, `[REV]`, `[VER]`, `AT-nnn` | não é deste papel → "use `sdd-iniciar <item>`" e pare |
| pedido em texto, ou épico fora do backlog | não está registrado → "use `sdd-triar`" e pare |

**DoR do épico:** a do [`backlog.md`](../sdd-fatiar/references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-elegivel)
(o problema, quem pede, o resultado e o `po`) — `elegivel` ou adiante já passou; `novo`, confira agora. Faltando →
liste e pare: a `sdd-triar` completa o registro antes. `concluido` ou `cancelado` → nada a especificar; pare —
salvo `concluido` com a linha da Especificação ainda `iniciada`: só os itens 2–3 de "Depois do GATE do backlog"
(Passo 6), que gravam `concluida` e concluem a `[ESP]`. Épico
não planejado (`novo` ou `elegivel`, sem `[ESP]`) → ofereça a `sdd-planejamento` (seção Especificação); a pessoa
pode seguir sem tarefa — a linha dele nasce na sprint aberta (Passo 2), como a da fatia puxada, e as horas ficam
`ELM pendente`. O `elegivel` que saiu de uma sprint sem começar (a linha dele nessa sprint tem `saiu da sprint`, e o
`elm` do épico no `backlog.md` guarda o `ESP <id>`) não conta como sem `[ESP]`: a dele ficou no backlog do EWM, é a
`[ESP]` da linha e move com o IB do épico para a iteração da sprint (Passo 2).

## Passo 2 — Assumir a `[ESP]`

1. **Situação na base** — a exceção ao "nada vai à base antes do GATE do PRD" (Regras): pelo bloco
   [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base), o épico `iniciado` no `backlog.md` e a linha
   dele na seção Especificação do `sprint-<nn>.md` aberto com Situação `iniciada`; um commit, `EP-<nn> iniciar`.
   Épico não planejado → no backlog, `sprint` = a chave da sprint aberta, e a linha nasce agora (quem assume, Horas
   previstas `—`, `ESP <id>` — a que ficou no backlog do EWM — ou `pendente`, Observação `puxada`), nova mesmo se a
   sprint tem a dele com `saiu da sprint` (histórico, pela Linha viva); nenhuma sprint aberta (planejamento ainda não
   feito) → ofereça a `sdd-planejamento` e não comece (nada na base nem no EWM). Já `iniciado` (retomada) → nada a
   gravar.
2. **EWM** — `elm_transicao(id, "assumir")`, com "sim" (já minha → `ja_estava`, nada a fazer; de outra pessoa →
   `conflito`: pergunte e repita com `forcar: true`). Épico não planejado → antes, no mesmo "sim", o IB do épico vai
   para a iteração da sprint, só com `iteracao`, e a `[ESP]` que ficou no backlog do EWM (Passo 1) move com ele:
   `elm_atualizar_wi([id], iteracao = a da sprint, dono = quem assume)`, com `estimativa_h` se faltar
   ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md), topo e §3). Sem o MCP `elm` →
   `ELM pendente [<chave>]: assumir [ESP] EP-<nn>` no `rascunho.md` da pasta de trabalho.

## Passo 3 — Pasta de trabalho (fora do git)

`.kiro/local/especificacao/<EP>-<slug>/` — é ali que a `sdd-entrevistar`, a `sdd-prd` e a revisão P trabalham até
o GATE. Monte-a pela primeira fonte que existir:

1. **Já existe nesta máquina** → use-a, mas compare antes com a `[ESP]`: último comentário de sessão mais novo que
   a última sessão registrada no `rascunho.md` local (outra máquina trabalhou depois) — compare as duas em UTC (o
   EWM devolve UTC; o rascunho, hora local) e nunca pelo mtime dos arquivos, que muda a cada download → mostre as duas datas e pergunte se baixa os anexos (item 2)
   por cima da pasta local.
2. **A `[ESP]` tem anexos** (`elm_anexo(id, "listar")`) → outra pessoa ou máquina já trabalhou: baixe cada `.md`
   (`elm_anexo(id, "baixar", caminho)`) para a pasta (os de `elm/` para `elm/`, pelo prefixo `elm-` do nome do anexo). Mostre a
   data do último comentário de sessão.
3. **Só a base** → copie `rascunho.md`, `decisoes.md` e `status.md` de `<produto>/epicos/<EP>-<slug>/` em
   `origin/<base>` (`git show origin/<base>:<caminho>`, depois de `git fetch`; criados pela triagem).
   Sem essa pasta na base → crie-os: `rascunho.md` com o título e a descrição do item do EWM (sem dado inventado),
   `decisoes.md` no formato do Passo 3 da [`sdd-entrevistar`](../sdd-entrevistar/SKILL.md) (título `# Decisões — <EP-nn> <título>` e a tabela vazia)
   e o `status.md` pelo modelo abaixo.

Em qualquer das três, a pasta tem o **`status.md` do épico** — a Fase (o detalhe do épico, como o da fatia; a
situação fica no `backlog.md`), o início e os créditos de cada sessão. A triagem o cria com Fase `rascunho` e
`[ESP]`, Responsável e Início `—`, que você preenche aqui; a fonte não o trouxe → crie-o:

```markdown
# EP-<nn> — <título>

| Campo | Valor |
|---|---|
| Épico | EP-<nn> · P.O. <login> |
| Fase | rascunho |
| [ESP] | <id \| pendente> |
| Responsável | <login> |
| Início | <AAAA-MM-DD> |

<!-- Fases: rascunho → em-revisao → aprovado → fatiado → concluido · cancelado
     rascunho: triado, na entrevista e na escrita do PRD (sdd-triar, sdd-especificar) · em-revisao: PRD na revisão P
     e na mudança depois de aprovado (sdd-prd) · aprovado: GATE do PRD (sdd-prd) · fatiado: GATE do backlog
     (sdd-fatiar) · concluido: última fatia concluída (sdd-consolidar) · cancelado: decisão do P.O. (sdd-fatiar).
     Até o GATE do PRD vive na pasta de trabalho; no GATE vai à base com a pasta, e a base passa a ser a fonte. -->

## Créditos

| Data | Papel | Login | Sessão Kiro | Power sdd | Créditos |
|---|---|---|---|---|---|
```

O `rascunho.md` é o **caderno do levantamento**: o que o cliente contou, exemplos reais, dúvidas para a próxima
reunião, com a data de cada sessão. Decisões vão para o `decisoes.md` (`D-nn`), nunca só para o rascunho.

## Passo 4 — Encaminhar pela Fase do épico

```
🧭 EP-<nn> — <título> · [ESP] <id | pendente> · fase <…>
Pasta de trabalho: .kiro/local/especificacao/<EP>-<slug>/
Próximo: <skill>
```

| Fase (`status.md` do épico: o da base se a linha do épico já tem `prd`; senão, o da pasta de trabalho) | Próxima skill |
|---|---|
| `rascunho`, sem `prd.md` | **`sdd-prd`** (Passo 1: explora o código e o ELM; Passo 2: `sdd-entrevistar`) |
| `rascunho`/`em-revisao` com `prd.md` | **`sdd-prd`** no passo em que parou (escrita, revisão P ou GATE) |
| `aprovado` na pasta de trabalho (`prd` `—` no `backlog.md`) | **Passo 6** desta skill — levar para a base |
| `aprovado` na base | **`sdd-fatiar`**; depois do GATE do backlog, volte aqui (Passo 6) |
| `fatiado`, Especificação ainda `iniciada` na sprint | **Passo 6** desta skill — concluir a `[ESP]` |
| `fatiado`, Especificação `concluida` | nada a especificar; refinamento de fatia → `sdd-fatiar` |

## Passo 5 — Fechar a sessão (toda sessão, antes de parar)

Pergunta única, com prévia do que vai:

```
📝 Sessão de especificação — EP-<nn> · <data>
Comentário na [ESP] <id>: <resumo do levantamento · decisões D-nn novas · dúvidas para a próxima reunião>
Anexos (última versão, substituem os anteriores): rascunho.md · decisoes.md · status.md · prd.md · elm-<arquivo>.md …
Horas desta sessão na [ESP]: <h> h em <data>   (pergunte à pessoa; nunca estime por ela)
Créditos desta sessão: <x.xx> (sessão <id>) · power sdd <versão>   (script da sdd-status, item 4)
Registrar? (sim)
```

Com "sim": primeiro a linha de créditos no `status.md` do épico ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4) — depois do GATE do PRD, no da
base, no commit que o fatiamento já faz —; então `elm_comentar` (o resumo), `elm_anexo(id, "enviar", caminho)` para cada `.md` da pasta de trabalho (os de
`elm/` com o prefixo `elm-`, para não colidir com o nome de outro arquivo) e `elm_lancar_horas(id, horas)` (lança;
não conclui). Sem o MCP `elm` ou com falha → `ELM pendente [<chave>]: registrar sessão [ESP] EP-<nn> (<data>)` no `rascunho.md`, e o
próximo fechamento registra.

## Passo 6 — Fechamentos da `[ESP]` (depois de cada GATE)

A `sdd-prd` e a `sdd-fatiar` conduzem o GATE e gravam só o próprio artefato; o que é da `[ESP]` é daqui.

**Depois do GATE do PRD** (Fase `aprovado` no `status.md` da pasta de trabalho, gravada pela `sdd-prd`):
1. Feche a sessão (Passo 5), para a `[ESP]` ter a versão aprovada.
2. Leve a pasta para a **base**, pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base):
   copie-a para `<produto>/epicos/<EP>-<slug>/` (substitui o `rascunho.md`, o `decisoes.md` e o `status.md` da
   triagem), com o `revisao-prd-<N>.md`; no `backlog.md`, só o link `prd` na linha do épico e, se estava `—`, o da
   `pasta` (ele segue `iniciado`; a sprint não muda). **Um** commit (padrão do `sdd.md`), direto na base; nunca numa
   branch de fatia. A partir daí a base é a fonte; a pasta local pode ser apagada pela pessoa (a skill não apaga).
3. Próximo, e pare: a [publicação dos requisitos](../sdd-consolidar/references/elm-publicar.md) (se o projeto usa ELM e
   a publicação é `na-aprovacao`) e **`sdd-fatiar`**.

**Depois do GATE do backlog** (Fase `fatiado` no `status.md` do épico na base, `[ESP]` aberta):
1. Pergunte se a especificação terminou. Continua (refinamento na próxima sprint) → não conclua: a linha segue
   `iniciada`, a virada a migra e, no EWM, só muda o `plannedFor`; pare.
2. No `sprint-<nn>.md` aberto, a linha do épico na seção Especificação com Situação `concluida` e os Créditos (a
   soma da seção Créditos do `status.md` do épico; o `creditos` do `backlog.md` é da virada da sprint), pelo bloco
   Gravar na base, um commit. O épico segue `iniciado` no `backlog.md`, com as fatias.
3. **Conclusão da `[ESP]`** (com ELM): mostre as horas já lançadas (`elm_horas(id)`) e pergunte só o saldo a quem especificou →
   `elm_lancar_horas(id, horas)` e `elm_transicao(id, "concluir")`, numa confirmação. Sem o MCP `elm` → `ELM pendente [<chave>]: lançar
   <h>h e concluir [ESP] EP-<nn>` no rodapé do PRD (no mesmo commit).

Situação da linha do épico na seção Especificação ([situações](../sdd-fatiar/references/backlog.md#situações)):
`planejada` (`sdd-planejamento`), `iniciada` (Passo 2) e `concluida` (GATE do backlog), estas duas gravadas aqui;
`cancelada` com o épico cancelado (`sdd-fatiar`).

## Fatia `nova` — a `[ESP]` da fatia

A fatia que não passa na DoR (`nova`, `obs` `falta: …`), de épico ou de Manutenção, é especificada na **branch
dela**: aqui nascem a branch, a pasta `.kiro/specs/<ft>-<slug>/` e o `status.md` (Fase `especificando`), e a
`sdd-desenvolver` começa dali. A `[ESP] FT-<nnn> Especificação` (filha do item da fatia,
[elm.md](../sdd/references/elm.md)) registra as sessões; esta skill atualiza o `status.md` e a ficha.

1. **Assumir** (só com a fatia na seção Especificação do `sprint-<nn>.md` aberto, ou puxada para ela):
   1. **Base**, pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base): a linha da fatia na
      Especificação com Situação `iniciada` (sem linha → nasce agora: quem assume, Horas previstas `—`, `ESP <id>` ou
      `pendente`, Observação `puxada`); no `backlog.md` a fatia segue `nova` (a `elm` ganha `ESP <id>`, se faltava).
      Commit `FT-<nnn> iniciar especificação`. Nenhuma sprint aberta → ofereça a `sdd-planejamento` e não comece.
   2. **EWM**: `elm_transicao(id, "assumir")`, com "sim". Sem `[ESP]` → ofereça a `sdd-planejamento` (seção
      Especificação); a pessoa pode seguir sem tarefa, com `ELM pendente [<chave>]: [ESP] FT-<nnn>` no Histórico.
   3. **Branch**, como o Passo 4, item 3, da [`sdd-desenvolver`](../sdd-desenvolver/SKILL.md) (sugira o nome e
      aguarde; `git fetch` e `git switch -c <branch> origin/<base>`, com o registro do item 1 já publicado).
   4. **Pasta** `.kiro/specs/<ft>-<slug>/` com o `status.md` do
      [status-template.md](../sdd-desenvolver/references/status-template.md): Fase `especificando`, Responsável =
      quem especifica, Modo o do `backlog.md`, ELM `ESP <id>` (e o item da fatia), Histórico
      `<AAAA-MM-DD HH:MM> — especificação iniciada (sdd-especificar)`. Commit e push da branch (no agente
      `sdd-produto`, que não faz push, entregue o comando pronto).

   Já `especificando` (retomada) → troque para a branch (Passo 1 da `sdd-desenvolver`: worktree, alterações locais)
   e siga do item 2.
2. **Encaminhar pelo `falta:`** da linha (confira a DoR da trilha de novo: pode já ter mudado):
   ```
   🧭 FT-<nnn> — <título> · [ESP] <id | pendente> · fase especificando · falta: <…>
   Branch: <…> · Pasta: .kiro/specs/<ft>-<slug>/
   Próximo: <esta skill | skill>
   ```
   | Falta | Quem faz |
   |---|---|
   | ficha (incompleta, em rascunho, como verificar) | **esta skill**, na branch: a ficha no formato da trilha ([ficha.md](../sdd-triar/references/ficha.md)), sem dado inventado; Manutenção → a aprovação do P.O. registrada na ficha |
   | decisão em aberto | **`sdd-entrevistar`** (Manutenção: seção Decisões da ficha; de épico: `.kiro/specs/<ft>-<slug>/decisoes.md`) |
   | regra do PRD (de épico) | **`sdd-prd`** (mudança do PRD, na base) |
   | trilha que não serve, vira épico, dividir | **`sdd-triar`** (Manutenção) · **`sdd-fatiar`** (de épico) |

   Artefatos que vão ao ELM (requisitos, casos de teste) ficam em `.kiro/specs/<ft>-<slug>/elm/`. A skill chamada não
   toca na `[ESP]` nem no `status.md`: terminada a sessão dela, volte aqui.
3. **Fechar a sessão** — como o Passo 5, sem anexos (os artefatos estão na branch): a linha de créditos na seção
   Créditos do `status.md` (Papel `especificação`), comentário na `[ESP]` (resumo, decisões novas, dúvidas) e as
   horas da sessão (pergunte; nunca estime), numa confirmação; commit e push da branch.
4. **Concluir** — a fatia passa na DoR da trilha; antes, feche a sessão (item 3), para os créditos fecharem a soma:
   1. **Quem implementa** — pergunte (sugira pelo `equipe.json`). O modo sai da senioridade dele
      ([Modo pela senioridade](../sdd-planejamento/SKILL.md#modo-pela-senioridade) da `sdd-planejamento`); `HITL` →
      o revisor (Dev Sênior, pela mesma regra) e o verificador (não quem implementa).
   2. **EWM**, numa confirmação: a `[ESP]` com o saldo de horas (`elm_horas(id)` → `elm_lancar_horas`) e
      `elm_transicao(id, "concluir")`; as tarefas pelo §4 do [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md)
      — a `[DEV]` (dono = quem implementa; a estimativa, pergunte) e, só no `HITL`, a `[REV]` e a `[VER]` (revisor e
      verificador). Sem o MCP → `ELM pendente` no Histórico do `status.md`.
   3. **Base** (Gravar na base): no `backlog.md`, `status` `planejada`, `sprint` (a aberta), `responsavel`, `modo`
      (diferente do registrado → `obs` `modo pela senioridade (<login>)`) e a `obs` sem o `falta:`; no
      `sprint-<nn>.md`, a linha da Especificação `concluida` com os Créditos (a soma das linhas `especificação` do
      `status.md`) e a linha da fatia nasce nas Fatias, `planejada`, com responsável, revisor e verificador (AFK:
      `—`), Tarefa ELM (os ids do item 2, ou `pendente`) e a Observação `especificada na sprint`. Commit `FT-<nnn> concluir especificação`.
   4. **`status.md`**, na branch: Fase `especificada`, Responsável = quem implementa, Modo, ELM com os ids
      (`ESP <id> · DEV <id> · REV <id> · VER <id>`), Histórico `especificação concluída · modo <…> · dev <login>`;
      commit e push.
   5. Próximo, e pare: `sdd-desenvolver FT-<nnn>` (agente `sdd-codificador`).

## Regras

- Fatia `nova`: o trabalho (ficha, decisões, `elm/`, `status.md`) mora na branch dela e chega à base com o merge; a
  base só recebe a situação, ao assumir e ao concluir.
- Até o GATE do PRD, nada da especificação vai para a base — só a situação do Passo 2: o registro é a `[ESP]`
  (comentários e anexos), atualizado ao fechar cada sessão.
- Nunca invente regra, valor ou ator: sem fonte e sem decisão de uma pessoa, é `em aberto`.
- Dado de cliente identificável não vai para os anexos: no rascunho, só o resumo anônimo.
- Toda escrita no EWM só com "sim"; sem o MCP `elm`, `ELM pendente` ([pendências](../sdd/references/elm.md#pendências)), e o fluxo segue.
- Não invoque outra skill por conta própria: diga a próxima e pare.
