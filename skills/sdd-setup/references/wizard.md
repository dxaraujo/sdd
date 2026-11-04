# Cartões do wizard — o que a pessoa vê

A setup é a porta de entrada do produto. Toda mensagem dela é um destes cartões, **copiado como está**: troque só
o que está entre `<…>`, apague as linhas marcadas `(se …)` quando a condição não vale e nunca invente ícone,
coluna ou formato. O que está entre `<…>` descreve o campo — **nunca é valor sugerido**: tudo vem do projeto, do ELM
ou da pessoa. `<a | b>` no cartão = escolha **uma** das opções (o `|` não vai para a tela). Tabela sem linha para mostrar → a linha `| — | nada a mostrar | ➖ |`; nunca linha em branco
como separador.

## Legenda (fixa — só estes ícones)

| Uso | Ícones |
|---|---|
| Trilha das etapas | `●` feita · `◉` atual · `○` por vir |
| Status | ✅ ok · ⚠️ atenção · ❌ falhou · ⏸️ não testado (sempre com o motivo) · ➖ não se aplica |
| De onde veio o valor | 🔍 detectado · 📐 padrão do sdd · 🙋 você · 🧩 ELM |
| Seleção (primeira coluna da tabela) | `[✅]` marcado · `[ ]` desmarcado |
| Permissão do agente | 🟢 livre · 🟡 pergunta antes · 🔴 negado |
| Modo | ✨ configuração inicial · 🔄 atualização |

"✅" só com resposta real (comando que rodou, MCP que respondeu); falhou por rede ou credencial → ⏸️ com o motivo,
nunca "testado".

## Peças de todo cartão

**Cabeçalho** (primeira linha de toda mensagem de etapa; a trilha tem 9 posições):

```
## 🧭 Etapa <n> de 9 · <nome da etapa>
`<●●◉○○○○○○>` <uma frase: o que esta etapa decide>
```

**Pergunta** (última coisa da mensagem; **uma** por mensagem):

```
> ❓ **<pergunta>**
> `ok` aceita tudo · `<n>: <novo valor>` muda a linha <n> · `voltar` refaz a etapa anterior
```

Escolha numa lista → as opções numeradas logo acima da pergunta, a recomendada com `⭐ (recomendado)`.

**Fechamento** (uma linha, antes do cabeçalho da etapa seguinte):

```
✔ **<nome da etapa>** — <valor 1> · <valor 2> · <valor 3>
```

**Trabalhando** (uma linha antes de ler ou rodar várias coisas; nada de narrar cada ferramenta):

```
🔎 <Lendo o projeto | Rodando os comandos | Consultando o ELM>…
```

**Bloqueio** (algo impede seguir):

```
### ⚠️ <o que aconteceu, em uma frase>
| # | Opção | O que acontece |
|---|---|---|
| 1 | <corrigir agora> | <…> |
| 2 | <seguir sem> | <…> |
| 3 | parar aqui | nada é gravado |
```

## W0 · Boas-vindas e pré-checagem (Passo 0)

```
## 👋 Configurar o sdd · <projeto>
<✨ configuração inicial | 🔄 atualização da configuração de <data do sdd.md>>

O sdd organiza o trabalho do time em fatias pequenas — plano aprovado, teste primeiro, revisão e verificação
independentes, PR lido por uma pessoa e o ELM como registro —, em sprints com fluxo puxado (Scrumban). São
**9 etapas** — e **nada é gravado antes da etapa 8**, quando você confere tudo numa tela só.

| # | Etapa | O que decide |
|---|---|---|
| 1 | Projeto | tipo, stack e steering |
| 2 | Comandos | compilar, testar, cobertura — rodados uma vez |
| 3 | Git, PR e banco | branch base, abertura de PR, consulta ao banco |
| 4 | Produto e ELM | pasta do produto, glossário, ADRs, project area |
| 5 | Skills | o que o projeto já sabe fazer |
| 6 | Agentes | o que cada um dos 6 agentes pode usar |
| 7 | Automação | hook, workflows e autonomia |
| 8 | Revisão e gravação | tudo numa tela; só então grava |
| 9 | Validação | confere e diz o próximo passo |

### Pré-checagem
| # | Item | Status |
|---|---|---|
| 1 | Repositório git | <✅ `<raiz>` | ❌ sem git — o fluxo depende de branches e PRs> |
| 2 | Power sdd | <✅ `~/.kiro/powers/installed/sdd` | ❌ não achei — onde está?> |
| 3 | Shell | <✅ bash/zsh | ✅ fish — comandos compostos vão em `bash -c '…'`> |
| 4 | `uv` (gera os agentes) | <✅ <versão> | ❌ instale: https://docs.astral.sh/uv/> |
| 5 | `kiro-cli` (valida os agentes) | <✅ <versão> | ➖ sem ele, a validação da etapa 9 é só a do gerador> |
| 6 | Credencial do ELM | <✅ responde como `<usuário>` | ⏸️ <motivo> | ➖ projeto sem ELM> |
| 7 | Credencial do GitLab | <⏸️ arquivo existe — a conexão é testada na etapa 3 | ❌ sem arquivo — modelo na etapa 3> |

O Kiro pede licença para ler os arquivos do power (cartões, modelos, gerador): `Always allow` evita a mesma
pergunta a cada etapa.

> ❓ **Começamos pela etapa 1?**
> `ok` começa · `<n>: …` corrige um item da pré-checagem
```

