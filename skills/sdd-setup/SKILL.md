---
name: sdd-setup
description: "Wizard de 9 etapas, em português do Brasil e em cartões padronizados, que configura o fluxo sdd num projeto: entende o repositório (tipo, stack, comandos de build e teste, git, banco, ELM), descobre as skills e os agentes do projeto, do usuário e dos toolkits de stack, pergunta agente por agente a quais skills e MCPs cada um dos seis agentes sdd terá acesso e, só depois de uma revisão final, grava o .kiro/steering/sdd.md, a pasta do produto, os agentes (gerados por script), hook e workflows. Refaz tudo em modo atualização. Use em \"configurar o sdd\", \"setup do sdd\", \"criar os agentes do sdd\", \"atualizar os agentes do sdd\", \"ligar o toolkit\", \"atualizar a configuração do sdd\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.7"
---

# sdd-setup — Configurar o fluxo no projeto

> **Voz do wizard — vale para cada linha que a pessoa lê, inclusive entre as ferramentas:** português do Brasil
> (mesmo que o Kiro esteja em inglês); entre uma ferramenta e outra, no máximo uma linha `🔎 <o que está
> fazendo>…` por etapa — nunca "Let me…", "I'll…", "Vou…", "Agora vou…". A mensagem que a pessoa lê é o cartão.

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-setup/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

O power `sdd` só entrega skills (o formato de power do Kiro não instala steering, agentes, hooks nem workflows):
esta skill instala no projeto o que o fluxo precisa, a partir de [assets/](assets/), e é a **única** parte do
fluxo que conhece os toolkits de stack ([references/toolkits.md](references/toolkits.md)).

## Como a setup se apresenta

A setup é a **porta de entrada do produto**: é a primeira impressão de quem adota o sdd. Ela é um wizard de 9
etapas, e **toda mensagem é um cartão de [references/wizard.md](references/wizard.md)** — leia-o antes da primeira
mensagem e copie o cartão da etapa como está, trocando só o que está entre `<…>`. Não achou o `wizard.md` na pasta da
skill → **pare** e diga que o power está incompleto ("reinstale ou atualize o power `sdd`"); nunca monte os
cartões de memória. Tabelas, colunas e ícones são
os de lá (legenda fixa); nunca improvise outro formato, outro ícone nem tabela com linha em branco.

- **Uma pergunta por mensagem**, sempre no fim, no bloco `❓`. Nunca duas etapas, nem duas perguntas, na mesma
  mensagem; nunca comece a etapa seguinte com uma pergunta da anterior em aberto.
- **Linhas numeradas** em toda tabela que a pessoa pode mudar: ela responde `ok` ou `<n>: <novo valor>`.
  Resposta ambígua → repita o que entendeu (em tabela) e **pare**: a confirmação é a próxima resposta, nunca a
  mesma mensagem que interpretou.
- **Fonte de cada valor** visível (🔍 detectado em <onde> · 📐 padrão do sdd · 🙋 você · 🧩 ELM): nada escondido,
  nada que a pessoa só descubra depois de gravado.
- **Status honesto:** ✅ só com resposta real; sem rede, sem credencial ou não rodado → ⏸️ com o motivo.
- **Português do Brasil em tudo** que a pessoa lê — cartões, linhas de trabalho e erros —, qualquer que seja o
  idioma padrão do Kiro.
- **Sem narração:** entre as ferramentas de uma etapa, **nenhum texto** além de uma linha `🔎 …` no começo; nada de
  "Vou fazer X / Agora vou Y / Let me…". A mensagem seguinte já é o cartão. Nenhum jargão interno sem explicação de meia linha (Passo N, V3, `{{…}}`, nomes de arquivos do
  power).
- **Feche cada etapa** com a linha `✔` do cartão antes do cabeçalho da próxima.

## Princípios

**Padrão primeiro.** O que tem padrão — detectado no projeto ou recomendado no template — é decidido **sem
perguntar** e aparece no cartão da etapa com a fonte (🔍 ou 📐), com **uma** confirmação: "ok" aceita tudo, ou a
pessoa diz só a linha que muda (`<n>: <valor>`). **Pergunte**
apenas o que não tem padrão nem dá para detectar (ex.: a URL do ambiente de teste, qual `pa_*.json` é o padrão quando
há mais de um), uma coisa por vez, mostrando o que foi detectado. Nunca pergunte o que só confirma um padrão. **Exceção: o `pa` do ELM** (Passo 4) é montado passo a passo, com a
pessoa ([references/elm-pa.md](references/elm-pa.md)) — valor errado ali só aparece quando a PA recusa.
Não achou o que procurava (arquivo, pasta, power, configuração) → **pergunte** onde está; nunca conclua "não há"
sem a pessoa confirmar. **Nada que o Kiro carrega é gravado antes da revisão do Passo 8 e do "ok"** — só dois
rascunhos de configuração, ambos mostrados: o `pa_<nome>.json` (conferido e validado no bloco 10 do ELM) e o
`.kiro/config/sdd/agentes.json` (entrada do gerador, no Passo 8). Nunca leia nem mostre arquivos de credenciais
(conferir se existem é permitido).

