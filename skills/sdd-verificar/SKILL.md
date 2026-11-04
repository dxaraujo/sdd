---
name: sdd-verificar
description: "Verificação de aceite de uma fatia do fluxo sdd — executa de ponta a ponta, na aplicação de verdade, cada cenário que a fatia cobre (API, job batch, tela no browser, carga de dados — conforme o tipo de projeto e o toolkit), com massa de teste, evidência por cenário (resposta, contagem, log, screenshot) e decisão ACEITO/REJEITADO; gera os casos de teste (CT.csv) para o ETM a partir dos cenários verificados. Cenário reprovado volta para a sdd-implementar com esperado × obtido. Com a tarefa [VER] (direto ou pelo hub sdd-iniciar), assume-a antes no EWM (elm_transicao). Use em \"verifica a FT-031\", \"pegar a [VER] da FT-031\", \"testa a fatia\", \"executa os cenários\", \"teste de aceitação\", \"gera os CTs\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.0"
---

# sdd-verificar — O comportamento existe de verdade?

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-verificar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Teste unitário verde prova que o código faz o que o teste diz; a verificação prova que o **sistema** faz o que o
cenário do PRD diz. Prefira o agente **`sdd-verificador`** (contexto limpo; não implementou a fatia).

Seja cético: quem implementou tende a achar que terminou, e funcionalidade pela metade costuma passar em teste de
unidade. "Feito" é uma afirmação; a evidência é a prova.

Entrada: pasta da fatia com revisão `APROVADO`, na branch da fatia. **HITL** (tarefa `[VER]` assumida no
Passo 0): só com `fase: em-verificacao` — a REV aprovou antes (sem isso, diga que a `[VER]` espera a revisão e
pare, **antes** do Passo 0, sem assumir a `[VER]`; retomando uma verificação interrompida, `em-verificacao` vale);
vá para a branch do PR (`git switch <branch>` com "sim", `git pull --ff-only`) e a rodada de verificação é sua. Tipo de projeto, como executar e onde ver o
resultado: seção **Verificação de aceite** do `.kiro/steering/sdd.md` (vem do toolkit, confirmado na setup).

## Passo 0 — Assumir a `[VER]` (só com a tarefa)

Chamada com a tarefa `[VER] FT-nnn` (só existe no HITL) — direto, pela pessoa do papel, ou pelo hub `sdd-iniciar`: antes de tudo,
quem está na sessão **não pode ser quem implementa** a fatia (o `responsavel` do `backlog.md` ou o `Responsável` do
`status.md`) — sem exceção, nem com "sim". É → diga isso, quem é o verificador da fatia (coluna Verificador no
`sprint-<nn>.md`, que a puxada também tem) e pare, sem assumir a `[VER]`. Numa sessão com o
MCP `elm`: `elm_transicao(<id da [VER]>, "assumir")`, com "sim" (regras: [elm.md](../sdd/references/elm.md)); já
concluída (o PR mudou depois do aceite: conflito no merge) → antes, `elm_transicao(<id>, "reabrir")`, na mesma
confirmação. Sem o MCP `elm` → `ELM pendente [<chave>]: assumir [VER] FT-<nnn>` no Histórico do `status.md`, e siga.
Chamada como subagente por outra skill (a rodada de verificação do loop ou da implementação), sem a tarefa → pule este passo: quem chamou é o dono da
rodada.

## Passo 1 — Roteiro

`status.md`: AFK → `fase: verificando`; HITL → a fase continua `em-verificacao`; linha no Histórico.

O roteiro parte do **contrato de pronto** do `design.md` (acordado no GATE do plano, antes do código) — não o
afrouxe agora. Para cada cenário que a fatia cobre, escreva-o em `verificacao.md` **antes** de executar
(trilha rápida: os comportamentos esperado e que não muda do `bugfix.md`):

```markdown
### HF-01 · 1.2 — Rejeitar após a terceira tentativa inválida
- Massa: <script/fixture e o estado que ele cria>
- Executar: <requisição HTTP | comando do job com parâmetros | passos no browser | carga>
- Esperado: <exatamente o "Então" do cenário, com valores>
- Verificar em: <resposta | SELECT … | log | tela>
```

## Passo 2 — Ambiente e massa

- Suba a aplicação/job como o `sdd.md` manda (comando **Executar**) — ambiente local ou de teste,
  **nunca produção**.
- Massa de teste: scripts da convenção do projeto (seção Verificação de aceite do `sdd.md`); sem convenção, crie-a
  em `.kiro/specs/<ft>-<slug>/massa/`. Escrita em banco **só** pelos scripts de massa; consultas pelo MCP de banco,
  somente leitura.
- Campo Banco do `status.md` = `pendente` → pare: a verificação depende da DDL aplicada em dev.

## Passo 3 — Executar e registrar

Execute cenário por cenário e registre logo abaixo do roteiro:

```markdown
- Resultado: ✅ aceito | ❌ rejeitado | ⚠️ ambiente
- Obtido: <o que aconteceu, com valores>
- Evidência: <trecho da resposta | resultado da consulta | linha de log | evidencias/ft-031-1.2.png>
```

