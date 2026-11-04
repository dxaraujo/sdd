# sdd

Power do Kiro para **engenharia agêntica orientada a especificação**, com o **IBM ELM** como fonte oficial da
documentação e o **planejamento ágil** dentro do fluxo. É a versão 3 do `sdd`: a v2 (que substituiu a v1 e o power
`sdd2`) com o power `elm` incorporado — o ELM vem pelo `mcp-elm` 3.0, no `mcp.json` deste power. Menos cerimônia onde ela não paga, mais verificação onde ela paga, e cada
decisão ancorada no que os principais praticantes de desenvolvimento com agentes defendem hoje (outubro de 2026).

O agente escreve muito código rápido; o que limita o resultado é o **alinhamento** antes e a **verificação**
depois. O sdd põe as pessoas onde elas têm mais alavanca — decidir o quê, aprovar o como, ler o código — e deixa
o resto com agentes de contexto limpo, presos a feedback automático.

```
ENTRADA   triar ─► backlog: EP novo · FT sem épico (padrão ou rápida, cada uma com a sua ficha) · Sustentação (AT-/IM-… + IB) ─► "mais algum?"
HUB       iniciar <item> ─► especificar · desenvolver · revisar ([REV], [APR]) · verificar · atender · planejamento (troca) · consolidar · executar (cada uma assume a sua tarefa)
            │
PRODUTO   entrevistar ─► PRD ─► GATE PRD ─► ELM (HF/REG/GL) ─► fatiar ─► GATE backlog ─► sprint (EWM)
                                                                                 │
FATIA     desenvolver (iniciada na base) ─► pesquisar ─► plano (spec do Kiro) ─► GATE plano ─► implementar (TDD) ─► PR ─► revisar ─► verificar   (AFK: revisão e verificação antes do PR)
                                                                                                                                     │
DEPOIS    merge (Dev; remove a worktree do loop) ─► pronta na base
            │
PRODUTO   consolidar (P.O./SM, [GB]): drift da REV/VER ─► ELM as-built (ET, CTs) ─► ADRs do PR ─► concluida ─► aprender
```

**Mapa interativo do fluxo:** <https://dxaraujo.github.io/kiro/> — cada trilha é uma linha de metrô e cada skill uma
estação. Escolha a linha (épico, fatia HITL ou AFK, Sustentação, ciclo da sprint), a senioridade de quem implementa
e a trilha da fatia; a ficha ao lado mostra papel, agente, tarefa no EWM, arquivos, chamadas ao ELM e as transições de
cada passo. Fonte: branch `gh-pages` deste repositório.

## O que mudou da v1 para a v2

| `sdd` v1 | `sdd` v2 |
|---|---|
| um fluxo para tudo (HF/REG/ET/CT + spec SDD em todo IB) | **trilhas** pelo tamanho: rápida (bugfix spec), padrão, épico — e sustentação (atendimento e outras categorias), sem código |
| especificação por IB, em três papéis assíncronos | **PRD por épico** + **fatias verticais** que cabem numa janela de contexto |
| entrevista uma pergunta por vez | entrevista em **rodadas pela fronteira** de decisões, sempre com recomendação |
| spec SDD → implementação → judge | **pesquisa** compactada → **plano com a forma do programa** e o **contrato de pronto** → **GATE do plano** |
| judge com rubrica única | revisão em **dois eixos separados** (spec × padrões) + **verificação de aceite** de ponta a ponta |
| testes unitários + cobertura | **teste primeiro**, **backpressure** a cada tarefa, **oráculo protegido** |
| ELM publicado antes do código | ELM como **registro oficial**: requisitos no GATE do PRD, **as-built** e drift na consolidação |
| retrabalho por causa raiz | **aprendizado composto**: erro mecânico vira checagem, julgamento vira regra do revisor |
| lote de IBs | **AFK/HITL** por fatia e **loop AFK** limitado pela capacidade de revisão humana |
| planejamento por pontos/hora e Excel | sprint como cadência (compromisso com a **meta**), fluxo puxado dentro dela, previsão pela **vazão** e lead time; pontos só opcionais no EWM |
| agentes JSON com permissões amplas | agentes **gerados** no formato V3 do Kiro (IDE e engine V3 do CLI), permissões mínimas por papel e **skills de toolkit escolhidas por agente** |

## Fundamentos

| # | Princípio | Quem defende |
|---|---|---|
| 1 | Alinhar antes de escrever: entrevista em rodadas, com resposta recomendada; fatos o agente busca, decisões a pessoa toma | Matt Pocock (`grilling`), Anthropic (entrevista → spec), Dex Horthy (QRSPI), Andrej Karpathy (modelos não pedem esclarecimento) |
| 2 | Cerimônia do tamanho do trabalho | Birgitta Böckeler ("marreta para quebrar noz"), Anthropic ("se o diff cabe numa frase, pule o plano"), Horthy (~40% *oneshot*), Spec Kit |
| 3 | Spec é registro de decisão, sem caminho de arquivo; o que dura é glossário, ADR e — aqui — o ELM | Pocock (`to-spec`), Böckeler (*spec-anchored*), Kent Beck e Martin Fowler (aprender durante a implementação) |
| 4 | Linguagem ubíqua num glossário usado no PRD, nos testes e no código | Pocock (`domain-modeling`), DDD |
| 5 | Fatias verticais (*tracer bullets*) que cabem numa janela de contexto nova, com critérios falsificáveis | Pocock (`to-tickets`), Horthy ("modelos amam planos horizontais"), Anthropic (uma funcionalidade por vez), Geoffrey Huntley (um item por loop) |
| 6 | Pesquisar → planejar → implementar, com compactação em arquivo e revisão humana do plano | Horthy (*Advanced Context Engineering*), Boris Cherny (comece no plan mode) |
| 7 | Desenhar a forma do programa antes do código (árvore de arquivos, assinaturas, árvore de chamadas) | Horthy (*Why Software Factories Fail*, 2026), Pocock (módulos profundos) |
| 8 | Teste primeiro, vermelho → verde, nos pontos de teste combinados | Beck, Simon Willison (*red/green TDD*), Karpathy ("dê critérios de sucesso, peça os testes primeiro"), Pocock (`tdd`) |
| 9 | Backpressure: compilar, testes e lint a cada passo; evidência em vez de afirmação | Huntley, Anthropic, Cherny ("dê ao agente como verificar o trabalho"), Willison ("first run the tests") |
| 10 | Proteger o oráculo: teste não se apaga nem se afrouxa | Anthropic (*long-running harnesses*), Beck ("o gênio trapaceando"), Karpathy (`autoresearch`) |
| 11 | Gerador ≠ avaliador; revisão em contexto limpo e em eixos separados; avaliador cético mas sem caçar gosto | Anthropic (*harness design*), Pocock (`code-review`), Cherny |
| 12 | Contexto limpo por fatia e estado em disco | Horthy (zona burra acima de ~40%), Pocock (*smart zone*), Huntley, Anthropic (*context engineering*) |
| 13 | Slider de autonomia: HITL até o tipo de trabalho provar que anda sozinho; WIP limitado pela revisão humana | Karpathy ("Iron Man suits"), Pocock (AFK/HITL), Addy Osmani (*orchestration tax*), DORA 2025 |
| 14 | Leia o código: PRs pequenos, com caminho de leitura e evidência | Horthy ("read the dang code"), Willison, Osmani (*comprehension debt*), Thoughtworks Radar vol. 34 |
| 15 | Aprendizado composto: cada correção muda o ambiente — checagem determinística primeiro | Mitchell Hashimoto (*engineer the harness*), Cherny, Pocock (`retro`), Fowler (*guides & sensors*) |
| 16 | Conhecimento mantido por LLM, com *lint* de contradições | Karpathy (*LLM Wiki*) — aqui, o bundle do ELM + glossário + ADRs |
| 17 | Harness mínimo, revisto a cada modelo; segurança sem a "tríade letal" | Anthropic, Fowler (*Are Harnesses Worth the Cost?*), Willison |

