---
name: sdd-triar
description: "Entrada de todo trabalho novo no fluxo sdd — recebe um pedido em texto, um item do EWM ou um lote de itens do EWM, procura duplicados e faz a triagem: épico (várias histórias ou decisão de produto em aberto), padrão (regra de negócio clara, ficha aprovada pelo P.O.), rápida (defeito ou ajuste ≤ 1 dia sem regra nova) ou sustentação (trabalho sem mudar o repositório, numa categoria: Atendimento, Implantação, Banco de dados, Infra, Operação, Apoio a outros times). Registra no backlog.md da base — épico EP-nn, fatia com ficha (a sem épico, sob a Manutenção) ou item de Sustentação (AT-nnn, IM-nnn…) com o registro e o IB do item ([AT-nnn]; a tarefa da categoria, [ATD], [IMPL]…, nasce na sprint); EWM com confirmação — e não começa nada: indica o hub sdd-iniciar e pergunta se há mais itens. Use em \"nova demanda\", \"chegou um pedido\", \"o cliente pediu\", \"nova funcionalidade\", \"registra o defeito 4567\", \"coloca no backlog\", \"triagem\", \"aprova a ficha da FT-040\", \"importar do EWM\", \"triar os defeitos do time\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.7"
---

# sdd-triar — Triagem e registro

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-triar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Toda demanda nova entra por aqui. Triar é decidir **se** ela entra, **em que trilha** e **com que informação** —
sem começar nada. O que sai é uma linha no `backlog.md` (e, em toda fatia sem épico, a ficha; na Sustentação, o
registro do item e o IB dele no EWM), que o planejamento puxa para a sprint. Começar é pelo hub **`sdd-iniciar`**, que
encaminha o item para a skill do papel.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare. Formato do
backlog e quem escreve cada coluna: [../sdd-fatiar/references/backlog.md](../sdd-fatiar/references/backlog.md).
Ficha da fatia (toda trilha): [references/ficha.md](references/ficha.md).

## Passo 1 — O que chegou

**Antes de tudo** — a triagem lê e escreve na base: itens 1 e 5 do bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base) (troca
com "sim", `pull --ff-only`, árvore suja → pare; no fim, oferecer voltar).