## W0-A · Modo atualização (Passo 0)

No lugar da tabela de etapas do W0 (a pré-checagem continua):

```
### 🔄 Configuração atual
| # | Etapa | Hoje | Mudou desde então |
|---|---|---|---|
| 1 | Projeto | <tipos · linguagem e versão · frameworks principais> | <➖ | ⚠️ <o que mudou no repositório>> |
| 2 | Comandos | <compilar · testes · cobertura> | <➖ | ⚠️ …> |
| 3 | Git, PR e banco | <base `<…>` · PR <…> · banco <…>> | <➖ | ⚠️ …> |
| 4 | Produto e ELM | <`<pasta>` · `pa_<nome>.json`> | <➖ | ⚠️ …> |
| 5 | Skills | <n> skills · <n> agentes do projeto | <➖ | ⚠️ <n> novas: `<…>` · <n> sumiram: `<…>`> |
| 6 | Agentes | gerados pelo power <versão> | <➖ | ⚠️ power atualizado → regenerar> |
| 7 | Automação | hook <[✅] | [ ]> · workflows <[✅] | [ ]> | <➖ | ⚠️ …> |

> ❓ **O que muda?**
> `nada` só regenera agentes, hook e workflows · `<n>` refaz a etapa <n> · `<n>,<m>` refaz várias
```

## W1 · Projeto (Passo 1)

```
## 🧭 Etapa 1 de 9 · Projeto
`◉○○○○○○○○` Entendi o projeto assim — confira.

| # | Item | Valor | Fonte |
|---|---|---|---|
| 1 | Tipos | <tipos detectados — tabela de toolkits.md> | 🔍 <sinal e arquivo onde apareceu> |
| 2 | Stack | <linguagem e versão · frameworks · banco> | 🔍 <arquivo de build> |
| 3 | Módulos | <único | lista dos módulos> | 🔍 <arquivo de build> |
| 4 | Testes e cobertura | <framework de teste · ferramenta de cobertura e gate | sem cobertura> | 🔍 <arquivo de build> |
| 5 | Steering de produto | <✅ `.kiro/steering/product.md` | ❌ não há> | 🔍 |
| 6 | Steering de tecnologia | <✅ `.kiro/steering/tech.md` | ❌ não há> | 🔍 |
| 7 | Steering de estrutura | <✅ `.kiro/steering/structure.md` | ❌ não há> | 🔍 |
| 8 | Regras críticas | <1. … 2. … | nenhuma além do steering> | 🔍 <tech.md> |

> ❓ **Está certo?**
> `ok` aceita tudo · `<n>: <novo valor>` muda a linha <n> · steering ❌ → `<n>: <arquivo>`, `<n>: gerar` ou `<n>: nenhum`
```

## W2 · Comandos (Passo 2)

Duas mensagens: a proposta (Status `⏸️ ainda não rodado`) e, depois do `ok`, o mesmo cartão com o resultado
**de cada comando rodado** e a pergunta `> ❓ **Fecho os comandos assim?**`. `pular` → Status `⏸️ você pulou`.

