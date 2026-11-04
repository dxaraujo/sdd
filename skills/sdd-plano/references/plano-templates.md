# Templates do plano da fatia (formato de spec do Kiro)

Os arquivos ficam em `.kiro/specs/<ft>-<slug>/` no formato de spec do Kiro: o painel de specs reconhece a pasta e o
`tasks.md` ganha **Start task** / **Run all tasks**. O texto é no idioma do projeto; os marcadores que o Kiro lê
(`.config.kiro`, `- [ ]`, `- [ ]*`, `_Requirements: …_`, `**Validates: Requirements …**`) e **os títulos que o
Kiro valida** ficam exatamente como abaixo, em inglês — traduzido, o Kiro acusa `Missing required section`:

| Arquivo | Títulos fixos (nesta ordem) |
|---|---|
| `requirements.md` | `# Requirements Document` · `## Introduction` · `## Glossary` · `## Requirements` · `### Requirement N: …` · `#### Acceptance Criteria` |
| `bugfix.md` | `# Bugfix Requirements Document` · `## Introduction` · `## Bug Analysis` · `### Current Behavior (Defect)` · `### Expected Behavior (Correct)` · `### Unchanged Behavior (Regression Prevention)` · `### Bug Condition` · `### Fix Property` · `### Preservation Property` |
| `design.md` | `# Design Document: …` · `## Overview` · `## Architecture` · `## Components and Interfaces` · `## Data Models` · `## Correctness Properties` · `## Error Handling` · `## Testing Strategy` |
| `tasks.md` | `# Implementation Plan: …` · `## Overview` · `## Tasks` · `## Task Dependency Graph` · `## Notes` |

Os demais subtítulos do sdd ("Padrões a seguir", "Decisões técnicas", "Riscos"…) vão no idioma do projeto. **Toda
seção fixa aparece sempre**, nas duas trilhas; sem o que dizer, ela leva só `Sem mudança.` ou `Não se aplica.` —
nunca conteúdo inventado para preenchê-la.

Plano curto: quem aprova tem de ler tudo numa sentada — um plano de 1.000 linhas esconde decisões em vez
de mostrá-las.

## `.config.kiro`

Uma linha de JSON, criada pela `sdd-desenvolver` junto com a pasta (a `sdd-plano` cria se faltar; `specId` = um
UUID novo: `uuidgen`, em minúsculas — é o comando que os agentes podem rodar):

```json
{"specId": "<uuid>", "workflowType": "requirements-first", "specType": "feature"}
```

`specType`: `feature` (trilha padrão) ou `bugfix` (trilha rápida, com `bugfix.md` no lugar do `requirements.md`).

## `requirements.md` (trilha padrão)

```markdown
# Requirements Document

## Introduction
FT-<nnn> — <título>. <O comportamento que esta fatia entrega, em 2–3 frases.>
Épico: <EP-<nn> | — (sem épico)> · PRD ou ficha: `<caminho>` · ELM: HF <id>, REG <id> · Fora de escopo: <lista curta>

## Glossary
- **Sistema_Login**: <o componente que responde pelos critérios — termo usado nos critérios EARS>
- **<Termo do domínio>**: <definição do glossário do projeto> (só os termos usados aqui)

## Requirements

### Requirement 1: <nome>
**User Story:** Como <ator>, quero <…>, para <…>.
**Origem:** HF-01 · cenários 1.1, 1.2 · REG-01

#### Acceptance Criteria
1. QUANDO o usuário errar a senha pela 3ª vez em 15 minutos, O Sistema_Login DEVE marcar a conta como **Bloqueada**.
2. ENQUANTO a conta estiver **Bloqueada**, O Sistema_Login DEVE recusar a autenticação com a mensagem MSG 2005.
3. SE a mesma falha for registrada duas vezes, ENTÃO O Sistema_Login DEVE contá-la uma vez só.

**Falsificável na base:** <a observação que mostra os critérios falsos hoje — ex.: "a 4ª tentativa ainda autentica">
```

- Padrões EARS: `QUANDO <gatilho>, O <Sistema> DEVE …` · `ENQUANTO <estado>, O <Sistema> DEVE …` ·
  `SE <condição indesejada>, ENTÃO O <Sistema> DEVE …` · `ONDE <variação opcional>, O <Sistema> DEVE …` ·
  sem gatilho: `O <Sistema> DEVE …`. O `<Sistema>` é um termo do Glossary.