**Backlog sem IB** (com ELM e o MCP `elm` nesta sessão): o backlog do EWM é a fonte dos relatórios das demandas, e
nenhum item espera a sprint para nascer nele. Linha do `backlog.md` não terminal com `elm` `—`, `pendente` ou id sem
link → `🏛️ <n> itens do backlog sem IB no EWM: <ids> → criar agora? (sim)`, com a prévia e o "sim" do
[elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §0, passo 4 (espelhamento). Os ids entram no commit
único do Passo 3. "não" → a triagem segue, e o painel da `sdd-status` continua contando.

| Entrada | Como ler |
|---|---|
| pedido em texto ("nova demanda: …", "corrigir o cálculo de juros") | a própria descrição |
| número do EWM (DF, IB) | `elm_ler_wi(id, comentarios)`; sem o MCP `elm` → peça à pessoa o título, a descrição e o comportamento esperado — nunca invente dado de work item |
| "importar do EWM", "triar os defeitos do time" | **lote** → Passo 5 |
| trabalho sem mudança no repositório — pedido de cliente ("extrai as contas bloqueadas", "por que o caso X deu Y?"), implantação, script de banco, ambiente, rotina de produção, ajuda a outro time | trilha sustentação (Passo 2) |

**Já existe?** Antes de triar, procure no `backlog.md` da base (ids, títulos parecidos e as colunas `origem`, `elm`
e `obs` — épicos, fatias e as `### <Categoria>` da `## Sustentação`), no `**Origem:**` das fichas e dos
`<produto>/sustentacao/**/*.md` e nos `status.md` das branches
(`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`). Achou → mostre a linha e:
- **fatia sem épico que volta para cá** — `nova` com `falta:`, ficha em `rascunho` ou a aprovar, mudança na
  ficha (pedida pela pessoa ou devolvida pela `sdd-plano` ou pela `sdd-consolidar`) ou trilha que não serve
  (devolvida pela `sdd-desenvolver` ou pela `sdd-especificar`) → **retome a triagem dela** (fatia com `status.md` em
  `especificando` e só a ficha a completar → é da `sdd-especificar`, na branch: diga e pare): Passo 2 com o mesmo `FT` e
  a ficha que existe; no Passo 3, só atualize a linha (sem id novo), com a situação pela Volta das
  [Situações](../sdd-fatiar/references/backlog.md#situações) — de `iniciada` em diante ela não muda: avise quem a
  conduz;
- **fatia sem épico que vira épico, se divide ou é cancelada** (decisão do P.O.) → `EP-nn` novo ou as fatias novas
  (Passo 3, `nova`, com `obs` `desmembrada de FT-…`; no EWM, o §3 "Fatia dividida" do
  [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md)) e a original, no `backlog.md` e na linha da sprint,
  `cancelada` (`obs` `substituida-por EP-nn` ou o motivo) ou `dividida` (`substituida-por FT-…`). Já `iniciada` →
  antes, conclua as tarefas abertas dela com as horas lançadas (sem o MCP, `ELM pendente`) e avise o Dev para
  fechar o PR. Cancelada → o IB (e, se não foi iniciada, as tarefas) cancela no EWM: `elm_transicao(<id>,
  "cancelar")`, um por id, com "sim"; na falha (sem o MCP, `precondicao`, erro), `ELM pendente [FT-<nnn> cancelar]`.
  As pendências da original moram no rodapé da ficha
  ([ficha.md](references/ficha.md));
- **épico `novo`** que voltou (falta de informação para o PRD, P.O. ou EWM pendentes —
  devolvido pela `sdd-prd`, pela `sdd-especificar` ou pela Definition of Ready) → **complete o registro**: o que
  falta da linha (`po`, descrição mínima, `elm`), sem id novo (passa na DoR → `elegivel`), e siga para o
  Passo 4;
- **item de Sustentação** registrado por engano, em dobro ou com o pedido retirado → `cancelado`, com o motivo, na
  linha do `backlog.md` (e na da sprint, se houver) e no `**Situação:**` do registro; o IB e a tarefa cancelam no
  EWM (`elm_transicao(<id>, "cancelar")`, com "sim"); na falha, `ELM pendente [<ID> cancelar]` no `**ELM:**` do
  registro;
- o resto → pare: começar ou retomar é pelo hub **`sdd-iniciar`**; mudar uma fatia de épico é refinamento na
  **`sdd-fatiar`**.

## Passo 2 — Triagem

| Trilha | Quando | O que se registra |
|---|---|---|
| **épico** | funcionalidade nova com várias histórias ou fatias, mais de ~3 dias, mais de um objetivo, ou decisão de produto em aberto | `EP-nn` `novo` ou `elegivel` (DoR do épico) → depois `sdd-prd` → `sdd-fatiar` |
| **padrão** | uma fatia (≤ G) que cria ou muda regra de negócio **clara** — o P.O. decide aqui —, sem decisão de produto em aberto | fatia sem épico, com **ficha** (regras, cenários, decisões) aprovada pelo P.O. |
| **rápida** | defeito ou ajuste ≤ 1 dia **sem** regra nova (o comportamento certo já está documentado ou é óbvio) — inclusive o diff que cabe numa frase (texto, configuração, ajuste trivial) | fatia sem épico, com ficha de **comportamento** (atual · esperado · não muda) e como verificar |
| **sustentação** | trabalho que não muda o repositório, numa das categorias da tabela **Sustentação** do `sdd.md` (Atendimento: consulta, extração, explicação ou conferência pedida pelo cliente; Implantação; Banco de dados; Infra; Operação; Apoio a outros times) | item da categoria (`AT-nnn`, `IM-nnn`…) na `### <Categoria>` da `## Sustentação`, com o registro, a sprint sugerida e o IB do item (a tarefa da categoria, `[ATD]`, `[IMPL]`…, nasce quando ele entra numa sprint) (a triagem registra; quem executa: **`sdd-atender`** no Atendimento, a **`sdd-executar`** nas demais) |

- Fatia de um épico não passa de novo por aqui: o épico foi triado na entrada e as fatias dele vêm da `sdd-fatiar`.
- Diga a trilha e o motivo numa linha; dúvida entre duas → sim/não pela mais leve (rápida, depois padrão, depois épico). Padrão que precisaria de mais de
  ~3 cenários de comportamentos diferentes, ou de mais de uma regra nova independente → é épico.
- **Padrão:** rodadas da `sdd-entrevistar` até as regras e os cenários fecharem, gravando na seção Decisões da
  ficha (ela nasce aqui, com o próximo `FT-nnn` de "Próximos ids"); regra nova ou alterada → [similares](../sdd-prd/references/similares.md) antes de escrevê-la; no fim, o P.O.
  aprova a ficha. Sem a aprovação, a fatia fica `nova` com `falta: aprovação do P.O.`.
- **Rápida:** **uma** rodada no formato da `sdd-entrevistar` (numerada, cada pergunta com a recomendação,
  "sim" aceita todas) para o que a ficha pede e a origem não traz: atual com evidência, esperado com fonte, o que
  não muda, como verificar.
- Fatos o agente busca (código, bundle do ELM pelas `elm_*_local`, banco só leitura); decisões são da pessoa.
- **Não fazer** (já entregue, fora do produto, recusado pelo P.O.) → nada no backlog; item do EWM → ofereça um
  comentário `sdd: não fazer — <motivo>` (`elm_comentar`, com "sim"), que o tira dos próximos lotes;
  cancelar o item é do P.O. (`elm_transicao(<id>, "cancelar")`, com "sim").

## Passo 3 — Registrar (na base)

Grava-se na base, conferida no Passo 1. Ids do EWM na coluna `elm` com o tipo antes de cada um (`IB [612010](…)`,
`DF [4567](…)` — formato do backlog).

Com ELM, **todo item triado tem o seu IB na iteração de backlog, no estado inicial** — épico, fatia, defeito ou IB de
origem e item de Sustentação (o de Sustentação que já entra na sprint vai na iteração dela). O que nasce já nasce
assim; o item de origem em outro estado volta a ele com `elm_transicao(<id>, "reabrir")`, na mesma confirmação. O IB
`Sustentação` e a `[GB]` já existem desde o modo inicial da `sdd-planejamento`
([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §2).

- **Épico:** próximo `EP-nn` de "Próximos ids"; linha em `## Épicos` com prioridade `—` (quem
  prioriza é o planejamento), `sprint` e `prd` `—` e `po` = o P.O. ativo do `equipe.json` (outro, se a pessoa disser).
  Descrição mínima (a que a [Definition of Ready](../sdd-fatiar/references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-elegivel)
  do épico confere): o problema, quem pede e o resultado esperado — falta algum → pergunte numa rodada. Completa →
  `status` `elegivel`; sem resposta, `novo` com `obs` `falta: <o quê>`. Com ELM:
  o épico nasce agora no backlog do EWM ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3, `iteracao = backlog`, com "sim"; `pa` sem
  backlog → §0 antes) e o id vai para a coluna `elm`; sem o MCP `elm` → `pendente`. Veio
  de um item do EWM: se ele já é do tipo de épico do `sdd.md`, ele é o épico (grave o id na coluna `elm` e leve-o
  para o backlog: `elm_atualizar_wi(id, iteracao = backlog)`) — quando
  esse tipo é o mesmo do item (Item de Backlog pai), pergunte se ele vira o épico ou o filho; filho (ou outro tipo)
  → `obs` `origem: <id>`, cria o épico e põe o item sob ele, no backlog (§3).

  **Pasta antecipada:** se o título tem mais de 3 palavras (slug formável), crie
  `<produto>/epicos/<EP>-<slug>/` com:
  - `rascunho.md`: o pedido original (nas palavras de quem pediu, sem dado inventado) + origem (EWM id,
    chamado, texto livre);
  - `decisoes.md`: o formato do Passo 3 da [`sdd-entrevistar`](../sdd-entrevistar/SKILL.md) (título `# Decisões — <EP-nn> <título>` e a tabela vazia);
  - `status.md`: o modelo do [Passo 3 da `sdd-especificar`](../sdd-especificar/SKILL.md#passo-3--pasta-de-trabalho-fora-do-git),
    com `Fase` `rascunho` e `[ESP]`, Responsável e Início `—` (a especificação os preenche).
  A pasta só é criada aqui; o `sdd-prd` completa com `prd.md`, `elm/` e os demais artefatos.
  Inclua o caminho relativo da pasta na coluna `pasta` do `backlog.md`:
  `[pasta](epicos/<EP>-<slug>/)` ou `—` se não criada.
- **Fatia sem épico** (padrão, rápida — a fatia de Manutenção): próximo `FT-nnn`; linha em `## Fatias` com:
  - `origem` `Manutenção`; `trilha`; `ficha` (`[ficha](fatias/FT-<nnn>-<slug>.md)`, sempre);
  - `tamanho` (padrão `P`/`M`/`G`; rápida `P`/`M`); `modo` proposto — `AFK` quando o esperado e o teste são claros
    e não há dado sensível, senão `HITL` (a fatia ainda não tem responsável: o modo final é gravado pela
    `sdd-planejamento` quando ela ganha um, pela senioridade de quem implementa — Júnior → `HITL` · Pleno → estes
    critérios · Sênior → `AFK` por padrão); prioridade, `sprint` e `responsavel` `—`;
  - `status` `elegivel` se passa na Definition of Ready da trilha (formato do backlog — a ficha da trilha completa),
    senão `nova` com `obs` `falta: <o quê>`;
  - de onde veio: o item do EWM (DF, IB) vai na `elm` como o item da fatia (`DF [4567](…)`; sem o MCP `elm`,
    `DF 4567` — o id já é conhecido, nunca `pendente`); o pedido (texto, chamado) fica no `**Origem:**` da ficha;
    desdobramento de um item de Sustentação (origem `AT-012`, `IM-003`…) → `obs`
    `vinculada a [<ID>](sustentacao/<pasta>/<ID>-<slug>.md)`.
  - **Ficha** (`<produto>/fatias/FT-<nnn>-<slug>.md`, formato da trilha em [references/ficha.md](references/ficha.md);
    crie a pasta se não existir): sempre.
  - EWM (com ELM, com "sim"), pelo §3 do [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) ("Fatia sem
    épico"; a Sustentação faltando → §2 antes): a primeira fatia de Manutenção (a linha da `## Sustentação` sem
    `Manutenção`) cria antes o IB `Manutenção`, com o id na linha. Item de origem → é o item da fatia, sem IB novo:
    `elm_atualizar_wi(origem, iteracao = backlog)`, com `pai` = a Manutenção se ele não tem pai (outro pai: mantenha e
    avise) e `dono` = o P.O. se não tem dono. Sem item de origem → o IB `[FT-nnn]` nasce agora sob a Manutenção, no
    backlog. Vinculada → `elm_ligar(wi = item da fatia, wi_destino = IB do <ID>, tipo relacionado)`. Sem o MCP
    `elm` → `pendente` (com item de origem, o id sem link).
- **Sustentação** (categorias sem mudança no repositório):
  - **Categoria:** proponha a da tabela **Sustentação** do `sdd.md` pelo pedido (consulta ou extração para o cliente →
    Atendimento; subida de versão → Implantação; script ou carga de dados → Banco de dados; ambiente, acesso →
    Infra; rotina de produção → Operação; ajuda a outra equipe → Apoio a outros times) e confirme. Muda o
    repositório → é fatia (de Manutenção): volte ao Passo 2.
  - **Entrevista curta:** Atendimento → `sdd-entrevistar` modo *atendimento* (uma rodada: o que o cliente precisa
    receber, origem, prazo, quem atende, critério de pronto). Demais categorias → sem entrevista: pergunte numa
    mensagem o pedido, a origem, o prazo, quem faz, o critério de pronto e a estimativa. Regra de negócio em aberto →
    não é item de categoria: volte ao Passo 2.
  - Próximo id da série da categoria em "Próximos ids" (`AT-`, `IM-`…; série que falta → começa em `001`).
  - **Sprint sugerida:** a aberta (`sprint-<nn>.md` com `**Situação:** aberta`), pela regra da reserva — a reserva
    (Sustentação + retrabalho) está na `## Sustentação` do `sprint-<nn>.md`; o usado é o retrabalho migrado mais a
    soma das estimativas dos itens das `### <Categoria>` dela, sem as linhas com `saiu da sprint` (o item
    saiu da sprint e não consome a reserva); cabe com a estimativa deste (A-6) → quem triou
    confirma; estourou → fica fora da sprint (`sprint` `—`), e a decisão é do P.O. pelo Encaixe da
    `sdd-planejamento` (a Sustentação não tira fatia sozinha). Sem sprint aberta → `sprint` `—` e o aviso "sem sprint
    aberta: o item entra no próximo planejamento". Responsável sugerido: quem tem `atende: true` no `equipe.json`.
  - Linha na `### <Categoria>` da `## Sustentação` (a seção nasce com o primeiro item da categoria, aberta pelo IB
    dela), com `status` `aberto`, na sprint ou fora dela; `<produto>/sustentacao/<pasta>/<ID>-<slug>.md` (`<pasta>`
    da tabela **Sustentação** do `sdd.md`) no formato da [`sdd-atender`](../sdd-atender/SKILL.md#registro), com a
    categoria e as respostas no cabeçalho (estimativa em `**Estimativa:**`) e `**Situação:** aberto`; na sprint, a
    linha na `### <Categoria>` da `## Sustentação` do `sprint-<nn>.md` (criada se faltar).
  - EWM (com ELM, com "sim"): [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §6 — o IB do item,
    `[<ID>] <pedido>` (dono = o P.O.), filho do IB da categoria; se o item já entra na sprint, na iteração dela e com
    a tarefa `<prefixo> <ID> <pedido>` (dono = quem faz); senão, só o IB, no backlog (a tarefa nasce quando o item
    entrar numa sprint). Veio de um IB ou DF do EWM → ele é o IB do item (sem IB novo), e a tarefa que já está sob ele
    (`elm_listar_wi(pai = <id>)`) é a do item, sem tarefa nova: sem pai, sob o IB da
    categoria (outro pai: mantenha e avise), e o título ganha o `[<ID>]` pelas opções do §9 (renomear · só incluir o
    prefixo · manter). Primeiro item da categoria → o IB `<Categoria>` nasce junto, na mesma confirmação, e o id dele
    abre a `### <Categoria>` (§6; §2 antes, se faltar a Sustentação). Sem o MCP `elm` → `pendente` (veio do EWM: o
    id sem link); a `sdd-atender` ou a `sdd-executar` criam o que faltar antes de assumir.

Atualize "Próximos ids". O commit é **um só, no fim da sessão de triagem** (Passo 4, resposta "não"), com o
`backlog.md` (também os ids do espelhamento do Passo 1), as fichas, as pastas dos épicos, os registros de Sustentação e, no `sprint-<nn>.md` aberto, as linhas
da Sustentação e a de créditos da sessão na seção **Créditos de gestão** (Atividade `triagem`;
([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4); sem sprint aberta, não há onde gravar) (padrão de
commit do `sdd.md`). A triagem não tem tarefa própria: o padrão é a tarefa **`[GB] Gerenciamento do backlog`** (o
`GB` da linha da `## Sustentação` do `backlog.md`): mostre-a e confirme (a pessoa pode indicar outra). Sem `GB` →
indique o modo inicial da `sdd-planejamento` (ou crie-a pelo
[elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §2, com "sim") ou pergunte a tarefa. **Créditos e
horas**, antes do commit: os créditos da sessão (item 4 do Fechar a sessão) vão também num comentário na `[GB]`,
com "sim" — `elm_comentar(<id da [GB]>, "Créditos triagem <ids>: <créditos> (sessão <sessão>, <login>,
<AAAA-MM-DD>)")`, ex.: `Créditos triagem FT-040, AT-013: 2.40 (sessão 9ec1dcaa, ana.souza, 2026-10-29)`. Horas da
triagem, só o SM lança, na `[GB]` (`elm_lancar_horas`, com "sim"); o P.O. nunca lança — nem quando também é o SM:
o registro dele é o comentário. Sem tarefa, não commite: deixe os arquivos e o comando pronto; push direto na base
com o "sim" da pessoa (no agente `sdd-produto`, que não faz push, entregue o comando pronto — a pessoa executa). **Conflito de id**
no push (outra pessoa registrou o mesmo número antes): o agente não faz merge nem rebase — peça à pessoa `git pull --rebase`; no
conflito do `backlog.md`, mantenha o remoto e, **antes de renumerar**, confira de novo de onde o item veio (DF, IB,
AT, chamado, pedido — colunas `origem`, `elm` e `obs`, `**Origem:**` da ficha ou do registro):
já está numa linha do remoto → a outra pessoa triou o mesmo item; descarte o que você registrou dele, mostre a
que existe e pare. Senão, pegue o próximo id livre para a sua linha (e para o nome
da ficha, do registro ou da pasta do épico) e, se o item já foi criado no EWM, troque o `[FT-nnn]`/`[EP-nn]`/`[<ID>]`
do título do IB, e da tarefa do item se ela já existe (`elm_atualizar_wi`, com "sim"). Id que ainda não chegou à
base pode mudar; o que já chegou, nunca.

## Passo 4 — Encaminhar

```
📥 <FT-nnn | EP-nn | AT-nnn | IM-nnn…> — <título> · trilha <…> (sustentação: · <categoria>) · <elegivel | nova: falta … | novo: falta … | aberto | aberto na sprint <pai>/Sprint <nn>> · modo <AFK | HITL>
Origem: <DF 4567 | IB 611 | AT-012 | chamado | pedido> · Ficha: <caminho | —> · EWM: <DF 4567 | criado IB <id> (· ATD <id>) | pendente | sem ELM>
Registrado. Para começar: use `sdd-iniciar <id>` (o hub encaminha para a skill do papel; a fatia e o épico fora
da sprint entram nela ao começar — `sdd-desenvolver` Passo 3, `sdd-especificar` Passo 2). Item de Sustentação fora
da sprint → use `sdd-planejamento` (Encaixe) antes.
Mais algum item para triar?
```

- **"sim"** → volte ao Passo 1 com o novo item, na mesma sessão e na base (sem novo `switch` nem `pull`).
- **"não"** → mostre o resumo da sessão (ids, trilhas, os itens espelhados no Passo 1, pendências `falta:` e `ELM
  pendente`), registre os créditos
  (o comentário na `[GB]`; as horas, só se é o SM e não é o P.O.), faça o commit único do Passo 3 e encerre; se a
  triagem trocou de branch no Passo 1, ofereça voltar à anterior.

A triagem termina aqui. **Nunca invoque nem simule outra skill** (nem `sdd-iniciar`, nem a do papel): responda com
a instrução acima e pare. Recomeçar a própria triagem com o próximo item não é invocar outra skill.

## Passo 5 — Lote do EWM

"Importar do EWM", "triar os defeitos do time" — precisa do MCP `elm` nesta sessão; sem ele → diga isso e pare.

1. **Filtro**, com padrão e uma confirmação: o `pa` (vários → pergunte qual), a iteração (padrão: o backlog do
   produto, `iteracao = backlog` — `pa` sem backlog → §0 antes; o MCP não lista sem iteração, dono ou pai), tipos
   Defeito e Item de Backlog, estado `Novo` (o nome do estado inicial na PA; a pessoa troca).
   `elm_listar_wi(iteracao, tipo, estado)`, por tipo.
2. **Fora do lote:** os itens do fluxo — pelo **id**, todo id do `backlog.md` (colunas `origem` e `elm` e as linhas
   da `## Sustentação` e das `### <Categoria>`), e pelo **título exato** `Sustentação`, `Manutenção` ou o de uma
   categoria (nunca pela palavra inicial: "Infra: certificado vencido" é demanda) —, as tarefas (as da iteração da
   sprint entram pela "sincroniza a sprint" da `sdd-planejamento`) e, depois de ler o item (item 3), o que tem pai
   do fluxo (um id do `backlog.md`) ou o comentário `sdd: não fazer`. Mais de 15 itens → mostre a contagem e peça
   um filtro mais fino.
3. Leia cada item (`elm_ler_wi(id, comentarios)`) e proponha a triagem numa tabela, com **uma
   confirmação para o lote**:
   ```
   📥 Lote EWM — <time> · <tipos> · estado <…> · <n> itens novos (<m> já no backlog)
   | Item | Tipo | Título | Trilha | Status | Motivo |
   |---|---|---|---|---|---|
   | DF 4567 | Defeito | Juros calculados em dobro no atraso | rápida | elegivel | comportamento certo na REG 2101 |
   | IB 611 | Item de Backlog | Portal de renegociação de dívidas | épico | novo | várias histórias, decisões de produto; falta: quem pede |
   | IB 613 | Item de Backlog | Limitar o desconto de pontualidade a 10% | padrão | nova | regra nova clara; falta: ficha |
   | DF 4570 | Defeito | Erro ao consultar CPF sem máscara | rápida | nova | falta: como reproduzir |
   | IB 615 | Item de Backlog | Relação de contas bloqueadas para a auditoria | sustentação · Atendimento | aberto · 2026/Sprint 03 | extração, sem mudança |
   "sim" registra tudo · ou ajuste por linha (ex.: "DF 4570: não fazer")
   ```
4. Com "sim": o Passo 3 para cada linha (o item fora do estado inicial volta a ele), com um commit para o lote e o
   EWM numa confirmação só. Padrão no lote → ficha em `rascunho` só com o Pedido e `falta: regras, cenários e aprovação do P.O.`; rápida
   sem o que a ficha da trilha pede → `nova` com `falta: <o quê>` (a entrevista é uma a uma, depois). Sustentação no
   lote → registrado como no Passo 3, sem a entrevista curta (o item do EWM é o pedido e o IB do item; prazo e
   critério de pronto ficam `—`), com a categoria, a sprint e o responsável da tabela e, se entra na sprint, a tarefa
   na mesma confirmação.
5. Saída: a tabela com os ids criados e o que ficou pendente — e **"Mais algum item para triar?"** (Passo 4).

## Regras

- Triar não começa: nunca cria branch, pasta de spec nem o `status.md` da fatia (o do épico nasce aqui, na pasta
  antecipada), e nunca assume tarefa no EWM.
- O `backlog.md` e as fichas só são escritos na base; ids nunca são reaproveitados ("Próximos ids" só cresce).
- Ficha aprovada só muda por pedido explícito: volta a `rascunho` (e a fatia, pela Volta das
  [Situações](../sdd-fatiar/references/backlog.md#situações)), mostre a diferença e peça a aprovação de novo; fatia
  `iniciada` ou adiante que dependa da mudança → avise quem a conduz.
- Nunca invente dado de work item, regra ou comportamento esperado: sem fonte e sem pessoa, fica `falta: …`.
- Toda escrita no EWM só com "sim"; sem o MCP `elm` ou com falha → `pendente` ([pendências](../sdd/references/elm.md#pendências)), e o fluxo segue.