```
## 🧭 Etapa 2 de 9 · Comandos
`●◉○○○○○○○` Backpressure: o que o agente roda a cada tarefa para provar que não quebrou nada.

| # | Ação | Comando | Status | Fonte |
|---|---|---|---|---|
| 1 | Compilar | `<comando do projeto>` | <✅ <tempo> | ❌ <erro em uma linha> | ⏸️ ainda não rodado> | 🔍 <arquivo de onde veio> |
| 2 | Testes | `<…>` | <…> | <…> |
| 3 | Teste único | `<… -Dtest={alvo} …>` | <…> | <…> |
| 4 | Lint | `<… | não há>` | <… | ➖> | <…> |
| 5 | Cobertura e gate | `<…>` · <gate> | <…> | <…> |
| 6 | Executar a aplicação/job | `<…>` | <…> | <…> |
| 7 | Verificar um cenário | <como o tipo do projeto verifica — tabela de toolkits.md> | ➖ | 📐 <tipo do projeto> |
| 8 | Massa de teste | `<dev/seeds>` | <✅ existe | ❌ não há> | 🔍 |

> ❓ **Rodo os comandos 1 a 5 uma vez para confirmar?** (recomendado — backpressure que não roda não é backpressure)
> `ok` roda · `pular` segue sem rodar · `<n>: <novo comando>` troca um
```

## W3 · Git, PR e banco (Passo 3)

```
## 🧭 Etapa 3 de 9 · Git, PR e banco
`●●◉○○○○○○` Para onde vão as branches, como o PR é aberto e como o agente consulta o banco.

| # | Item | Valor | Status | Fonte |
|---|---|---|---|---|
| 1 | Branch base | `<branch>` | ✅ | 🔍 <sinal: origin/HEAD · destino dos merges · única remota> |
| 2 | Prefixo das branches | `<feature/>` | ✅ | 🔍 <branches remotas> |
| 3 | Padrão de commit | `<Task <id> - <descrição>>` | ✅ | 🔍 <git log> |
| 4 | PR (merge request) | <MCP `gitlabpr` | entregar título e descrição> | <✅ respondeu | ⏸️ sem rede — testo de novo na etapa 9 | ❌ sem credencial> | 🔍 |
| 5 | Banco (só consulta) | <`banco/consultar` | não há> | <✅ | ⏸️ …> | 🔍 <.kiro/settings/mcp.json> |
| 6 | Artefatos de produto | direto na branch base | ➖ | 📐 fixo |
| 7 | Push na base para quem desenvolve | requisito: o Dev grava ali a situação da fatia (`iniciada`, `pronta`) | ⚠️ confira no GitLab se a `<branch>` protegida aceita o push dele — sem isso, nenhuma fatia começa | 📐 fixo |

(se a branch base for ambígua) mostre os candidatos **antes** desta tabela e pergunte só isso:

| # | Branch | Sinal |
|---|---|---|
| 1 | `<branch>` ⭐ (recomendado) | <sinal mais forte: destino de <n> dos últimos <m> merges> |
| 2 | `<master>` | <origin/HEAD> |
```

## W4 · Produto e ELM (Passo 4)

```
## 🧭 Etapa 4 de 9 · Produto e ELM
`●●●◉○○○○○` Onde o produto mora no repositório e como o fluxo conversa com o ELM.

| # | Item | Valor | Fonte |
|---|---|---|---|
| 1 | Pasta do produto | `<.kiro/planejamento>` — backlog, épicos, PRDs, aprendizado | <🔍 backlog.md existente | 📐> |
| 2 | Glossário | <`docs/glossario.md` (existe) | `docs/glossario.md` (será criado) | não há> | <🔍 | 📐 | 🙋> |
| 3 | ADRs | <`docs/adr` (existe) | `docs/adr` (será criada) | não há> | <🔍 | 📐 | 🙋> |
| 4 | Usa ELM | <sim — `pa_<nome>.json` | não> | <🔍 | 🙋> |
| 5 | Bundle do RM | <`docs/elm/<nome>` · <n> documentos | não baixado — `sdd-sync` depois | ➖> | <🔍 | 🧩> |
| 6 | Regras do ELM | publicar requisitos na aprovação · ET não publica · fatia dividida = filhos do item | 📐 |
```

Montagem do `pa` (só quando falta): um cartão por bloco, com o cabeçalho
`### 🧩 ELM · Bloco <n>/10 · <nome do bloco>` e a trilha de 11 posições (blocos 0 a 10) — formato e regras em
[elm-pa.md](elm-pa.md).

## W5 · Skills (Passo 5)

