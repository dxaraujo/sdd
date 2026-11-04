---
name: sdd
description: "Guia do fluxo sdd — engenharia agêntica orientada a especificação, com o IBM ELM como fonte oficial da documentação e planejamento ágil Scrumban: trilhas por tamanho (rápida, padrão, épico) e de sustentação (Atendimento, Implantação, Banco de dados, Infra, Operação, Apoio a outros times), fases, gates humanos, artefatos e onde moram, agentes, princípios e qual skill usar para cada pedido. Use para entender ou explicar o fluxo, decidir o próximo passo quando nenhuma outra skill sdd se encaixa, e em \"como funciona o sdd\", \"qual o fluxo\", \"o que eu faço agora com isso\", \"sdd\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.5"
---

# sdd — Engenharia agêntica orientada a especificação

O agente escreve muito código rápido; o que limita o resultado é o **alinhamento** antes e a **verificação**
depois. O sdd põe as pessoas onde elas têm mais alavanca — decidir o quê, aprovar o como, ler o código — e
deixa o resto com agentes de contexto limpo, presos a feedback automático. O IBM ELM é o registro oficial do que
o sistema faz; o repositório guarda como cada mudança foi feita.

Configuração do projeto: `.kiro/steering/sdd.md` (gerado pela **`sdd-setup`**). Sem ele, comece por
"configurar o sdd".

## Trilhas (o tamanho decide a cerimônia)

Toda demanda nova entra pela **`sdd-triar`**: ela decide a trilha e registra o trabalho no backlog — inclusive a
Sustentação —, sem começar, e pergunta se há mais algum item. O hub **`sdd-iniciar`** recebe um item registrado e
diz a skill do papel; cada skill de papel assume a própria tarefa no EWM (`elm_transicao`) e pode ser
chamada direto:

| Papel | Tarefa | Skill |
|---|---|---|
| Especificador | `[ESP]` | `sdd-especificar` (épico: entrevista → PRD → fatias; fatia `nova`: até a DoR) |
| Dev | `[DEV]` | `sdd-desenvolver` (compromisso, `iniciada` na base, branch) → pesquisar → plano → implementar → PR → merge (`pronta` na base; a fatia é dele de ponta a ponta) |
| Revisor (Dev Sênior) | `[REV]` | `sdd-revisar` |
| Aprovador (Dev Sênior) | `[APR]` — só nos gates sem tarefa de papel; nasce quando a fatia chega ao gate | `[APR] … Aprovar plano` → `sdd-revisar` (Aprovação do plano) · `[APR] … Aprovar PR` (AFK) → `sdd-revisar` (Aprovação do PR) |
| Verificador (QA) | `[VER]` | `sdd-verificar` |
| quem atende | `[ATD]` (Sustentação — Atendimento) | `sdd-atender` |
| quem faz o item de Sustentação | `[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]` (demais categorias) | `sdd-executar` (assumir no ELM, registrar o trabalho, lançar horas, concluir) |
| P.O. ou SM (analista de negócio) | `[GB] Gerenciamento do backlog` (do SM; o P.O. nunca lança horas: os créditos de toda sessão vão num comentário na `[GB]`) | `sdd-triar` (triagem) · `sdd-consolidar` (fatia `pronta`: processo de produto, no agente `sdd-produto`) · `sdd-planejamento` (sprint, ritos e sincronização) |

