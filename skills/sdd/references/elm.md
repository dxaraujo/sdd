# ELM — como o sdd grava

O ELM é o registro oficial: o que o sistema faz (DOORS Next), o que está sendo feito (EWM) e como foi testado (ETM).
O repositório guarda as propostas de mudança e o histórico. Quem fala com o ELM é o MCP **`elm`** do power: ele lê
o `.kiro/config/elm/pa_<nome>.json` (um por project area; gravado pela `sdd-setup`) — tipos, campos, padrões,
pastas, ids. **A skill passa só `projeto` (caminho absoluto da raiz do repositório), `pa` (quando o projeto tem
mais de um) e os ids e o conteúdo.** Nunca repasse campos, URLs ou ids do `pa`: o MCP resolve.

Toda tool devolve `{"ok":true,"dados":{…}}` ou `{"ok":false,"erro":{"codigo","detalhe","campo"}}`; `elm_ler_wi` e
`elm_ler_req` devolvem Markdown. Os parâmetros de cada tool estão no schema dela — não os repita aqui.

## Operações

| Operação | Tool |
|---|---|
| conferir conexão e `pa` | `elm_status` |
| ler · listar work items | `elm_ler_wi(id)` · `elm_listar_wi(iteracao, dono, tipo, pai, titulo_prefixo, estado)` |
| criar · atualizar (pai, iteração, campos; vários ids = virada) | `elm_criar_wi` · `elm_atualizar_wi` |
| assumir · concluir · reabrir · cancelar | `elm_transicao(id, alvo)` |
| comentar · anexos | `elm_comentar` · `elm_anexo(acao)` |
| horas lançadas · relatório da iteração · lançar · remover (lançamento errado) | `elm_horas(id)` · `elm_horas(iteracao)` · `elm_lancar_horas` · `elm_remover_horas(id, data)` |
| ligar (implementa, rastreia, afeta, testado por, valida, depende, relacionado) | `elm_ligar` |
| buscar · ler · publicar requisito | `elm_buscar_req` · `elm_ler_req` · `elm_publicar_req` |
| buscar · ler · listar requisito local (bundle) + indexar | `elm_buscar_req_local` · `elm_ler_req_local(id ou path)` · `elm_listar_req_local` · `elm_indexar_local` |
| visualizar o bundle (explorar.html, grafo 3D) | `elm_explorar_local` (skill `sdd-sync`; exige o índice: `precondicao` com `campo: "indice"` → `elm_indexar_local`) |
| criar caso de teste (já ligado) | `elm_criar_ct` |
| iteração e plano da sprint | `elm_iteracao` |
| backlog do produto (onde os itens nascem; `iteracao: "backlog"`) | `elm_backlog` |
| bundle do DOORS Next | `elm_sync` (skill `sdd-sync`, que pergunta se indexa no fim) |

**Comentário e anexo na própria tarefa:** todo papel com tarefa — Dev na `[DEV]`, revisor na `[REV]` e na `[APR]`,
verificador na `[VER]`, produto na `[ESP]` e na `[GB]` (o P.O. e o SM, que é o dono), quem faz o item de Sustentação na tarefa dele (`[ATD]`,
`[IMPL]`…) — pode comentar (`elm_comentar`) e anexar (`elm_anexo enviar`, arquivo de dentro do projeto) nela, sempre
com "sim"; na tarefa de outro papel, não.

## Bundle local

Consulta de requisito: **local primeiro** (`elm_buscar_req_local`, `elm_ler_req_local`), nunca lendo os arquivos do
bundle. Sem nada baixado — erro `nao_encontrado` com `campo: "bundle"` — diga isso à pessoa, pesquise no ELM remoto
(`elm_buscar_req`/`elm_ler_req`) e ofereça a `sdd-sync` para baixar. Sem o ELM remoto (pesquisador) → registre que
não há bundle e indique a `sdd-sync`. `indexando: true, restantes: n` → a busca usou o que já estava indexado; a indexação
segue em segundo plano (`elm_indexar_local` mostra o progresso). A busca local, a indexação e a visualização usam
a API de embeddings do `elm.properties` (`provider_url`, `provider_api_key`; não há modelo local): sem elas, erro
`config` — peça a configuração e o reinício do MCP. Trocar o modelo exige reindexar.

Visualização do bundle: `elm_explorar_local` (skill `sdd-sync`) gera o `explorar.html` na pasta do bundle — grafo 3D
(links dos artefatos ou vizinhos semânticos; as libs vêm do CDN, abrir exige internet); lê o índice em modo somente leitura, sem índice →
`precondicao` com `campo: "indice"`: indexe antes (`elm_indexar_local`).

