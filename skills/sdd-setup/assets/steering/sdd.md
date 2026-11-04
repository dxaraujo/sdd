---
inclusion: always
---

# sdd — <nome do projeto>

Este repositório usa o fluxo **sdd** (power `sdd`): alinhar antes de escrever, fatias verticais pequenas, plano
aprovado por um Dev Sênior (GATE pela senioridade), teste primeiro com backpressure, revisão e verificação independentes, PR lido por uma
pessoa, e o IBM ELM como registro oficial da documentação. Como funciona: skill `sdd`. Toda demanda nova: `sdd-triar`.
Começar um item registrado: hub `sdd-iniciar` (diz a skill do papel: `sdd-especificar`, `sdd-desenvolver`,
`sdd-revisar`, `sdd-verificar`, `sdd-atender`; `sdd-revisar` também nas `[APR]` (plano e PR), `sdd-planejamento` na troca de modo, `sdd-consolidar` na fatia `pronta`, `sdd-executar` nas demais tarefas de Sustentação — `[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]`). Onde parei ou fechar a sessão: `sdd-status`.

- **Créditos do Kiro:** nenhuma sessão termina sem registrá-los. Skill que termina (diz a próxima e para) sem ter
  registrado os desta sessão, ou pessoa que encerra → pergunte `💳 Fechar a sessão e registrar os créditos? (sim)`
  e, na resposta, `sdd-status` › Fechar a sessão, item 4. A leitura é sempre depois de uma resposta da pessoa: o Kiro
  só grava o consumo do turno quando ele termina.
- Nada inventado (confirme no código, no banco — só leitura — ou no ELM). Nunca apague nem afrouxe teste.
- **Falha de escrita:** pasta inexistente → crie; permissão negada ou confirmação recusada → `fase: bloqueada (de:
  <fase>)` com o caminho e o que faltou (fora de fatia: diga e pare); gravação parcial → o próximo passo retoma pelo
  que está no disco. Nunca siga como se tivesse gravado.
- Estado limpo entre sessões: quem grava um passo na pasta da fatia commita o que gravou **com o `status.md`**,
  antes de seguir. AFK: quem pede a rodada (plano, implementação, loop) commita o relatório do subagente assim que o
  recebe — revisor, verificador e pesquisador como subagentes não commitam. HITL: cada papel commita o seu
  relatório e a fase na branch do PR.
- **Entrega (todo papel do HITL):** commit → push → **conferir no remoto** (`git fetch`; `git rev-parse HEAD` =
  `git rev-parse origin/<branch>`) → só então lançar horas ou concluir a tarefa do papel e avisar o próximo. Push
  da entrega pelo agente com a confirmação do Kiro, só da branch da fatia; sem ela, o comando pronto e a pessoa diz
  que publicou. Subagente do AFK não faz push (quem conduz commita).
- **Uma skill por vez:** cada skill termina dizendo a próxima e para — nunca invoca nem simula a do passo seguinte
  (os subagentes que ela manda chamar fazem parte dela); quem chama a próxima é a pessoa, ou o
  orquestrador no loop. Consolidar (fatia `pronta`) é do P.O. ou do SM, no `sdd-produto` — nunca do agente do Dev.
- Push, troca de branch e escrita no ELM só com "sim" de uma pessoa; push de agente para a base só dos registros de
  situação da fatia (`<FT> iniciar`, `<FT> registrar merge`), com os arquivos conferidos antes (bloco Gravar na base
  do `references/backlog.md` da `sdd-fatiar`). Merge só do PR aprovado, pelo **Dev responsável**
  (`gitlab_mesclar_mr`, com confirmação); nunca `--force`.
- Dado de cliente (consulta, extração, tela com dado real) nunca vai para o git: fica em `.kiro/local/<origem>/<id>/`;
  o versionado guarda consulta, contagem, caminho e resumo sem identificar pessoas.
- Scrumban: a sprint é cadência (meta, review, retro), não contêiner de escopo: o compromisso é a meta; dentro dela,
  fluxo puxado — a `elegivel` de maior prioridade entra quando o WIP de revisão tem folga. Previsão pela vazão, sem
  pontos.
- **Modo pela senioridade** de quem implementa (`equipe.json`): Júnior → sempre HITL; Pleno → os critérios da fatia;
  Sênior → AFK por padrão (HITL só com motivo forte, registrado). Só Pleno ou Sênior dispara o `sdd-loop`. A `[REV]`
  e a `[APR]` são sempre de um **Dev Sênior** (PR de um Sênior: outro Sênior; único Sênior ativo → ele mesmo,
  `revisor único`). **GATE do plano** pela senioridade: Júnior → sempre; Pleno → pergunta (no loop, vale para o
  lote); Sênior → nunca (aprova o próprio plano). Fatia AFK cujo plano mostra risco → sugerir HITL; a troca é do
  P.O. na base. HITL → AFK nunca.
