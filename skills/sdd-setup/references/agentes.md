# Agentes — como a setup gera `.kiro/agents/sdd-*.json`

Os agentes são **gerados**, nunca editados à mão. Três fontes:

| Fonte | Onde | O quê |
|---|---|---|
| `papeis.json` | [../assets/agents/](../assets/agents/papeis.json) (power) | permissões de cada papel, em grupos reutilizáveis |
| `sdd-<papel>.md` | [../assets/agents/](../assets/agents/) (power) | o prompt de cada agente |
| `agentes.json` | `.kiro/config/sdd/agentes.json` (projeto, versionado) | as escolhas do projeto: caminhos, comandos, skills e MCPs por agente |

O script [../scripts/gerar_agentes.py](../scripts/gerar_agentes.py) junta as três e grava os seis agentes:

```bash
uv run --no-project python <power>/skills/sdd-setup/scripts/gerar_agentes.py --projeto <raiz>            # mostra o diff e a tabela
uv run --no-project python <power>/skills/sdd-setup/scripts/gerar_agentes.py --projeto <raiz> --gravar   # grava
```

Sai com código 1 (sem gravar nada) se sobrou um `{{…}}` ou se um `skill://`/`file://` não existe ou é absoluto.
"Atualizar os agentes do sdd" depois de atualizar o power é só rodar o script de novo: as escolhas estão no
`agentes.json`.

O formato é o **V3** do Kiro (campo `permissions`), carregado pela IDE e pela engine V3 do `kiro-cli`. A engine V2
do CLI não é suportada pelos agentes do sdd: use a IDE ou `kiro-cli chat --agent-engine v3`. Não rode
`/upgrade-agent` nem `kiro-cli agent upgrade` neles — os três com subagentes aparecem como `out of sync (not
rebuilt)` no `--dry-run` (por causa do `toolsSettings.subagent`, que a V3 ainda usa), e o conversor os deixa de lado.

## `agentes.json` do projeto

| Campo | O quê |
|---|---|
| `power` | a pasta do power, relativa ao home (Passo 0): `~/.kiro/powers/installed/sdd` |
| `produto`, `glossario`, `adr` | os caminhos do Passo 4 (`null` = não há) |
| `base` | a branch base, sem `origin/` — nas regras de push da base (pergunta no codificador e no orquestrador; negado nos demais) |
| `bundle` | o `rm.download` do `pa` (leitura negada: a consulta é pelas `elm_*_local`), ou `null` |
| `massa` | a pasta de massa do projeto que o verificador escreve, ou `null` |
| `elm` | `false` → nenhuma tool do `elm` em nenhum agente (`sdd/elm/*` negado) |
| `push_pr_no_loop` | `false` ("não — a pessoa abre") → o orquestrador não faz push (nem o da `iniciada` do lote, na base) nem abre PR |
| `http_sh` | `true` se a setup instalou `.kiro/sdd/http.sh` |
| `steering` | `file://` do steering de produto, tecnologia e estrutura, para todos os agentes |
| `comandos.build` | compilar, testes, teste único, lint, cobertura (padrões de shell: `mvn test*`) |
| `comandos.verificacao` | executar a aplicação ou o job, scripts de massa |
| `agentes.sdd-<papel>.skills` | `skill://` das skills escolhidas no Passo 6 |
| `agentes.sdd-<papel>.ler` | pastas dessas skills fora do projeto e do power (`~/.kiro/skills/<skill>/**`) |
| `agentes.sdd-<papel>.mcp` | tools de MCP do projeto: `servidor/tool` (banco: só a de consulta) ou `servidor` (inteiro, ex.: browser) |
| `agentes.sdd-<papel>.subagentes` | `[{"nome", "para"}]` — agentes do projeto (codificador e orquestrador) |
| `agentes.sdd-<papel>.modelo` | o modelo, se não for o padrão |

Codificador e orquestrador recebem `build` e `verificacao` (chamam revisor e verificador como subagentes); revisor
recebe `build`; verificador, `verificacao`.

## Como as permissões são montadas

- **Leitura:** o projeto e o power; negados `.env*`, `*.pem`, `*.key`, `~/.ssh`, `~/.aws`, as credenciais dos MCPs
  e o bundle. Os agentes leem e procuram com as ferramentas do Kiro, não com `cat`/`grep` no shell.
