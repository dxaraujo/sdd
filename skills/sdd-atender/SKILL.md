---
name: sdd-atender
description: "Skill de quem atende no fluxo sdd — executa um atendimento (chamado ou pedido do cliente; a categoria Atendimento da Sustentação) já registrado pela sdd-triar (AT-nnn: IB [AT-nnn] e tarefa [ATD]): assume a [ATD] no EWM (criando o IB e a tarefa que faltarem) e grava o AT em-andamento na base, consulta o banco (somente leitura) e o bundle do ELM, com código só em escopo fechado, guarda extrações fora do git (.kiro/local/sustentacao/atendimento/), redige a resposta para o \"ok\" da pessoa e finaliza — registra a resposta, lança o saldo de horas, conclui a [ATD] e o IB do AT e pergunta os desdobramentos (arquivar · alteração pela sdd-triar · regra pela sdd-entrevistar · lição pela sdd-aprender). Pedido novo não abre aqui: passa pela sdd-triar. Use em \"atender o AT-012\", \"pegar a [ATD] 669380\", \"extrai os dados do AT-012\", \"enviei a resposta\", \"conclui o AT-012\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.7"
---

# sdd-atender — Atender sem perder o rastro

Atendimento é trabalho real que não vira código: alguém pergunta (chamado, e-mail, pedido), o time consulta, responde
e segue. É a categoria **Atendimento** da **Sustentação** — a única categoria com fluxo próprio; as demais
(Implantação, Banco de dados, Infra, Operação, Apoio a outros times) usam a [`sdd-executar`](../sdd-executar/SKILL.md).
A **`sdd-triar`** registra a demanda (`AT-nnn`, linha na `### Atendimento` da `## Sustentação` do `backlog.md`, IB
`[AT-nnn]` no EWM; a tarefa `[ATD]` nasce quando o AT entra numa sprint); esta skill é a de quem **atende**: assume
a `[ATD]`, executa e finaliza, deixando um registro versionado **sem dado de cliente**.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Arquivos

- `<produto>/sustentacao/atendimento/AT-<nnn>-<slug>.md` — o registro (formato no fim), criado pela triagem.
- Linha do AT na `### Atendimento` da `## Sustentação` do `backlog.md` e do `sprints/<pai>/sprint-<nn>.md`.
- `.kiro/local/sustentacao/atendimento/AT-<nnn>/` — extrações, telas e respostas com dado real. Fora do git.

## Passo 1 — O que chegou

| Entrada | Como ler |
|---|---|
| `AT-nnn` ou `[ATD] AT-nnn` | a linha na `### Atendimento` do `backlog.md` e o `AT-<nnn>-<slug>.md`, na base (itens 1 e 5 do bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base): o registro é gravado ali durante todo o atendimento) |
| número do EWM do IB `[AT-nnn]` ou da `[ATD]` | a linha do `backlog.md` com esse id em `elm` |
| pedido novo ("o cliente pediu …"), ou AT fora do backlog | não está registrado → "use `sdd-triar`" e pare — nunca abra AT aqui |
| AT `concluido` ou `cancelado` | mostre a situação e pare; reabrir é um AT novo pela triagem |
| item de outra categoria da Sustentação (`IM-`, `BD-`, `IN-`, `OP-`, `EX-`; tarefa `[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]`) | não é desta skill → "use `sdd-executar <item>`" e pare |

Não é atendimento (pedido que muda o comportamento do sistema, ou regra que ninguém decidiu) → devolva à
`sdd-triar` para refazer a triagem e pare.

## Passo 2 — Assumir a `[ATD]`

AT fora da sprint aberta (`sprint` `—`, sem linha viva na `### Atendimento` do `sprint-<nn>.md` aberto: sem sprint,
fora da reserva na triagem ou só a linha com `saiu da sprint` — [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base),
Linha viva) → a decisão é do P.O. (`sdd-planejamento`, Encaixe) e pare; com a linha viva na sprint, siga
(a reserva já foi decidida ali).