Fontes no fim deste arquivo.

## Conteúdo

| Skill | Função |
|---|---|
| `sdd` | guia do fluxo: trilhas, gates, princípios, qual skill usar |
| `sdd-setup` | configura o projeto: entende o repositório, descobre skills e toolkits, cria os agentes perguntando as skills de cada um |
| `sdd-status` | painel "onde parei", WIP de revisão, próxima ação de maior alavanca |
| `sdd-triar` | entrada de toda demanda nova: triagem em qualquer trilha, duplicados, ficha da fatia padrão sem épico, registro no backlog (inclusive a Sustentação: categoria, AT-nnn/IM-nnn…, IB do item no EWM; a tarefa `[ATD]`/`[IMPL]`… nasce quando o item entra numa sprint), importação de itens do EWM, "mais algum item?" — não começa nada |
| `sdd-iniciar` | hub: recebe o item registrado (ou "minha próxima tarefa") e diz a skill do papel |
| `sdd-especificar` | Especificador: assume a `[ESP]`, conduz entrevista → PRD → fatias numa pasta local até o GATE e registra cada sessão na tarefa (comentário + anexos) |
| `sdd-desenvolver` | Dev: compromisso (Definition of Ready, sprint/encaixe, WIP), `iniciada` na base, branch, pasta, assume a `[DEV]`; retomada pela fase; merge do PR aprovado, `pronta` na base e conclusão da `[DEV]` |
| `sdd-entrevistar` | alinhamento em rodadas (grill), decisões e glossário |
| `sdd-prd` | PRD do épico (o quê e por quê) e GATE do PRD |
| `sdd-fatiar` | PRD → fatias verticais AFK/HITL, backlog e GATE do backlog |
| `sdd-planejamento` | roadmap, acordos (cadência Scrumban, DoR/DoD, WIP, reserva para Sustentação e retrabalho), sprint com especificação e Sustentação, encaixe, troca AFK → HITL, "sincroniza a sprint", review, retrospectiva, virada e relatório de horas |
| `sdd-executar` | executa os demais itens de Sustentação já triados (`[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]`; a pessoa faz o trabalho fora do repositório): assumir no ELM (`em-andamento`), registrar o trabalho, lançar horas, concluir a tarefa e o IB do item |
| `sdd-atender` | executa o atendimento (categoria Atendimento da Sustentação) já triado (AT-nnn): assume a `[ATD]`, consulta só leitura, extração fora do git, resposta, saldo de horas, desdobramentos |
| `sdd-pesquisar` | pesquisa do código compactada em `research.md` |
| `sdd-plano` | spec do Kiro (`requirements.md`/`bugfix.md`, `design.md`, `tasks.md`) e GATE do plano |
| `sdd-implementar` | TDD + backpressure, commits pequenos, revisão e PR (termina no PR) |
| `sdd-revisar` | revisão independente: PRD (P), plano (L), código (C, dois eixos) |
| `sdd-verificar` | aceite de ponta a ponta com evidência; `CT.csv` para o ETM |
| `sdd-consolidar` | fatia `pronta` (pós-merge) → `concluida`, processo de produto (P.O. ou SM, agente `sdd-produto`, créditos num comentário na `[GB]`; horas só do SM): drift marcado pela revisão e pela verificação, ELM as-built (requisitos, ET, casos de teste criados no ETM), ADRs do PR, glossário, conclusão |
| `sdd-sync` | sincroniza o bundle OKF do DOORS Next nas duas vias (plano, baixar, enviar, conflitos) e, depois de baixar, pergunta se indexa o bundle local e gera a visualização offline dele (`explorar.html`, galáxias 3D) |
| `sdd-loop` | fatias AFK até o PR, uma worktree por fatia, uma fase por contexto limpo |
| `sdd-aprender` | lições, promoção de regras, retrospectiva com dados, casos de avaliação |

## O que a setup instala no projeto

O formato de power recomendado pelo Kiro (Agent Plugins, `plugin.json`) carrega só `skills/` e `mcp.json` — steering,
agentes, hooks e workflows dentro de um power são ignorados. Por isso a `sdd-setup` instala no projeto, a partir
de `skills/sdd-setup/assets/`:

| Arquivo | O quê |
|---|---|
| `.kiro/steering/sdd.md` | o único steering do fluxo (sempre carregado): resumo, configuração do projeto (pasta do produto, comandos, verificação, git, banco, autonomia, ELM, agentes) e regras aprendidas |
| `.kiro/config/sdd/agentes.json` | as escolhas do projeto para os agentes (caminhos, comandos, skills e MCPs por agente) — a entrada do gerador |
| `.kiro/agents/sdd-*.json` | `produto`, `pesquisador`, `codificador`, `revisor`, `verificador`, `orquestrador` — gerados pelo script da setup a partir do `agentes.json`, cada um com as skills e MCPs que a pessoa liberou |
| `.kiro/hooks/sdd.json` (opcional) | backpressure: compila e testa depois de cada tarefa de spec |
| `.kiro/workflows/sdd-*.workflow.json` (opcional, experimental) | `planejar-fatia` (até o GATE do plano, com a `[APR]`) e `entregar-fatia` (AFK até o PR aberto pelo `gitlabpr`, com a `[APR] Aprovar PR`) nos Kiro Workflows — quem dispara é a pessoa, no chat do Kiro ("rode o workflow `sdd-entregar-fatia` para a FT-031" ou `/workflow-run`), uma fatia por vez; nenhum agente as dispara |
| `.kiro/sdd/http.sh` (opcional) | única chamada HTTP que o verificador faz sem perguntar: só à URL de teste, com corpo da pasta `massa/` |
| pasta do produto (proposta pela setup; padrão `.kiro/planejamento`) | `backlog.md`, épicos e PRDs, `equipe.json`, `acordos.md`, `roadmap.md`, `sprints/<iteração pai>/`, `sustentacao/<pasta>/`, `aprendizado/` — versionada; o que é local fica em `.kiro/local/` (fora do git) |

O ELM vem no próprio power: o MCP **`mcp-elm`** (≥ 3.6.4) lê o `.kiro/config/sdd/pa_<nome>.json` do projeto (um por
project area, gravado pela `sdd-setup`) e expõe operações (`elm_transicao`, `elm_lancar_horas`, `elm_criar_wi`,
`elm_ligar`, `elm_publicar_req`…): a skill do passo passa só o caminho do projeto, os ids e o conteúdo, e recebe
`{"ok": …}`. Regras comuns em [`skills/sdd/references/elm.md`](skills/sdd/references/elm.md). Leituras liberadas nos
agentes; escritas com confirmação do Kiro, além do "sim" da skill; cada papel comenta e anexa só na própria tarefa; o
pesquisador só consulta o bundle local. Sem o MCP, a escrita vira pendência registrada.

Cada agente tem as permissões mínimas do papel, definidas uma vez em
[`skills/sdd-setup/assets/agents/papeis.json`](skills/sdd-setup/assets/agents/papeis.json) e geradas no campo
`permissions` do Kiro: lê o projeto e o power, mas não `.env`, chaves, `~/.ssh`, `~/.aws` nem as credenciais do ELM;
escreve só o que produz; no shell, só o que o papel usa — git de leitura e, conforme o papel, `add`/`commit` e os
comandos de build e verificação —, e o resto o Kiro pergunta. Merge,
rebase, `--force`, `reset --hard` e `git -C` (que esconde o subcomando das regras) são negados em todos; push com
confirmação a cada um (`ask`), só da branch da fatia, no orquestrador, no codificador, no revisor e no verificador —
e, no codificador e no orquestrador, o da base com os registros de situação (`backlog.md`, `sprints/**` e o
`status.md` da fatia, conferidos antes; quem desenvolve precisa de push na base); o merge do PR aprovado é do Dev
responsável, pelo codificador. Detalhes em
[`skills/sdd-setup/references/agentes.md`](skills/sdd-setup/references/agentes.md).

## Toolkits

O fluxo não sabe programar em nenhuma stack: o conhecimento de Java, Spring Batch, Angular, React etc. vem de
**toolkits** — pacotes de skills mantidos fora do power, um por tipo de projeto ou stack. A `sdd-setup` é a única
parte do fluxo que sabe procurá-los (`.kiro/toolkits/`, `~/.kiro/toolkits/`, powers instalados com `toolkit.json`,
ou skills com `metadata.toolkit`), detecta o tipo do projeto e **propõe, agente por agente**, as skills a ligar (uma confirmação por agente) —
num projeto 100% Spring Batch, o codificador recebe as de batch e Java que a pessoa escolher, e não as de REST ou
frontend. Contrato em [`skills/sdd-setup/references/toolkits.md`](skills/sdd-setup/references/toolkits.md) e
schema em [`toolkit.schema.json`](skills/sdd-setup/assets/toolkit.schema.json).

## IBM ELM

O ELM é o sistema de registro; o repositório guarda as propostas de mudança (PRD, fatias) e como cada mudança foi
feita. Mapeamento padrão (ajustável na setup): história → artefato *História de Usuário* (DOORS Next); regra →
*Regra*; termo → *Termos de Glossário*; épico → *Épico* (EWM); fatia → *Item de Backlog* que **implementa** as
histórias (sem épico, filho da `Manutenção`); item de Sustentação → *Item de Backlog* `[AT-nnn]`, filho do IB da
categoria; tarefas filhas na sprint; cenário verificado → *Caso de Teste* (ETM) que **valida** a história.
Cada história, regra e termo nasce como um conceito **OKF v0.2** na pasta da spec (o mesmo formato do bundle da
`sdd-sync`), com aprovação registrada em `verified`; sobe para o DOORS Next só depois do GATE, de baixo para cima,
com HF → REG como embed, sem nada extra no texto publicado e sempre com prévia e confirmação. Atributos e links entre
requisitos ficam registrados nos conceitos, porque o MCP não os grava. Detalhes em [`skills/sdd/references/elm.md`](skills/sdd/references/elm.md)
e [`skills/sdd-consolidar/references/elm-publicar.md`](skills/sdd-consolidar/references/elm-publicar.md).

Na consolidação, o agente cria no ETM um caso de teste por cenário verificado, com o link **valida**
(`elm_criar_ct`); sem permissão de criar no ETM, o `CT.csv` é importado à mão. O MCP `elm` ainda não grava atributos de requisito, links requisito↔requisito, módulos, change sets nem baselines: quando o
processo do projeto exige algum deles, a skill do passo entrega o roteiro manual e registra a pendência.

## Pré-requisitos

- Kiro IDE 1.x ou Kiro CLI 2.32+ na engine V3 (`--agent-engine v3`); repositório git com branch base e PRs. A
  engine V2 do CLI não lê as permissões dos agentes, nem o hook e os workflows; e `uv` para os scripts da setup e
  da `sdd-status`.
