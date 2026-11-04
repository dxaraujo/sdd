---
id: EP-<nn>
titulo: <título curto, linguagem do negócio>
po: <login do P.O.>
demanda: <id da demanda/épico no EWM | —>
atualizado: <AAAA-MM-DD>
---

# PRD — EP-<nn> <título>

> O quê e por quê, na linguagem do negócio. O **como** técnico fica no plano de cada fatia (`design.md`).
> Decisões: `decisoes.md` (nesta pasta) · Glossário e ADRs: caminhos no `.kiro/steering/sdd.md`

## Problema

<O problema do ponto de vista de quem sofre com ele: quem, quando, quanto custa hoje. 3–6 linhas.>

## Solução

<A solução do ponto de vista do usuário: o que passa a ser possível. Sem tecnologia. 3–6 linhas.>

## Atores

| Ator | Quem é | Como interage |
|---|---|---|
| <Operador do faturamento> | <perfil> | <tela X · API · agendamento · arquivo do parceiro> |

## Histórias, regras e termos (artefatos do ELM)

<!-- Cada história (HF), regra (REG) e termo novo (GL) é um conceito OKF v0.2 próprio em elm/ (formato em
     okf-elm.md da skill sdd-prd): é o que sobe para o DOORS Next depois do GATE. Aqui fica só o índice.
     Cenários são os critérios de aceite: cada um é verificável e vira caso de teste (ETM). -->

| Artefato | Arquivo | Resumo | No ELM |
|---|---|---|---|
| HF-01 | [HF - <nome>](elm/HF-01-<slug>.md) | <description> | novo (verificado <AAAA-MM-DD>) \| altera <id> |
| HF-02 | [HF - <nome>](elm/HF-02-<slug>.md) | <description> | novo (verificado <AAAA-MM-DD>) |
| REG-01 | — (existente no ELM) | <description> | reusa <id> |
| GL | [<termo>](elm/GL-<termo>.md) | <definição curta> | novo (verificado <AAAA-MM-DD>) |

## Decisões de implementação

<!-- Estilo Pocock: módulos, interfaces e contratos — sem caminho de arquivo nem código (eles envelhecem rápido).
     Só o que precisa de acordo antes de fatiar. -->

- **Módulos afetados:** <módulo e o que muda nele; módulo novo e sua interface pública>
- **Contratos:** <API, arquivo, mensagem — formato e versão>
- **Dados:** <entidades/tabelas novas ou alteradas — a DDL é do time de banco>
- **Integrações:** <sistema, sentido, frequência>

## Decisões de teste

- **Pontos de teste (seams):** <onde os testes entram — o mais alto possível; ex.: "a API `POST /login`" e
  "o módulo de bloqueio, pela interface pública">
- **O que é um bom teste aqui:** <comportamento externo, sem mock de detalhe interno, sem recalcular o esperado
  do jeito que o código calcula>
- **Precedente no código:** <testes vizinhos que servem de modelo>

## Não funcionais

| Tema | Requisito |
|---|---|
| Volume | <ordem de grandeza> |
| Desempenho | <tempo máximo, janela de execução> |
| Segurança e auditoria | <quem pode, o que é registrado> |

## Fora de escopo

- <o que fica explicitamente de fora — evita fatias que crescem sozinhas>

## Em aberto

<!-- Decisões "em aberto" do decisoes.md. Uma que muda comportamento impede a aprovação (GATE PRD). -->

| D | Tema | Bloqueia? |
|---|---|---|

---
Artefato produzido com apoio de IA generativa — fluxo sdd · Versão <x.y> · <AAAA-MM-DD>