1. **EWM**, com "sim": falta o IB `[AT-nnn]` (`elm` `pendente`: AT registrado sem o MCP `elm`) ou a `[ATD]` → antes,
   crie o que faltar ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §6) e grave os ids na coluna `elm`
   do `backlog.md` e em "Tarefa ELM" da linha do AT no `sprint-<nn>.md`. Depois `elm_transicao(<id da [ATD]>,
   "assumir")` (já minha → `ja_estava`, nada a fazer; de outra pessoa → `conflito`: pergunte e repita com
   `forcar: true`; já fechada → `precondicao` "já concluída: reabra antes": mostre o estado e, com "sim",
   `elm_transicao(<id>, "reabrir")` e de novo o `assumir`, ou o AT a `concluido` como a sincronização faz — linha
   "tarefa concluída" da Sustentação ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §9) — e pare).
   Sem o MCP `elm` → `ELM pendente [<chave>]: assumir [ATD] AT-<nnn>` no registro do AT, e siga.
2. **Base:** `em-andamento` no `status` do `backlog.md`, na Situação da linha do sprint e no `**Situação:**` do
   registro, pelos itens 3 e 4 do bloco Gravar na base — commit `AT-<nnn> iniciar`, antes de executar (atender e
   concluir de uma vez, nesta sessão → um commit só, o do Passo 5). Já `em-andamento` (retomada) → nada a gravar.

## Passo 3 — Executar

