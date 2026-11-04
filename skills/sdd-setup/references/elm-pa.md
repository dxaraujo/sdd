# ELM — montar o `pa_<nome>.json`, passo a passo

O `pa` decide o que o MCP `elm` grava em cada work item: um valor errado só aparece quando a PA recusa a criação, a
transição ou o lançamento de horas. Por isso aqui **não vale "padrão sem perguntar"**:

- **Só dois lugares de onde vem um valor:** a descoberta (`elm_setup_descobrir`) ou a pessoa. Nunca deduza um nome, um
  `qname`, um time code ou um valor de enumeração; nunca copie de outro projeto nem de um `pa` antigo sem mostrar a
  origem e pedir confirmação daquele valor.
- **Um bloco por mensagem**, na ordem abaixo: mostre as opções que a descoberta trouxe (numeradas), marque a
  recomendada, e espere a escolha. Valor de enumeração só da lista da PA.
- **Formato:** leia [assets/pa.schema.json](../assets/pa.schema.json) antes do bloco 0 e monte o `pa` nele — chaves,
  aninhamento e obrigatórios vêm do schema, não da memória.
- **Cartão de cada bloco** (ícones e peças em [wizard.md](wizard.md)):

  ```
  ### 🧩 ELM · Bloco <n>/10 · <nome do bloco>
  `<●●◉○○○○○○○○>` (11 posições: blocos 0 a 10) <o que este bloco decide, em uma frase>

  | # | Opção | Detalhe | Fonte |
  |---|---|---|---|
  | 1 | <valor> ⭐ (recomendado) | <…> | 🧩 |

  <n> de <n> da descoberta

  > ❓ **<pergunta do bloco>**
  > `<n>` escolhe · `ok` aceita a recomendada · `<n>: <valor>` muda uma linha
  ```

  **Todas** as opções que a descoberta trouxe aparecem na tabela — nunca "os mais prováveis" nem "os relevantes",
  com o resto resumido ou cortado; logo abaixo da tabela, a linha `<n> de <n> da descoberta` (os dois números iguais:
  conte os itens que o MCP devolveu antes de montar a tabela); a recomendada vai primeiro, com ⭐. Lista com mais de 12 opções → tabela em duas colunas
  (`| # | Opção | # | Opção |`). O resultado de um bloco pode abrir a mensagem do bloco seguinte só como a linha
  `✔ Bloco <n> — <valores>`, sem pergunta: dúvida sobre o bloco anterior → fica nele, com a pergunta dele. Resposta que não deixa claro o
  que muda (um "não" no meio de uma linha, "ok" a uma pergunta com duas partes, um formato que não é o do bloco)
  → repita o que entendeu, em tabela, e **pare**: a confirmação é a próxima resposta da pessoa — nunca feche o bloco
  na mesma mensagem em que interpretou; nunca passe ao bloco seguinte com uma pergunta aberta.
- **Nada é gravado** antes da conferência do bloco 10.
- **Modo atualização** (já existe `.kiro/config/sdd/pa_<nome>.json`): mostre o `pa` atual em tabela, bloco a bloco,
  e pergunte só o que muda.

## 0. Credencial e project areas

Não suponha rede: o ELM pode responder sem VPN mesmo quando o GitLab ou o banco não respondem — teste e diga o que
respondeu. `elm_status(projeto=<raiz>)` (sem `pa` ainda, `faltando` vem preenchido — normal): erro `credencial` → peça o `~/.config/mcp-elm/elm.properties` (`server`, `user`,
`password`; você não lê nem grava esse arquivo) e pare. Pergunte um trecho do nome da PA do EWM e se o DOORS Next e o
ETM usam o mesmo nome (ou qual) → `elm_setup_descobrir(ccm, rm?, qm?)`. Mostre as PAs achadas de cada um e confirme
qual é (nenhuma no ETM → sem `qm`: o fluxo não cria caso de teste no ETM, o `CT.csv` fica).