Erro `config` → o `pa` está incompleto: diga o campo e ofereça a `sdd-setup`. `credencial` → peça a configuração do
`~/.config/mcp-elm/elm.properties` (o agente não lê esse arquivo). `indisponivel` → o servidor não respondeu: tente uma vez mais;
persistindo, registre `ELM pendente` e siga. `permissao`/`precondicao` → mostre o atributo;
não chute valor. Os campos que a PA exige por regra de processo (criar, mudar de estado, lançar horas) ficam em
`obrigatorios` do tipo no `pa` e são exigidos já na criação (`elm_criar_wi`), para as transições e as horas não
esbarrarem neles — Estimativa → pergunte e passe `estimativa_h`; outro campo sem padrão → ofereça a `sdd-setup`. Item
criado fora do fluxo recusado numa transição → mostre o campo e peça o valor.

## Regras de toda escrita

1. **Prévia e um "sim" por lote:** `Ação (criar | atualizar | ligar | sem mudança) | Alvo | Título`. Nada é escrito
   sem "sim". Mostre nomes, nunca ids internos (`FR_`, `OT_`, `_uuid`).
2. **Idempotência:** o repositório guarda o id (coluna `elm` do `backlog.md`, com o tipo antes de cada um —
   `IB [612010](…) · DEV [612011](…)` —, campo ELM do `status.md`, `resource` do conceito). Com id → atualizar o
   mesmo. Sem id → procure uma publicação interrompida: tarefa ou IB por `elm_listar_wi(pai, titulo_prefixo)`
   (`[DEV] FT-031`, `[FT-031]`, `[EP-03]`, `[AT-012]`); requisito por `elm_buscar_req`
   (título). Achou → mostre e pergunte se é ele. Não achou → criar. A tarefa descartada e a que tem pendência de
   cancelamento aberta (`[<tipo> <id> cancelar]`) não contam: o papel nasce de novo, e a velha segue com a pendência
   ([elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md), topo).
3. **Grave de volta** cada id assim que nasce (falha no meio: o próximo passo 2 retoma). Commit no fim.
4. **Nunca apague** nada no ELM: IB ou tarefa que deixou de valer é cancelado (`elm_transicao(<id>, "cancelar")`);
   o resto (requisito) vira roteiro manual (obsoleto/remoção na UI).
5. **Conflito no DOORS Next:** `elm_publicar_req` com `modificado_em` devolve `conflito` se o ELM mudou depois →
   mostre os dois lados e pergunte qual fica.
6. **Sprint não publicada** (`**Publicação no EWM:** pendente` no cabeçalho do `sprint-<nn>.md`): nenhuma tool, de
   leitura inclusive, recebe a iteração dela antes do §1 do
   [elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) — sem ele, o MCP procura o caminho pelo nome na PA
   inteira e pode achar a sprint homônima de outro produto. No agente de produto, rode o §1 antes — sprint em pai
   novo: também o §2 (a `[GB]` do pai novo nasce, e a antiga conclui com o saldo e sai da linha) —, com o mesmo "sim",
   e tire o marcador no commit (linha `migrada de` ou linha sem ids: indique também "sincroniza a sprint"); nos
   agentes sem o `elm_iteracao` (codificador, orquestrador), registre o lado do EWM como `ELM pendente [<chave>]` e
   indique "sincroniza a sprint" (`sdd-planejamento`).

## Pendências

Sem o MCP `elm` nesta sessão (outra máquina), sem as tools de escrita (pesquisador) ou com falha: não grave; registre
`ELM pendente [<chave>]: <o que falta>` no lugar único do artefato e siga — o ELM nunca trava o fluxo. A chave
identifica ação e alvo (`[DEV 669412 concluir]`, `[IB FT-031 concluir]`, `[IB AT-012 concluir]`,
`[REG-01 publicar]`, `[CT FT-031 criar]`, `[DEV FT-031 horas]`); uma pendência por chave. Cancelar IB ou tarefa é
`elm_transicao(<id>, "cancelar")`, com "sim" (já descartado → `ja_estava`; concluído → `precondicao` `já concluída:
reabra antes`; workflow sem descarte → `precondicao` `o workflow não tem cancelamento`). Só na falha (sem o MCP,
`precondicao`, erro): `ELM pendente [<tipo> <id> cancelar]` (`[DEV 669412 cancelar]`) ou a do item
(`[FT-031 cancelar]`, `[AT-012 cancelar]`), até o `ELM feito`.

WI que sumiu do EWM (`nao_encontrado` na sincronização da sprint, §9) e que a pessoa mantém: `ELM pendente
[<tipo> <id> sumiu]: confira na UI do EWM` (`[DEV 669412 sumiu]`, `[IB 669410 sumiu]`), no lugar das pendências do
item (tabela abaixo). Até o `ELM feito`, o id sai da comparação do §9 e da contagem da
`sdd-status`.