- Kiro Web não lê `~/.kiro`: os agentes do projeto aparecem lá, mas sem as skills do power — use a IDE ou o CLI.
- MCPs do próprio power (o `mcp.json` os sobe com `uvx`): [`mcp-elm`](https://pypi.org/project/mcp-elm/), que também consulta o
  bundle do ELM (`elm_*_local`, nunca lendo os arquivos), e [`mcp-gitlabpr`](https://pypi.org/project/mcp-gitlabpr/), que lista, lê e abre os PRs (merge
  requests do GitLab) — credencial em `~/.config/mcp-gitlabpr/gitlabpr.properties` (`url` e `token`). Repositório
  fora do GitLab, ou sem a credencial → o fluxo entrega título e descrição do PR, e a pessoa o abre.
- Opcional: IBM ELM — credencial em `~/.config/mcp-elm/elm.properties` e o `pa` gerado pela `sdd-setup`; MCP de consulta ao banco (somente leitura);
  MCP de browser/Playwright para verificar frontend; Kiro Workflows habilitado (IDE: `kiroAgent.workflows.enabled`;
  CLI: `chat.enableWorkflows`) para as receitas experimentais.
- Toolkits da stack do projeto (opcional — sem eles os agentes dependem do steering e do código vizinho).

Horas: **lançar ≠ concluir** — lançar é registro de empenho, a qualquer momento numa tarefa assumida (ao fechar a
sessão, por exemplo); concluir é da skill do papel, com o saldo. No AFK há a `[DEV]` e a `[APR] Aprovar PR`.

## Primeiros passos

1. Instale pelo painel **Powers** do Kiro (pasta `sdd` deste repositório ou uma cópia local).
2. No projeto, peça **"configurar o sdd"** e confirme as propostas (os padrões vêm marcados; uma confirmação por bloco).
3. Comece: **"nova demanda: …"** (a `sdd-triar` faz a triagem e registra no backlog; épico → PRD), **"iniciar a
   FT-031"** ou **"minha próxima tarefa"** (o hub `sdd-iniciar` diz a skill do papel), **"corrigir o defeito 4567"**
   (registra pela triagem, se preciso) — ou **"onde parei?"**.

Depois de atualizar o power ou um toolkit: "atualizar os agentes do sdd" — na 2.5.0 é obrigatório: os agentes
passam a carregar as skills de papel (`sdd-especificar`, `sdd-desenvolver`) e o hub `sdd-iniciar`, o `sdd-codificador`
ganha `git switch`, o `sdd-produto` a pasta `.kiro/local/especificacao/` e os anexos do EWM, e o revisor e o
verificador o ELM pelo power `elm` (`includePowers: true`, só para a própria tarefa); o servidor `elm` sai do
`mcp.json` do projeto. Requer o power `elm` ≥ 1.3.0 e o `mcp-elm` ≥ 1.0.42 (anexos; mudança de estado em várias transições).
Na 2.6.0, "atualizar os agentes do sdd" de novo: o `sdd-revisor` passa a gravar a revisão do PRD na pasta de
trabalho local, e o `sdd.md` ganha a linha "Padrões do EWM" ("atualizar a configuração do sdd"). Na 2.6.1, nada nasce no EWM
fora de sprint: épico, item de backlog e `[ATD]` são criados quando entram na sprint, com "Planejado para" = a
iteração dela; saem a opção `backlog no EWM` e a iteração de backlog dos "Padrões do EWM". `equipe.json`,
`acordos.md`, `roadmap.md` e `sprints/` voltam para a raiz da pasta do produto (sem a subpasta `planejamento/`). Na 2.6.2, a triagem commita na tarefa `[GB] Gerenciamento do backlog` (filha da
Sustentação, criada pela `sdd-elm` com ela) e a `sdd-elm` procura no EWM a iteração que falta no `pa_*.json` antes de
propor criar (requer o power `elm` ≥ 1.3.2). A 2.6.3 só acerta textos e exemplos (sem regra nova) e alinha a versão
das skills à do power. Na 2.7.0: a senioridade do Dev (Júnior, Pleno, Sênior) decide o modo da fatia e o GATE do
plano; a tarefa `[APR]` registra as aprovações do Dev Sênior; a trilha direta sai; o agente faz o push com
confirmação, abre o PR e o Dev leva a fatia até o merge (a `[DEV]` é concluída no merge); a troca AFK → HITL é
sugerida na conclusão do plano e feita pelo P.O. na base; a consolidação é do P.O. ou do SM, com horas na `[GB]`, e
cria os casos de teste no ETM; o bundle do ELM é consultado pelo `okf` e os PRs pelo `gitlabpr` (requer o power
`elm` ≥ 1.4.0 e o `mcp-elm` ≥ 1.0.43). Na 2.8.0, "atualizar a configuração do sdd" e "atualizar os agentes do sdd"
de novo: cada tarefa é assumida e concluída pela mesma skill de papel, e toda skill termina dizendo a próxima e
para. A `sdd-implementar` termina no PR; o merge do PR aprovado, as lições da fatia e a conclusão da `[DEV]` passam
para a `sdd-desenvolver` (Passo 6). A `[APR]` do plano sai da `sdd-plano` para a `sdd-revisar`, no `sdd-revisor`.
A ET *as-built* é escrita pelo Dev no PR, e a consolidação só a publica. A `sdd-especificar` leva o PRD aprovado
para a base e conclui a `[ESP]`, e a `sdd-prd` e a `sdd-fatiar` só conduzem o próprio GATE. O `equipe.json` é da
`sdd-planejamento` (modo inicial), não da setup. A 2.8.1 só encurta as descrições de `sdd-desenvolver`,
`sdd-implementar` e `sdd-revisar`, que passavam do limite de 1024 caracteres e eram puladas pelo Kiro (sem regra
nova; reinstale o power). Na 2.8.2, a linha "Padrões do EWM" do `sdd.md` cobre o IB e a Tarefa (categoria
obrigatória do IB, categoria de horas e OTR da Tarefa), e a `sdd-elm` copia o valor do item anterior ou pergunta em vez
de chutar — peça "atualizar a configuração do sdd" para preencher a linha. Na 2.9.0, cada sessão registra os créditos do Kiro que
gastou: o script `creditos.py` da `sdd-status` lê o consumo no `~/.kiro` de quem fecha a sessão, e a linha vai para o
`status.md` da fatia, para o `status.md` do épico (novo, criado pela `sdd-especificar`), para a ficha do AT ou para
"Créditos de gestão" na sprint; na conclusão, a soma vai para o `sprint-<nn>.md` e, na virada da sprint, para o
`backlog.md` (coluna `creditos`); a sprint também diz as versões do power usadas (`**Power sdd:**`). Peça "atualizar a configuração do sdd" (steering: nenhuma sessão termina sem registrar os créditos) e "atualizar os agentes do sdd"
(o orquestrador deixa os créditos do loop para o merge). Na **3.0.0**, o power `elm` foi incorporado: o MCP
`mcp-elm` 3.0 (reescrito) vem no `mcp.json` do `sdd`, lê o `.kiro/config/sdd/pa_<nome>.json` e expõe operações com
entrada e saída fixas; a `sdd-elm` e as skills `elm-ccm`/`elm-rm`/`elm-qm`/`elm-gc`/`elm-setup` saem — cada skill
chama a tool no próprio passo, e as regras comuns ficam em `sdd/references/elm.md`; a `sdd-setup` gera o `pa` (sem
migração do formato antigo: gere de novo); a `sdd-sync` passa a ser deste power; o MCP `okf` sai — o bundle local é consultado pelo próprio `elm` (`elm_buscar_req_local`, `elm_ler_req_local`, `elm_listar_req_local`, `elm_indexar_local`, em segundo plano; o `elm_sync baixar` não indexa — a `sdd-sync` pergunta). Os agentes passam a ser
**gerados** pelo `scripts/gerar_agentes.py` da `sdd-setup`, a partir do `papeis.json` do power e do
`.kiro/config/sdd/agentes.json` do projeto, só no formato V3 (sai o bloco V2): o shell libera só o que cada papel
usa (sem a política `read-only-shell`; o resto o Kiro pergunta), toda tool de power que o papel não usa é negada, e
todo papel com tarefa comenta e anexa nela (`elm_comentar`, `elm_anexo`). As receitas de workflow terminam no
mesmo ponto que as skills — o plano no GATE com a `[APR]`; a entrega AFK com o PR aberto e a `[APR] Aprovar PR` —,
com o último passo feito com a pessoa. Desinstale o power `elm`, peça "atualizar a configuração do sdd" e
"atualizar os agentes do sdd" (a setup monta o `agentes.json` com as respostas atuais). Projeto configurado com o power
`sdd2` ou com a v1 do `sdd`: desinstale o power antigo, instale este e peça "atualizar a configuração do sdd" — a
setup pergunta a pasta do produto, junta os steerings num só, renomeia hooks, workflows e agentes e move
`.kiro/produto/` e `.kiro/aprendizado/` com `git mv`.

Na **3.1.0**, o backlog do EWM volta a ser a cópia do `backlog.md` (desfaz o "nada nasce fora de sprint" da
2.6.1): épico, IB de fatia e `[ATD]` nascem no **backlog do produto** — a triagem cria o épico e a fatia sem épico,
o GATE do backlog os IBs das fatias, e a Sustentação e o `Atendimento` ficam lá —, já na sprint quando nascem
endereçados a uma; entrar na sprint só muda o "Planejado para". O backlog do produto é um só por projeto (pode
servir a várias entregas) e fica no `pa` (`ccm.backlog`): a setup pergunta se ele já existe (link ou id do plano)
ou o cria, com pai ou sem pai, pela nova tool `elm_backlog`; o `elm_iteracao` passa a criar só o plano da sprint.
Peça "atualizar a configuração do sdd" (configura o backlog e espelha no EWM o que está no `backlog.md`). Requer o
`mcp-elm` ≥ 3.1.0.

Na **3.2.0**, a consolidação vira pré-condição dos ritos de fechamento da sprint: antes da review, da
retrospectiva e da virada, a `sdd-planejamento` (e a `sdd-aprender`, na retrospectiva de sprint) lista as fatias
mergeadas que esperam a `sdd-consolidar` e para; só segue com a decisão do P.O., gravada em `**Fechamento sem
consolidar:**` no `sprint-<nn>.md` (essas fatias migram como `não consolidada`). O painel da `sdd-status` avisa no
último dia da sprint. Reinstale o power (sem mudança no `mcp-elm`).

Na **3.3.0**, três mudanças. (1) **A sprint traz o que nasceu no EWM por fora:** "sincroniza a sprint" (`sdd-planejamento`,
também depois de publicar a sprint e antes da review, da retrospectiva e da virada) lista as tarefas da iteração que
o sdd não conhece, infere o que cada uma é — tarefa de papel de uma fatia ou épico (`[DEV]`, `[ESP]`… abertas à mão,
por exemplo quando a sessão parou por limite de tokens) ou uma categoria de Apoio —, pergunta e as traz com o mesmo
id, renomeando o título ou incluindo o prefixo se for o caso; o painel da `sdd-status` conta as que estão por fora.
(2) **Sprints por iteração pai:** a sprint segue a iteração do EWM de que é filha — `sprints/2026/sprint-01.md`,
`sprints/2027/sprint-01.md`, chave `2026/01` no `backlog.md` e no `equipe.json`; o `elm_iteracao` recebe o caminho
`<pai>/<nome>` e cria o pai que faltar; a `sdd-setup` migra as sprints sequenciais (move e renumera dentro do pai).
(3) **Apoio:** o atendimento vira uma das categorias do Apoio — Atendimento `[ATD]` `AT-`, Implantação `[IMPL]` `IM-`,
Banco de dados `[BD]` `BD-`, Infra `[INF]` `IN-`, Operação `[OPE]` `OP-`, Apoio a outros times `[EXT]` `EX-` (tabela
**Apoio** do `sdd.md`); não há item nem tarefa "de Apoio" genérica. No EWM, cada categoria tem o IB
`<Categoria> <produto> - <iteração pai>`, filho do IB `Sustentação <produto> - <iteração pai>` e pai das tarefas
dela; ele nasce com o primeiro item triado da categoria no pai, e o id vai para a linha `Sustentação <pai>:` do
backlog (a Sustentação nasce com a primeira sprint de cada pai). As fichas ficam em `apoio/<categoria>/`
(`apoio/operacao/OP-001-…`). `## Atendimentos` vira `## Apoio` (com a coluna `categoria`) e `atendimentos/` vira `apoio/atendimento/` na
próxima escrita da triagem; os `AT-nnn` não mudam. A `sdd-atender` continua só para o Atendimento; as demais
categorias usam o fluxo mínimo da `sdd-iniciar` (iniciar a tarefa no ELM, registrar o trabalho, lançar horas,
concluir). Peça "atualizar a configuração do sdd" (seção Apoio e nome do produto no `sdd.md`, prefixos no `pa`,
migração das sprints) e "atualizar os agentes do sdd" (libera ao agente de produto a pasta local `.kiro/local/apoio/`). Requer o `mcp-elm` ≥ 3.3.0.

Na **3.3.1**, correções da 3.3.0. As tarefas de Apoio sem fluxo próprio (`[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]`) ganham
a skill **`sdd-executar`** (no agente `sdd-produto`), e a `sdd-iniciar` volta a só encaminhar. A Sustentação passa a ser
**uma por produto**: o IB `Sustentação - <produto>`, no backlog do EWM, com os IBs `<Categoria> - <produto>` filhos dela,
também no backlog; a linha do `backlog.md` é `Sustentação:`, e na troca de iteração pai só a `[GB]` muda. A sprint nova
herda o pai da anterior; pai novo só quando a pessoa diz, com o nome que ela der. Estrutura padrão no EWM:
`<linha de base>/Backlog` (plano `Backlog`) e `<linha de base>/<pai>/<sprint>` (cada sprint é uma iteração, com o
plano `<sprint> - <nome curto da meta>`); o caminho `<pai>/<sprint>` é relativo à linha de base, o pai da iteração do backlog
([elm-sprint.md](skills/sdd-planejamento/references/elm-sprint.md#estrutura-no-ewm-padrão)). O `mcp-elm` 3.3.5
resolve e cria assim, cria só o plano numa iteração que já existe, nunca escolhe nem cria uma terceira entre duas
homônimas (dois backlogs do time, duas `2026` no mesmo pai) e recusa caminho com parte vazia. A sprint nasce no EWM só
depois do "ok", com as datas e o plano `**Plano no EWM:**` do cabeçalho (`Sprint 01 - <nome curto da meta>`). Peça "atualizar a configuração do sdd" (backlog na linha de base) e "atualizar os agentes do sdd".
Requer o `mcp-elm` ≥ 3.3.5.

Na **3.4.0**, o `backlog.md` e a sprint passam a responder ao P.O. e ao SM o que falta fazer e o que cada sprint fez.
(1) **Situações gravadas por quem as causa**, no mesmo commit no `backlog.md` e na sprint
([backlog.md](skills/sdd-fatiar/references/backlog.md#situações)): fatia `nova → elegivel → planejada → iniciada →
pronta → concluida` (desvios `dividida`, `cancelada`) — `elegivel` passou na Definition of Ready (era `pronta`), e o Dev
grava `iniciada` na base antes da branch (no loop, o orquestrador) e `pronta` depois do merge, com o push perguntado e
os arquivos conferidos: quem desenvolve precisa de push na base; épico `novo → elegivel → planejado → iniciado →
concluido` (`cancelado`), com a especificação como uma fase dele (linha da Especificação `planejada → iniciada →
concluida`) e o fluxo detalhado (`rascunho → em-revisao → aprovado → fatiado → concluido`) na Fase do `status.md` do
épico, que nasce na triagem (o frontmatter do PRD perde o `status`); item de Sustentação `aberto → em-andamento →
concluido` (`cancelado`). (2) **Fases do `status.md`:** `aguardando-aprovacao-plano`, `aceita` (só HITL) e `pronta` no
lugar de `plano-em-revisao`, `pronta-para-merge` e `mergeada`; no AFK, `verificada` e `aguardando-aprovacao-pr`;
`pronta` e `concluida` só na base, que prevalece sobre a branch; conflito no merge → `retrabalho`. (3) **Sustentação no
lugar de Apoio**, com a mesma árvore no repositório e no EWM: `## Sustentação` com uma `### <Categoria>` por categoria
no backlog e na sprint, pastas `sustentacao/`, IBs `Sustentação`, `Manutenção` (pai das fatias sem épico) e
`<Categoria>` sem o nome do produto, um IB `[AT-nnn] <pedido>` por item e a tarefa `[ATD] AT-nnn …` só quando o item
entra numa sprint; a reserva é de Sustentação + retrabalho (a Manutenção entra pela vazão). (4) **Uma tabela
`## Fatias`**, com a coluna `origem` (`EP-nn` ou `Manutenção`); a fatia que veio de um atendimento leva `vinculada a
[AT-…]` na `obs` e o link `relacionado` no EWM. (5) **Formatos:** prioridade `baixa · média · alta · crítica`; coluna `elm` com
o tipo antes de cada id (`IB`, `DEV`, `DF`…); créditos em todas as tabelas; chave da sprint `2026/Sprint 03`; as
Observações `migrada para`/`migrada de <chave>` no lugar do `→ sprint <chave>`; o lote da triagem filtra pela iteração
do backlog. (6) **Só Scrumban:** sai a escolha entre Scrum e Kanban nos acordos e a chave `cadencia` do `equipe.json`. O
`sdd-codificador` e o `sdd-orquestrador` passam a gravar `backlog.md` e `sprints/**` e a dar o push da base com
pergunta. Sem migração: o power ainda não tem usuários — e saem as regras de compatibilidade e migração das versões
anteriores. Requer o `mcp-elm` ≥ 3.3.5 (sem mudança no MCP).

Na **3.4.1**, a sincronização com o EWM ("sincroniza a sprint", `sdd-planejamento`) passa a comparar também o que
mudou no EWM nos itens que os arquivos já conhecem — estado, iteração, dono e estimativa —, e não só as tarefas
criadas por fora: lista a iteração da sprint sem filtro de tipo e mostra **uma tabela** com todas as divergências e as
tarefas por fora, cada linha com a solução proposta (`arquivo:`, `EWM:`, `manter:`, `encaixe` ou `triar`); "ok" aplica
tudo, ou a pessoa ajusta uma ou mais linhas, e o que muda o escopo (o item que sai da sprint, o encaixe, o épico que
entra com a `[ESP]`) espera o "sim" do P.O. A situação da fatia e do épico nunca muda pelo estado do EWM; na
Sustentação, o arquivo recebe o EWM. Nada diverge → sempre a linha `🔄 <chave> × EWM: iguais — <n> itens conferidos`,
também na pré-condição da review, da retrospectiva e da virada (o agente não diz mais que "não é preciso
sincronizar"); o painel da `sdd-status` conta as tarefas por fora, as divergências e os ids a conferir. A virada move
no EWM só o que está aberto — o que fechou fica na iteração em que fechou, com as horas —, depois de criar a iteração
da próxima sprint e antes de publicar as linhas novas dela; a sprint gravada antes de ser publicada leva
`**Publicação no EWM:** pendente` no cabeçalho, e nenhuma skill passa a iteração dela ao MCP antes da publicação, que
a acha dentro da linha de base do produto. O item que volta a uma sprint leva as tarefas que ficaram no backlog do
EWM, que movem com o dono e a estimativa do papel em vez de nascer de novo, e ganha linha nova (a com `saiu da sprint`
fica como histórico). Requer o `mcp-elm` ≥ 3.3.5 (sem mudança no MCP).

Na **3.4.2**, todo item triado nasce no backlog do EWM, e a sincronização leva o sdd até onde o trabalho chegou. (1)
**Base no EWM desde o início:** o modo inicial da `sdd-planejamento` cria o IB `Sustentação` e a `[GB] Gerenciamento
do backlog` na iteração de backlog; a `[GB]` move para a primeira sprint de cada pai. Todo IB triado nasce no backlog
no estado inicial e volta a ele quando o item sai da sprint. (2) **A `[GB]` é do SM:** só o SM lança horas nela; o
P.O. nunca lança, nem quando também é o SM (a mesma pessoa pode ter os dois papéis), e o `equipe.json` exige um SM
ativo. Toda sessão do P.O. ou do SM no agente de produto registra os créditos num comentário na `[GB]`. (3)
**Desenvolvimento por fora do sdd:** quando os tokens acabam, a pessoa segue sem agente (código, PR, merge, tarefas no
EWM), e a "sincroniza a sprint" cruza o EWM (a sprint e o backlog), o `status.md` com a fase, o `sprint-<nn>.md` com o
`backlog.md` e o git (branch, PR, merge): o PR mergeado por fora vira `pronta`, com a `[DEV]` concluída e a `[APR]`, a
`[REV]` e a `[VER]` canceladas; o PR aberto ou a branch com commits, `iniciada`; as tarefas fora do esperado pela fase
do `status.md`, o IB do backlog fora do estado inicial e o WI que sumiu do EWM também ganham linha. A rede de proteção
dos ritos passa a rodar dentro da sincronização, e a tabela agrupa as linhas por item. (4) **Tarefa já fechada na
retomada:** a `sdd-desenvolver`, a `sdd-atender` e a `sdd-executar` mostram o estado e oferecem reabrir ou fechar o
item. (5) **Cancelar pelo MCP:** o `elm_transicao` ganha o alvo `cancelar`, e a pendência de cancelamento fica só para
a falha. Requer o `mcp-elm` ≥ 3.4.2.

Na **3.4.3**, o item do backlog que ficou sem IB chega ao EWM sem esperar a sprint: o backlog do EWM é a fonte dos
relatórios das demandas. O espelhamento (§0, passo 4 do `elm-sprint.md`) passa a rodar na triagem (em toda sessão,
antes do primeiro item), na "sincroniza a sprint" (linha `EWM: criar no backlog`) e em "atualizar a configuração do
sdd", também com o backlog do EWM já configurado. O IB `Sustentação`, `Manutenção` ou de categoria com título
parecido (`Sustentação - <produto>`) e sem o id no `backlog.md` é perguntado, e não nasce outro. O painel da
`sdd-status` conta os itens sem IB. Requer o `mcp-elm` ≥ 3.4.2 (sem mudança no MCP).

Na **3.4.4**, o `pa.schema.json` é publicado no repositório [`dxaraujo/mcps`](https://github.com/dxaraujo/mcps), em
`https://dxaraujo.github.io/mcps/elm/pa.schema.json` (o `$id` e o `$schema` dos `pa_*.json`). O power e o `mcp-elm`
guardam cópias iguais à publicada; com o `mcps` clonado ao lado, os testes conferem. Sem mudança no fluxo.

Na **3.5.0**, a `sdd-sync` ganha a visualização do bundle: `elm_explorar_local` gera o `explorar.html` na pasta do
bundle — HTML único que abre o bundle no navegador sem internet, em galáxias (planeta = documento, lua = chunk do
planeta selecionado), na vista 3D (3d-force-graph/three.js) ou 2D (Cytoscape.js), com busca e filtros por tipo, pasta
e galáxia e Markdown. Os documentos e vetores saem do índice local em modo somente leitura: sem índice, a skill indexa
antes (`elm_indexar_local`); a skill oferece a visualização junto com a indexação depois de um download, e o
`explorar.html` vive no bundle (fora do git). A tool entra no catálogo `mcp_do_power` do `papeis.json` — negada a todo
agente, porque a `sdd-sync` roda na sessão padrão. Requer o `mcp-elm` ≥ 3.6.4 (a tool e os assets do visualizador são
novos nessa versão).

Não use o `/upgrade-agent` (nem `kiro-cli agent upgrade`) nos agentes `sdd-*`: quem os gera é o script da setup
("atualizar os agentes do sdd").

## Como foi verificado

**Documentação oficial do Kiro**, lida inteira nas páginas `.md` de `kiro.dev/docs` em 14/10/2026 (powers, skills,
steering, custom agents e referência de configuração, subagentes, permissões, hooks, specs, workflows, CLI V3 e
migração), mais o schema do `plugin.json` (Agent Plugins) e a especificação Agent Skills. Uma auditoria do power
contra essas páginas gerou as correções desta versão: `git -C` negado, leitura restrita, confirmação de push e PR,
delegação a subagente sem pergunta por agente, falha do hook na saída de erro, pausa e falha dos passos de workflow
por `send_message`, chamada HTTP do verificador por script.

Com o **Kiro CLI 2.31.0** (o binário oficial), na 2.x, quando os agentes eram templates no formato universal (V2 + V3):

- `kiro-cli powers install <pasta>` instala o power em `~/.kiro/powers/installed/sdd/`, com todas as skills,
  `references/` e `assets/` — o caminho que a setup usa nos agentes;
- o bloco `permissions` dos templates foi gerado pelo próprio `kiro-cli agent upgrade` a partir do `toolsSettings`
  (V2) e conferido regra a regra; depois receberam o que só existe na V3: `skill` liberada (com leitura restrita o
  conversor avisa que cada skill pediria aprovação), `ask` de push/PR no orquestrador e de `curl`/`wget` no
  verificador. `subagent/<nome>` em `tools` e a regra `subagent` vêm do conversor (de `availableAgents` e
  `trustedAgents`);
- os seis agentes, com os placeholders preenchidos, passam no `kiro-cli agent validate`, aparecem no
  `kiro-cli agent list`, e o `kiro-cli agent upgrade --dry-run` os deixa intactos (`out of sync (not rebuilt)`);
- o formato `.md` de agente **não** é carregado pela engine V2 do CLI (ainda a padrão), por isso os agentes são
  JSON universais; padrões de comando encadeado (`cd … && …`) são descartados pelo conversor, por isso as
  permissões usam comandos simples;
- o `http.sh` foi exercitado contra um servidor local (método, caminho e corpo fora da pasta `massa/` recusados).

Com o **Kiro CLI 2.32.0**, engine V3 (23/10/2026), os agentes gerados pelo `gerar_agentes.py`: os seis passam no
`kiro-cli agent validate`; numa conversa sem interação, comando liberado roda, comando fora da lista e exceção
(`git log --output`) caem em aprovação, e `git commit -n` e push para a base são negados pela regra; as duas
receitas passam no validador do Kiro ao iniciar e param no primeiro passo com uma fatia inexistente. Não foi
possível abrir a IDE.

**O que a documentação não resolve** (comportamento a observar no primeiro uso): o formato do `.config.kiro` das
specs; EARS em português no Analyze Requirements; se os subagentes somam ou intersectam os `allow` de quem os
chama (a doc diz "deny-wins intersection" — se um subagente do loop falhar por permissão, libere o comando também
no orquestrador); o alcance de `trustedAgents`; e as páginas de
steering e de configuração divergem sobre agentes herdarem o steering padrão (a setup oferece
`chat.disableInheritingDefaultResources` no CLI).

## Limitações conhecidas e próxima versão

- O Kiro só valida uma receita quando a execução começa: a setup confere o JSON e os agentes citados.
- Kiro Workflows é experimental: as receitas são opcionais; `/workflow-run` exige a IDE 1.3+.
- **Próxima versão:** toolkits oficiais (backend Java/Spring, Spring Batch, frontend Angular/React); execução automatizada dos
  casos de avaliação que a `sdd-aprender` já guarda em `<produto>/aprendizado/avaliacoes/`; e — quando o MCP do ELM
  suportar — atributo de chave, links entre requisitos, módulos, change sets e baselines automáticos.

## Fontes (consultadas em 13 e 14/10/2026)

- Andrej Karpathy — *Software Is Changing (Again)*, YC AI Startup School, jun/2025 · *2025 LLM Year in Review*,
  dez/2025 · notas sobre programar com agentes, jan/2026 · [autoresearch](https://github.com/karpathy/autoresearch),
  mar/2026 · [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), abr/2026 · Sequoia AI
  Ascent, abr/2026
- Matt Pocock — [mattpocock/skills](https://github.com/mattpocock/skills) (v1.3.1, out/2026: `grilling`, `to-spec`,
  `to-tickets`, `tdd`, `code-review`, `triage`, `retro`) · *Software Fundamentals Matter More Than Ever*, AI Engineer
  Europe 2026 · dicas de Ralph, jan/2026
- Dex Horthy / HumanLayer — [12-factor agents](https://github.com/humanlayer/12-factor-agents) ·
  [Advanced Context Engineering](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents) ·
  *No Vibes Allowed*, nov/2025 · *Everything We Got Wrong About RPI*, mar/2026 · *Why Software Factories Fail*, jul/2026
- Geoffrey Huntley — *Ralph Wiggum as a software engineer*, 2025 · [Ralph Playbook](https://github.com/ghuntley/how-to-ralph-wiggum), jan/2026
- Anthropic Engineering — *Effective context engineering for AI agents* (set/2025) · *Effective harnesses for
  long-running agents* (nov/2025) · *Demystifying evals for AI agents* (jan/2026) · *Harness design for long-running
  application development* (mar/2026) · [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- Boris Cherny — fios sobre o fluxo de trabalho com Claude Code, jan/2026
- Simon Willison — *The lethal trifecta* (jun/2025) · *Vibe engineering* (out/2025) · *Agentic Engineering Patterns* (2026)
- Kent Beck — *Augmented Coding: Beyond the Vibes* (jun/2025) · crítica ao SDD citada por Martin Fowler (jan/2026)
- Birgitta Böckeler / Martin Fowler — [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
  (out/2025) · *Harness Engineering* (2026) · *Are Harnesses Worth the Cost?* (out/2026)
- Addy Osmani — *How to write a good spec for AI agents* (jan/2026) · *Comprehension debt* (mar/2026) · *Loop Engineering* (jun/2026)
- Mitchell Hashimoto — *My AI Adoption Journey* (fev/2026) · Armin Ronacher — *The Coming Loop* (jun/2026)
- Thoughtworks Technology Radar vol. 33 (nov/2025) e vol. 34 (abr/2026) · DORA *State of AI-assisted Software
  Development* 2025 · [GitHub Spec Kit](https://github.com/github/spec-kit)
- Kiro — [docs](https://kiro.dev/docs/) (powers, skills, custom agents, steering, specs, hooks, workflows),
  [kirodotdev/powers](https://github.com/kirodotdev/powers), [Agent Plugins](https://github.com/agentplugins/agent-plugins-spec),
  [Agent Skills](https://agentskills.io/specification)
- IBM — ELM 7.2 (dez/2025) · Engineering AI Hub 1.3/1.4 (MCP oficial, agente de geração de testes) · vocabulário
  [OSLC RM](https://github.com/oslc-op/oslc-specs)

## Licença

[MIT](../../LICENSE)
