# `CT.csv` — casos de teste para importação no ETM

Um caso por cenário **verificado** (aceito com evidência) da fatia. Na consolidação, `elm_criar_ct` cria cada caso no ETM, com o Resumo como título e a Descrição como cenário, já
ligado ([elm-publicar.md](../../sdd-consolidar/references/elm-publicar.md)). Sem permissão de criar no ETM ou sem
o MCP `elm`, o arquivo é importado à mão (Importar → CSV) e os links são feitos depois (`elm_ligar`).

## Arquivo

- `.kiro/specs/<ft>-<slug>/CT.csv` · UTF-8 **com BOM** · quebras de linha **LF** · separador `;`.
- Grave o arquivo já assim: o conteúdo começa pelo caractere BOM (U+FEFF) e usa só `\n` nas quebras de linha —
  inclusive dentro da Descrição. Não dependa de `sed` depois (no Windows ele nem existe).

## Colunas (nesta ordem)

Valores do ELM vêm do `.kiro/config/sdd/pa_<nome>.json` e do `sdd.md`; sem ELM, deixe
vazios os que não souber. A ordem, os nomes e os valores fixos (tipo, status inicial, categoria) vêm da tabela
linha `CT.csv` da seção ELM do `sdd.md` — o template de importação do ETM do projeto manda.

| # | Coluna | Valor |
|---|---|---|
| 1 | Tipo | tipo de artefato de teste da importação (padrão: Caso de Teste) |
| 2 | Resumo | `<FT-nnn> <título curto> : CT<nn> - <título do cenário>` |
| 3 | Responsável | login do ELM de quem verificou (AFK, verificado por subagente: quem disparou o loop ou o workflow — o responsável da `[DEV]`) |
| 4 | Status | estado inicial (padrão do projeto) |
| 5 | Categoria | do projeto, se houver |
| 6 | Planejado para | a iteração no EWM da sprint da fatia, se houver: o `**Iteração no EWM:**` do `sprint-<nn>.md` (o nome no EWM é livre e pode diferir da chave da sprint) |
| 7 | Descrição | bloco abaixo, entre aspas duplas, com quebras de linha reais |

## Descrição

```
"OBJETIVO:
<o que o caso comprova> (HF-01 · cenário 1.2; REG-01)

PRÉ-CONDIÇÕES:
- <massa: script/fixture e o estado criado>

PASSOS:
1. <executar: requisição, job, tela> com <entradas>
2. <verificar em: consulta, resposta, log, tela>

RESULTADO ESPERADO:
- <o 'Então' do cenário, com valores>

EVIDÊNCIA DA VERIFICAÇÃO (FT-<nnn>, <AAAA-MM-DD>):
- <resumo do obtido>"
```

Aspas duplas dentro do texto são dobradas (`""`), como manda o CSV.