| Trilha | Quando | Caminho |
|---|---|---|
| **rápida** | defeito ou ajuste ≤ 1 dia, comportamento certo já conhecido — inclusive o diff que cabe numa frase | `bugfix.md` + `tasks.md` → implementação → PR → revisão → verificação → consolidação (AFK: revisão e verificação antes do PR) |
| **padrão** | uma fatia do backlog: de um épico, ou sem épico (Manutenção) com regra clara e ficha aprovada pelo P.O. | pesquisa → plano → **GATE do plano** → implementação (TDD) → PR → revisão → verificação → consolidação (AFK: revisão e verificação antes do PR) |
| **épico** | funcionalidade com várias histórias ou decisão de produto em aberto | entrevista → PRD → **GATE do PRD** → ELM → fatias → **GATE do backlog** → planejamento → cada fatia na trilha padrão |
| **sustentação** | trabalho que não muda o repositório, numa categoria da tabela **Sustentação** do `sdd.md` — Atendimento (o cliente pede consulta, extração ou explicação), Implantação, Banco de dados, Infra, Operação, Apoio a outros times. Mudança no repositório sem épico é fatia (rápida ou padrão) da Manutenção | triagem: categoria e entrevista curta → item da categoria (`AT-nnn`, `IM-nnn`…) no backlog e o IB dele no EWM (`[AT-nnn] <pedido>`), filho do IB da categoria (nasce com o 1º item dela, filho da `Sustentação`); a tarefa (`[ATD]`, `[IMPL]`…) nasce quando o item entra numa sprint · Atendimento: `sdd-atender` (assume → banco só leitura e bundle → resposta com "ok" → saldo de horas → desdobramentos) · demais: `sdd-executar` (assumir → registrar → horas → concluir) |

Toda hora trabalhada cabe numa tarefa da sprint: `[ESP]` (especificação do épico ou da fatia `nova`), `[DEV]`, `[REV]`, `[VER]` (por
fatia; no AFK só a `[DEV]`), `[APR]` (por gate com aprovação: plano, PR do AFK), as de Sustentação (`[ATD]`,
`[IMPL]`… — uma por item, filha do IB dele) e `[GB]` (triagem, consolidação, planejamento e sincronização; horas só
do SM; os créditos de toda sessão do P.O. ou do SM vão num comentário nela — [elm.md](references/elm.md)). **Lançar ≠
concluir:** lançar horas é registro de empenho, a qualquer momento numa tarefa assumida (inclusive antes de um
GATE); concluir é da skill do papel quando o trabalho dela termina, perguntando só o saldo —
`[DEV]` no merge, `[REV]` ao aprovar (depois do push), `[VER]` ao aceitar (depois do push), `[APR]` na aprovação,
`[ESP]` no GATE do backlog (da fatia: quando ela fica `elegivel`), Sustentação ao finalizar (com o IB do item). **Entrega** (todo papel do HITL):
commit → push → conferir no remoto (`git rev-parse HEAD` = `git rev-parse origin/<branch>`) → só então lançar horas
ou concluir a tarefa e avisar o próximo — quem vem depois só acha no remoto o que foi publicado.

```
ENTRADA       triar ─► backlog: EP novo · FT sem épico (padrão ou rápida, cada uma com a sua ficha) · Sustentação (AT-/IM-… + IB) ─► "mais algum?"
                │
HUB           iniciar <item> ─► especificar · desenvolver · revisar ([REV], [APR]) · verificar · atender · executar · planejamento (troca) · consolidar   (cada uma assume a sua tarefa)
                │
PRODUTO       especificar ─► entrevistar ─► PRD ─► GATE PRD ─► ELM (HF/REG/GL) ─► fatiar ─► GATE backlog ─► sprint (EWM)
                                                                                    │
FATIA         desenvolver (iniciada na base) ─► pesquisar ─► plano ─► GATE plano ─► implementar (TDD) ─► PR ─► revisar ─► verificar   (AFK: revisão e verificação antes do PR)
                                                                                                                            │
DEPOIS        merge (Dev, PR aprovado; remove a worktree do loop) ─► pronta na base
                │
PRODUTO       consolidar (P.O./SM, [GB]): drift marcado pela REV/VER ─► ELM as-built (ET, CTs) ─► ADRs do PR ─► concluida ─► aprender
```

**Scrumban:** a sprint é a cadência de inspeção (meta, review, retrospectiva, virada), não escopo congelado. O
compromisso é a meta; a seleção é previsão, e dentro da sprint o fluxo é puxado, com WIP limitado (a `elegivel` do
topo entra quando o WIP de revisão tem folga). Previsão pela vazão e pelo lead time, sem pontos.

