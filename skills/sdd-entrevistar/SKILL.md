---
name: sdd-entrevistar
description: "Entrevista de alinhamento do fluxo sdd (técnica \"grill me\"): percorre a árvore de decisões de uma demanda, PRD, fatia ou plano em rodadas (só as decisões da fronteira, numeradas, cada uma com a resposta recomendada) até haver entendimento compartilhado confirmado; responde sozinha o que o código, a documentação do ELM (bundle OKF) ou o glossário já respondem; registra cada decisão em decisoes.md e cada termo novo do domínio no glossário (linguagem ubíqua). Use em \"me entreviste\", \"grill me\", \"vamos alinhar\", \"quais decisões estão em aberto\", \"o que falta definir\", e sempre que sdd-prd, sdd-fatiar ou sdd-plano encontrarem decisão em aberto. Modo atendimento: uma rodada curta para registrar um AT na triagem (sdd-triar)."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.5"
---

# sdd-entrevistar — Alinhar antes de escrever

O erro mais caro de um fluxo com agentes é escrever bem a coisa errada. Antes de qualquer PRD, fatia ou plano,
feche as decisões que as fontes não respondem — o agente **não** preenche lacuna com suposição plausível.

## Entrada

- **O que está sendo alinhado:** demanda (texto, work item do EWM), PRD, fatia ou plano técnico.
- **Onde registrar:** a pasta do épico — até o GATE do PRD, a pasta de trabalho da `sdd-especificar`
  (`.kiro/local/especificacao/<EP>-<slug>/decisoes.md`, fora do git); depois, `<produto>/epicos/<EP>-<slug>/` — ou da fatia
  (`.kiro/specs/<ft>-<slug>/decisoes.md`) — ou, na triagem de uma fatia sem épico, a seção Decisões da ficha
  (`<produto>/fatias/FT-<nnn>-<slug>.md`). Quem chamou informa; chamada direta → pergunte uma vez.
- **Glossário:** o caminho está no `.kiro/steering/sdd.md` (seção Projeto; padrão `docs/glossario.md`).

## Passo 1 — Montar a árvore de decisões (sem perguntar nada ainda)

1. Leia o que já existe: a demanda, o `decisoes.md` (se houver), o glossário, os ADRs que tratam do assunto, o
   steering de produto e o PRD/fatia em questão.
2. Liste as decisões necessárias como uma **árvore**: escopo → atores → comportamento principal → exceções →
   dados → integrações → não funcionais (volume, prazo, segurança, auditoria) → fora de escopo. Uma decisão pode
   depender de outra: ordene para que a resposta de cima mude as de baixo.