## 1. Time e categoria

Liste os times (`ccm.times`) com as categorias de cada um; recomende o de quem configura. A categoria
(`filedAgainst`) é a do time escolhido.

## 2. Tipos

Confirme o tipo do EWM para `ib` (épico, fatia e os da Sustentação) e `tarefa`, entre os tipos da descoberta, e
pergunte se o projeto registra **defeitos** no EWM: `defeito` é opcional — "não" → o `pa` fica sem ele e os blocos
seguintes não falam de defeito.

| # | Uso no fluxo | Tipo do EWM | Fonte |
|---|---|---|---|
| 1 | `ib` — épico, fatia, Sustentação, Manutenção, categoria e item de Sustentação | <Item de Backlog> | 🧩 |
| 2 | `tarefa` — ESP, DEV, REV, VER, APR, GB e as da Sustentação (ATD, IMPL, BD, INF, OPE, EXT) | <Tarefa> | 🧩 |
| 3 | `defeito` (opcional) | <Defeito | não usa> | 🧩 |

## Modelo do sdd: obrigatórios e valores por item

Os campos abaixo a PA cobra para criar, mudar de estado ou lançar horas, **mesmo com o tipo marcando-os como
opcionais** — por isso a descoberta não os traz em `obrigatorios`. É a configuração esperada em todo projeto: os
blocos 3 a 5 **já começam com ela marcada e preenchida**; a pessoa só confirma ou muda. Cada valor sugerido é
conferido contra a lista da PA (bloco 4): se a PA não tiver aquele valor, mostre a lista e pergunte — nunca grave um
valor que não está nela.

**Item de Backlog** — obrigatório 🔒 `Categoria` (o campo do tipo, não a categoria do time):

| # | Item | Título começa por | Categoria |
|---|---|---|---|
| 1 | épico | `[EP-` | Nova funcionalidade |
| 2 | fatia (de épico ou da Manutenção) | `[FT-` | Nova funcionalidade |
| 3 | Sustentação (pai da `[GB]`, da Manutenção e dos IBs de categoria) | `Sustentação` | Apoio Técnico |
| 4 | Manutenção (pai das fatias sem épico) | `Manutenção` | — (pergunte: valor da lista da PA) |
| 5 | item de Sustentação (`[AT-012] <pedido>`) | `[AT-` · `[IM-` · `[BD-` · `[IN-` · `[OP-` · `[EX-` | Apoio Técnico (a mesma da linha 3) |
| 6 | IB de defeito | — (vai na chamada) | Correção → linha "IB de defeito" do `sdd.md` |
| — | padrão do tipo (`padroes`) | qualquer outro título (inclusive o IB de categoria: `Atendimento`, `Implantação`…) | Apoio Técnico |

**Tarefa** — obrigatórios 🔒 `Categoria` (de integração de horas), `OTR`, `ID do Produto (Clarity)` e `Classificação
da Tarefa`:

| # | Tarefa | Título começa por | Classificação da Tarefa |
|---|---|---|---|
| 7 | especificação | `[ESP]` | Análise / Especificação |
| 8 | desenvolvimento | `[DEV]` | Desenvolvimento (Transacional / Analítico / IA / etc ) |
| 9 | revisão | `[REV]` | Desenvolvimento (Transacional / Analítico / IA / etc ) |
| 10 | verificação | `[VER]` | Testes |
| 11 | aprovação do plano e do PR | `[APR]` | Outra - Não listada |
| 12 | Sustentação — Atendimento | `[ATD]` | Suporte / Apoio Técnico Especializado |
| 13 | gerenciamento do backlog | `[GB]` | Outra - Não listada |
| 14 | Sustentação — Implantação | `[IMPL]` | — (pergunte: valor da lista da PA) |
| 15 | Sustentação — Banco de dados | `[BD]` | — (pergunte) |
| 16 | Sustentação — Infra | `[INF]` | — (pergunte) |
| 17 | Sustentação — Operação | `[OPE]` | — (pergunte) |
| 18 | Sustentação — Apoio a outros times | `[EXT]` | — (pergunte) |
| — | padrão do tipo (`padroes`) | qualquer outro título | Outra - Não listada |

