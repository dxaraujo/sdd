---
name: sdd-planejamento
description: "Planejamento ágil do projeto no fluxo sdd, ajustado a times que trabalham com agentes — roadmap e releases a partir dos épicos, acordos do time (Scrumban: duração da sprint, Definition of Ready e Done, limites de WIP incluindo a capacidade de revisão humana, que é o gargalo), planejamento da sprint como cadência — compromisso com a meta, previsão por prioridade, dependências e capacidade (vazão de fatias e lead time, especificação e reserva para Sustentação e retrabalho), fluxo puxado dentro da sprint —, acompanhamento, review com as evidências de aceite, retrospectiva com dados e virada de sprint, troca AFK → HITL e relatório de horas; publica e sincroniza a sprint com o EWM pelo MCP elm. Use em \"monta o planejamento\", \"planejar a sprint\", \"roadmap\", \"virada de sprint\", \"fechar a sprint\", \"review da sprint\", \"capacidade do time\", \"acordos do time\", \"encaixe na sprint\", \"sincroniza a sprint\", \"sincronizar com o EWM\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.7"
---

# sdd-planejamento — Planejar o fluxo, não só o calendário

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-planejamento/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Com agentes escrevendo código, o que limita a entrega é a **atenção humana**: decidir (P.O.), revisar planos e
PRs, verificar e aceitar. O planejamento do sdd mede e protege essa capacidade, trabalha com fatias pequenas e de
tamanho parecido e prevê pela **vazão** (fatias concluídas por sprint) e pelo **lead time** por fatia — sem pontos
(opcionais só no IB do EWM, para quem usa o relatório de velocidade de lá).

**A sprint é cadência, não contêiner de escopo:** o time se compromete com a **meta**; a seleção do planejamento é
uma **previsão**. Dentro da sprint o fluxo é **puxado** — terminou uma fatia, a `elegivel` do topo entra, enquanto o
WIP de revisão humana tiver folga (a `sdd-desenvolver` puxa, sem cerimônia). O Encaixe (abaixo) fica para quem
fura a fila ou estoura o WIP.
Toda hora do time cabe numa tarefa da sprint, em seis frentes: entrega `[DEV]`, revisão `[REV]`, aprovação `[APR]`
(do Dev Sênior, nos gates sem tarefa de papel: plano e PR do AFK), verificação `[VER]`, especificação `[ESP]` e
Sustentação (`[ATD]`, `[IMPL]`, `[BD]`, `[INF]`, `[OPE]`, `[EXT]` — tabela **Sustentação** do `sdd.md`; as fatias
de Manutenção, sem épico, usam as tarefas de papel, como as de épico).

Arquivos na raiz de `<produto>/` (formatos em [references/arquivos.md](references/arquivos.md)):
`equipe.json`, `acordos.md`, `roadmap.md`, `sprints/<pai>/sprint-<nn>.md` (a sprint segue a iteração pai do EWM;
chave `<pai>/Sprint <nn>`: `2026/Sprint 03`). Fatias: `<produto>/backlog.md`.

Regra de ouro: cada etapa termina com a proposta na tela e "ok" antes de gravar.

## Modo inicial — acordos e roadmap