## Gates — sempre de uma pessoa

| Gate | Quem | O que se aprova |
|---|---|---|
| PRD | P.O. | o quê e o porquê: histórias, cenários, regras, fora de escopo |
| Backlog | P.O. + time | as fatias: granularidade, dependências, AFK/HITL |
| Ficha | P.O. | a fatia padrão sem épico: regras e cenários |
| Plano | um Dev Sênior, na `[APR] Aprovar plano` (de preferência quem vai revisar o PR), com a fatia em `aguardando-aprovacao-plano` | a forma do programa e o contrato de pronto — maior alavanca |
| PR | HITL: revisor (`[REV]`) e verificador (`[VER]`) · AFK: um Dev Sênior, na `[APR] Aprovar PR`, com a fatia em `aguardando-aprovacao-pr` | o código, lido de verdade, com a evidência de aceite; aprovado, o merge é do Dev responsável |

GATE do plano pela **senioridade** de quem implementa (trilha e modo não entram): **Júnior** → sempre; **Pleno** → o
fluxo pergunta se ele quer a aprovação de um Dev Sênior (no loop, a escolha vale para o lote); **Sênior** → nunca: ele
aprova o próprio plano, inclusive quando muda a expectativa de um teste existente. Aprovação só vale na sessão de quem
aprova (é ela que assume, lança e conclui a `[APR]`). PRD e backlog nunca são AFK. O PR e o merge nunca são
dispensados.

## Modos — o `modo` da fatia vale para todos os papéis

| | **HITL** — pessoas nos papéis, subfluxos assíncronos | **AFK** — a IA coordena, um fluxo só |
|---|---|---|
| Quem roda | cada pessoa, a skill do seu papel | `sdd-loop` (`sdd-orquestrador` + subagentes) |
| Codificador (Dev) | revisão automática (rubrica C, subagente) → PR, com a `[DEV]` em andamento → merge depois da REV e da VER → `pronta` na base e `[DEV]` concluída | o loop leva a fatia até o PR (`aguardando-aprovacao-pr`); quem disparou o loop faz o merge do PR aprovado, grava `pronta` na base e conclui a `[DEV]` |
| Revisão | o revisor assume a `[REV]` e revisa o PR: aprova → VER; reprova → retrabalho | subagente, até 2 rodadas |
| Verificação | o verificador assume a `[VER]` (só depois da REV): aceita → fase `aceita` (o Dev mergeia → `pronta` na base; `concluida` na consolidação); rejeita → retrabalho | subagente: aceita → `verificada`, e o PR abre em `aguardando-aprovacao-pr` |
| Retrabalho | a `[DEV]`, ainda em andamento, recebe a correção no mesmo PR, que passa de novo pela REV | volta à implementação |
| Tarefas no EWM | `[DEV]` `[REV]` `[VER]`, cada uma da sua pessoa; `[APR]` do plano, se houver GATE | a `[DEV]`, de quem disparou; as `[APR]` (plano com GATE, PR) do Dev Sênior que aprova |

O modo final sai da **senioridade** de quem implementa (o `responsavel` da fatia, no `equipe.json`), gravado pela
`sdd-planejamento` quando a fatia ganha responsável; antes disso, o `modo` da triagem ou do fatiamento é proposta:

| Senioridade | Modo |
|---|---|
| Júnior | sempre HITL (não começa fatia AFK nem dispara o `sdd-loop`) |
| Pleno | os critérios da fatia (`sdd-fatiar`), propostos pelo sdd e confirmados pela pessoa |
| Sênior | AFK por padrão; HITL só com motivo forte, registrado |

A `[REV]` e a `[APR]` são sempre de um **Dev Sênior**: ele revisa os PRs do Pleno e do Júnior; o PR de um Sênior,
outro Sênior — se ele é o único Sênior ativo, ele mesmo (`revisor único` na Observação do `sprint-<nn>.md`).

