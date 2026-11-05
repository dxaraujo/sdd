---
name: sdd-prd
description: "Escreve o PRD de um épico ou demanda no fluxo sdd — o quê e o porquê na linguagem do negócio: problema, solução, atores, histórias com cenários de aceite (Gherkin), regras de negócio, decisões de implementação e de teste em nível de módulo, não funcionais e fora de escopo. Explora o código e a documentação do ELM antes, entrevista a pessoa (sdd-entrevistar) e conduz o GATE do PRD (aprovação do P.O.), depois do qual as histórias, regras e termos vão para o DOORS Next pelo MCP elm. Use em \"escreve o PRD\", \"documenta a demanda\", \"épico\", \"especificar a demanda\", \"aprova o PRD\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.7"
---

# sdd-prd — O quê e por quê (épico)

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-prd/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Saída, na **pasta de trabalho** da especificação — `.kiro/local/especificacao/<EP>-<slug>/`, fora do git, montada
pela **`sdd-especificar`** — até o GATE; depois dele, a `sdd-especificar` a leva para `<produto>/epicos/<EP>-<slug>/`: o `prd.md` no formato de
[references/prd-template.md](references/prd-template.md), o `decisoes.md` e a pasta `elm/` com **um conceito OKF
v0.2 por história, regra e termo novo** — o formato de [references/okf-elm.md](references/okf-elm.md), o mesmo do
bundle que a `sdd-sync` mantém. São esses arquivos que sobem para o DOORS Next depois do GATE; até lá, ficam aqui.

O PRD é um **registro de decisões** e a **proposta de mudança** da documentação oficial — não um documento vivo.
Depois de aprovado, as histórias (HF), regras (REG) e termos (GL) vão para o DOORS Next ([publicação](../sdd-consolidar/references/elm-publicar.md)), que é a fonte
oficial; o que vale a longo prazo é o ELM, o glossário e os ADRs. Se o PRD afirma algo que ninguém decidiu, é um
defeito do PRD. Toda demanda entra pela `sdd-triar`; só o que ela classifica como **épico** chega aqui. Uma fatia
com regra clara é trilha padrão sem épico, com uma ficha no lugar do PRD.

Leia antes: `.kiro/steering/sdd.md` (ELM, caminhos, papéis) e o steering de produto que ele aponta.

## Passo 1 — Entender a demanda

PRD é decisão de uma pessoa (o GATE do PRD): chamada em modo autônomo (`AUTONOMO=true`, pelo loop ou por um agente
sem pessoa na conversa) → "PRD, backlog e itens de Sustentação (`AT-`, `IM-`…) nunca são AFK — especifique numa
sessão com o P.O." e pare.

1. Peça (ou leia, se veio da `sdd-triar`) a descrição **longa** da demanda: quem pediu, o problema, exemplos
   reais, prazos. Work item do EWM → `elm_ler_wi(id, comentarios)`.