1. **Fontes, nesta ordem** — subagente `sdd-pesquisador`, se houver: banco pelo MCP de consulta (**somente
   leitura**) e bundle do ELM pelo `elm_buscar_req_local`/`elm_ler_req_local` ([sem bundle → ELM remoto](../sdd/references/elm.md#bundle-local)). Código só se necessário e em escopo fechado:
   termos ou arquivos indicados e um limite de leitura, para não gastar tokens. Se a demanda envolver lógica de
   negócio complexa (regras de cálculo, fluxos condicionais, comportamentos do sistema) — e não for uma extração
   simples de dados — considere acionar o **`sdd-pesquisar`** antes das consultas SQL para entender o contexto
   do código; nesse caso, registre no AT: `"análise baseada em pesquisa de código"`. Sem tempo para pesquisa:
   registre `"resposta baseada apenas no bundle do ELM e no banco"` na seção Consultas do AT.
2. **Resultado com dado real** (linhas, telas, planilhas) → `.kiro/local/sustentacao/atendimento/AT-<nnn>/`. No registro
   ficam só a consulta (SQL), a contagem, o caminho do arquivo e um resumo **sem identificar pessoas**.
3. **Rascunho da resposta** → "ok" da pessoa antes de enviar. Quem envia é a pessoa; o agente não manda e-mail
   nem responde chamado.
4. **Horas** podem ser lançadas a qualquer momento (`elm_lancar_horas(id, horas)`, com "sim"): lançar não conclui a
   `[ATD]`. Ao fechar cada sessão do atendimento, os **créditos** dela na seção Créditos da ficha ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4)
   — vão no commit do atendimento.

## Passo 4 — Finalizar ("enviei", "conclui o AT-012")

1. Grava no registro a resposta enviada (sem dado de cliente; o texto com dado real fica em `.kiro/local/`).
2. **Saldo de horas:** mostre o que já foi lançado na `[ATD]` (`elm_horas(id)`) e pergunte só o que falta →
   `elm_lancar_horas(id, horas)`; depois `elm_transicao(id, "concluir")` na `[ATD]` e no IB `[AT-nnn]`, com uma
   confirmação. Cada lançamento ganha uma linha na tabela Horas do registro. Sem o MCP `elm` ou com
   falha → `ELM pendente [<chave>]: lançar <h>h e concluir [ATD] e IB AT-<nnn>` no registro.
3. Créditos desta sessão na ficha (como no Passo 3, item 4); `**Situação:** concluido` no registro; na linha do AT
   no `backlog.md`, `status` `concluido` e `concluida-em`; na `### Atendimento` do `sprint-<nn>.md`, a Situação e os
   Créditos da linha do AT (a soma da seção Créditos; o `creditos` do `backlog.md` é da virada da sprint). O commit
   é **um só**, no fim do Passo 5 (com a Saída), pelos itens 3 e 4 do bloco Gravar na base.

## Passo 5 — Desdobramentos

Pergunte o que mais sai do atendimento e registre a resposta em **Saída** no registro:

```
✅ AT-<nnn> concluído. Algum desdobramento?
  1. arquivar — nada mais a fazer
  2. gerar alteração (defeito ou mudança) → use `sdd-triar` com origem AT-<nnn>
  3. regra que ninguém decidiu → use `sdd-entrevistar`
  4. consulta reaproveitável → lição pela `sdd-aprender`
```

Grave a resposta em **Saída** e faça agora o commit único do Passo 4, item 3 (registro, backlog e sprint). Só
instrui e para: **nunca invoque nem simule outra skill**.

## Registro

`<produto>/sustentacao/<pasta>/<ID>-<slug>.md` (pasta da categoria na tabela **Sustentação** do `sdd.md`) — o mesmo formato para toda categoria; fora do Atendimento, `## Consultas`
e `## Resposta enviada` dão lugar a `## O que foi feito` (passos e evidência, sem dado de cliente).

```markdown
# AT-012 · Extração de contas bloqueadas em setembro

**Categoria:** Atendimento · **Origem:** chamado 4521 · **Pedido por:** área de segurança · **Prazo:** 2026-10-16
**Responsável:** joao.lima · **Situação:** aberto | em-andamento | concluido | cancelado
**Critério de pronto:** planilha com as contas bloqueadas por tentativas, por dia · **Estimativa:** 3 h

## Pedido
<o que o cliente precisa receber, nas palavras dele, sem dado pessoal>

## Consultas
| # | Consulta (SQL) | Resultado |
|---|---|---|
| 1 | `select count(*) from conta where situacao = 'B' and dt_bloqueio between …` | 1.284 contas |

Arquivo: `.kiro/local/sustentacao/atendimento/AT-012/contas-bloqueadas-2026-09.csv` (fora do git)

## Resposta enviada
<texto, sem dado que identifique pessoas>

## Horas
| Data | Horas |
|---|---|
| 2026-10-14 | 2 |

## Créditos
| Data | Papel | Login | Sessão Kiro | Power sdd | Créditos |
|---|---|---|---|---|---|
| 2026-10-14T16:20:05 | atendimento | joao.lima | 5753e516 | 2.9.0 | 3.12 |

**ELM:** feito | pendente: <o que falta>
**Saída:** — | FT-040 (defeito) | D-07 em aberto | lição L-015
```

## Regras

- **Dado de cliente nunca vai para o git**: resultado de consulta, extração ou tela com dado real fica em
  `.kiro/local/sustentacao/atendimento/AT-<nnn>/`. O registro guarda consulta, contagem, caminho e resumo anônimo.
- Banco só em leitura. Pedido que exige escrita na base não é atendimento: vira Banco de dados (`[BD]`, a pessoa
  executa o script fora; pela `sdd-executar`) ou, se muda o repositório, fatia de Manutenção.
- Um IB `[AT-nnn]` e uma `[ATD]` por demanda, sem balde. Registrar o AT é da `sdd-triar`; esta skill nunca numera
  nem abre AT (só cria no EWM o IB e a tarefa que faltam a um AT registrado).
- Lançar horas é registro de empenho, a qualquer momento na `[ATD]` assumida; concluir é o Passo 4, com o saldo.
- Toda escrita no EWM e todo envio de resposta pedem confirmação da pessoa.