- Por tipo de projeto: **backend** → chamada HTTP (pelo `sh .kiro/sdd/http.sh <MÉTODO> <caminho> [corpo]`, se o
  `sdd.md` o registra — o corpo vem da pasta `massa/`; senão `curl`, que pede confirmação) e estado no
  banco; **batch** → execução do job com a massa, status da execução e contagens; **frontend** → navegação real
  no browser (Playwright ou MCP de browser ligado ao agente), screenshot em `evidencias/`; **dados** → carga e
  consultas de verificação.
- Rode também os cenários de **repetição** (execute duas vezes; conte de novo) e de **erro em um item**.
- Falha por ambiente (serviço fora do ar, credencial de teste) → `⚠️ ambiente`, não rejeição; diga o que faltou.

## Passo 4 — Decisão

```
🔎 Verificação FT-<nnn> — rodada <N>
Cenários: <a> aceitos · <r> rejeitados · <e> ambiente
Drift de negócio: não | sim — <cenário ajustado e por quê>
VERIFICACAO: ACEITO | REJEITADO
```

**Drift de negócio** = `sim` quando algum cenário foi ajustado nesta verificação (o roteiro ou o Esperado deixou de
ser o do PRD ou da ficha, por decisão registrada). HITL: grave-o no campo do `status.md` (só sobe de `não` para
`sim`); AFK: fica no relatório e quem conduz grava. A consolidação só lê esse campo.

- **ACEITO** (todos aceitos) → gere o `CT.csv` (Passo 5).
  - **AFK** (subagente do loop ou da `sdd-implementar`): `fase: verificada` e devolva para abrir o PR (Passo 5 da
    `sdd-implementar`). Não há `[VER]` no EWM (Q8).
  - **HITL**: `fase: aceita`, e a **entrega**, nesta ordem — o Dev só acha o seu trabalho no remoto:
    1. créditos da sessão no `status.md` ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4); commit de `verificacao.md`, `CT.csv`, `evidencias/`,
       `massa/` e `status.md` (`FT-<nnn> verificação: ACEITO`);
    2. push da branch do PR (`git push origin <branch>`, nunca a base; o Kiro pergunta). Push recusado (pela
       pessoa ou pela regra) → entregue o comando pronto e espere a pessoa dizer que publicou;
    3. **confira no remoto:** `git fetch` e `git rev-parse HEAD` = `git rev-parse origin/<branch>`. Diferente → não
       siga: diga o que falta;
    4. só então: saldo de horas e conclusão da `[VER]` (`elm_horas` → `elm_lancar_horas` do saldo → `elm_transicao(<id>, "concluir")`, numa
       confirmação; sem o MCP `elm` → `ELM pendente [<chave>]: lançar <h>h e concluir [VER] FT-<nnn>`) e avise o **Dev
       responsável** de que a fatia está `aceita`, à espera do merge (Passo 6 da `sdd-desenvolver`).
- **REJEITADO** → para cada cenário, esperado × obtido + evidência, registrados no `status.md` como achados.
  AFK: `fase: implementando`; a `sdd-implementar` corrige e a verificação roda de novo (só os rejeitados + os de
  repetição). HITL: `fase: retrabalho (de: em-verificacao)`, "retrabalho" +1 em Rodadas e uma linha na tabela
  **Retrabalho** (papel VER); a `[VER]` fica em andamento; entrega como no aceito (commit `FT-<nnn> verificação: REJEITADO` → push →
  conferir no remoto) e avise o Dev responsável. Se o
  problema é o cenário estar errado no PRD, diga isso: é com o P.O., não com o código.
- Só `⚠️ ambiente` → `fase: bloqueada (de: verificando)` (HITL: `de: em-verificacao`) com o que falta; ninguém corrige código. Cenário misto
  (❌ + ⚠️) → REJEITADO, e o ⚠️ também vai para Achados como "ambiente".
- Cenário errado no PRD (não no código) → `fase: bloqueada (de: verificando)` (HITL: `de: em-verificacao`) com a pergunta ao P.O.; a
  correção é a mudança do PRD depois de aprovado (`sdd-prd`), não o código.

## Passo 5 — Casos de teste para o ETM

Gere `CT.csv` na pasta da fatia — um caso por cenário verificado — no formato de
[references/ct-csv.md](references/ct-csv.md). Na consolidação, depois do merge, a `sdd-consolidar`
cria a partir dele um caso de teste por cenário no ETM, já ligado à história (`elm_criar_ct`,
[elm-publicar.md](../sdd-consolidar/references/elm-publicar.md)); o CSV também é a
alternativa para importar à mão quando a criação falha.

Rodadas: quem pediu a verificação incrementa "verificação" (a `sdd-implementar` ou o orquestrador); só no
pedido direto de uma pessoa, incremente você.

## Regras

- Nunca marque aceito sem evidência. Nunca altere código de produção aqui — só massa, fixtures e evidências.
- Nunca rode contra produção, nem com dado real de pessoa. Evidência ou trecho de resposta que traga dado real
  (homologação com cópia de produção, por exemplo) vai para `.kiro/local/verificacao/<ft>/`, fora do git; no
  `verificacao.md` ficam a consulta, a contagem, o caminho e um resumo sem identificar pessoas.
- Não invoque nem simule outra skill do fluxo: termine com a decisão (e, com a `[VER]`, o aviso ao Dev) e pare. Como
  subagente, devolva o relatório a quem chamou.