2. **Explore antes de perguntar** (subagente `sdd-pesquisador`, se houver; senão você mesmo, só leitura):
   - documentação atual no bundle do ELM, pelo `elm_buscar_req_local`/`elm_ler_req_local` ([sem bundle → ELM remoto](../sdd/references/elm.md#bundle-local)): histórias e regras
     que já tratam do assunto —
     o PRD **altera** o que existe, não duplica;
   - código: onde o comportamento mora hoje, funcionalidades análogas;
   - glossário e ADRs (caminhos na seção Projeto do `sdd.md`): termos e decisões que já valem.
   Registre o que achou como fontes (id ELM, `arquivo:linha`).
3. Defina o id: o `EP-<nn>` que a `sdd-triar` registrou (linha com `prd` `—`: `novo` ou `elegivel` na triagem,
   `iniciado` pela `sdd-especificar`); sem registro, a demanda não passou pela triagem → "use `sdd-triar`" e pare.
   Pasta de trabalho: a da `sdd-especificar` (`.kiro/local/especificacao/<EP>-<slug>/`, `slug` em kebab-case, sem
   acento); sem ela → "use `sdd-especificar EP-<nn>`" e pare (é ela que assume a `[ESP]` e monta a pasta).
4. **EWM:** nada a registrar aqui — o épico nasceu no backlog do EWM na triagem (o `IB` da coluna `elm`;
   `pendente` → crie pela [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3) e entrou na sprint com a
   `[ESP]`.

## Passo 2 — Entrevistar

Rode a **`sdd-entrevistar`** sobre a demanda, gravando em `decisoes.md` da pasta de trabalho. Ela termina quando a
árvore de decisões está fechada ou a pessoa diz "chega".

## Passo 3 — Escrever

### 3.1 Similares no ELM (obrigatório, antes de criar qualquer arquivo em `elm/`)

Projeto com ELM: liste os artefatos que o PRD vai propor (tipo, título provisório, palavras-chave da entrevista e
do glossário) e rode [similares](references/similares.md). Mostre a tabela à pessoa e peça
uma decisão por artefato com acerto:

| Relação encontrada | Decisões possíveis (recomendada primeiro) |
|---|---|
| igual | **reutilizar** o existente (não cria conceito) · criar novo só com o motivo da diferença registrado |
| sobrepõe | **alterar** o existente (caminho "Alteração" abaixo) · criar novo com o motivo registrado |
| relacionado | **criar novo**, citando o existente em `## Relações` |
| nenhum | criar novo |

Registre cada decisão no `decisoes.md` (`D-nn`: artefato, id do ELM encontrado, relação, decisão, motivo) e, na
tabela de artefatos do PRD, a coluna **No ELM**: `reusa <id>` · `altera <id>` · `novo (verificado <AAAA-MM-DD>)`.
Verificação ao vivo pendente (sem o MCP `elm`) → `novo (só bundle <data>)`: a publicação refaz a busca.
Artefato que surgir depois (na escrita, na revisão ou numa mudança depois de aprovado) passa por aqui antes de
virar arquivo. Projeto sem ELM → pule.

### 3.2 Escrever

Preencha o template do `prd.md` e crie, em `elm/`, um arquivo por artefato (`HF-nn-<slug>.md`,
`REG-nn-<slug>.md`, `GL-<termo>.md`), com `status: draft`, `sources` (PRD, decisões), `generated` e o corpo do tipo
(formato em [references/okf-elm.md](references/okf-elm.md)), mais o `index.md` e uma entrada no `log.md`. O `prd.md`
só aponta para eles. Regras de escrita:

- **Histórias** pequenas o bastante para caber em poucas fatias; cada uma com cenários que cubram: caminho feliz,
  o que **não** deve ser aceito, repetição/reexecução, erro em um item (a operação continua? o que fica
  registrado?). "Então" sempre verificável — nada de "corretamente".
- **Regras** testáveis, com valores, uma por bloco, citando a decisão de origem (`D-nn`) ou a fonte.
- **Alteração** de comportamento documentado → traga o artefato do bundle da `sdd-sync` pelo
  `elm_ler_req_local` (`id` = o id; o `markdown` devolvido é o arquivo inteiro) e grave-o em `elm/`, mantendo `resource`, `id` e o `sources` do ELM; ponha
  `status: draft` e um `generated` novo; reescreva no estado **depois** da mudança. Sem bundle, leia o artefato
  pelo `elm_ler_req(id)` e grave a mesma estrutura. A publicação atualiza o artefato existente em vez
  de criar outro. Na tabela do PRD, coluna "No ELM" = `altera <id>`.
- **Reutilizar** (decisão do 3.1) → não crie conceito: a HF embute a REG existente (`[<id>](<id>)`), linka o termo
  existente e cita a HF existente; a linha na tabela do PRD fica com `reusa <id>` e sem arquivo em `elm/`.
- **HF → REG** sempre por link para o arquivo da regra: na publicação ele vira **embed**. Relações entre requisitos
  (restringe, satisfaz) vão na seção `## Relações` do conceito — ficam só no repositório.
- **Decisões de implementação** sem caminho de arquivo e sem código — módulos, interfaces e contratos.
- **Decisões de teste:** proponha os **pontos de teste** (seams) — o mais alto possível, idealmente um por
  comportamento — e confirme com a pessoa: é por eles que as fatias vão provar que funcionam.
- Termos do glossário em todo o texto; termo novo já registrado pela entrevista.
- Mais de ~8 histórias ou mais de um objetivo de negócio → proponha dividir em dois épicos antes de escrever.

## Passo 4 — Revisão independente

Peça ao agente **`sdd-revisor`** a revisão do PRD (rubrica **P** de
[../sdd-revisar/references/rubricas.md](../sdd-revisar/references/rubricas.md)); sem o agente, aplique a rubrica
você mesmo, sem usar o raciocínio de quem escreveu como evidência. Corrija os achados (até 2 rodadas); o que for
decisão de negócio volta para a entrevista. Fase `em-revisao` no `status.md` do épico
([modelo](../sdd-especificar/SKILL.md#passo-3--pasta-de-trabalho-fora-do-git)) enquanto isso.

## Passo 5 — GATE do PRD (pessoa)

```
📄 PRD EP-<nn> — <título>
Histórias: <n> (<c> cenários) · Regras: <n> · Termos novos: <n> · No ELM: reusa <ids | —> · altera <ids | —> · novos verificados <n>
Decisões: <d> decididas · <a> em aberto (<bloqueantes>)
Revisão: <OK na rodada N | achados aceitos: …>
Aprovar? (o P.O. ou quem ele delegou)
```

- Decisão **em aberto que muda comportamento** → não há aprovação; volte à entrevista.
- Aprovado → Fase `aprovado` no `status.md` do épico; no `prd.md`, versão `1.0`, data e quem aprovou no rodapé. Em
  **cada** conceito de `elm/`: `status: stable` e um `verified` com `{ by: human:<login de quem aprovou>, at:
  <agora> }` — sem esse `verified` humano nada é publicado. Entrada `**Update**` no `log.md`. Grave só onde o PRD
  está:
  - **primeiro GATE** (PRD na pasta de trabalho) → só ali; levar a pasta para a base e gravar no `backlog.md` só o
    link `prd` e, se estava `—`, o da `pasta` (o épico segue `iniciado`) são da `sdd-especificar`. Próximo: "use
    `sdd-especificar EP-<nn>`" — ela fecha a sessão, leva o PRD aprovado para a base e diz o que vem depois
    (publicação no ELM e `sdd-fatiar`). Pare;
  - **mudança depois de aprovado** (PRD já na base) → na base, pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base),
    um commit; próximo: a [publicação dos requisitos](../sdd-consolidar/references/elm-publicar.md#requisitos-conceitos-okf-de-elm--doors-next) alterados (se a publicação é `na-aprovacao`)
    e o refinamento das fatias afetadas (`sdd-fatiar`). Pare — chamada pela `sdd-consolidar` (drift), devolva a ela,
    que segue para a publicação.

## Mudança depois de aprovado

Épico na Fase `aprovado` ou `fatiado`: o PRD só muda por um pedido explícito — incremente a versão (`1.1` correção,
`2.0` mudança de escopo), registre no rodapé, Fase `em-revisao` enquanto o que mudou é revisto, e repita o GATE.
Conceito alterado: `status: draft`, `generated.at` novo; no GATE, um `verified` novo é acrescentado à lista. A
publicação atualiza os mesmos artefatos (pelo `resource`/`id` de cada conceito). Fatias já entregues (`pronta` ou
`concluida`) que dependem do que mudou → avise e proponha fatias novas; não as altere.

## Regras

- Nunca invente regra, valor ou ator: sem fonte e sem decisão de uma pessoa, é `em aberto`.
- O PRD não tem caminho de arquivo, nome de classe nem SQL — isso é do plano da fatia.
- Escreva no idioma do projeto; nomes de sistemas, tabelas e campos na forma original.
- Não invoque nem simule outra skill além das que os passos mandam chamar (`sdd-entrevistar`, o subagente revisor): depois do GATE, diga a próxima e pare.