- Um requisito por grupo de cenários da fatia; critérios numerados `N.M`, citados pelo `tasks.md`.
- Só o que a fatia cobre (`cobre` no backlog, ou os `C<n>` da ficha). Nada de regra que não esteja no
  PRD/ELM/`decisoes.md`/ficha.

## `bugfix.md` (trilha rápida — defeito)

```markdown
# Bugfix Requirements Document

## Introduction
FT-<nnn> — <título> (DF <id>). Ficha: `<produto>/fatias/FT-<nnn>-<slug>.md`. Fonte do comportamento correto:
<HF/REG do ELM | decisão D-nn | regra óbvia>.

## Bug Analysis

### Current Behavior (Defect)
1.1 QUANDO <condição>, ENTÃO o sistema <faz o errado> — evidência: <log, consulta, passo a passo>

### Expected Behavior (Correct)
2.1 QUANDO <condição>, ENTÃO o sistema DEVE <o certo>

### Unchanged Behavior (Regression Prevention)
3.1 QUANDO <condição vizinha>, ENTÃO o sistema DEVE CONTINUAR A <comportamento correto de hoje>

### Bug Condition
    FUNÇÃO condicaoDoDefeito(entrada)
      RETORNA <predicado que separa as entradas afetadas das não afetadas>
    FIM

### Fix Property
Para toda entrada com `condicaoDoDefeito`, o resultado é o de 2.x.

### Preservation Property
Para toda entrada sem `condicaoDoDefeito`, o resultado é igual ao de antes da correção.
```

As primeiras tarefas do `tasks.md` de um bugfix são sempre: **1.** teste que reproduz a condição do defeito
(vermelho) e **2.** testes de preservação (verdes antes e depois da correção). A tarefa 1 e a da correção fecham
num **ciclo só** (um commit, verde — `sdd-implementar` Passo 1).

**Testes existentes que mudam** (qualquer trilha): a correção ou o comportamento novo contradiz o esperado de um
teste que já existe → declare no `bugfix.md` (em Expected Behavior, um item `2.x` com o teste, o esperado de hoje
e o novo) ou no `requirements.md` (critério com o teste citado), com a **fonte da decisão** (pessoa, `D-nn`) — e
uma tarefa própria para mudar a expectativa. Aparece no resumo do GATE do plano (`sdd-plano` Passo 5): quem aprova
lê isso primeiro, e o Pleno ouve a recomendação de pedir a aprovação. Sem decisão de uma pessoa → é lacuna de
negócio: pergunte (ou, autônomo, `bloqueada`).

## `design.md`

```markdown
# Design Document: FT-<nnn> <título>

## Overview
<Abordagem em 3–6 linhas.>

## Architecture
### Padrões a seguir (pattern grounding)
| Referência real (research) | O que imitar |
|---|---|
| `<caminho>` | <estrutura, transação, teste> |

### Forma do programa
Árvore de arquivos:
    src/…/LoginService.java          alterar  conta tentativas e consulta o bloqueio
    src/…/BloqueioConta.java         criar    regra de bloqueio (módulo profundo: 1 método público)
    test/…/BloqueioContaTest.java    criar

Árvore de chamadas do caminho principal:
    LoginController.autenticar → LoginService.autenticar → BloqueioConta.registrarFalha → TentativaRepository.contar

## Components and Interfaces
    BloqueioConta.registrarFalha(login: String, instante: Instant): ResultadoBloqueio

## Data Models
<tabelas/colunas reais (research), queries, contratos de API/arquivo; DDL necessária → time de banco>

## Correctness Properties
*Uma propriedade é algo que deve valer em toda execução válida — vira teste baseado em propriedades quando o
toolkit do projeto tiver a biblioteca; senão, testes de exemplo.*

### Property 1: <título>
*Para qualquer* sequência de falhas de um mesmo login, a conta DEVE ficar **Bloqueada** se e só se houver 3 ou mais
falhas numa janela de 15 minutos.
**Validates: Requirements 1.1, 1.3**

## Error Handling
<o que é rejeitado, registrado, desfeito; transação; como repetir não duplica>

## Testing Strategy
- **Pontos de teste (seams):** <o mais alto possível; ex.: `BloqueioConta` pela interface pública; `POST /login`>
- **Contrato de pronto (verificação de aceite):**

| Cenário | Como executar | Esperado | Onde verificar |
|---|---|---|---|
| HF-01 · 1.2 | 4× `POST /login` com senha errada (massa: usuário `teste.bloqueio`) | 4ª resposta 423, conta **Bloqueada** | resposta + `SELECT situacao FROM conta WHERE login=…` |

O Esperado repete o **"Então" do cenário** com os mesmos valores visíveis (texto, rótulo, mensagem, nome de
arquivo) — palavra por palavra; o valor interno que o produz (enum, código) vai em Data Models, nunca no lugar dele.

## Decisões técnicas
| Decisão | Alternativas | Motivo | Vira ADR? |
|---|---|---|---|
<!-- Vira ADR? sim = muda como o time vai construir daqui para a frente: o Dev escreve o ADR no PR, em `adr/` desta
     pasta (Passo 5 da sdd-implementar); o Dev Sênior o julga e a consolidação o leva para a pasta de ADRs. -->

## Riscos
<concorrência, volume, dependências, DDL pendente>
```