- **Shell — só o necessário:** cada papel libera grupos de comandos (`git-leitura`, `worktree`, `git-escrita`,
  `creditos`) e os do projeto. Comando fora da lista → o Kiro pergunta (sem interação, é negado). Cada grupo tem
  exceções (`exclude`) que caem em "perguntar" (`git log --output`, `git add -f`…). Negados em todos (`shell.negar`):
  `git -C`/`-c` (escondem o subcomando das regras), merge, rebase, `pull --rebase`/`--no-ff`, `commit -n`,
  `--no-verify`, `reset --hard`, `clean`, `stash`, `restore`, `checkout --`/`.`, `--force`, `--delete`, `rm -rf`,
  credenciais e o bundle em qualquer comando.
- **Push:** codificador, revisor, verificador e orquestrador — `git push *` pergunta sempre (`ask`, sem "sempre
  permitir"); `push-perigoso` nega `-f`, `+ref`, `:ref`, `--mirror`, `--all`, `--prune`, o push sem a branch nomeada
  (`git push`, `git push origin`, `HEAD`, `@`: as skills sempre a nomeiam) e outra ref para a base (`<ref>:<base>`,
  `heads/<base>`). O push da base (`git push origin <base>`) pergunta no codificador e no orquestrador, só para os
  registros de situação da fatia, com os arquivos conferidos antes
  ([Gravar na base](../../sdd-fatiar/references/backlog.md#gravar-na-base)); nos dois, `git reset --keep origin/*`
  também pergunta (desfaz o commit de registro de um push recusado). Revisor e verificador: push da base negado
  (`shell_negar`). Produto e pesquisador: push negado.
- **MCP do power** (`elm`, `gitlabpr`): regra `power` `sdd/<servidor>/<tool>` — leitura liberada (`mcp_libera`),
  escrita com confirmação (`mcp_pergunta`), e **toda tool do catálogo que o papel não usa, negada**: a IDE chama
  tool de power pela `kiro_powers`, fora do filtro de `tools`. Comentar e anexar: todo papel com tarefa, só na
  própria (regra em [`sdd/references/elm.md`](../../sdd/references/elm.md)). Merge do PR: só o codificador.
- **MCP do projeto:** `tools` (`@servidor/tool`), regra `mcp` `allow` e `includeMcpJson: true` — o gerador faz os
  três a partir de `agentes.sdd-<papel>.mcp`.
- **Subagentes:** `tools` `subagent/<nome>`, `toolsSettings.subagent` e a regra `subagent`. O subagente herda as
  regras de quem o chama (interseção, o mais restritivo vence): por isso o orquestrador já tem os comandos de build
  e verificação e escreve nas worktrees.
- **Escrita:** só o que o papel produz (`escreve`, `nao_escreve` no `papeis.json`; `nao_escreve_exceto` vira o
  `exclude` da negação). O codificador escreve no projeto, menos `.kiro/agents`, `hooks`, `workflows`, `steering`,
  `settings`, `skills`, `toolkits`, `config`, o `AGENTS.md`, a pasta do produto (fora o `backlog.md` e as `sprints/`,
  onde grava a situação da fatia na base; nas worktrees, toda ela), `.kiro/local/wf`, `.kiro/sdd` e `.git`; o
  orquestrador grava os mesmos dois caminhos do produto, para a `iniciada` do lote. Os relatórios do revisor e do
  verificador não podem ser negados nele (os subagentes herdariam a negação): quem barra relatório forjado é o
  merge, que confere as tarefas no ELM.
- **Limite: redireção.** O Kiro compara as regras só com o comando, sem o `> arquivo`: `git show … > <caminho>` passa
  pelo `allow` de `git show*`. A defesa é fora do agente — a confirmação de cada push, a revisão do PR por pessoa e
  o merge conferindo o ELM.

Conferido em 23/10/2026 com o `kiro-cli` 2.32 na engine V3, com as regras de então: os seis passam no
`agent validate`; comando liberado roda, comando fora da lista e exceção caem em aprovação, `commit -n` e push para
a base são negados pela regra. O `agent validate` não lê o `permissions`: o `exclude` no `fs_write` (3.4.0) foi
conferido no motor V3 do `kiro-cli` 2.35, que o aplica aos caminhos como aos comandos.

**Mudar uma regra** é no `papeis.json` do power, com o teste
(`uv run --no-project python -m unittest test_gerar_agentes`, na pasta `scripts/`); os projetos pegam a mudança
com "atualizar os agentes do sdd".

## Gravação

O Kiro sempre pergunta antes de gravar em `.kiro/agents/`, `.kiro/hooks/` e `.kiro/workflows/`: o script grava
pelo shell, então a confirmação é a do comando — mostre antes o diff (o script sem `--gravar`).