3. **Responda sozinho o que tiver fonte**, citando-a — não pergunte o que dá para descobrir:
   - comportamento atual → o código (`arquivo:linha`);
   - regra documentada → bundle do ELM, pelo `elm_buscar_req_local` e `elm_ler_req_local` (nunca lendo os
     arquivos; [sem bundle → ELM remoto](../sdd/references/elm.md#bundle-local));
   - termo do domínio → glossário;
   - dado → banco pelo MCP de consulta (somente leitura), se o `sdd.md` declarar um.
   Fato encontrado vira decisão `confirmada — fonte: <…>`; não ocupa a pessoa.

## Passo 2 — Perguntar em rodadas, pela fronteira

A cada rodada, pergunte só a **fronteira**: as decisões cujos pré-requisitos já estão decididos. Numere, traga a
recomendada de cada uma e escreva de modo que **"sim" aceite todas as recomendadas**:

```
Rodada 2 · ramo: exceções · faltam ~5 decisões depois desta rodada

D-04 · Tentativas contam por usuário ou por IP?
     Contexto: o login registra só o usuário (`LoginService.java:42`); não há tabela por IP.
     Recomendo: por usuário — é o que o dado atual permite e o que a demanda descreve.
D-05 · O que a tela mostra para a conta bloqueada?
     Recomendo: a mensagem MSG 2005 do ELM ("Conta bloqueada temporariamente"), já usada no desbloqueio manual.

"sim" aceita as recomendações · ou responda por número (ex.: "D-05: mensagem nova, texto a definir")
```

- **Fatos são trabalho seu, decisões são da pessoa.** Antes de perguntar, mande buscar (subagente
  `sdd-pesquisador`, se houver) o que o código, o ELM ou o banco respondem.
- Recomendação sempre com o motivo em uma linha. Pergunta sem recomendação transfere o trabalho de pensar.
- Rodadas pequenas (até ~5 perguntas). Resposta que abre ramos novos → eles entram na próxima rodada.
- Resposta vaga ("tanto faz", "o de sempre") → registre a recomendada como decisão e diga isso.
- Termo novo ou ambíguo (dois nomes para a mesma coisa, um nome para duas coisas) → vira pergunta da rodada
  seguinte: qual é o termo canônico (Passo 4).
- Termina quando a fronteira está vazia: resuma as decisões e **peça a confirmação do entendimento** antes de quem
  chamou escrever qualquer coisa. A pessoa pode dizer "chega" antes: o que restar fica `em aberto` (Passo 3).

## Passo 3 — Registrar

`decisoes.md` — o formato único do fluxo (triagem, especificação e PRD criam por este) — (cria na primeira; só acréscimo — decisão revista ganha nova linha que **substitui** a antiga):

```markdown
# Decisões — <EP-xx | FT-xxx> <título>

| D | Pergunta | Decisão | Fonte / quem decidiu | Data | Situação |
|---|---|---|---|---|---|
| D-01 | Reprocessar registros já pagos? | Não: ignora e registra no log | ana.souza (P.O.) | 2026-10-13 | decidida |
| D-02 | Qual o limite diário? | 3 tentativas | código: `LoginService.java:42` | 2026-10-13 | confirmada |
| D-03 | Como notificar o bloqueio? | — | — | 2026-10-13 | em aberto |
| D-04 | (revisa D-01) Reprocessar os pagos de ontem? | Sim, só D-1 | ana.souza | 2026-10-14 | decidida — substitui D-01 |
```

Situações: `decidida` (uma pessoa respondeu) · `confirmada` (fonte encontrada) · `em aberto` (sem resposta) ·
`substituída`.

## Passo 4 — Linguagem ubíqua

Todo termo de negócio que apareceu (novo, renomeado ou desambiguado) vai para o glossário do projeto (artefato de
produto: pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base); durante uma especificação em andamento, o termo fica no `decisoes.md` da pasta de
trabalho e vai ao glossário no GATE do PRD):

```markdown
| Termo | Definição | Evitar | Fonte | ELM |
|---|---|---|---|---|
| Tentativa de login | Envio de credenciais pelo usuário, válido ou não | acesso, tentativa de acesso | D-02 | GL 3120 |
```

- Um termo por conceito; sinônimos vão para "Evitar". O código novo usa o termo canônico (o revisor confere).
- Termo que já existe no ELM (bundle) → cite o id na coluna ELM; termo novo fica com `—` e, num épico, vira um
  conceito `GL-<termo>.md` em `elm/` (`sdd-prd`), publicado como Termo de Glossário ([elm-publicar.md](../sdd-consolidar/references/elm-publicar.md)).
- O glossário é artefato de produto: só na branch base. Entrevista de uma **fatia** (na branch dela) → não grave o
  glossário; registre o termo no `decisoes.md` da fatia como `termo pendente`, e a `sdd-consolidar` o leva para o
  glossário depois do merge.

## Saída para quem chamou

```
Entrevista — <EP | FT> · <N> decisões: <d> decididas · <c> confirmadas por fonte · <a> em aberto
Termos no glossário: <novos> novos · <alterados> alterados
Em aberto (bloqueiam?): D-03 <tema> — <sim: muda o comportamento | não: detalhe de apresentação>
```

## Modo atendimento (chamado pela `sdd-triar`)

Uma rodada só, no mesmo formato (numerada, com recomendação, "sim" aceita tudo), sem árvore nem glossário:

```
Atendimento AT-012 · 6 perguntas

A-1 · O que o cliente precisa receber?   Recomendo: planilha com as contas bloqueadas por dia em setembro.
A-2 · Origem?                            Recomendo: chamado 4521 (citado no pedido).
A-3 · Prazo?                             Recomendo: 2026-10-16 (2 dias úteis).
A-4 · Quem responde?                     Recomendo: joao.lima (atende: true no equipe.json).
A-5 · Critério de pronto?                Recomendo: planilha enviada e chamado respondido.
A-6 · Estimativa?                        Recomendo: 3 h (extração simples no banco).
```

As respostas voltam para quem chamou (a `sdd-triar`), que as grava no cabeçalho do `AT-<nnn>-<slug>.md` — não num
`decisoes.md`. Regra de negócio em aberto que aparecer → não decide aqui: não é atendimento, e a triagem a trata
como fatia padrão ou épico.

## Regras

- Nunca invente resposta para destravar a entrevista. Sem fonte e sem pessoa → `em aberto`.
- Decisão de negócio é de uma pessoa (P.O. ou quem ela delegou); decisão técnica entre alternativas equivalentes é
  do codificador e vai para o `design.md`, não para cá.
- Modo autônomo (`AUTONOMO=true`, chamado por um agente sem pessoa na conversa): não pergunte — monte a árvore,
  resolva o que tem fonte e registre o resto como `em aberto` com a opção recomendada na coluna Decisão entre
  parênteses (`(recomendada: …)`). Quem chamou não pode tratar recomendação como decisão.