- Toda hora tem tarefa (`[ESP]` `[DEV]` `[REV]` `[VER]` e as da Sustentação — `[ATD]` `[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]`; no AFK, só a `[DEV]`; `[APR]` do Dev Sênior nos
  gates sem tarefa de papel — aprovar plano, aprovar PR do AFK —, criada quando a fatia chega ao gate; `[GB]
  Gerenciamento do backlog` do SM: só ele lança horas nela; o P.O. nunca lança, nem quando é também o SM, e toda
  sessão do P.O. ou do SM no `sdd-produto` comenta nela os créditos gastos). Lançar horas é
  registro de empenho, a qualquer momento na tarefa assumida; concluir é da skill do papel, com o saldo: `[DEV]` no
  merge, `[REV]` ao aprovar (depois do push), `[VER]` ao aceitar (depois do push), `[APR]` na aprovação, `[ESP]` no
  GATE do backlog, a da Sustentação ao concluir o item (junto com o IB dele). A sincronização com o EWM
  (`sdd-planejamento`, "sincroniza a sprint") leva o sdd até onde o trabalho chegou por fora: traz a tarefa criada
  direto no EWM, compara os itens conhecidos (estado, iteração, dono, estimativa, a fase do `status.md`, o IB do
  backlog fora do estado inicial) e lê o git (branch, PR, merge → `iniciada` ou `pronta`), numa tabela com a solução
  proposta.
- **Consolidação é processo de produto:** fatia `pronta` → o P.O. ou o SM, no agente `sdd-produto`
  (`sdd-consolidar`, créditos na `[GB]`): lê o Drift de negócio que a REV e a VER marcaram no `status.md`, publica no
  ELM o *as-built* (requisitos, ET, casos de teste), leva os ADRs do PR à pasta de ADRs e fecha a fatia na base
  (`concluida`).
- Estado em disco: a situação de cada item no `backlog.md` e na sprint, gravada na base por quem a causa (seção
  Situações do `references/backlog.md` da `sdd-fatiar`); o detalhe da fatia em `.kiro/specs/<ft>-<slug>/` (comece
  pelo `status.md`; em `pronta` e `concluida` vale o da base — regra A base prevalece do `status-template.md` da
  `sdd-desenvolver`); produto na pasta abaixo.

> Gerado pela `sdd-setup` (power `sdd` <x.y.z>) em <AAAA-MM-DD>. Para mudar: "atualizar a configuração do sdd".
> As skills e os agentes `sdd-*` leem os valores daqui.

## Projeto

| Item | Valor |
|---|---|
| Pasta do produto (`<produto>` nas skills) | `<.kiro/planejamento>` — backlog, épicos e PRDs, planejamento, aprendizado |
| Tipos · stack · módulos | `<batch>` · <Java 21, Spring Batch 5, Oracle> · <módulo único | lista> |
| Toolkits | <nome (origem) | nenhum> |
| Steering | produto `<product.md>` · tecnologia `<tech.md>` · estrutura `<structure.md>` · extras `<… | nenhum>` |
| Glossário · ADRs | `<docs/glossario.md>` · `<docs/adr | não há>` |
| Bundle do ELM (cópia local em Markdown, baixada pela `sdd-sync`) | `<rm.download do pa — ex.: docs/elm/<pa>> | não há` — consulta **só pelo MCP `elm`**: `elm_buscar_req_local` para achar, `elm_ler_req_local` para ler, `elm_listar_req_local` para listar (o MCP acha a pasta pelo `pa` e reindexa o que mudou); sem nada baixado (erro `nao_encontrado` campo `bundle`) → diga isso, pesquise no ELM remoto (`elm_buscar_req`/`elm_ler_req`) e ofereça a `sdd-sync`. Nunca leia nem busque os arquivos dela |

**Regras críticas** (BLOQUEANTE na revisão):
- <ex.: escrita em lote sempre idempotente por chave de negócio>

## Comandos (backpressure)

Uma coluna por módulo quando houver mais de um; a fatia usa a do módulo que altera (o `design.md` diz qual).
Na worktree do `sdd-loop`: `cd .kiro/local/wt/<ft> && <comando>`. Falha de ambiente → `AMBIENTE`, nunca consertar.

| Ação | `<módulo>` |
|---|---|
| Compilar | `<…>` |
| Testes · teste único (`{alvo}`) | `<…>` · `<…>` |
| Lint · cobertura e gate | `<… | não há>` · `<comando> · <gate | sem gate>` |

