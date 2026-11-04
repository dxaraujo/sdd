# Publicar no ELM (requisitos, ET, casos de teste, conclusão)

Regras comuns (prévia, um "sim", idempotência, pendências): [../../sdd/references/elm.md](../../sdd/references/elm.md).
Formato dos conceitos: [../../sdd-prd/references/okf-elm.md](../../sdd-prd/references/okf-elm.md).

## Requisitos (conceitos OKF de `elm/` → DOORS Next)

Entrada: a pasta `elm/` do épico ou, numa fatia padrão sem épico, a da fatia. Publica só conceito `status: stable`
com um `verified` humano posterior ao `generated.at`; o resto aparece na prévia como "aguardando aprovação".
Ordem **de baixo para cima** — termos (`GL`), regras (`REG`), histórias (`HF`) — para cada um nascer com os ids que cita.

1. **Conceito novo** (sem `resource`): a coluna "No ELM" do PRD/ficha tem de dizer `novo (verificado <data>)`; sem
   isso → [similares](../../sdd-prd/references/similares.md) só para ele. Acerto `igual`/`sobrepõe` → não cria: devolve
   à `sdd-prd`; o lote segue.
2. **Texto:** o corpo sem a seção `## Relações`; regra ou termo já publicado → `[<id>](<id>)`; conceito sem id → só
   o título. Regras citadas por uma história vão em `embutir` (embed); o resto fica hyperlink.
3. `elm_publicar_req(sigla = o prefixo do conceito, titulo, texto_md, id?, modificado_em = last_modified da entrada
   do ELM em sources, embutir = ids das regras)`. Erro `conflito` → mostre os dois lados e pergunte (regra 5).
4. **Grave de volta** no conceito: `resource`, `id` e `{id: elm, resource, last_modified}` em `sources`; `**Publication**`
   no `log.md`; termos, o id também na coluna ELM do glossário.

Depois: sugira a `sdd-sync` (baixar) para o bundle receber a versão oficial.

## ET as-built (só se a seção ELM do `sdd.md` disser `as-built no merge`)

A ET chega no PR (`.kiro/specs/<ft>-<slug>/elm/ET-<slug>.md`); publique como um requisito (sigla `ET`) e
`elm_ligar(wi = IB, req = ET)`.

## Casos de teste (cenários `✅ aceito` do `verificacao.md`)

Para cada cenário sem id ao lado: `elm_criar_ct(titulo = Resumo do CT.csv, cenario_md = Descrição, reqs = ids das
histórias que ele cobre — sem épico: a regra da ficha —, wi = IB)` → grave o id ao lado do cenário e no campo ELM do
`status.md` (`CT <id>, …`). Erro (`permissao`, `config` sem `qm`) → `ELM pendente [CT FT-<nnn> criar]` e o `CT.csv`
para importar à mão no ETM; com os ids que a pessoa informar, `elm_ligar(ct, req)` e `elm_ligar(wi, ct)`.

## Conclusão do IB e do épico

IB da fatia: `elm_comentar(id, "PR <link> · pasta <pasta> · publicados: <ids de requisitos, ET, CT>")` e
`elm_transicao(id, "concluir")`, na mesma confirmação. Na última fatia do épico (as demais `concluida`, `dividida`
ou `cancelada`), também o IB do épico (`elm_transicao(id, "concluir")`), junto com o `concluido` no `backlog.md` e
na Fase do `status.md` do épico (`sdd-consolidar` Passo 4); épico `cancelado` não conclui (fica como está). Erro
`precondicao` → `ELM pendente [IB FT-<nnn> concluir]` (no épico, `[EP-<nn> concluir]`) com o atributo.