Na trilha rápida, o `design.md` é curto, mas com todas as seções fixas: a causa raiz (com `arquivo:linha` da
research) no Overview, a correção em Architecture/Components and Interfaces, e a Testing Strategy com exploração
da condição do defeito, verificação da correção e da preservação. Seção que a correção não toca (ex.: Data Models)
→ `Sem mudança.` / `Não se aplica.`.

## `tasks.md`

````markdown
# Implementation Plan: FT-<nnn> <título>

## Overview
<1–2 linhas: ordem e estratégia (teste primeiro, do núcleo para a borda).>

## Tasks

- [ ] 1. Bloqueio após a terceira falha (unidade)
  - [ ] 1.1 Teste em `BloqueioContaTest`: 3 falhas em 15 min → **Bloqueada**; 2 falhas → **Ativa** (vermelho)
  - [ ] 1.2 Implementar `BloqueioConta.registrarFalha` imitando `<análogo>` (verde)
  - Pronto quando: `<comando de teste único> BloqueioContaTest` verde
  - _Requirements: 1.1, 1.3_
- [ ] 2. Login usa o bloqueio (integração)
  - [ ] 2.1 Teste de `POST /login` 4× → 423 (vermelho)
  - [ ] 2.2 `LoginService` consulta `BloqueioConta`; resposta 423 com a MSG 2005 (verde)
  - Pronto quando: `<comando>` verde
  - _Requirements: 1.1, 1.2_
- [ ]* 3. Teste de propriedade da Property 1
  - _Requirements: 1.1, 1.3_
- [ ] 4. Checkpoint — validação completa (compilar, suíte inteira, lint, cobertura)
  - A revisão não é tarefa daqui: é da `sdd-revisar`, em outro contexto (quem implementou não se revisa)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["2.1", "3"] },
    { "id": 3, "tasks": ["2.2"] }
  ]
}
```

## Notes
- Tarefas com `*` são opcionais.
- 2.1 depende de 1.2 (usa `BloqueioConta`); 3 testa a Property 1, implementada em 1.2.
````

- Uma tarefa = um comportamento, começando pelo teste que falha (corretiva: o teste que reproduz o defeito).
- Toda tarefa diz o comando que prova que terminou.
- Ordem de dependência. O **Run all tasks** do Kiro roda as tarefas pelas *waves* do `## Task Dependency Graph`:
  as de uma wave rodam ao mesmo tempo, e a wave N só começa quando 0..N-1 terminaram. O bloco ```` ```json ```` com
  `waves` não vazio é obrigatório (sem ele o Kiro acusa `tasks/missing-dag-json`) — nunca `Não se aplica.` nem
  lista de setas. Regras: toda tarefa folha não marcada (subtarefa `N.M`, ou `N` sem subtarefas) aparece em
  exatamente uma wave, inclusive as opcionais `*`; checkpoint e tarefa-mãe ficam de fora; ids de wave contíguos a
  partir de 0; dependente (ou que mexe no mesmo arquivo) vai numa wave posterior; sem dependência → uma wave só.
  O porquê de cada dependência, se não for óbvio, vai em `## Notes`.
- Mudança em código compartilhado → primeiro a tarefa de **preparação** ("deixar a mudança fácil"), depois a
  mudança; refatoração larga usa expandir → migrar → contrair, em fatias próprias.
- DDL não vira tarefa: vai para Riscos e para o campo Banco do `status.md`.
