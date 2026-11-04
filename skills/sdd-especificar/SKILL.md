---
name: sdd-especificar
description: "Skill do papel Especificador no fluxo sdd — conduz a especificação de um épico (EP-nn) a partir da tarefa [ESP]: assume a [ESP] no EWM (o épico fica iniciado na base), monta a pasta de trabalho local fora do git (.kiro/local/especificacao/), encaminha pela Fase do status.md do épico (sdd-entrevistar → sdd-prd → GATE do PRD → sdd-fatiar), leva o PRD aprovado para a base, conclui a [ESP] depois do GATE do backlog e, no fim de cada sessão com o cliente, registra o levantamento na [ESP] (comentário + anexos .md com a última versão de cada artefato) e lança as horas da sessão. Outra máquina retoma baixando os anexos. Use em \"especificar o EP-03\", \"pegar a [ESP] do EP-03\", \"retomar a especificação\", \"fechar a sessão de especificação\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.0"
---

# sdd-especificar — Especificação de épico

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
| `FT-nnn`, `[DEV]`, `[REV]`, `[VER]`, `AT-nnn` | não é deste papel → "use `sdd-iniciar <item>`" e pare |
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

## Regras

- Até o GATE do PRD, nada da especificação vai para a base — só a situação do Passo 2: o registro é a `[ESP]`
  (comentários e anexos), atualizado ao fechar cada sessão.
- Nunca invente regra, valor ou ator: sem fonte e sem decisão de uma pessoa, é `em aberto`.
- Dado de cliente identificável não vai para os anexos: no rascunho, só o resumo anônimo.
- Toda escrita no EWM só com "sim"; sem o MCP `elm`, `ELM pendente` ([pendências](../sdd/references/elm.md#pendências)), e o fluxo segue.
- Não invoque outra skill por conta própria: diga a próxima e pare.