As linhas 12 e 14–18 são as categorias da tabela **Sustentação** do `sdd.md` (a Classificação escolhida aqui vai
também para a coluna dela lá); categoria que o projeto acrescenta ganha uma linha aqui, com o prefixo dela, e a série
dela entra na linha 5. A Manutenção não tem linha de tarefa: as fatias dela usam as das linhas 8–11.

Iguais em toda tarefa (vão em `padroes`): `Categoria` = Aplicativo · `OTR` = 1-Apoio-Produtos · `ID do Produto
(Clarity)` = o código do produto do projeto — campo de texto, **sempre perguntado** (é de cada projeto; sem ele a
PA recusa o lançamento de horas).

## 3. Campos de cada tipo

**Um tipo por mensagem** (IB, depois tarefa, depois defeito se houver). Por tipo, **todos** os campos da descoberta
numa tabela `| | # | Campo | Tipo do valor | Obrigatório |` com a caixa `[✅]`/`[ ]` e a linha `<n> de <n> da
descoberta`. Já vêm marcados os do fluxo (Planejado para, Responsável, Estimativa na tarefa, critérios de aceite no
IB) e, como 🔒, os obrigatórios do **modelo do sdd** e os que a descoberta trouxe em `obrigatorios`. Campo do modelo
que a PA não tem → diga qual e pergunte se há um equivalente. `ok` aceita a marcação; `tirar <n>` tira (confirme:
sem ele a PA recusa depois); `pôr <n>` acrescenta (pergunte se é obrigatório).

A **categoria do time** (`filedAgainst`, "Atendido por", bloco 1) não é um campo desta tabela: o "Categoria" do tipo
é outro atributo, com a própria lista de valores — nunca use o nome da categoria do time como valor dele.

Os marcados entram em `campos`; os 🔒 também em `obrigatorios` — o MCP os exige já na criação, para nenhuma transição
ou lançamento esbarrar neles depois. Planejado para, Responsável e Estimativa podem ir em `obrigatorios` (chegam pela
iteração, pelo dono e pelas horas da chamada), nunca em `padroes`.

## 4. Valores

Antes do cartão, chame de novo `elm_setup_descobrir` com `valores_de` = **todos** os campos de enumeração marcados
no bloco 3 — sem isso a descoberta só traz valores dos obrigatórios do shape, e os do modelo ficam de fora. Um campo
por linha, com o valor do modelo já preenchido (⭐) e marcado ✔ se estiver na lista da PA; valor fora da lista →
mostre a lista inteira e pergunte. Campo de texto (o id de produto) → pergunte o valor; nunca deixe obrigatório sem
valor. "Planejado para" nunca vai em `padroes`: é a iteração da sprint ou o backlog do produto (`ccm.backlog`,
gravado pela `elm_backlog` depois do bloco 10).

## 5. Valor por item de trabalho

O MCP aplica, na criação: os `padroes` do tipo, depois o `por-prefixo` cujo texto **inicia** o título, depois os
campos da chamada. Mostre as tabelas do **modelo do sdd** (IB e tarefa), com os valores conferidos no bloco 4 e
**uma linha por item** — cada papel de tarefa na própria linha. A pessoa muda célula a célula (`<n>: <campo> =
<valor>`; `<n>: não usa` tira o prefixo — confirme, porque o fluxo cria esses itens). Valor de enumeração só da
lista da PA. Grave a linha "padrão do tipo" em `padroes` e cada prefixo com valor diferente em `por-prefixo`.
Antes da conferência, confira: todo campo de `obrigatorios` tem valor em `padroes` ou chega por parâmetro
(iteração, dono, estimativa).