## Verificação de aceite

| Item | `<módulo>` |
|---|---|
| Executar · exercitar um cenário | `<comando | job + parâmetros>` · <HTTP | job | browser | carga> |
| Onde verificar · massa de teste | <resposta, banco, log> · `<pasta e convenção>` |
| Ambiente · chamada HTTP | <local | dev — nunca produção> · `<sh .kiro/sdd/http.sh — <url> | curl com confirmação | não se aplica>` |

## Git, banco e autonomia

| Item | Valor |
|---|---|
| Branch base · prefixo · commit | `<develop>` · `<feature/>` · `<FT-<nnn> <verbo> <descrição> | Task <id> - …>` |
| Mensagens do fluxo (dentro do padrão acima) | início: `<id> iniciar` (fatia, épico ou item de Sustentação; lote do loop: `FT-031, FT-032 iniciar`) · fatia: `<FT> registrar plano` · `registrar análise do plano <N>` · `registrar aprovação do plano` · `registrar revisão <N>` · `registrar verificação` · `<FT> registrar merge` · tarefa: `<id> <o que a tarefa fez>` · triagem: `backlog: triagem <ids>` · Sustentação: `<ID> concluir` · sprint: `<pai>/Sprint <nn>: <planejar | encaixe | virada | sincronizar com o EWM>` (ex.: `2026/Sprint 03: planejar`) · PRD: `EP-<nn> aprovar PRD` · ELM: `<id> publicar no ELM` · consolidação: `<id> consolidar` |
| PR (merge request) | `<MCP gitlabpr — gitlab_listar_mrs · gitlab_obter_mr · gitlab_criar_mr (origem e destino sempre explícitos) · gitlab_mesclar_mr (merge pelo Dev responsável, com o `sha` aprovado) | entregar título e descrição>` — nunca `gh` nem `glab` |
| Artefatos de produto (pasta do produto, glossário, ADRs, consolidação) | direto na branch base — nunca em branch de fatia; push com o "sim" da pessoa (o agente `sdd-produto` não faz push: entrega o comando; o agente do Dev publica ali só os registros de situação da fatia) |
| MCP de banco | `<@servidor/tool | não há>` — **somente leitura** (`SELECT`/`WITH`), exceto os scripts de massa; DDL fora do fluxo |
| Paralelo no loop | `<1>` (máx. 3) — o GATE do plano não se configura: sai da senioridade de quem implementa (`sdd-plano` Passo 5) |
| Push e PR no loop | `<perguntar a cada lote (o Kiro confirma cada um) | não — a pessoa abre (o push da base com a iniciada do lote também: o orquestrador entrega o comando e espera a publicação)>` |
| Instalados | hook `<sdd-backpressure | nenhum>` · workflows `<sdd-planejar-fatia, sdd-entregar-fatia | nenhum>` (disparados pela pessoa) |

## ELM

| Item | Valor |
|---|---|
| Usa ELM | `<sim — .kiro/config/sdd/pa_<nome>.json (padrão; outros: …) | não>` — o MCP `elm` lê o `pa`; regras em `references/elm.md` da skill `sdd`; sem o MCP, a escrita vira `ELM pendente` |
| Publicar requisitos · ET | `<na-aprovacao | no-merge>` · `<não publica | as-built no merge>` (itens do EWM: nascem no backlog do produto do `pa` — `ccm.backlog` — e mudam de iteração ao entrar na sprint) |
| Manual no DOORS Next | `<change set, módulo, links restringe, baseline | nada>` |
| Fatia dividida no EWM | `<itens novos como filhos do item original | fecha o original e cria itens novos>` |
| Pontos P/M/G no EWM | `<não | 2 · 3 · 5>` (opcional; o planejamento prevê pela vazão) |
| Critérios de aceite no IB | `<nome do campo em ccm.tipos.ib.campos do pa | descrição>` |
| IB de defeito | `<campo = valor de correção (ex.: Categoria = Correção) | —>` (os demais padrões estão no `pa`) |
| Tarefas (títulos padrão; editáveis à mão) | `[ESP] EP-<nn> Especificação` · `[DEV] FT-<nnn> Implementar` · `[REV] FT-<nnn> Revisar` · `[VER] FT-<nnn> Verificar` · `[APR] FT-<nnn> Aprovar plano` · `[APR] FT-<nnn> Aprovar PR` · `<prefixo da categoria> <ID> <pedido>`, filha do IB do item `[<ID>] <pedido>` (ex.: `[ATD] AT-012 <pedido>` sob `[AT-012] <pedido>`) · `[GB] Gerenciamento do backlog` |
| `CT.csv` (colunas na ordem do template do ETM) | `<Tipo=Caso de Teste · Resumo · Responsável · Status=<inicial> · Categoria · Planejado para · Descrição>` |