**Troca AFK → HITL** (nunca o contrário): o plano de uma fatia AFK mostra risco (regra sensível, muitos cenários,
integração externa, mudança de dado) → o fluxo sugere HITL ao Dev; aceita, a fatia para em `bloqueada` com
`aguardando troca para HITL` e o P.O. (ou SM) troca na `sdd-planejamento` (modo no backlog, revisor e verificador de
menor alocação, `[REV]` e `[VER]` no EWM); o Dev retoma pela `sdd-desenvolver`, que só sincroniza o `status.md`. No
loop, a fatia para sozinha e o lote segue.

## Princípios

1. **Alinhar antes de escrever** — entrevista em rodadas, com recomendação; fatos o agente busca, decisões a pessoa toma.
2. **Cerimônia do tamanho do trabalho** — nada de 16 critérios para um ajuste de uma linha.
3. **Fatias verticais** que cabem numa janela de contexto nova e provam algo demonstrável.
4. **Verificação acima de geração** — teste primeiro, backpressure (compilar, testes, lint) a cada passo, aceite
   com evidência, oráculo protegido (teste não se apaga nem se afrouxa).
5. **Gerador ≠ avaliador** — revisão e verificação em contexto limpo, em eixos separados (spec × padrões).
6. **Contexto limpo e estado em disco** — uma fatia por sessão; `status.md`, `research.md` e o plano carregam o fio.
7. **Autonomia gradual** — HITL até o tipo de trabalho provar que anda sozinho; AFK limitado pela capacidade de
   revisão humana.
8. **Documentação ancorada no ELM** — PRD e plano são registros de decisão descartáveis; o ELM, o glossário e os
   ADRs são o que dura; a consolidação (processo de produto) fecha o drift.
9. **Aprendizado composto** — cada correção humana muda o ambiente (checagem, regra, skill, glossário), não só o código.
10. **Leia o código** — PRs pequenos, com caminho de leitura e evidência; nada é mergeado sem uma pessoa.

## O que dizer

| Quero… | Skill |
|---|---|
| configurar o fluxo, os agentes e os toolkits no projeto | `sdd-setup` |
| saber onde parei / o que fazer agora · fechar a sessão | `sdd-status` |
| registrar qualquer demanda nova — pedido, defeito, ajuste, pedido de cliente, item ou lote do EWM (triagem) | `sdd-triar` |
| começar um item registrado, ou "minha próxima tarefa" (o hub diz a skill do papel) | `sdd-iniciar` |
| especificar um épico ou uma fatia `nova` (`[ESP]`) e registrar cada sessão com o cliente na tarefa | `sdd-especificar` |
| começar ou retomar o código de uma fatia (`[DEV]`), mergear o PR aprovado | `sdd-desenvolver` |
| alinhar decisões | `sdd-entrevistar` |
| escrever o PRD de um épico | `sdd-prd` |
| quebrar o PRD em fatias / refinar o backlog | `sdd-fatiar` |
| planejar sprint, roadmap, virada, review | `sdd-planejamento` |
| levar o sdd até onde o trabalho chegou por fora — tarefas no EWM, divergências das conhecidas, PR e merge ("sincroniza a sprint") | `sdd-planejamento` |
| executar um atendimento já triado (`AT-nnn`, `[ATD]`) | `sdd-atender` |
| assumir, registrar, lançar horas e concluir outro item de Sustentação (`[IMPL]`, `[BD]`, `[INF]`, `[OPE]`, `[EXT]`) | `sdd-executar` |
| lançar horas ou ver o relatório de horas | `sdd-status` (fechar a sessão) · Sustentação: `sdd-atender` ou `sdd-executar` · relatório: `sdd-planejamento` |
| entender o código antes de planejar | `sdd-pesquisar` |
| planejar uma fatia (spec do Kiro) | `sdd-plano` |
| implementar e abrir o PR | `sdd-implementar` |
| revisar PRD, plano ou código | `sdd-revisar` |
| verificar o aceite de ponta a ponta | `sdd-verificar` |
| fechar a fatia depois do merge (P.O. ou SM, agente `sdd-produto`) | `sdd-consolidar` |
| publicar no ELM (DOORS Next, EWM, ETM) | a skill do passo ([references/elm.md](references/elm.md)) · bundle: `sdd-sync` |
| levar várias fatias AFK até o PR | `sdd-loop` (com o agente `sdd-orquestrador`) |
| rodar uma receita de workflow numa fatia | você, no chat do Kiro: "rode o workflow `sdd-entregar-fatia` para a FT-031" ou `/workflow-run` (IDE 1.3+) |
| registrar uma lição / retrospectiva | `sdd-aprender` |