```
## 🧭 Etapa 5 de 9 · Skills
`●●●●◉○○○○` O que já existe para os agentes usarem. Na próxima etapa você escolhe, agente por agente.

| # | Skill | Para quê | Origem | Toolkit |
|---|---|---|---|---|
| 1 | `<nome da skill>` | <início da description> | <projeto | usuário | power `<nome>`> | <`<nome>` 🔍 detectado | —> |

Agentes do projeto (podem virar subagentes do codificador e do orquestrador):

| # | Agente | Para quê | Status |
|---|---|---|---|
| 1 | `<nome do agente>` | <início da description> | <✅ | ⚠️ tem campo `hooks` — a IDE ignora> |

> ❓ **Falta alguma skill ou agente que eu não achei?**
> `ok` segue · `<caminho>` acrescenta
```

## W6 · Um agente (Passo 6) — seis cartões, um por mensagem

```
## 🧭 Etapa 6 de 9 · Agentes — <n> de 6 · `sdd-<papel>`
`●●●●●◉○○○` <papel em uma frase: ex. "planeja e implementa uma fatia por sessão, até o merge">

**Já vem do fluxo:** <desenvolver · plano · implementar · iniciar · status>

| | # | Skill | Para quê · origem |
|---|---|---|---|
| <[✅] | [ ]> | 1 | `<nome da skill>` | <início da description> · <projeto | usuário | toolkit `<nome>` 🔍> |

| | # | MCP | Acesso |
|---|---|---|---|
| [✅] | <n> | `elm` | <🟢 consulta · 🟡 escrita na própria tarefa | 🟢 só o bundle local> |
| <[✅] | [ ]> | <n> | `<banco/consultar>` | 🟢 só consulta |
| [✅] | <n> | `gitlabpr` | <🟢 consulta · 🟡 abrir e mesclar PR | 🟢 consulta · 🟡 abrir PR | 🟢 consulta> |

(se o agente tem subagentes — produto, codificador, orquestrador: os do fluxo, da tabela do Passo 6, mais os do projeto)
| | # | Subagente | Para quê |
|---|---|---|---|
| [✅] | <n> | `sdd-revisor` | análise do plano e revisão do código |
| [ ] | <n> | `<agente do projeto>` | <início da description> |

| Item | Valor |
|---|---|
| Push | <🟡 pergunta a cada push (só a branch da fatia) | 🟡 pergunta a cada push (a branch da fatia e, na base, só os registros de situação) | 🔴 negado> |
| Modelo | padrão do Kiro |

> ❓ **Confirma o `sdd-<papel>`?**
> `ok` · `tirar 3,5` · `pôr 7` · `só 1,2` · `nenhuma skill` · `modelo: <nome>` · `as mesmas do sdd-<outro>`
```

Linhas numeradas em sequência pelas três tabelas (skills, MCPs, subagentes), para "tirar 3,5" valer em qualquer uma.
As linhas `elm` e `gitlabpr` são fixas do papel (não se tiram por projeto); a do `gitlabpr` só existe no produto,
codificador, revisor e orquestrador — o MCP serve só ao PR.
Toda opção aparece — marcada ou não —, na ordem: marcadas primeiro, depois as desmarcadas. Depois de um ajuste,
mostre o cartão de novo com as caixas atualizadas antes de pedir o "ok" final do agente.

## W7 · Automação e autonomia (Passo 7)

```
## 🧭 Etapa 7 de 9 · Automação e autonomia
`●●●●●●◉○○` O que roda sozinho e o que sempre passa por uma pessoa.

| # | Item | Valor | Fonte |
|---|---|---|---|
| 1 | Hook `sdd-backpressure` | <[✅] compila e testa depois de cada tarefa | [ ] sem comandos> | 📐 |
| 2 | Workflows `sdd-planejar-fatia` · `sdd-entregar-fatia` | <[✅] instalados — você dispara no chat | [ ] ficam de fora — recurso desligado na IDE e no CLI> | 🔍 <IDE `kiroAgent.workflows.enabled` | CLI `chat.enableWorkflows`> |
| 3 | GATE do plano | pela senioridade: Júnior sempre · Pleno pergunta · Sênior nunca | 📐 fixo |
| 4 | Paralelo no loop | 1 fatia por vez (máx. 3) | 📐 |
| 5 | Push e PR no loop | 🟡 o Kiro pergunta a cada lote | 📐 |
| 6 | Push pelos agentes | 🟡 pergunta sempre — na base, só os registros de situação da fatia, com os arquivos conferidos · 🔴 nunca `--force` | 📐 fixo |
| 7 | Chamada HTTP do verificador | <[✅] `.kiro/sdd/http.sh` → `<url de teste>` | ➖ projeto sem HTTP> | <🙋 | 📐> |
```

## W8 · Revisão final (Passo 8)