## Sustentação

O que não vem de épico. No EWM, o IB `Sustentação` (um por produto, no backlog do EWM; nasce com a `[GB]` no modo
inicial da `sdd-planejamento`) é o pai da `[GB]`, do IB `Manutenção` e dos IBs de categoria.

- **Manutenção:** o IB pai das fatias sem épico (trilha padrão ou rápida; `origem` `Manutenção` no `backlog.md`),
  que nasce com a primeira delas. Elas mudam o repositório e seguem o fluxo da fatia: são do Dev e podem ser AFK.
  Não é categoria: não tem prefixo de tarefa, série de ids nem pasta próprios.
- **Categorias** (tabela abaixo): trabalho sem mudança no repositório (mudança de código ou config é fatia da
  Manutenção). Cada item é de uma categoria, com prefixo de tarefa, série de ids e pasta de fichas próprios. No EWM:
  IB `<Categoria>` (filho da Sustentação; nasce com o primeiro item triado dela, como a `### <Categoria>` do
  `backlog.md`) → IB do item `[<ID>] <pedido>` (nasce na triagem; dono = P.O.) → tarefa `<prefixo> <ID> <pedido>`
  (nasce quando o item entra numa sprint; dono = quem faz). Ficha: `<produto>/sustentacao/<pasta>/<ID>-<slug>.md`;
  dado de cliente: `.kiro/local/sustentacao/<pasta>/<ID>/` (fora do git).

Item de categoria (`AT-`, `IM-`, `BD-`, `IN-`, `OP-`, `EX-` e as tarefas deles) não é do agente do Dev nem AFK: a
regra vale pelo tipo de id, não pelo nome Sustentação.

| Categoria | O que cobre | Tarefa | Id | Pasta | Classificação da Tarefa (PA) | Skill |
|---|---|---|---|---|---|---|
| Atendimento | chamado ou pedido do cliente: consulta, extração, explicação, conferência | `[ATD]` | `AT-` | `atendimento` | `<Suporte / Apoio Técnico Especializado>` | `sdd-atender` |
| Implantação | preparar e acompanhar a subida de versão: pacote, janela, roteiro, validação pós-implantação | `[IMPL]` | `IM-` | `implantacao` | `<…>` | `sdd-executar` |
| Banco de dados | script de correção ou carga de dados, conferência de base, apoio ao DBA | `[BD]` | `BD-` | `banco-de-dados` | `<…>` | `sdd-executar` |
| Infra | ambiente, acesso, certificado, fila, servidor, pedido a outra equipe | `[INF]` | `IN-` | `infra` | `<…>` | `sdd-executar` |
| Operação | rotina de produção: reprocessar job, acompanhar execução, incidente sem mudança de código | `[OPE]` | `OP-` | `operacao` | `<…>` | `sdd-executar` |
| Apoio a outros times | ajuda técnica a outra equipe ou outro produto | `[EXT]` | `EX-` | `outros-times` | `<…>` | `sdd-executar` |

## Agentes

| Agente | Skills extras | Oferecidas e recusadas | MCP | Modelo | Subagentes |
|---|---|---|---|---|---|
| `sdd-produto` | <…> | <…> | <…> | <padrão> | `sdd-pesquisador`, `sdd-revisor` |
| `sdd-pesquisador` | <…> | <…> | <…> | <padrão> | — |
| `sdd-codificador` | <…> | <…> | <…> | <padrão> | `sdd-pesquisador`, `sdd-revisor`, `sdd-verificador` <+ do projeto> |
| `sdd-revisor` | <…> | <…> | <…> | <padrão> | — |
| `sdd-verificador` | <…> | <…> | <…> | <padrão> | — |
| `sdd-orquestrador` | <…> | <…> | — | <padrão> | os `sdd-*` <+ do projeto> |

## Regras aprendidas

Regras de **julgamento** promovidas pela `sdd-aprender` (lições em `<produto>/aprendizado/licoes.md`). O revisor
as cobra como itens da rubrica; o plano as respeita. Erro mecânico não entra aqui: vira lint, teste, hook ou CI.
Formato: `### R-<nn> · <título> · aplica a: <codificador | revisor | plano | PRD | todos> · severidade: <BLOQUEANTE | IMPORTANTE>`,
a regra em 1–2 frases imperativas, `- ✅ <certo> · ❌ <errado>`, `- Origem: L-<nnn>`.

<!-- Nenhuma regra promovida ainda. -->
