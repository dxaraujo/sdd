# Ficha da fatia — `<produto>/fatias/FT-<nnn>-<slug>.md`

**Toda fatia tem ficha**: o que fazer, os critérios de aceite e como verificar, num arquivo que a pesquisa, o
plano, a revisão, a verificação e a consolidação leem. Quem escreve: a **`sdd-triar`** (fatia sem épico) ou a
**`sdd-fatiar`** (fatia de épico). Artefato de produto: só na branch base. A coluna `ficha` do `backlog.md` é
sempre preenchida e a Definition of Ready confere o arquivo. O conteúdo muda com a trilha:

| Trilha | Seções | De onde vem o critério |
|---|---|---|
| padrão sem épico | Pedido · Regras · Cenários de aceite · Decisões · Fora de escopo (formato abaixo) | os cenários `C<n>` da própria ficha |
| padrão de épico | Objetivo · Cobre (links para os cenários do PRD, sem copiar) · Como verificar | o PRD (`cobre`) |
| rápida | Comportamento (atual com evidência · esperado com fonte · o que não muda) · Como verificar | a ficha — é o que o `bugfix.md` detalha |

Item das categorias da Sustentação (`AT-nnn`, `IM-nnn`…) não é fatia: não tem ficha, tem o registro
`<produto>/sustentacao/<pasta>/<ID>-<slug>.md`. A fatia de Manutenção (sem épico) tem ficha, como toda fatia.

## Formato — padrão sem épico

```markdown
# FT-040 · Limitar o desconto de pontualidade a 10% da parcela

**Trilha:** padrão · **Origem:** IB 613 · **Pedido por:** área financeira · **Modo:** HITL · **Tamanho:** M
**Situação:** aprovada por ana.souza em 2026-10-15

## Pedido
<o que mudar e por quê, nas palavras de quem pediu>

## Regras
| Regra | Texto | Fonte / decisão | No ELM |
|---|---|---|---|
| R1 · Teto do desconto de pontualidade | O desconto de pontualidade nunca passa de 10% do valor da parcela. | D-01 (ana.souza) | altera 2101 |

## Cenários de aceite
**C1 · Desconto acima do teto é limitado**
Dado uma parcela de R$ 1.000,00 com desconto de pontualidade calculado em R$ 150,00
Quando o pagamento é feito até o vencimento
Então o desconto aplicado é de R$ 100,00

**C2 · Desconto abaixo do teto não muda**
Dado uma parcela de R$ 1.000,00 com desconto de pontualidade calculado em R$ 50,00
Quando o pagamento é feito até o vencimento
Então o desconto aplicado é de R$ 50,00

## Decisões
| D | Pergunta | Decisão | Fonte / quem decidiu | Data | Situação |
|---|---|---|---|---|---|
| D-01 | O teto vale por parcela ou por contrato? | Por parcela | ana.souza (P.O.) | 2026-10-15 | decidida |

## Fora de escopo
- Parcelas já pagas não são recalculadas.
```

## Formato — padrão de épico (escrita pela `sdd-fatiar`)

```markdown
# FT-031 · Bloquear a conta após 3 tentativas inválidas

**Trilha:** padrão · **Épico:** EP-03 · **Modo:** AFK · **Tamanho:** M

## Objetivo
<o comportamento que a fatia entrega, em 1–2 frases>

## Cobre
- [HF-01 · 1.1](../epicos/EP-03-<slug>/elm/HF-01-<slug>.md) · [HF-01 · 1.2](…) · [REG-01](…)

## Como verificar
<o ponto de observação: chamada, job, tela, consulta — o detalhe fica no contrato de pronto do `design.md`>
```

## Formato — rápida

```markdown
# FT-044 · Não gerar espaço duplo ao remover pontuação do nome

**Trilha:** rápida · **Origem:** DF 4567 · **Modo:** AFK · **Tamanho:** P

## Comportamento
- **Atual:** `"Maria - Joao"` sai `"Maria  Joao"` (evidência: <log, teste, passo a passo>)
- **Esperado:** um espaço entre as palavras — fonte: <DF, HF/REG do ELM, decisão D-nn, regra óbvia>
- **Não muda:** nome nulo ou em branco continua nulo; pontuação sem espaços em volta só é removida

## Como verificar
<chamada, teste ou execução que mostra o esperado>
```

## Regras de escrita

- **Situação** (padrão sem épico): `rascunho` ou `aprovada por <login do P.O.> em <data>`. Regra nova ou alterada só vale aprovada;
  sem isso, a fatia fica `nova` com `falta: aprovação do P.O.`.
- **Cenários** como na `sdd-prd`: caminho feliz, o que **não** deve ser aceito, repetição, erro em um item — ou por
  que não se aplica; "Então" sempre verificável. Numerados `C1`, `C2`… — são o `cobre` da fatia: o plano, a
  rubrica L e a verificação leem daqui.
- **Regras:** uma por linha, com valores e a fonte (`D-nn` ou id do ELM). Antes de escrever uma regra nova ou
  alterada, [similares](../../sdd-prd/references/similares.md); "No ELM" = `reusa <id>` · `altera <id>` ·
  `novo (verificado <data>)`. A regra vai para o DOORS Next na consolidação, as-built (`sdd-consolidar`).
- **Rápida:** sem Regras nem Cenários — o que está no formato dela. Aprovação do P.O. só se a fonte do esperado é
  uma decisão nova (aí é `D-nn` aprovada).
- **Padrão de épico:** nada de regra ou cenário copiado do PRD — só os links; o PRD continua a fonte.
- **Decisões** no formato do `decisoes.md` da `sdd-entrevistar`, aqui dentro (a ficha não tem pasta).
- **Pendências do ELM** da fatia não iniciada, `dividida` ou `cancelada` (sem `status.md` que valha): no rodapé da
  ficha, `ELM pendente [<chave>]: <o que falta>` — ex.: `[FT-040 cancelar]`, quando o `elm_transicao(<id>,
  "cancelar")` do IB ou das tarefas falhou (sem o MCP, `precondicao`, erro); resolvida, `ELM feito [<chave>]: …`
  abaixo dela ([pendências](../../sdd/references/elm.md#pendências)).
- Termos do glossário em todo o texto; termo novo vai para o glossário (a triagem roda na base).
- Mais de ~3 cenários de comportamentos diferentes, ou mais de uma regra nova independente → não é uma fatia: a
  `sdd-triar` refaz a triagem como épico.