**Shell da pessoa.** Os comandos rodam no shell dela (`echo $SHELL`). Em `fish`, nada de sintaxe de bash
(`for …; do`, `&&` em versões antigas, `$(…)` em heredoc): comando composto vai em `bash -c '<comando>'`. Prefira
comandos simples, um por chamada, e as ferramentas de leitura e busca do Kiro para arquivos.

**Rede.** Não suponha o que exige VPN ou rede interna: teste cada serviço (GitLab, banco, ELM) e diga qual
respondeu. Falhou por rede → ⏸️ no cartão, siga com o resto e teste de novo na validação (Passo 9).

## Passo 0 — Boas-vindas e pré-checagem (cartão W0)

Rode esta skill na **sessão padrão** do Kiro (sem agente `sdd-*`): ela grava em `.kiro/steering`, `.kiro/agents`,
`.kiro/hooks` e `.kiro/workflows`, que os agentes do fluxo não podem escrever. Num agente `sdd-*` → peça para
trocar para a sessão padrão e pare.

1. **Raiz do repositório:** `git rev-parse --show-toplevel` (sem git → avise: o fluxo depende de branches e PRs).
2. **Pasta do power instalado** (`power` do `agentes.json`): o Kiro instala em `~/.kiro/powers/installed/sdd/`
   (conferido com o `kiro-cli` 2.31). Confirme que `skills/sdd-setup/SKILL.md` existe ali; senão procure
   (`find ~/.kiro/powers -path '*sdd/skills/sdd-setup/SKILL.md'`) ou use a pasta de onde esta skill foi
   carregada. Escreva o caminho **relativo ao home** (`~/.kiro/powers/installed/sdd`), com `/`. Não achou →
   pergunte à pessoa onde o power está.
   `KIRO_HOME` definida → o Kiro guarda a configuração global ali, não em `~/.kiro`: procure o power em
   `$KIRO_HOME/powers/installed/sdd/`; fora do home, avise que os agentes gerados só valerão nesta máquina e peça
   "ok" para usar o caminho absoluto.