1. **Equipe** (`equipe.json` ou `equipe.md` existe → mostre e pergunte só o que mudou): nome do projeto, data de
   início da sprint 1, pessoas (todas `ativo: true`; quem sai fica
   `false`, nunca é apagado), papéis (um ou mais por
   pessoa: `P.O.`, `Especificador`, `Dev`, `QA`, `SM`; exatamente um P.O. e um SM ativos — a mesma pessoa pode ter
   os dois —; o SM é o dono da `[GB]`), **senioridade** de quem é Dev
   (`Júnior`, `Pleno` ou `Sênior` — decide o modo das fatias da pessoa e quem revisa PR: [Modo pela
   senioridade](#modo-pela-senioridade); arquivo existente com Dev sem ela → pergunte só isso, para cada um; nenhum Dev
   Sênior ativo → avise: nenhum PR teria quem o revise), login do ELM, horas por
   semana, ausências. Pergunte também, por pessoa, quantas horas por semana vão para **revisar** (planos, PRs) e
   **verificar** — somadas em `horas-revisao-semana` —, para **especificar** (entrevista, PRD, fatiamento:
   `horas-especificacao-semana`; P.O. e Especificador) e quem faz **Sustentação** (`atende`). Grave no formato
   detectado — **só depois dos acordos (passo 2)**, que dão `duracao-sprint-semanas` (antes deles o JSON não
   valida), com `atualizado` = hoje, `historico: []` e `ausencias: []` em quem não tem; confirme que há
   **exatamente um** P.O. e **exatamente um** SM ativos — (`equipe.json` → validado contra `assets/equipe.schema.json`; `equipe.md` → valide só pela presença
   das colunas obrigatórias: Login, Papéis, Horas/semana e, para Dev, Senioridade). Se nenhum arquivo existir ainda, prefira `equipe.json`
   (padrão com validação de schema); só use `equipe.md` se o time preferir edição direta em Markdown.

   **equipe.md** (formato Markdown, alternativo): o formato é o de
   [assets/equipe-template.md](assets/equipe-template.md) (cabeçalho com duração e início; tabelas
   Pessoas — com `Ativo` —, Ausências e Histórico), que mapeia 1:1 para os campos do schema. Não valide contra
   `equipe.schema.json` neste caso — valide pela presença das colunas obrigatórias (Login, Nome, Papéis,
   Horas/semana e, para Dev, Senioridade).
2. **Acordos** (`acordos.md`) — proponha e ajuste:
   - cadência **Scrumban**: sprints de N semanas (planejamento, review, retrospectiva, virada) com fluxo puxado e
     WIP limitado dentro da sprint; pergunte só a duração (padrão 2 semanas);
   - **WIP:** uma fatia por sessão de agente; fatias esperando pessoa (`aguardando-aprovacao-plano`, `pr-aberto`,
     `em-revisao`, `em-verificacao`, `aceita`, `verificada`, `aguardando-aprovacao-pr`) ≤ capacidade de revisão
     (ex.: 2 por revisor); PR parado há mais de 1 dia → recomendar destravá-lo
     antes de começar fatia nova (seguir mesmo assim fica registrado: `WIP excedido`);
   - **Definition of Ready** e **Definition of Done** (padrão no `arquivos.md`);
   - tamanho: `P`/`M`/`G` — só para a Definition of Ready e para saber quando dividir (maior que G → dividir);
     pontos por tamanho, só se o time os quiser no EWM;
   - **reserva (Sustentação + retrabalho)** (padrão **20% das horas da sprint do time**) — cobre a
     **Sustentação** sem mudança no repositório (toda categoria: `[ATD]`, `[IMPL]`…; a Manutenção não: as fatias
     dela entram pela vazão, como as de épico) e o **retrabalho da sprint anterior** (o que falta das fatias
     migradas); e a **cadência de lançamento de horas** (padrão: ao fechar cada sessão; lançar ≠ concluir; na `[GB]`,
     só o SM lança, e o P.O. nunca — nem quando é também o SM).
3. **Roadmap** (`roadmap.md`): épicos do `backlog.md` em ordem de valor e risco (maior incerteza mais cedo),
   agrupados em releases com um objetivo cada; épico sem PRD aparece como "a descobrir" (`sdd-prd`).
4. **Base no EWM** (com o `equipe.json` gravado; antes da primeira triagem e da primeira sprint): o IB `Sustentação`
   e a tarefa `[GB] Gerenciamento do backlog` (filha dela, dono = o SM ativo), os dois com `iteracao = backlog`, pelo
   §2 do [references/elm-sprint.md](references/elm-sprint.md), com "sim" — a idempotência do §2 acha os que já existem
   (mostre os ids; só nasce o que falta). Ids na primeira linha da `## Sustentação` do `backlog.md`, pelo bloco
   [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base). Sem o MCP `elm` ou com falha → `pendente`
   na linha, no lugar de cada id (o §2 cria depois); sem o `ccm.backlog` no `pa` (`precondicao`) → peça "atualizar a
   configuração do sdd" (§0), nunca outra iteração.

## Modo sprint — planejar a próxima

0. **Senioridade:** Dev ativo sem `senioridade` no `equipe.json` (ou na coluna do `equipe.md`) → pergunte só isso,
   para cada um, e grave antes de seguir. Nenhum **Dev Sênior** ativo → avise antes de planejar: nenhum PR teria quem
   o revise (a `[REV]` é sempre de um Dev Sênior); o time decide se alguém passa a Sênior ou se a sprint segue assim,
   com as fatias HITL paradas em `pr-aberto`.
1. **Capacidade**, da `equipe.json` (horas da sprint menos ausências):
   - **revisão humana** (horas de revisão e verificação) — o limite principal;
   - **HITL**: fatias HITL consomem horas de dev acompanhando;
   - **vazão**: média de fatias concluídas nas últimas 3 sprints, incluídas as puxadas (primeira sprint: comece
     com 1 fatia por dev por semana e ajuste na virada), e o lead time médio por fatia;
   - **especificação**: horas de especificação da sprint (`horas-especificacao-semana`); zero no time inteiro e
     épico ou fatia `nova` a especificar no topo → avise antes de seguir (sem horas não há `[ESP]`: alguém ganha horas de
     especificação no `equipe.json`, ou o épico fica para depois);
   - **reserva (Sustentação + retrabalho)**: o percentual do `acordos.md` sobre as **horas da sprint do time
     inteiro** (todos os ativos, menos ausências), descontado antes de selecionar fatias. Dentro dela entram primeiro
     as **fatias migradas** da sprint anterior (horas que faltam, pela estimativa da `[DEV]` restante); o resto fica
     para a Sustentação da sprint, a começar pelos itens `aberto` com `sprint` `—` do `backlog.md` (triados sem
     sprint aberta, fora da reserva ou que saíram de uma sprint). Migradas que passam da reserva consomem a
     capacidade das fatias novas.
2. **Especificação:** épicos `elegivel` que entram em especificação nesta sprint (do `roadmap.md`, os "a
   descobrir" do topo, e os do `backlog.md` que o roadmap ainda não tem — proponha a posição deles); épico `novo`
   no topo → confira a Definition of Ready do épico e grave `elegivel` se passa, senão aponte o que falta. Um
   `[ESP]` por épico, com responsável e horas previstas dentro da capacidade de especificação. Entram aqui também
   as fatias `nova` do topo (passo 3): uma `[ESP] FT-<nnn>` por fatia, na mesma capacidade.
3. **Previsão** (não compromisso): confira a [Definition of Ready](../sdd-fatiar/references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-elegivel)
   das fatias `nova` e `elegivel` do topo e grave `elegivel` nas que passam (ou `nova`, com `obs` `falta: <o quê>`,
   nas que deixaram de passar). Entram as `elegivel` — de épico e de Manutenção — pela `prioridade` (crítica →
   baixa, `—` no fim; no empate, a ordem da linha no `backlog.md`), respeitando `bloqueada-por` — a fatia só entra
   se as dependências entram antes ou já estão `pronta` ou `concluida`. Pare ao atingir a menor das capacidades.
   Fatia `nova` no topo → aponte o que falta (decisão, PRD, fatiar) e proponha-a na Especificação (passo 2) antes
   de pular para a próxima. Cada fatia ganha
   **responsável**, e o modo final sai da senioridade dele ([Modo pela senioridade](#modo-pela-senioridade)). Cada fatia **HITL** ganha
   **revisor** — um **Dev Sênior**, pela [regra do revisor](#modo-pela-senioridade) — e **verificador** (não quem
   implementa), e a soma das revisões e verificações cabe nas horas de revisão de cada um; fatia **AFK** não tem
   (revisão e verificação por subagente, sem `[REV]`/`[VER]`) — a revisão humana dela é a leitura do PR. As
   **aprovações previstas** também consomem as horas de revisão dos Dev Sêniores: o plano de cada fatia de Júnior
   (e de Pleno que costuma pedir o GATE) e o PR de cada fatia AFK. A `[APR]` não nasce aqui — nasce no gate.
4. **Meta da sprint:** uma frase de resultado de negócio que as fatias entregam juntas, e o **nome curto** dela
   (até ~6 palavras: `Exportar o relatório de contas`), que vai no nome do plano no EWM.
5. **Iteração e número:** o **pai** é o da sprint anterior (a nova herda); pai novo só quando a pessoa diz, com o
   nome que ela der (`2026`, `Entrega 3`…); primeira sprint do projeto → pergunte o nome. A `<nn>` é a próxima
   dentro do pai (pai novo → `01`). Proponha o nome da iteração no EWM (padrão `Sprint <nn>`; é livre: a chave da
   sprint vem do número do arquivo) e o do plano
   (`<nome> - <nome curto da meta>`: `Sprint 01 - Exportar o relatório de contas`); nada é criado no EWM antes do
   "ok" — a iteração, o pai que faltar e o plano nascem na publicação (passo 7;
   [references/elm-sprint.md](references/elm-sprint.md) §1), com as datas da sprint. A iteração é o `plannedFor` de
   todos os IBs e tarefas desta sprint — os IBs que estão no backlog do EWM só mudam de iteração (§3), e a tarefa que
   ficou lá (o item saiu de uma sprint sem começar) move com o dono e a estimativa do papel dela: só nasce o papel que
   falta (elm-sprint.md, topo). A `[GB]`, que nasceu no backlog (modo inicial, passo 4), move para a primeira sprint
   do pai; pai novo → nasce a `[GB]` dele, e a antiga conclui (§2).
6. **Proposta**, com as três seções:
   ```
   🗓️ <pai>/Sprint <nn> · <início> → <fim> · iteração <pai>/<nome> · plano <nome> - <nome curto da meta> · meta: <…>
   Fatias
   | Prioridade | FT | Título | Origem | Tam. | Modo | Depende de | Responsável | Revisor | Verificador |
   Especificação
   | Item (EP ou FT) | Responsável | Horas previstas |
   Reserva (Sustentação + retrabalho): <h>h (<p>% da sprint) · retrabalho migrado <x>h · itens <AT-…> <y>h · livre <z>h
   Capacidade: revisão <h>h (usa <x>h) · especificação <h>h (usa <x>h) · vazão prevista <n> fatias · lead time médio <d> dias · HITL <h>h
   Próximas a puxar (fora da previsão, na ordem): <FT…>
   ```
7. "ok" → grave `sprints/<pai>/sprint-<nn>.md` (com `**Power sdd:**` = o `metadata.version` desta skill; as linhas
   novas nascem `planejada`, e as da Sustentação, `aberto`) e, no `backlog.md`, `status` `planejada` (no épico da
   `[ESP]`, `planejado`; a fatia da `[ESP]` segue `nova`, só a `elm` ganha `ESP <id>`), `sprint`, `responsavel` e o `modo` final, pelo bloco
   [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base), e **publique sempre no EWM** ([references/elm-sprint.md](references/elm-sprint.md) §1–4 e §6), para a sprint e o EWM ficarem iguais. Sem o MCP `elm` ou com
   falha, a coluna "Tarefa ELM" fica `pendente` e é publicada depois. O `sprint-<nn>.md` gravado antes do §1 — sem o
   MCP, com falha ou sessão parada antes da publicação; e o da próxima, no passo 4 da virada — leva no cabeçalho
   `**Publicação no EWM:** pendente`, que o §1 tira no commit da publicação. Publicada, **sincronize** (Sincronizar
   com o EWM, abaixo): as tarefas por fora entram na sprint, e os itens que os arquivos já conhecem são comparados
   (estado, iteração, dono, estimativa); o resultado é a tabela ou a linha
   `🔄 <chave> × EWM: iguais — <n> itens conferidos`. Na virada, a publicação da próxima e a sincronização dela seguem
   a ordem do §5 — o §1 da próxima antes do movimento, o §3–4 e o §6 das linhas novas depois dele e então o §9 dela
   ([Retrospectiva e virada](#retrospectiva-e-virada), passo 5).

## Modo pela senioridade

O `modo` que a triagem ou o fatiamento gravaram é a proposta para a **fatia** (critérios da `sdd-fatiar`). O modo
final sai quando a fatia ganha responsável — na seleção da sprint ou no encaixe —, pela `senioridade` de quem
implementa no `equipe.json`:

| Senioridade | Modo da fatia |
|---|---|
| `Júnior` | sempre `HITL` |
| `Pleno` | o sdd aplica os critérios da `sdd-fatiar` (inclusive "tipo de trabalho novo começa `HITL`") e propõe; a pessoa confirma |
| `Sênior` | `AFK` por padrão; `HITL` só com motivo forte da fatia — decisão de produto ou de UX no caminho, dado sensível, risco alto (diga qual) |

Modo final diferente do backlog → grave-o com `obs` `modo pela senioridade (<login>)`; o `HITL` do Sênior leva o
motivo: `modo pela senioridade (<login>): HITL — <motivo>`.

**Revisor** (fatia HITL): a `[REV]` é sempre de um **Dev Sênior** ativo — o Sênior revisa os PRs do Pleno e do
Júnior. PR de um Sênior → outro Sênior; se ele for o **único** Sênior ativo, ele mesmo, com `revisor único` na
Observação da linha da fatia no `sprint-<nn>.md`. Conte essas revisões, e as aprovações (`[APR]`), nas horas de
revisão dos Sêniores. A senioridade também decide o GATE do plano (Júnior sempre, Pleno se pedir, Sênior nunca —
`sdd-plano` Passo 5).

Fatia `iniciada` só troca de **AFK para HITL**, pela [Troca de modo](#troca-de-modo-afk--hitl);
**HITL → AFK nunca** — nem sugerido nem aceito.

## Durante a sprint

"Como está a sprint?" → **`sdd-status`** filtrado pela sprint (fase de cada fatia, bloqueios, WIP de revisão,
PRs parados). Fatia que cresceu (passou de `G` no plano) → volte para a `sdd-fatiar` (dividir) em vez de esticar.
Sustentação que estoura a reserva → o P.O. decide pelo Encaixe (abaixo); a Sustentação nunca tira fatia sozinha.

**Sincronizar com o EWM** ("sincroniza a sprint", "sincronizar com o EWM"; o painel da `sdd-status` avisa quando há
tarefa por fora, divergência ou id `a conferir`) — **leva o sdd até onde o trabalho chegou**: acabados os tokens, o
time segue no desenvolvimento tradicional (código, PR, merge, tarefas no EWM), e a sincronização põe os arquivos e o
EWM em dia ([references/elm-sprint.md](references/elm-sprint.md) §9). Fontes: o EWM (a iteração da sprint e, numa
chamada, a de backlog — `elm_listar_wi(iteracao = backlog)`), o `status.md` (base e branch, pela regra A base
prevalece, inclusive a fase), o `sprint-<nn>.md` × `backlog.md` e o git (a branch da fatia, o PR e o merge: a **rede
de proteção**, que roda dentro do §9, também sob pedido). Traz o que nasceu **por fora** — tarefa criada direto no EWM
(Sustentação, ou uma `[DEV]`/`[ESP]` aberta à mão quando a sessão do agente parou) entra na sprint com o mesmo id: o
sdd infere o que ela é e propõe o tipo e o título (renomear, só incluir o prefixo ou manter o título); a de
Sustentação sem item vira item, com o IB dele acima dela (a que tem por pai um IB ou defeito fora do `backlog.md` vai
com ele para a triagem) — e compara **o que mudou** nos itens que os arquivos já
conhecem (estado, iteração, dono, estimativa; as tarefas de papel pela fase do `status.md`; o IB do backlog fora do
estado inicial). Mostra **uma tabela**, agrupada por item, com todas as divergências e as por fora, cada linha com a
solução proposta: "ok" aplica tudo como proposto, ou a pessoa ajusta uma ou mais linhas (`<n>: arquivo`,
`<n>: EWM`, `<n>: manter`; na por fora, o tipo e o título). A situação da fatia e do épico nunca muda pelo estado do
EWM, só pela skill que a causa ou pela evidência do git (PR mergeado → `pronta`; PR aberto, branch com commits ou
`status.md` numa branch → `iniciada`, fora a branch da especificação: `status.md` em `especificando` ou `especificada`); na Sustentação, o arquivo recebe o EWM. As linhas que mudam o escopo (o item que sai
da sprint, o encaixe, o épico que entra com a `[ESP]`) esperam o "sim" do **P.O.** — sem ele, ficam `manter` nesta
rodada —, e as `encaixe` seguem depois, uma a uma, para o Encaixe (abaixo). Sprint não publicada
(`**Publicação no EWM:** pendente`) → a primeira linha cria a iteração e o plano (§1), e a listagem vem depois do
"ok". Nada diverge → sempre a linha `🔄 <chave> × EWM: iguais — <n> itens conferidos`; nunca diga que "não é preciso
sincronizar" sem ter rodado a comparação. Sem o MCP `elm` → diga que não há como comparar com o EWM; só as linhas do
git (a rede de proteção) seguem.

**Encaixe** — só quando puxar não basta: a fatia `elegivel` que alguém quer começar **não é a do topo** (fura a
fila) ou o **WIP de revisão está no limite** (de qualquer trilha); a `sdd-desenvolver` manda para cá. Item de
Sustentação com a reserva estourada é o mesmo encaixe (a `sdd-triar` manda para cá; o trazido do EWM já fica na
sprint, §9, e só se decide se uma fatia sai): a decisão do P.O. vai na linha do item na `## Sustentação` do
`sprint-<nn>.md`. A fatia fora da sprint cujo IB ou tarefas entraram na iteração da sprint pelo EWM (inclusive uma
tarefa de papel por fora) chega aqui pela sincronização (§9) como linha `encaixe`: a mesma decisão com o P.O.
(responsável, modo pela senioridade e, no HITL, revisor e verificador), com a Observação
`encaixe: trazida do EWM — <decisão> (<quem decidiu>, <data>)`, e a tarefa que já existe é a do papel inferido.
Mostre ao P.O. a fatia (trilha, tamanho, modo, origem), o que sobra da capacidade (revisão, vazão, HITL; no item de
Sustentação, a reserva, cujo usado não soma as linhas com `saiu da sprint`: o item saiu da sprint e não a consome) e
as opções, com a recomendada:
- **entra na folga** — cabe sem tirar nada;
- **entra no lugar de** `FT-…` — uma `planejada` (ainda não iniciada), que sai da sprint;
- **fica para a próxima sprint** (a trazida do EWM: o IB e as tarefas voltam ao backlog do EWM, o IB no estado
  inicial).

Com a decisão do P.O. (ou de quem ele delegou): `status` `planejada`, `sprint`, `responsavel` e o modo final pela
[senioridade](#modo-pela-senioridade) no `backlog.md` (e, na fatia HITL, revisor — Dev Sênior, pela [regra do
revisor](#modo-pela-senioridade) — e verificador, que não seja quem implementa — as `[REV]`/`[VER]` precisam deles),
uma linha `planejada` no `sprint-<nn>.md` com a Observação `encaixe: <decisão> (<quem decidiu>, <data>)` (item de
Sustentação: a `sprint` e a linha `aberto` na `### <Categoria>`, que nasce se for a primeira), pelo bloco [Gravar na
base](../sdd-fatiar/references/backlog.md#gravar-na-base), e no EWM o IB da fatia passa do backlog para a iteração da
sprint (só `iteracao`), cada tarefa que já existe (a que ficou no backlog do EWM quando a fatia saiu de uma sprint sem
começar, ou a que o EWM trouxe) move na chamada dela, com o dono e a estimativa do papel — uma por papel: com duas, a
que o EWM trouxe é a dele, e a que ficou no backlog não move e é cancelada (`elm_transicao(<id>, "cancelar")`, no
mesmo "sim"; na falha, `ELM pendente [<tipo> <id> cancelar]` no rodapé da ficha) —, e só nasce o papel que falta
([references/elm-sprint.md](references/elm-sprint.md), topo e §3–4; item de Sustentação: o IB dele muda de iteração e
a tarefa move ou nasce, §6). Na troca, a fatia que sai fica `elegivel` com `sprint` `—` no `backlog.md`, e a linha
dela no `sprint-<nn>.md` recebe Status `elegivel` e a Observação `saiu da sprint: encaixe de <FT> (<quem>, <data>)`;
o IB dela e as tarefas voltam ao backlog do EWM (`elm_atualizar_wi(ids, iteracao = backlog)`;
[references/elm-sprint.md](references/elm-sprint.md) §3), o IB no estado inicial (fora dele →
`elm_transicao(<id>, "reabrir")`: no backlog, fora de sprint, o IB fica sempre no estado inicial), e ficam lá até ela
voltar a uma sprint, quando movem. Depois, volte à `sdd-desenvolver` (Passo 3, item 4) ou à sincronização (a próxima
linha `encaixe`). Sem decisão, a fatia não começa; urgência acelera a decisão, não a dispensa.

## Troca de modo (AFK → HITL)

O plano de uma fatia AFK mostrou risco e o Dev aceitou a sugestão (`sdd-plano` Passo 5), ou o loop parou a fatia:
ela está em `bloqueada (de: planejando)` com `aguardando troca para HITL` e o motivo. A decisão é do P.O. (ou do
SM), aqui, na base:

1. Mostre a fatia, o motivo (Histórico do `status.md` da branch, por `git show origin/<branch>:…`) e a sugestão de
   **revisor** (Dev Sênior ativo, pela [regra do revisor](#modo-pela-senioridade)) e de **verificador** (não quem
   implementa), cada um o de **menor alocação** na sprint: a soma das horas estimadas das tarefas abertas de cada
   pessoa na iteração da sprint no EWM (`elm_listar_wi(iteracao, dono)`); sem ELM, a contagem
   de fatias de cada um no `sprint-<nn>.md`.
2. "ok" → `modo: HITL` na linha da fatia no `backlog.md`; no `sprint-<nn>.md`, Modo `HITL`, Revisor, Verificador e a
   Observação `modo: AFK → HITL (<quem>, <data>, <motivo>)` — pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base).
   Com o "ok", crie a `[REV]` e a `[VER]` que faltam (a que já existe move,
   [references/elm-sprint.md](references/elm-sprint.md) §7) e grave os ids na coluna "Tarefa ELM"
   (`REV <id> · VER <id>`) e no `elm` do `backlog.md`.
3. Avise o Dev: ele retoma pela `sdd-iniciar` → `sdd-desenvolver`, que sincroniza o `status.md` com a troca.

Não troca → Observação `modo: AFK mantido (<quem>, <data>)` no `sprint-<nn>.md` e avise o Dev, que retoma no AFK
(`sdd-plano` Passo 5, GATE). **HITL → AFK nunca.**

## Review

### Pré-condição dos ritos de fechamento

Antes da review, da retrospectiva da sprint e da virada — **em cada um** —, **sincronize com o EWM** (§9 do
[elm-sprint.md](references/elm-sprint.md), que já inclui a **rede de proteção**: os `status.md` das branches, o PR e
o merge de cada fatia, como a [`sdd-status`](../sdd-status/SKILL.md) (Coleta, itens 1–2), pela regra A base prevalece
do [status-template.md](../sdd-desenvolver/references/status-template.md) — a `iniciada` que ficou para trás e a
`pronta` do merge por fora são linhas `arquivo:` da tabela —, e as tarefas por fora e as divergências dos itens
conhecidos, na tabela com a solução proposta; sem tarefa por fora nem divergência, **sempre** a linha
`🔄 <chave> × EWM: iguais — <n> itens conferidos` — nunca diga que "não é preciso sincronizar" sem ter rodado a
comparação; sem o MCP `elm` → avise "sincronização com o EWM não feita" e siga, só com as linhas do git; antes da
virada, é a sincronização da virada: roda antes da migração, e o §5 não roda outra).

Depois, as fatias da sprint aberta que esperam a consolidação: Status `pronta` nas Fatias do `sprint-<nn>.md`
(inclusive as que a sincronização acabou de gravar), mais as do PR `merged` sem `pronta` (a linha `arquivo: pronta`
ficou `manter`). Nenhuma → siga o rito. Alguma → **pare** e mostre:

```
⛔ Consolidação antes do fechamento de <pai>/Sprint <nn>
| FT | Status | PR | Falta |
| FT-031 | pronta | <link> | sdd-consolidar (P.O. ou SM, agente sdd-produto) |
| FT-033 | iniciada, PR mergeado | <link> | Passo 6 da sdd-desenvolver (o Dev) ou o arquivo: pronta da sincronização, depois sdd-consolidar |
Consolide todas antes da review, da retrospectiva e da virada: só fatia consolidada conta na vazão, entra na
review e fecha no EWM. Seguir mesmo assim? (decisão do P.O.)
```

Segue só com o "sim" do **P.O.** (outra pessoa → peça a decisão a ele), gravado no cabeçalho do `sprint-<nn>.md`:
`**Fechamento sem consolidar:** FT-… (<P.O.>, <data>)`. A decisão vale para essas fatias nos ritos seguintes da
mesma sprint (não pergunte de novo); elas migram como as não concluídas, com a Observação `não consolidada`. Fatia
sem merge (`pr-aberto`, `em-revisao`…) não entra aqui: migra, como sempre.

### Rito

Abra pelo resumo da coluna Status das Fatias do `sprint-<nn>.md` — concluídas · prontas sem consolidar · iniciadas
e planejadas que migram —: é o que foi feito na sprint. Para cada fatia concluída: o cenário entregue e a
**evidência** do `verificacao.md` (resposta, contagem, screenshot). Registre o retorno do P.O. no `sprint-<nn>.md`;
pedido novo vira cenário/fatia nova pela `sdd-prd`/`sdd-fatiar` — não reabre fatia concluída.

## Retrospectiva e virada

0. **Pré-condição** — a [dos ritos de fechamento](#pré-condição-dos-ritos-de-fechamento), antes da retrospectiva
   e de novo antes da virada.
1. **Retrospectiva com dados** — `sdd-aprender` modo retrospectiva (vazão, lead time, rodadas de revisão,
   correções humanas por causa, AFK que chegaram ao PR sozinhas). Registre no `sprint-<nn>.md`: bom · melhorar ·
   ações (cada ação com dono).
2. **Horas:** relatório da sprint por tipo e por pessoa ([references/elm-sprint.md](references/elm-sprint.md) §5). Preencha "Números"
   (planejadas × lançadas) e aponte as tarefas concluídas sem horas lançadas — só aqui, no fechamento; a `[GB]` sem
   horas não é falta (só o SM lança nela, e a dona que também é P.O. não lança).
   **Créditos** (só do git, nunca do `~/.kiro`): a coluna Créditos dos Números soma as colunas Créditos das seções
   Fatias, Especificação e Sustentação (todas as `### <Categoria>`) e a seção Créditos de gestão; `**Power sdd:**`
   ganha as versões que aparecem nessas linhas e nos `status.md`/fichas dos itens concluídos, em ordem crescente;
   aponte fatia, item de Sustentação ou `[ESP]` concluída com Créditos `—` (ninguém fechou a sessão). Fatia migrada
   leva os créditos para a sprint em que for consolidada. **`backlog.md`:** a coluna `creditos` de cada fatia e item
   de Sustentação concluídos na sprint, e a do épico cuja linha na Especificação ficou `concluida` nesta sprint,
   recebe o valor da coluna Créditos dele no `sprint-<nn>.md` — só aqui, no commit da virada (bloco Gravar na base).
3. **Fechar:** concluídas — previstas e puxadas — contam na vazão e no lead time; a meta é avaliada (atingida ou
   não, e por quê). **Migram** para a próxima sprint as linhas fora de situação terminal (`concluida`, `dividida`,
   `cancelada`, `concluido`, `cancelado`) cujo item tem, no `backlog.md`, a `sprint` que fecha — fatias (inclusive
   as do `**Fechamento sem consolidar:**`, com `não consolidada`), Especificação (pela Situação da linha, não pelo
   `status` do épico: épico `iniciado` com a Especificação `concluida` não migra) e Sustentação: no `sprint-<nn>.md`
   que fecha, a linha guarda a última situação e ganha `migrada para <próxima chave>` (`2026/Sprint 04` →
   `2027/Sprint 01` na troca de pai; o histórico não é apagado), e ele fica com `**Situação:** fechada`; no da
   próxima, a linha nasce na mesma seção, com a mesma situação e `migrada de <chave>`. A linha com `saiu da sprint`
   não migra: é histórico; o item que voltou à sprint tem a linha viva, que migra se não está em situação terminal
   ([Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base), Linha viva). No `backlog.md` só muda a
   `sprint` (a próxima chave; no épico, quando a linha dele na Especificação migra), pelo bloco
   [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base).
4. Recalcule vazão média, lead time médio e horas por tipo (`equipe.json` → `historico`). Reserva (Sustentação +
   retrabalho): o % é o do `acordos.md`; mostre o consumido da sprint (horas das tarefas de Sustentação +
   retrabalho) contra ela e, se ficou muito acima ou abaixo, **proponha** um novo % ao P.O. — muda o acordo só com
   "ok". Replaneje a próxima pelo modo sprint (migradas consomem capacidade primeiro); o `sprint-<nn>.md` dela nasce
   com `**Publicação no EWM:** pendente` no cabeçalho (o §1 dela ainda não rodou; a publicação vem no passo 5).
5. **ELM** — virada ([references/elm-sprint.md](references/elm-sprint.md) §5). O §9 da sprint que fecha é o da
   pré-condição (passo 0; o §5 não roda outro). Depois, nesta ordem: o §1 da próxima, também com o mesmo pai (pai
   novo: também o §2, com a `[GB]` do pai novo); o **movimento** (os ids abertos na listagem da iteração que
   fecha — as tarefas e o item das linhas que migram, o IB de todo épico `planejado` ou `iniciado` e a `[GB]`, se o
   pai não muda — e os abertos de linha migrada que ainda estão numa sprint anterior da cadeia `migrada de`; o que
   está fechado fica na iteração em que fechou, com as horas dele); o §3–4 e o §6 das linhas novas; e só então o §9
   da próxima. **Virada pela metade** (sem o MCP, falha no movimento ou sessão parada depois do passo 4): os
   arquivos seguem; diga que o movimento fica para a sincronização da próxima, que o reconhece (§5 e §9). Iteração
   do EWM mais longa que a sprint (a mesma cobre as duas) → o movimento não muda nada (os ids já estão nela; diga
   isso), mas o §1 da próxima roda do mesmo jeito — acha a iteração e o plano, não cria nada e tira o
   `**Publicação no EWM:** pendente` —, e também o §3–4, o §6 e o §9 dela; o relatório de horas da sprint conta só
   as tarefas listadas no `sprint-<nn>.md`, não a iteração inteira.

## Regras

- Créditos do Kiro: toda sessão desta skill (planejamento, encaixe, troca de modo, ritos, virada, sincronização)
  registra os créditos no Fechar a sessão ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4): um
  comentário na `[GB]` — `elm_comentar(<id da [GB]>, "Créditos <atividade> <ids>: <créditos> (sessão <sessão>,
  <login>, <AAAA-MM-DD>)")`, ex.: `Créditos planejamento 2026/Sprint 03: 2.40 (sessão 9ec1dcaa, ana.souza,
  2026-10-29)` — e, com sprint aberta, no mesmo commit, a linha na seção **Créditos de gestão** do `sprint-<nn>.md`
  (Atividade = o modo).
- Horas de gestão: só o SM lança, na `[GB]` (`elm_lancar_horas`); o P.O. nunca lança, nem quando é também o SM.

- Nunca planeje acima da capacidade de revisão: trabalho que ninguém revisa não está entregue, só está parado.
- Fatia nunca se espalha por sprints para caber; se não cabe, divide.
- Tamanho é do time; o agente propõe P/M/G com justificativa, a pessoa decide. Nada de Planning Poker em pontos: a
  previsão é pela vazão.
- Pontos, se o time os usar no EWM, ficam só no IB (plan item), nunca nas tarefas, e não entram no planejamento.
- O compromisso da sprint é a meta: fatia prevista que não entrou não é falha; meta não atingida vai para a retro.
- Toda hora planejada tem tarefa: nada de especificação ou Sustentação fora da sprint.