```
## 🧭 Etapa 8 de 9 · Revisão e gravação
`●●●●●●●◉○` Tudo numa tela. Nada foi gravado ainda, além dos rascunhos de configuração abaixo.

### Projeto
| Item | Valor |
|---|---|
| Projeto | <nome> · <tipos> · <stack> |
| Comandos | compilar `<…>` · testes `<…>` · cobertura `<…>` (<✅ rodados | ⏸️ não rodados>) |
| Git | base `<…>` · prefixo `<…>` · commit `<…>` · PR <…> |
| Produto | `<pasta>` · glossário <…> · ADRs <…> |
| ELM | <`pa_<nome>.json` ✅ válido · time <…> | não usa> |
| Automação | hook <[✅] | [ ]> · workflows <[✅] | [ ]> · paralelo <n> |

### Agentes
<a tabela que o gerador imprimiu (sem `--gravar`), colada como está — mesmas colunas, mesma ordem>

### Arquivos
| Arquivo | Ação |
|---|---|
| `.kiro/steering/sdd.md` | <criar | alterar — diff abaixo | manter> |
| `.kiro/config/sdd/agentes.json` | rascunho gravado (o Kiro não carrega) |
| `.kiro/config/sdd/pa_<nome>.json` | <gravado e validado no bloco 10 | manter | ➖> |
| `.kiro/agents/sdd-*.json` (6) | <criar | alterar — diff abaixo> |
| `.kiro/hooks/sdd.json` | <criar | alterar | ➖> |
| `.kiro/workflows/sdd-*.workflow.json` (2) | <criar | alterar | ➖> |
| `.kiro/sdd/http.sh` | <criar | ➖> |
| `<produto>/` | <criar backlog.md, aprendizado/licoes.md, fatias/ | acrescentar <…> | manter> |
| `<glossário>` | <criar | manter | ➖ não há> |
| `<pasta de ADRs>/` | <criar com README.md | manter | ➖ não há> |
| `.gitignore` | <acrescentar `.kiro/local/` | manter> |

O Kiro pede confirmação para cada arquivo em `.kiro/agents`, `.kiro/hooks` e `.kiro/workflows` — se recusar um
por engano, diga `regravar <arquivo>`.

> ❓ **Gravo tudo?**
> `ok` grava · `<item>: <mudança>` ajusta antes · `parar` sai sem gravar (os rascunhos ficam em `.kiro/config/sdd/`)
```

## W9 · Validação e pronto (Passo 9)

```
## 🧭 Etapa 9 de 9 · Validação
`●●●●●●●●◉` Conferindo o que foi gravado.

| # | Verificação | Status |
|---|---|---|
| 1 | Agentes gerados = os combinados (tabela do gerador) | <✅ | ❌ <diferença>> |
| 2 | `kiro-cli agent validate` nos 6 | <✅ | ❌ <agente: campo> | ➖ sem kiro-cli> |
| 3 | Hook e workflows fazem parse; agentes citados existem | <✅ | ❌ | ➖> |
| 4 | `pa` do ELM válido (`elm_status`) | <✅ | ❌ <faltando> | ➖> |
| 5 | GitLab responde (`gitlab_listar_mrs`) | <✅ | ⏸️ <motivo> | ➖> |
| 6 | Caminhos citados no `sdd.md` e nos agentes existem | <✅ | ❌ <caminho>> |
| 7 | Ferramentas que varrem a raiz ignoram `.kiro/local/` | <✅ | ⚠️ <ferramenta>> |
| 8 | Workspace confiável no Kiro | <✅ | ⚠️ confie no workspace para carregar agentes e skills> |
```

Depois, numa mensagem só:

```
## ✅ sdd pronto · <projeto>
`●●●●●●●●●`

| Quero… | Diga | Agente |
|---|---|---|
| montar equipe, acordos e roadmap | "monte o planejamento" | `sdd-produto` |
| registrar uma demanda nova | "nova demanda: …" | `sdd-produto` |
| começar o que é meu | "minha próxima tarefa" ou "iniciar <id>" | o do seu papel |
| saber onde parei | "onde parei?" | qualquer um |

### Próximo passo
<1. **Monte o planejamento** (`sdd-planejamento`) — sem a equipe não há modo da fatia, GATE do plano nem revisor.
| 1. **Nova demanda: …** (`sdd-triar`).>

### Commit
`<git add … && git commit -m "<padrão de commit>: configurar o sdd">`

> ❓ **Faço o commit?**
> `ok` commita · `não` deixa para você
```
