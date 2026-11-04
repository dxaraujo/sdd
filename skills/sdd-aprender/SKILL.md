---
name: sdd-aprender
description: "Aprendizado composto do fluxo sdd — transforma cada correção humana em melhoria permanente: registra a lição (o que o agente fez, o que era o certo, onde estava a informação, causa: falta de contexto, regra não escrita, revisão branda, PRD incompleto, skill desatualizada), propõe a correção na fonte certa (steering, glossário, skill do toolkit, rubrica, PRD) e promove regras para a seção Regras aprendidas do .kiro/steering/sdd.md com aprovação de uma pessoa. Também faz a retrospectiva da fatia/sprint com dados. Use em \"isso está errado, aprenda\", \"registra a lição\", \"o agente sempre erra X\", \"retrospectiva\", \"resumo das lições\", e quando a revisão, a verificação ou o PR reprovarem algo que um humano teve de corrigir."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.0"
---

# sdd-aprender — Cada erro corrigido uma vez só

Todo retrabalho tem uma causa no **ambiente** do agente: contexto, verificação ou processo. Corrigir só o código
resolve hoje; corrigir o ambiente resolve para sempre. Arquivos (versionados):

- `<produto>/aprendizado/licoes.md` — log de lições (só acréscimo);
- a seção **Regras aprendidas** do `.kiro/steering/sdd.md` — regras promovidas de **julgamento** (o revisor
  cobra, o plano respeita; o steering é sempre carregado, então cada regra é curta, imperativa, com exemplo).

Os dois só mudam na **branch base** (artefato de produto), pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base) (com
"sim" na troca de branch; alterações pendentes na branch da fatia → commite-as ou peça à pessoa antes).

**Ordem de preferência da correção:** (1) erro **mecânico** → checagem determinística (lint, teste, hook, CI) —
ponto final, não vira texto; (2) regra de **julgamento** → seção Regras aprendidas do `sdd.md` (o revisor
cobra); (3) conhecimento de domínio → glossário, ADR ou PRD/ELM; (4) conhecimento de stack → skill do toolkit. O steering recebe só a regra
curta, nunca a explicação longa (ela fica no `licoes.md`).

## Modo registrar (a cada correção)

Gatilhos: achado da revisão que chegou ao humano, cenário rejeitado na verificação, PR com mudança pedida,
pessoa dizendo "não é assim", bloqueio por falta de informação.

Chamada pela `sdd-consolidar` com uma linha das **Lições candidatas** do `status.md` (gravada pelo Dev com a `pronta`,
no `status.md` da base):
os fatos e a causa já vêm de quem recebeu a correção — grave-os no `licoes.md` sem perguntar de novo (passo 3).

1. **Fatos** (só verificados; o que a pessoa disse é registrado como dito por ela):
   - o que foi feito (`arquivo:linha`, trecho) × o que era o certo;
   - onde a informação certa estava — ou que não estava em lugar nenhum.
2. **Causa** (proponha; a pessoa confirma):

| Causa | Quando | Correção na fonte |
|---|---|---|
| `contexto-ausente` | a informação não existia em steering, PRD, glossário ou skill | escrever onde ela deve morar |
| `contexto-ignorado` | existia e o agente não seguiu | se é mecânico: checagem determinística; senão regra em Regras aprendidas |
| `prd-incompleto` | faltava regra/cenário no PRD | PRD nova versão (`sdd-prd`) + publicar no ELM |
| `plano-errado` | estava no PRD e não foi para o plano | regra R-nn em Regras aprendidas (aplica a: plano) |
| `revisao-branda` | a revisão viu e não reprovou (ou não viu) | regra R-nn em Regras aprendidas (aplica a: revisor) com a severidade certa — as rubricas ficam no power e não são editadas no projeto |
| `skill-desatualizada` | a skill do toolkit ensinou o jeito errado | corrigir a skill do toolkit (avisar quem mantém) |
| `ambiente` | build, dado ou serviço de teste | registrar; não vira regra |

3. Grave em `licoes.md`:

```markdown
## L-<nnn> · <AAAA-MM-DD> · FT-<nnn> · <causa>
- Feito: <…> (`arquivo:linha`)
- Certo: <…> — fonte: <onde estava | "não estava escrito">
- Correção na fonte: <proposta> · Situação: <proposta | aplicada | promovida → R-<nn> | descartada>
```

4. Mesma causa e mesmo tipo de erro já registrado (2ª ocorrência) **ou** a pessoa pede → proponha a promoção.

## Modo promover

Regra promovida é curta, imperativa, verificável e com exemplo — o revisor consegue checá-la:

```markdown
### R-<nn> · <título> · aplica a: <codificador | revisor | plano | PRD | todos> · severidade: <BLOQUEANTE | IMPORTANTE>
<A regra em 1–2 frases imperativas.>
- ✅ <exemplo certo> · ❌ <exemplo errado>
- Origem: L-<nnn>, L-<nnn>
```

Mostre o diff da seção Regras aprendidas do `.kiro/steering/sdd.md` e grave só com "ok" (o resto do arquivo
não muda). Regra que pertence à stack (ex.: "todo
`ItemWriter` deve ser idempotente") → proponha também levá-la para a skill do toolkit, onde serve a outros projetos.

Mantenha a seção curta: regras que viraram checagem determinística, rubrica, ADR ou skill saem dele com
`→ movida para <destino>` no `licoes.md`. Lições reais também viram **casos de avaliação** do fluxo: guarde o
pedido e o resultado esperado em `<produto>/aprendizado/avaliacoes/` para conferir, quando o modelo ou o fluxo mudar,
que o erro não voltou.

## Modo retrospectiva (fim de fatia, épico ou sprint)

De **sprint**: antes dos dados, a [pré-condição dos ritos de fechamento](../sdd-planejamento/SKILL.md#pré-condição-dos-ritos-de-fechamento)
inteira — a sincronização com o EWM ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §9, com a rede
de proteção: sempre a tabela com as divergências e as por fora, ou a linha `🔄 <chave> × EWM: iguais — <n> itens
conferidos`; sem o MCP `elm` → avise "sincronização com o EWM não feita" e siga, só com as linhas do git) e a
consolidação (fatia `pronta` que a espera → pare, salvo decisão do P.O.).

Com dados, não impressões:

```
🔁 Retrospectiva — <FT | EP | <pai>/Sprint <nn>>
Fluxo: <fatias concluídas> · lead time médio <d> dias · retrabalho <n> rodadas de revisão / <n> verificações
Onde o humano corrigiu: <lista de L-nnn por causa>
Autonomia: AFK <n> (<x> chegaram ao PR sem intervenção) · HITL <n>
Créditos: <total> · por fatia <média> · por versão do power sdd <versão> <x> · …
Propostas: <promoções, rubricas, skills, steering>
```

Fontes: `status.md` das fatias (Histórico; a seção Créditos, para a versão do power), `revisao-*`, `verificacao.md`,
`licoes.md`, `backlog.md` e `sprint-<nn>.md` (Status; a coluna Créditos, para o total por item). Termine
perguntando quais propostas aplicar. Retrospectiva de épico ou de sprint grava, no commit dela, a linha de créditos
da sessão na seção **Créditos de gestão** do `sprint-<nn>.md` aberto (Atividade `retrospectiva`; ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4))
e, na sessão do P.O. ou do SM, o comentário de créditos na `[GB]` (o mesmo item 4).

**Lint do conhecimento** (retrospectiva de épico — a consolidação da última fatia o sugere — ou de sprint, ou
quando a pessoa pedir; nunca a cada fatia): procure contradições entre glossário, ADRs, bundle do ELM (pelo
`elm_buscar_req_local`) e steering — termo com duas definições, ADR superado sem marcação, regra do ELM que o código não
segue. Liste como achados na retrospectiva; cada um vira correção na fonte ou fatia nova.

## Regras

- Nunca culpe pessoas; a lição é sobre o contexto e o processo.
- Nunca promova sem "ok". Nunca apague lição (só acréscimo).