## Onde as coisas moram (no projeto)

| Caminho | O quê |
|---|---|
| `.kiro/steering/sdd.md` | o único steering do fluxo: resumo, configuração do projeto e regras aprendidas |
| `.kiro/agents/sdd-*.json` | agentes (criados pela setup, com as skills escolhidas por agente) |
| `<produto>/` — a pasta escolhida na setup (padrão `.kiro/planejamento`), registrada no `sdd.md` | `backlog.md`, `epicos/<EP>-<slug>/` (PRDs), `equipe.json`, `acordos.md`, `roadmap.md`, `sprints/<pai>/sprint-<nn>.md` (a sprint segue a iteração pai do EWM; chave `2026/Sprint 03`), `sustentacao/<pasta>/` (a pasta de cada categoria na tabela **Sustentação** do `sdd.md`), `aprendizado/` (só na branch base) |
| `.kiro/specs/<ft>-<slug>/` | uma pasta por fatia: `status.md`, `research.md`, spec do Kiro, revisões, verificação |
| glossário · ADRs · bundle do ELM | caminhos na seção Projeto do `sdd.md` |
| `.kiro/hooks/sdd.json` · `.kiro/workflows/sdd-*` · `.kiro/sdd/http.sh` | opcionais da setup: backpressure por tarefa, receitas, chamada HTTP do verificador |
| `.kiro/local/` (fora do git) | worktrees do loop, vereditos dos workflows, log dos lotes, dados de cliente (extrações, evidências com dado real), especificação em andamento (`especificacao/<EP>/`, até o GATE do PRD) |

## Fronteiras de fase

Ao terminar uma fase, nesta ordem: seguir na mesma sessão se o contexto ainda serve → sessão nova se o contexto
anterior não importa mais (o estado está nos arquivos) → mandar para um agente se a próxima fase pode correr AFK.
Nunca compacte no meio de uma fase. Quem segue é a pessoa (ou o orquestrador, no loop): toda skill termina dizendo
a próxima e para — nunca invoca nem simula a do passo seguinte.

## Regras de ouro

- **Falha de escrita:** pasta inexistente → crie; permissão negada ou confirmação recusada → `fase: bloqueada (de:
  <fase>)` com o caminho e o que faltou (fora de fatia: diga e pare); gravação parcial → o próximo passo retoma pelo
  que está no disco. Nunca siga como se tivesse gravado.
- Nada inventado: tabela, coluna, regra, id de work item — confirme no código, no banco (somente leitura) ou no ELM.
- **Pergunte antes de varrer** (regra do `.kiro/steering/sdd.md`): com uma pessoa na sessão, antes de procurar além
  do que o passo manda ler (jobs irmãos, outras fatias, a base), uma pergunta sobre o que ela já sabe; subagente não
  pergunta — quem chama passa as **Indicações da pessoa** no pedido. A resposta é ponto de partida, não prova.
- Toda escrita no ELM, troca de branch, push e alteração de work item só com "sim" de uma pessoa; na base, o agente
  só dá push dos registros de situação, com a conferência dos arquivos
  ([Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base)). Merge só do PR aprovado, pelo **Dev
  responsável** (`gitlab_mesclar_mr`, com confirmação); nunca `--force`.