## 6. Horas

**Não pergunte**: time code e tipo de trabalho são fixos — grave `"horas": { "time-code": "Horas Diretas",
"work-type": "Tarefa" }` e mostre-os na conferência do bloco 10 como padrão.

## 6 e 7 sem pergunta

Os blocos 6 (horas fixas) e 7 (links) não têm cartão nem pergunta: cada um vira uma linha `✔ Bloco <n> — …` no
começo da mensagem do bloco 8. A única exceção é a do bloco 7 abaixo: a descoberta trouxe um tipo de link de
dependência entre work items.

## 7. Links

Não escreva `links`: os padrões do MCP (pai, filhos, implementa, relacionado) são os do EWM. Só `depende`, e só se a
descoberta trouxer um tipo de link de dependência — mostre-o e confirme.

## 8. DOORS Next

Para cada sigla — `HF` (história), `REG` (regra), `GL` (termo de glossário), `ET` (especificação técnica) — pergunte o
tipo de artefato (lista `rm.tipos`) e a pasta (lista `rm.pastas`), com a recomendada pelo nome. Projeto sem uma delas
→ a sigla fica de fora. **Bundle** (`rm.download`): procure no repositório pastas com `index.md` de `okf_version` e
mostre; senão sugira `docs/elm/<nome>` e pergunte.

## 9. ETM

PA do ETM do bloco 0 → `qm` (nome e id). Sem PA → registre "sem casos de teste no ETM". Já decidido no bloco 0: sem cartão
nem pergunta — vira a linha `✔ Bloco 9 — …` no começo da conferência (bloco 10).

## 10. Conferência

Mostre o `pa` inteiro numa tabela legível — PA, time e categoria, cada tipo com campos, obrigatórios, padrões e
`por-prefixo`, horas, RM com cada sigla (tipo e pasta), bundle e ETM —, com a origem de cada valor (descoberta, pessoa ou
fixo), e depois o JSON. O JSON mostrado é **o que será gravado, byte a byte**: monte-o no formato do schema
(ids da descoberta inclusos — `ccm.id`, `time.id`, `categoria.id`, `tipos.*.id`, `campos` como `nome → qname`) e
confira contra o [schema](../assets/pa.schema.json) **antes** de mostrar. "ok" → grave `.kiro/config/sdd/pa_<nome>.json` (relativo à raiz, `/`, sem segredos — vai
para o git) e confira com `elm_status(projeto)`: `valido` e `faltando` vazio. A validação pediu mudança → mostre o diff do que
muda e peça "ok" de novo; nunca regrave em silêncio o que a pessoa aprovou.

**Validação** (recomendada; a PA recusa o que o `pa` não cobre): com "sim", `elm_criar_wi` de uma tarefa `[TESTE]
sdd-setup` (pai = um IB que a pessoa indicar), de um IB e de um defeito, `elm_transicao` de cada um até concluir e um
`elm_lancar_horas` na tarefa → cada recusa `precondicao` traz o `campo`: pergunte o valor (bloco 4), ponha-o em
`obrigatorios` e `padroes` e tente de novo. Os itens criados a pessoa cancela na UI; as horas de teste, remova com
`elm_remover_horas`.

**Backlog do produto** (depois do `pa` gravado, e também em "atualizar a configuração do sdd"; com o `pa` que já tem
`ccm.backlog`, só o espelhamento): é onde os itens triados nascem no EWM — siga
[elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §0 (pergunta a linha de base; já existe `<linha de base>/Backlog` → link ou id do plano; não existe → cria a
iteração e o plano `Backlog`; depois, com o `backlog.md` já em uso, o espelhamento).
Sem `ccm.backlog`, nada nasce no backlog do EWM. Outra project area → repita tudo (outro `pa_<nome>.json`) e diga na seção ELM qual é o padrão.
