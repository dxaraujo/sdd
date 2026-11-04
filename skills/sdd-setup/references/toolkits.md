# Toolkits — como a `sdd-setup` encontra as skills de cada tipo de projeto

O fluxo `sdd` não sabe programar em nenhuma stack: ele organiza **o quê** (produto), **o como** (plano) e **a
verificação**. O conhecimento de stack — Java, Spring Batch, Angular, React, Python, mainframe — vem de
**toolkits**: pacotes de skills mantidos **fora** do power, um por tipo de projeto ou stack. A `sdd-setup` é a
única parte do fluxo que sabe procurá-los; depois de configurado, cada agente só enxerga as skills que a pessoa
liberou para ele.

```
toolkit (fora do fluxo)            sdd-setup                          agentes do projeto
┌──────────────────────┐   descobre   ┌──────────────────────┐  liga   ┌──────────────────────────┐
│ toolkit.json         │ ───────────► │ detecta o tipo de    │ ──────► │ sdd-codificador         │
│ skills/<skill>/      │              │ projeto, propõe as   │         │   skill://…/java/SKILL.md │
│ steering/ (opcional) │              │ skills por agente e  │         │   skill://…/spring-batch… │
│ comandos de build    │              │ PERGUNTA à pessoa    │         │ sdd-revisor …           │
└──────────────────────┘              └──────────────────────┘         └──────────────────────────┘
```

## Tipos de projeto

Um repositório pode ter mais de um tipo (ex.: `backend` + `batch`). O tipo decide quais toolkits a setup propõe
e quais verificações a `sdd-verificar` usa para executar os cenários de aceite.

| Tipo | Sinais no repositório | Como a aceitação é verificada (padrão) |
|---|---|---|
| `backend` | controladores/rotas HTTP, OpenAPI, `spring-boot-starter-web`, `express`, `fastapi`, `*.csproj` web | chamada à API (HTTP), resposta e estado no banco |
| `batch` | `spring-batch-core`, `@EnableBatchProcessing`, `Job`/`Step`, `*.jcl`, agendadores, `cron` | execução do job com massa de teste; contagens e estado no banco; log de execução |
| `frontend` | `package.json` com `@angular/core`, `react`, `vue`, `svelte`; `src/app`, `pages/` | navegação no browser (Playwright/MCP de browser), screenshot como evidência |
| `mobile` | `android/`, `ios/`, `pubspec.yaml`, `react-native` | emulador/dispositivo, quando houver; senão roteiro manual |
| `dados` | dbt, Airflow, notebooks, SQL de carga, Spark | execução da carga em ambiente de teste; consultas de verificação |
| `biblioteca` | pacote publicado (`<packaging>jar</packaging>` sem app, `pyproject` de lib) | testes de contrato/unidade públicos |
| `infra` | Terraform, Helm, Ansible, pipelines | `plan`/`lint`/`dry-run`; nunca `apply` |

## Onde procurar (nesta ordem)

1. **Projeto:** `.kiro/toolkits/*/toolkit.json`
2. **Usuário:** `~/.kiro/toolkits/*/toolkit.json`
3. **Powers instalados:** `~/.kiro/powers/installed/*/toolkit.json` (um toolkit pode ser distribuído como power;
   não achou nada ali → `~/.kiro/powers/**/toolkit.json`)
4. **Sem manifesto** (toolkit implícito): skills em `.kiro/skills/*/SKILL.md`, `~/.kiro/skills/*/SKILL.md` e
   `~/.kiro/powers/installed/*/skills/*/SKILL.md` cujo frontmatter traga `metadata.toolkit` (nome do toolkit) —
   e, opcionalmente, `metadata.papeis` e `metadata.tipos-de-projeto`. Skills com o mesmo `metadata.toolkit` formam
   um toolkit.
5. **Skills avulsas** (sem toolkit): entram no inventário geral; a pessoa decide por agente, como qualquer outra.

Ficam de fora do inventário: as skills deste power (`sdd`, `sdd-*`) e `sdd2`, `sdd2-*` de uma instalação antiga.

Use `glob`/`ls` nesses caminhos (expandindo `~` para o home). Pastas inexistentes são normais — siga sem comentar.
Nunca leia arquivos de credenciais que encontrar no caminho.

## Manifesto `toolkit.json`

Formato definido por [../assets/toolkit.schema.json](../assets/toolkit.schema.json). Caminhos sempre relativos
à pasta do toolkit, com `/`.