- **ELM pelo MCP `elm` do power:** a skill do passo chama a tool (`elm_*`) com `projeto` e os ids; o MCP lê o
  `.kiro/config/sdd/pa_<nome>.json`. Regras de escrita, pendências e tarefas: [references/elm.md](references/elm.md).
  Sem o MCP ou com falha, a escrita vira `ELM pendente` registrada — o ELM nunca trava o fluxo.
- **Bundle do ELM e PR, só pelos MCPs do power:** a documentação baixada pela `sdd-sync` (`<rm.download>`) —
  cópia local, em Markdown, dos artefatos do ELM, válida até o último sincronismo (o ELM ao vivo é pelo `elm_buscar_req`/`elm_ler_req`) — é
  consultada pelo **`elm`** — `elm_buscar_req_local` para achar, `elm_ler_req_local` para ler um artefato, `elm_listar_req_local`
  para listar uma pasta (o MCP acha a pasta pelo `pa` e reindexa o que mudou; sem nada baixado → ELM remoto, ver
  [elm.md](references/elm.md#bundle-local)) —, nunca
  lendo ou buscando os arquivos (os agentes nem têm leitura nessa pasta). PR é o merge request do GitLab, pelo
  **`gitlabpr`**: `gitlab_listar_mrs`, `gitlab_obter_mr`, `gitlab_criar_mr` e `gitlab_mesclar_mr` (com o "sim" da pessoa; `origem` e
  `destino` sempre explícitos, porque o MCP roda no checkout principal, não na worktree) — nunca `gh` nem `glab`.
  MCP indisponível → diga e siga sem ele: bundle → o ELM ao vivo (`elm_buscar_req`); PR → título e descrição entregues.
- Dado de cliente (resultado de consulta, extração, tela com dado real) nunca vai para o git: fica em
  `.kiro/local/` (`sustentacao/<pasta>/<ID>/`, `verificacao/`…); o registro versionado guarda consulta, contagem,
  caminho e resumo sem identificar pessoas.
- **Skills sem agente exclusivo:** `sdd-setup` e `sdd-aprender` rodam na **sessão padrão** (com o power
  carregado): gravam onde nenhum agente pode (steering, agentes); o modo registrar da `sdd-aprender`, que só grava
  as lições, também roda no `sdd-produto`. A **`sdd-consolidar`** é do P.O. ou do SM, no `sdd-produto`. **Push pelo agente:** orquestrador (no loop), codificador, revisor e verificador,
  com `ask` (o Kiro pergunta sempre), só a branch da fatia — e, no codificador e no orquestrador, a base com os
  registros de situação (`iniciada`, `pronta`; o orquestrador, só a `iniciada` do lote); push recusado (pela pessoa
  ou pela regra) → a skill entrega o comando pronto e espera a pessoa dizer que publicou; o da base recusado pelo
  remoto → desfaz só o commit de registro, com "sim", e para; produto e pesquisador não
  fazem push. Subagente do AFK não faz push (quem conduz commita). Com a branch no remoto, o PR é aberto pela
  `gitlab_criar_mr`, que o Kiro confirma (`ask` no codificador e no orquestrador; negada aos demais).
  **O que os agentes não fazem:** merge (exceto a `gitlab_mesclar_mr` no codificador, com `ask`: o Dev mergeia o
  PR aprovado), `--force`, `worktree remove` — nunca. O hub `sdd-iniciar` está em todos os agentes de papel, e a `sdd-status`
  em todos os agentes, menos o `sdd-pesquisador`; os dois também funcionam na sessão padrão. Nenhuma skill depende de um agente para operar: o agente apenas recebe a skill
  pré-carregada para conveniência.
- **Nenhuma skill cria branch ou `.kiro/specs/<ft>/status.md`** sem passar pelos Passos 3–4 da `sdd-desenvolver`
  (DoR, sprint, WIP, `iniciada` na base, branch, commit). O `sdd-loop` é a única exceção (opera em worktree como
  orquestrador e grava a `iniciada` do lote na base).