Exceção, na sincronização da sprint ([elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §9, passo 5): a
falha que a próxima comparação vê de novo (estado, dono, estimativa ou iteração de item não terminal da sprint) não
grava pendência — a pendência a esconderia —, e a linha que entra na sprint ou sai dela cujo movimento falhou não
grava o lado do arquivo.

| Artefato | Onde mora |
|---|---|
| fatia `iniciada`, `pronta` ou `concluida` | Histórico do `status.md` |
| fatia não iniciada, `dividida` ou `cancelada` | rodapé da ficha `<produto>/fatias/FT-<nnn>-<slug>.md` |
| épico | rodapé do `prd.md` (antes do GATE, o `rascunho.md`) |
| item de Sustentação (toda categoria) | campo `**ELM:**` da ficha `<produto>/sustentacao/<pasta>/<ID>-<slug>.md` |
| `[GB]` e IBs de estrutura (`Sustentação`, `Manutenção`, `<Categoria>`) | na `## Sustentação` do `backlog.md` (ou na `### <Categoria>`), logo abaixo da linha dos ids |
| sprint | coluna "Tarefa ELM" do `sprint-<nn>.md` (`pendente`) |

Resolver ("resolve as pendências do ELM"): a `sdd-status` lista; para cada uma, faça a operação e acrescente
`ELM feito [<mesma chave>]: <o que foi feito> (<data>)` no mesmo lugar — a pendência nunca é apagada.

## Tarefas no EWM (quem, quando)

| Tarefa | Pai | Responsável | Nasce | Conclui |
|---|---|---|---|---|
| `[ESP] EP-<nn> Especificação` | épico | quem especifica | planejamento | GATE do backlog |
| `[ESP] FT-<nnn> Especificação` | item da fatia `nova` | quem especifica | planejamento | conclusão da especificação (a fatia passa na DoR) |
| `[DEV] FT-<nnn> Implementar` | IB da fatia | Dev | planejamento, ou conclusão da `[ESP]` da fatia | merge |
| `[REV] FT-<nnn> Revisar` · `[VER] FT-<nnn> Verificar` | IB | revisor · verificador (só HITL) | planejamento, conclusão da `[ESP]` da fatia ou troca AFK→HITL | aprovar · aceitar (depois do push) |
| `[APR] FT-<nnn> Aprovar plano` · `Aprovar PR` | IB | Dev Sênior | no gate | na aprovação |
| Sustentação: `[ATD] AT-<nnn>` · `[IMPL] IM-<nnn>` · `[BD] BD-<nnn>` · `[INF] IN-<nnn>` · `[OPE] OP-<nnn>` · `[EXT] EX-<nnn>` + `<pedido>` | IB do item (`[AT-<nnn>] <pedido>`) | quem faz | quando o item entra numa sprint, ou trazida do EWM ([elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §9) | ao finalizar, com o IB do item (`sdd-atender` no Atendimento; `sdd-executar` nas demais) |
| `[GB] Gerenciamento do backlog` | IB `Sustentação` | SM | planejamento inicial (no backlog, com a `Sustentação`); move para a 1ª sprint de cada pai | na troca de pai (a do pai novo nasce); senão move na virada |

**Os pais** (todo trabalho tem pai): épico `[EP-<nn>]` → IB `[FT-<nnn>]`; IB `Sustentação` (um por produto) → IB
`Manutenção` (das fatias sem épico: o IB `[FT-<nnn>]` ou o item de origem, DF ou IB) e um IB por categoria
(`Atendimento`, `Implantação`…) → IB `[AT-<nnn>] <pedido>` de cada item (dono = P.O.). A `Sustentação`, a
`Manutenção` e as categorias ficam no backlog do EWM; quem cria cada IB e quando:
[elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §2, §3 e §6.

O `pa` aplica os campos que a PA exige (categoria, campos exigidos por processo, classificação por prefixo); `iteracao` é a
da sprint, ou `backlog` para épico e IB fora de sprint — tarefa nasce só na sprint, salvo a `[GB]` (o backlog do EWM é a cópia do
`backlog.md`: [elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md)). Assumir =
`elm_transicao(id, "assumir")`; concluir = saldo de horas e `elm_transicao(id, "concluir")`; voltar ao estado inicial
(IB no backlog fora de sprint, item que sai da sprint) = `elm_transicao(id, "reabrir")`; cancelar =
`elm_transicao(id, "cancelar")`.

**Horas e créditos de gestão:** só o SM lança horas na `[GB]` (`elm_lancar_horas`); o P.O. nunca lança, nem quando
também é o SM. Toda sessão do P.O. ou do SM no agente de produto (triagem, consolidação, planejamento, ritos,
sincronização) fecha com os créditos num comentário na `[GB]`: `elm_comentar(<id da [GB]>, "Créditos <atividade>
<ids>: <créditos> (sessão <sessão>, <login>, <AAAA-MM-DD>)")` — ex.: `Créditos triagem FT-040, AT-013: 2.40 (sessão
9ec1dcaa, ana.souza, 2026-10-29)` —, além da linha em Créditos de gestão do `sprint-<nn>.md` aberto
([`sdd-status`](../../sdd-status/SKILL.md#fechar-a-sessão), item 4). `[GB]` sem horas é normal.

## O que o MCP não grava (roteiro manual)

Atributos de requisito, links requisito ↔ requisito (*satisfaz*, *restringe*), módulos, change sets e baselines.
Quando o processo do projeto exigir (seção ELM do `sdd.md`), entregue o roteiro com os ids exatos e registre
`ELM pendente [<chave>]` até a pessoa confirmar.