3. **Caminhos nos arquivos gerados — sempre relativos, nunca absolutos** (são versionados e usados em Linux,
   macOS e Windows): do projeto → relativos à raiz (`file://.kiro/steering/sdd.md`); do power ou do usuário →
   relativos ao home (`skill://~/.kiro/powers/installed/sdd/skills/...`, `skill://~/.kiro/skills/...`); separador
   `/`; nunca `/home/…`, `/Users/…`, `C:\…`, `\` nem variáveis de ambiente.
4. **Modo:** já existe `.kiro/steering/sdd.md` ou `.kiro/agents/sdd-*.json` → **atualização** (cartão W0-A): mostre a
   configuração atual e pergunte o que mudar ("nada — só regenerar os agentes", útil depois de
   atualizar o power ou um toolkit). Refaça só o que mudou nas respostas, mas agentes, hook e workflows
   **sempre** a partir do power atual: os agentes pelo gerador, com o `.kiro/config/sdd/agentes.json` do projeto,
   e hook e workflows dos templates. Mostre o diff de cada um.
5. **Pré-checagem** (tabela do W0): shell, `uv --version` (o gerador dos agentes precisa; sem ele → como instalar
   e pare), `kiro-cli --version` (opcional), `elm_status(projeto=<raiz>)` (credencial do ELM; sem `pa` ainda, ele responde com `faltando`, o que é normal aqui) e se
   `~/.config/mcp-gitlabpr/gitlabpr.properties` existe (sem abrir). Mostre o W0 e espere o "ok" antes do Passo 1.

## Passo 1 — Entender o projeto (cartão W1)

Leia antes de perguntar: `README*`, `AGENTS.md`, `CONTRIBUTING*`, `.kiro/steering/*.md`, arquivos de build na
raiz e nos módulos (`pom.xml`, `build.gradle*`, `package.json`, `pyproject.toml`, `go.mod`, `*.csproj`,
`Cargo.toml`, `Makefile`), a árvore de pastas (2–3 níveis) e os últimos `git log --oneline -20`.

Proponha no cartão W1 (tipos, stack, módulos, testes, os três steerings e as regras críticas, cada um com a fonte)
e confirme. Tipos de projeto e sinais: tabela de [references/toolkits.md](references/toolkits.md). Depois:

- **Steering de produto/tecnologia/estrutura:** padrão do Kiro (`.kiro/steering/product.md`, `tech.md`,
  `structure.md`) → confirme; faltando → pergunte, um papel por vez, qual arquivo faz aquele papel (liste os `.md`
  candidatos) ou ofereça gerar (o Kiro tem "Generate Steering Docs"); "nenhum" é resposta válida.
- **Regras críticas:** leia o steering de tecnologia/estrutura e proponha as regras que, violadas, causam perda de
  dado, duplicidade ou falha em produção; a pessoa confirma, edita ou diz "nenhuma além do steering".

## Passo 2 — Backpressure e verificação (cartão W2)

Proponha os comandos (do arquivo de build, do steering, do README ou dos `comandos` do toolkit detectado) e
**ofereça rodá-los uma vez** — backpressure que não roda não é backpressure:

| Item | Como detectar |
|---|---|
| compilar, testes, teste único, lint, cobertura + gate | build + plugins de teste/cobertura/lint configurados |
| executar a aplicação/job | README, scripts, `spring-boot:run`, `npm start`, parâmetros de job |
| exercitar e verificar um cenário | tipo de projeto (tabela do `toolkits.md`) + `verificacao` do toolkit |
| massa de teste | pastas `massa/`, `seed/`, `fixtures/`, `src/test/resources/` |

A etapa tem duas mensagens: (1) a proposta, com "Rodo?"; (2) com `ok`, **rode de fato** cada
comando proposto, um por vez, e mostre o W2 de novo com o status e o tempo de cada um, pedindo o "ok" que fecha a
etapa. Só `pular` fecha sem rodar (status ⏸️ "não rodado — você pulou"). Nunca feche a etapa com "não rodados"
depois de um `ok`. Falhou → o cartão
de bloqueio com o erro em uma linha; a pessoa decide (corrigir o comando, seguir assim ou parar).

## Passo 3 — Git, PR e banco (cartão W3)

| Item | Como detectar |
|---|---|
| Branch base | candidatos: `git symbolic-ref refs/remotes/origin/HEAD`, as remotas `develop`/`desenvolvimento`/`dev`/`main`/`master` e o destino dos últimos merges (`git log --merges -30 --format=%s` — "into '<branch>'"). Um só candidato, ou todos os sinais na mesma → padrão; sinais divergentes (ex.: `origin/HEAD` = `master`, merges em `desenvolvimento`) → pergunte, com a tabela de candidatos do W3. Vai também no `{{BASE}}` dos agentes (push para a base negado, salvo os registros de situação do codificador e do orquestrador, com pergunta) |
| Prefixo da branch | branches remotas existentes; padrão `feature/` |
| Padrão de commit | `git log --oneline -20` (Task/IB do EWM? Conventional Commits?) |
| PR (merge request) | pelo MCP **`gitlabpr`** do power (GitLab, API v4, CE 10.8+; projeto vem do `origin` da raiz do workspace, informada em `pasta` a cada chamada; fora de um repositório, a URL do projeto colada pela pessoa vai em `url_projeto`). Teste uma vez com `gitlab_listar_mrs(pasta=<raiz do workspace>, limite=1)`: respondeu → `MCP gitlabpr` ✅; erro de rede → `MCP gitlabpr` ⏸️ (sem rede — testado de novo no Passo 9). Erro de credencial → mostre o modelo de `~/.config/mcp-gitlabpr/gitlabpr.properties` (`url` do GitLab e `token` pessoal com escopo `api`; a pessoa cria o arquivo, o agente não lê nem grava credencial) e teste de novo. `origin` fora do GitLab, ou a pessoa segue sem credencial → "entregar título e descrição" (troca depois por "atualizar a configuração do sdd"). Nunca `gh` nem `glab` |
| MCP de banco | servidores em `.kiro/settings/mcp.json` e `~/.kiro/settings/mcp.json` — qual é o de consulta e **qual tool** só consulta (ou "não há"); recomende um usuário de banco somente leitura |
| Artefatos de produto | fixo: `direto na branch base` (não pergunte) |
| Push na base (requisito) | não se detecta: quem desenvolve grava na base a situação da fatia (`iniciada`, `pronta`) e dá o push — base protegida contra o push dele barra o início de toda fatia. Avise na linha 7 do W3 e siga |

## Passo 4 — Produto, conhecimento e ELM (cartão W4)

O W4 mostra as seis linhas de uma vez (pasta do produto, glossário, ADRs, ELM, bundle e regras do ELM), com uma
pergunta. Glossário e ADRs aparecem sempre, mesmo quando a resposta é "não há". Faltando o `pa`, a montagem
dele vem depois do "ok" do W4, em cartões próprios (um bloco por mensagem); antes do bloco 0, avise que é a parte
mais longa (10 blocos) e o que ela decide.

1. **Pasta do produto** (`produto` do `agentes.json` e `<produto>` nas skills): onde ficam `backlog.md`, épicos
   e PRDs, planejamento e aprendizado — versionada. Já existe um `backlog.md` do sdd no repositório → a pasta dele;
   senão o padrão `.kiro/planejamento`. Vai na linha 1 do W4 (📐 ou 🔍). Grave o caminho real na seção Projeto do
   `sdd.md`.
2. **Glossário** (padrão `docs/glossario.md`) e **ADRs** (padrão `docs/adr`, sem barra no fim) — use os que já
   existirem; não existindo, o padrão é criá-los (linhas 2 e 3 do W4). A pessoa recusou na tabela → registre
   "não há" e remova dos agentes as regras e linhas que os citam (`{{GLOSSARIO}}`, `{{ADR}}`).
3. **ELM** — o MCP `elm` vem com o power. `.kiro/config/elm/pa_*.json` no repositório (um por project area)?
   - Há `pa_*.json` em `.kiro/config/sdd/` (lugar antigo, antes da 3.5.7) → mova para `.kiro/config/elm/` (`git mv`),
     que é onde o MCP `elm` lê, e siga daqui com eles.
   - Não há e a pessoa diz que o projeto não usa ELM → `Usa ELM: não` (o fluxo funciona igual; os ids vêm do
     `backlog.md`).
   - **Gerar o `pa` — guiado, um bloco por vez:** siga [references/elm-pa.md](references/elm-pa.md) (credencial e
     PAs → time → tipos → campos e obrigatórios → valores → valor por item de trabalho → horas → DOORS Next → ETM →
     conferência). Aqui **não há padrão sem perguntar**: todo valor vem da descoberta (`elm_setup_descobrir`) ou da
     pessoa, escolhido de uma lista que você mostra; nada de deduzir nome, `qname`, time code ou enumeração, nem de
     copiar de um `pa` antigo sem mostrar a origem. O `pa` inteiro é mostrado para conferência antes de gravar, e a
     validação com itens de teste é recomendada.
   - Seção ELM do `sdd.md`, sem perguntas (linha 6 do W4): publicar requisitos `na-aprovacao`, ET `não
     publica`, manual `nada`, pontos `não`, fatia dividida "filhos do item original", títulos das tarefas e colunas
     do `CT.csv` do template; a categoria do IB de defeito é a do bloco 5 do `elm-pa.md`. A Sustentação não é
     perguntada: o IB `Sustentação` nasce no backlog do EWM, um por produto, com a `[GB]`, no modo inicial
     da `sdd-planejamento` ou no espelhamento do backlog ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md)
     §0 e §2); o IB
     `Manutenção` e os de categoria, com o primeiro item de cada um. A seção **Sustentação** do `sdd.md` vem do
     template — a Manutenção (as fatias sem épico) e as seis categorias, a Classificação de cada uma pelo bloco 5 do
     `elm-pa.md`, que também pergunta a Categoria do IB `Manutenção`.
   - **Backlog do produto no EWM** (`ccm.backlog` do `pa`; também no modo atualização — com `pa` que já o tem, só o espelhamento): onde os
     itens triados nascem — [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §0 (pergunta a linha de
     base e se `<linha de base>/Backlog` já existe; senão cria a iteração e o plano `Backlog`; com `backlog.md` em uso,
     oferece o espelhamento). Estrutura padrão no início do [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md#estrutura-no-ewm-padrão).
   - **Bundle do RM** (`rm.download` do `pa`): pastas com `index.md` de `okf_version` → mostre e confirme; vazio →
     ofereça a `sdd-sync` (baixar). É a base que os agentes consultam **pelas `elm_*_local` do MCP `elm`**, nunca lendo os arquivos —
     com "sim", `elm_indexar_local` (segundo plano: responde na hora; a 1ª vez baixa o modelo) e mostre quantos
     documentos há; o caminho vai no `{{BUNDLE}}` dos agentes, como leitura negada (no `.gitignore` → avise que só
     existe nesta máquina, depois da `sdd-sync`).

## Passo 5 — Inventário de skills e toolkits (cartão W5)

Siga [references/toolkits.md](references/toolkits.md): procure toolkits (com e sem manifesto) e skills avulsas
do projeto (`.kiro/skills/*/SKILL.md`), do usuário (`~/.kiro/skills/*/SKILL.md`) e de outros powers
(`~/.kiro/powers/installed/*/skills/*/SKILL.md`; não achou nada ali → `~/.kiro/powers/**/skills/*/SKILL.md`),
**exceto** as do fluxo (`sdd`, `sdd-*`, e `sdd2`, `sdd2-*` de uma instalação antiga). Para cada uma:
nome, início da `description`, origem e, se houver, toolkit e papéis. Toolkit cujo `deteccao` casa com o projeto
→ "detectado". Liste também os **agentes do projeto** (`.kiro/agents/*.json` e `~/.kiro/agents/*.json`, exceto
`sdd-*`), com o "para quê" tirado da `description` — eles são oferecidos como subagentes no Passo 6, sem a pessoa
precisar lembrar deles.

## Passo 6 — Agentes, um de cada vez (cartão W6, seis mensagens)

Para cada agente, nesta ordem, monte a proposta com o inventário **agrupado por toolkit/origem** e as skills
pré-marcadas pelos `papeis` do toolkit e pelo tipo de projeto (formato em `toolkits.md`):

| Agente | Já tem (do fluxo) | `elm` | `gitlabpr` | Subagentes do fluxo | Push | Sugestão de extras |
|---|---|---|---|---|---|---|
| `sdd-produto` | triar, entrevistar, especificar, prd, fatiar, planejamento, atender, executar, consolidar, aprender (registrar), iniciar, status | 🟢 consulta · 🟡 escrita | 🟢 consulta | `sdd-pesquisador`, `sdd-revisor` | 🔴 negado | skills de domínio/negócio |
| `sdd-pesquisador` | pesquisar | 🟢 só o bundle local | ➖ | — | 🔴 negado | skills de stack para ler o código |
| `sdd-codificador` | desenvolver, plano, implementar, iniciar, status | 🟢 consulta · 🟡 escrita | 🟢 consulta · 🟡 abrir e mesclar PR | `sdd-pesquisador`, `sdd-revisor`, `sdd-verificador` | 🟡 pergunta | skills de stack e de teste do toolkit |
| `sdd-revisor` | revisar, iniciar, status | 🟢 consulta · 🟡 escrita | 🟢 consulta | — | 🟡 pergunta | skills de padrões e de revisão da stack |
| `sdd-verificador` | verificar, iniciar, status | 🟢 consulta · 🟡 escrita | ➖ | — | 🟡 pergunta | skills de teste de aceite |
| `sdd-orquestrador` | loop, desenvolver, plano, implementar, status | 🟢 consulta · 🟡 escrita | 🟢 consulta · 🟡 abrir PR | `sdd-pesquisador`, `sdd-codificador`, `sdd-revisor`, `sdd-verificador` | 🟡 pergunta | normalmente nenhuma |

As colunas `elm`, `gitlabpr`, Subagentes do fluxo e Push vêm do `papeis.json` e vão **todas** no W6 do agente, como
estão (projeto sem ELM → a linha do `elm` com ➖; PR entregue como texto → a do `gitlabpr` continua, com a nota
"sem projeto no GitLab ainda"): nunca omita uma linha fixa nem mude o acesso dela. O `gitlabpr` só serve ao PR e
só aparece em quem lida com PR (produto: conferir o PR mergeado na pré-condição dos ritos e no painel; codificador:
abrir e mesclar; revisor: ler o PR; orquestrador: abrir no loop) — pesquisador e verificador não o têm. Pedido de
tirar uma linha fixa → explique que é do papel, não do projeto, e siga sem ela mudar.

Aprender e setup rodam na **sessão padrão** (sem agente); o modo registrar da aprender também no `sdd-produto`,
na consolidação. A consolidação é do P.O. ou do SM, no `sdd-produto`
(grava na base, publica a ET *as-built* e os casos de teste).

Para cada agente, **uma mensagem só** (cartão W6): a proposta completa já marcada pelos padrões e **uma**
confirmação ("ok", ou o que muda pelos números — `tirar 3,5`, `pôr 7`, `modelo: …`). Nada é perguntado item a
item. Pedido que não é marcar/desmarcar (ex.: "quando a tarefa for de batch, use o agente X") → traduza para o
que o fluxo tem (subagente com o "para quê" do pedido), mostre o cartão atualizado e confirme.

Padrões da proposta:
1. **Skills:** marcadas só as de toolkits **detectados** com o papel do agente; as outras aparecem desmarcadas —
   inclusive skill avulsa que pareça útil (recomende em texto, ex. "recomendo `pôr 1`") e skill que a pessoa marcou
   em **outro** agente: a escolha de um agente não passa para o seguinte.
2. **MCPs:** o de banco entra como somente leitura em pesquisador, codificador, revisor e verificador — só a tool
   de consulta (`<servidor>/<tool>` em `agentes.sdd-<papel>.mcp`), nunca o servidor inteiro se ele tiver tool de
   escrita; browser/Playwright marcado no verificador em projeto `frontend`. **ELM** (projeto com ELM): as tools do
   `elm` que o `papeis.json` dá a cada papel (leitura liberada; escrita com `ask`) — `sdd-produto`,
   `sdd-codificador`, `sdd-orquestrador`, `sdd-revisor` e `sdd-verificador`, cada um comentando e anexando só na
   própria tarefa; o pesquisador só consulta o bundle local (`elm_*_local`). Projeto sem ELM → `"elm": false` no
   `agentes.json` (a escrita vira `ELM pendente`).
3. **Modelo:** sempre o padrão do Kiro — não pergunte; a pessoa troca na proposta se quiser.
4. Só codificador e orquestrador: **subagentes** — os `sdd-*` do fluxo marcados; os agentes do projeto do
   inventário (Passo 5) **sempre listados**, desmarcados, com o "para quê" — que vai em
   `agentes.sdd-<papel>.subagentes[].para` e no prompt do agente. Agente com o campo `hooks` (mesmo vazio) é
   ignorado pela IDE: fica desmarcado, com o ⚠️.

Registre também as skills **oferecidas e recusadas** por agente (coluna própria no `sdd.md`): no modo
atualização, só skill que não está em nenhuma das duas colunas é "nova".

A autonomia (seção Git, banco e autonomia do template) aparece no cartão do Passo 7 (linhas 3 a 7 do W7), **sem
perguntas**: GATE do
plano pela senioridade de quem implementa (fixo: Júnior sempre, Pleno pergunta, Sênior nunca — `sdd-plano` Passo 5);
paralelismo do loop `1`; push e PR no loop perguntando a cada lote (o orquestrador tem regra `ask` para push e PR, então
o Kiro confirma cada um; a pessoa muda para "não — a pessoa abre" → `"push_pr_no_loop": false`, e a regra vira
`deny`: o orquestrador entrega também o comando do push da base (`iniciada` do lote) e espera a publicação);
**push pelo agente** no codificador, no revisor e no verificador (fixo, não é perguntado): `git push *` com
`ask` (o Kiro pergunta sempre), com as negações de `--force`, `-f`, `+ref`, `:ref`, `--mirror`, `--all`, `--prune`,
`--delete` e do push sem a branch nomeada (`git push`, `git push origin`, `HEAD`, `@`); revisor e verificador só
publicam a branch do PR (push para a base negado); na base, o codificador publica só os registros de situação da
fatia (`iniciada`, `pronta`) e o orquestrador, só a `iniciada` do lote, com os arquivos conferidos antes
([Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base)); push da branch recusado → o agente entrega o
comando pronto e espera a pessoa dizer que publicou (o da base segue o Gravar na base); e, se a verificação chama a
aplicação por HTTP, o **script de chamada** do verificador `.kiro/sdd/http.sh` (o verificador roda só esse script sem
perguntar, só contra a URL de teste e com corpo da pasta `massa/`; precisa de `sh` e `curl`; a pessoa pode trocar por
"nenhum": cada `curl` pede confirmação, e no loop a verificação fica para a sessão dela). A única pergunta aqui é a
**URL base do ambiente de teste**, e só em projeto que a verificação chama por HTTP (`backend`, `frontend`), quando
não está no repositório (`.env.example`, `application-*.yml`, README). Projeto `batch`, `dados` ou `biblioteca` →
não pergunte (`➖`). Nunca uma URL de produção.

## Passo 7 — Hook, workflows e autonomia (cartão W7)

Um só cartão para o que roda sozinho. Padrões (linhas 1 e 2 do W7), conforme [references/automacoes.md](references/automacoes.md): hook `sdd-backpressure` **ligado**
quando há comandos de compilar e testar; receitas de Kiro Workflows **instaladas** só quando o recurso já está
habilitado, senão de fora. Onde conferir — basta um dos dois `true`: na IDE, `kiroAgent.workflows.enabled` no
`settings.json` do usuário (macOS `~/Library/Application Support/Kiro/User/settings.json`; Linux
`~/.config/Kiro/User/settings.json`; Windows `%APPDATA%\Kiro\User\settings.json`); no CLI, `kiro-cli settings
chat.enableWorkflows`. Diga na linha 2 do W7 qual dos dois foi lido. Na tabela, diga quem dispara as
receitas (a pessoa, no chat do Kiro; nenhum agente as dispara) e que os dois exigem a IDE ou a engine V3 do
`kiro-cli`. A pessoa tira um da tabela → não instale.

## Passo 8 — Revisão e gravação (cartão W8)

Na ordem:
- **a.** Monte em memória os itens 1 a 5 abaixo.
- **b.** Grave o rascunho `.kiro/config/sdd/agentes.json` e rode o gerador **sem `--gravar`** (só mostra; não grave
  o `sdd.md` nem nada mais antes do "ok" — o gerador não precisa dele): ele confere os caminhos e
  **imprime a tabela dos agentes** (skills, MCPs, ELM, subagentes, push) lida dos agentes que vai gerar. Confira
  cada linha com o que a pessoa aprovou no Passo 6 — diferente → corrija o `agentes.json` e rode de novo; nunca
  mostre nem grave um agente que não bate.
- **c.** Mostre o W8 com essa tabela **colada sem mudar nada** — a partir da linha `| Agente |` que o gerador
  imprimiu, com as mesmas colunas, na mesma ordem; nunca uma tabela sua — e, no modo atualização, o diff de cada arquivo que
  muda.
- **d.** "ok" → grave nesta ordem: `sdd.md`, agentes (gerador com `--gravar`), hook, workflows, `http.sh`, pasta do
  produto, glossário e ADRs, `.gitignore`. Recusa de uma confirmação do Kiro → diga qual arquivo ficou de fora e ofereça regravar;
  nunca siga como se tivesse gravado.

Itens:
1. `.kiro/steering/sdd.md` ← [assets/steering/sdd.md](assets/steering/sdd.md) com as respostas (nada de `<…>`
   sobrando; o que não se aplica fica "não há"/"nenhum"). É o **único** steering do fluxo. No modo atualização, a
   seção Regras aprendidas fica como está (nunca apague regras promovidas).
2. `.kiro/config/sdd/agentes.json` com as respostas (campos em [references/agentes.md](references/agentes.md):
   caminhos, base, bundle, ELM, push no loop, `http.sh`, steering, comandos, e skills, leituras, MCPs, subagentes e
   modelo por agente) e, a partir dele, os agentes pelo gerador:
   `uv run --no-project python <power>/skills/sdd-setup/scripts/gerar_agentes.py --projeto <raiz>` mostra
   o que muda e a tabela dos agentes, sem gravar; depois do "ok", o mesmo comando com `--gravar` grava `.kiro/agents/sdd-*.json`
   (e imprime a tabela de novo). As chaves de `agentes` são os nomes dos agentes (`sdd-codificador`, …); chave
   desconhecida faz o gerador parar. Nunca edite os agentes à mão nem os passe pelo `kiro-cli agent upgrade`.
3. Hook e workflows escolhidos (Passo 7); script de chamada do verificador, se escolhido (Passo 6):
   `.kiro/sdd/http.sh` ← [assets/scripts/http.sh](assets/scripts/http.sh) com `{{URL_TESTE}}` trocado pela URL
   base do ambiente de teste (sem barra no fim).
4. `<produto>/` (só o que não existir): `backlog.md` mínimo
   (`# Backlog — <nome>`, `Próximos ids: EP-01 · FT-001 · AT-001 · IM-001 · BD-001 · IN-001 · OP-001 · EX-001` e
   as seções `## Épicos`, `## Fatias` e `## Sustentação` vazias, sem `### <Categoria>`: cada uma nasce com o primeiro
   item dela — formato na `sdd-fatiar`), `<produto>/aprendizado/licoes.md` com o título `# Lições` (a pasta
   `sustentacao/` nasce com o primeiro item de categoria, pela `sdd-triar`) e `fatias/` (as fichas). O `equipe.json`
   e o `acordos.md` não: são da `sdd-planejamento` (modo inicial), que só grava a equipe depois dos acordos (duração
   da sprint). No modo atualização, acrescente só o que falta — nunca recrie o que existe.
5. Glossário e ADRs que o W4 disse "será criado" (só o que não existe): `<glossario>` com `# Glossário — <nome>` e a
   tabela vazia `| Termo | Definição | Evitar | Fonte | ELM |` (formato da `sdd-entrevistar`); `<adr>/` com um
   `README.md` de uma linha ("Decisões que devem durar — um arquivo por decisão, gravado pela consolidação").
   Prometido no W4 e não gravado → o fluxo aponta para um caminho que não existe: confira na etapa 9.
6. `.gitignore`: acrescente `.kiro/local/` se faltar.

Agente existente e editado à mão → mostre o diff e pergunte antes de sobrescrever. O Kiro pede confirmação para
cada arquivo gravado em `.kiro/agents/`, `.kiro/hooks/` e `.kiro/workflows/` — avise antes.

## Passo 9 — Validar e entregar (cartão W9)

Rode as verificações abaixo e mostre o W9 com o status de cada uma; depois o cartão "✅ sdd pronto", com a tabela
"Quero… / Diga" e o próximo passo. A tabela final dos agentes é a que o gerador imprimiu ao gravar — nunca uma
escrita de memória.

- Todo caminho que o `sdd.md` e o `agentes.json` citam (pasta do produto, glossário, ADRs, massa) existe — ou é
  "não há"/`null`.
- O GitLab que ficou ⏸️ no Passo 3 → teste de novo (`gitlab_listar_mrs`) e diga o resultado.
- O gerador já confere os agentes (sai com 1 e não grava se sobrou `{{…}}` ou se um `skill://`/`file://` não existe
  ou é absoluto). Confira também: nenhum servidor `elm` no `mcp.json` do projeto.
- Ferramentas que varrem a raiz do repositório (test runners, linters, `tsc`, varredura de arquivos) ignoram
  `.kiro/local/` — onde o loop cria as worktrees? Não ignoram → acrescente a exclusão na configuração delas (com
  "ok") ou registre no `sdd.md` que o loop não deve ser usado.
- JSON dos hooks e workflows faz parse; agentes citados nos workflows existem em `.kiro/agents/`. O Kiro valida a
  receita quando uma execução começa: com Workflows ligado, ofereça rodar `sdd-planejar-fatia` com `fatia=FT-000`
  (não existe) — erro de validação aparece antes do primeiro passo; sem ele, o passo `conferir` para com erro sem
  gravar nada. Erro de validação → mostre-o e ofereça remover o arquivo (o fluxo funciona sem ele).
- `kiro-cli` disponível → para cada agente, `kiro-cli agent validate --path .kiro/agents/<agente>.json` (saída
  vazia = válido; erro aponta o campo); `kiro-cli agent list` (na raiz do repositório) lista os seis;
  `kiro-cli agent upgrade --dry-run .kiro/agents` diz `v3-only` para três e `out of sync (not rebuilt)` para os
  que têm subagentes — esperado (ver [references/agentes.md](references/agentes.md)). No CLI V3, `/config` e `/hooks` mostram os agentes, as
  permissões e o hook carregados.
- Herança: por padrão, agentes customizados recebem também o steering, as skills e o `AGENTS.md` padrão do
  workspace e do usuário — as skills de `~/.kiro/skills` chegam a todos, além das escolhidas no Passo 6. Para que
  cada agente tenha só as suas, no CLI: `kiro-cli settings --workspace chat.disableInheritingDefaultResources
  true` (ofereça; a IDE não documenta essa opção).
- Workspace não confiável → avise: até a pessoa confiar nele, o Kiro não carrega os agentes, o steering, as skills
  e os workflows do projeto e pergunta antes de cada comando de shell.

Sugira o commit — o comando pronto no shell da pessoa, no padrão de commit do projeto — (`.kiro/steering/sdd.md`, `.kiro/config/sdd/agentes.json`, `.kiro/agents/sdd-*.json`, `.kiro/hooks/`, `.kiro/workflows/`,
`.kiro/sdd/`, `<produto>/` e `.gitignore`) — só com confirmação — e termine
com o próximo passo — sem `<produto>/equipe.json`, primeiro "monte o planejamento" (`sdd-planejamento`, modo
inicial: equipe com a senioridade, acordos e roadmap; sem ela não há modo da fatia, GATE do plano nem revisor); depois
"nova demanda: …" (`sdd-triar`: faz a triagem e registra no backlog; épico → `sdd-prd`), "iniciar <id>" ou "minha próxima tarefa"
(`sdd-iniciar`: o hub diz a skill do papel) ou "onde parei?" (`sdd-status`).

## Regras

- Não altere nada fora de `.kiro/`, da pasta do produto, do glossário/ADRs que a pessoa pediu para criar e do
  `.gitignore`.
- As skills `sdd-*` ficam no power — nunca as copie para o projeto (uma atualização do power as atualiza; depois
  rode esta skill em modo atualização para refazer caminhos e agentes).
- Toolkit nunca é ligado sem a pessoa dizer sim, agente por agente.