```json
{
  "$schema": "https://raw.githubusercontent.com/dxaraujo/kiro/main/powers/sdd/skills/sdd-setup/assets/toolkit.schema.json",
  "nome": "spring-batch",
  "versao": "1.0.0",
  "descricao": "Jobs Spring Batch 5: steps chunk e tasklet, readers/writers JDBC, reexecução e testes de job",
  "tipos-de-projeto": ["batch"],
  "deteccao": {
    "arquivos": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "contem": ["spring-batch-core", "org.springframework.batch"]
  },
  "skills": [
    { "caminho": "skills/spring-batch-job/SKILL.md", "papeis": ["codificador", "revisor"] },
    { "caminho": "skills/spring-batch-teste/SKILL.md", "papeis": ["codificador", "verificador"] },
    { "caminho": "skills/java/SKILL.md", "papeis": ["codificador", "revisor", "pesquisador"] }
  ],
  "steering": [
    { "caminho": "steering/batch-regras.md", "papeis": ["codificador", "revisor"] }
  ],
  "comandos": {
    "compilar": "mvn -q -DskipTests compile",
    "testes": "mvn -q test",
    "teste-unico": "mvn -q -Dtest={alvo} test",
    "cobertura": "mvn -q verify",
    "lint": "mvn -q checkstyle:check"
  },
  "verificacao": "Executar o job pelo teste de integração (JobLauncherTestUtils) ou pela linha de comando do projeto com a massa de teste; conferir BATCH_JOB_EXECUTION e as contagens nas tabelas de destino"
}
```

| Campo | Uso pela setup |
|---|---|
| `tipos-de-projeto` | casa com o tipo detectado → o toolkit vira **sugestão** (nunca é ligado sem a pessoa dizer sim) |
| `deteccao` | `arquivos` existe na raiz (ou em módulos) **e** algum `contem` aparece nele → toolkit "detectado" |
| `skills[].papeis` | pré-seleciona a skill na proposta de cada agente (`pesquisador`, `codificador`, `revisor`, `verificador`, `produto`, `orquestrador`) |
| `steering[]` | regras da stack: vira `file://` nos agentes dos papéis indicados |
| `comandos` | **proposta** para a seção Comandos do `sdd.md` quando o repositório não deixa claro; a pessoa confirma |
| `verificacao` | texto que a `sdd-verificar` usa para executar os cenários de aceite desse tipo de projeto |

## Proposta por agente

A setup nunca liga uma skill sem a confirmação da pessoa — mas confirma a proposta inteira do agente de uma vez
(skills, MCPs, modelo e subagentes; ver o Passo 6 da `SKILL.md`). Para cada agente, mostra o inventário **agrupado por toolkit**. Vêm
pré-marcadas só as skills de toolkits **detectados** cujo `papeis` inclui o papel do agente; toolkit não
detectado, skill do projeto e skill do usuário aparecem desmarcadas:

O cartão é o W6 de [wizard.md](wizard.md): skills numeradas com a caixa `[✅]`/`[ ]` na primeira coluna, agrupadas por toolkit e origem na coluna
"Para quê" (ex.: `spring-batch-job` — steps chunk/tasklet · toolkit spring-batch 🔍 detectado), e a resposta pelos
números (`tirar 3,5`, `pôr 7`, `nenhuma skill`, `as mesmas do sdd-<outro>`).

Num projeto 100% Spring Batch, o normal é o codificador receber as skills de batch e Java, e não as de REST ou
de frontend — mas quem decide é a pessoa.

## Sem toolkit

Nenhum toolkit encontrado para o tipo detectado → diga isso uma vez, siga com as skills avulsas e registre no
`sdd.md` (`Toolkits: nenhum — <tipo>`). Os agentes passam a depender do steering de tecnologia e do
código vizinho (pattern grounding) — funciona, mas com mais revisão. Sugira à pessoa criar as skills da stack em
`.kiro/skills/` (ou um toolkit em `.kiro/toolkits/<nome>/`) e rodar a setup em modo atualização depois.

## Atualização

Toolkit novo ou atualizado → "atualizar os agentes do sdd" (`sdd-setup`, modo atualização): a setup compara o
inventário atual com o `sdd.md` e pergunta só sobre as skills **novas** de cada agente; skill que sumiu
sai dos agentes com aviso.
