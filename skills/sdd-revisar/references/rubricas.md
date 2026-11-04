# Rubricas de revisão do sdd

Cada verificação tem severidade. **BLOQUEANTE** reprova; **IMPORTANTE** reprova (barato de corrigir agora, caro
depois); **SUGESTÃO** não reprova nem reabre ciclo. Todo achado tem **evidência** (`arquivo:linha`, comando +
saída, ou "procurado em X, não encontrado") e a **correção** esperada. Achado sem evidência não é achado.

Regras promovidas (seção Regras aprendidas do `.kiro/steering/sdd.md`) valem como itens extras da rubrica do artefato a que se
referem, com a severidade registrada nelas.

## P — PRD (`prd.md` + `decisoes.md`)

| # | Verificação | Severidade |
|---|---|---|
| P1 | Problema e solução descritos do ponto de vista do usuário, sem tecnologia | IMPORTANTE |
| P2 | Toda história tem cenários, e todo "Então" é verificável (valor, resposta, mensagem, contagem) | BLOQUEANTE |
| P3 | Cada história cobre: caminho feliz, o que não deve ser aceito, repetição/reexecução e erro em um item — ou diz por que não se aplica | BLOQUEANTE |
| P4 | Toda regra é testável, tem valores e cita a origem (`D-nn`, artefato do ELM ou fonte) | BLOQUEANTE |
| P5 | Nada inventado: regra, ator, valor ou integração sem fonte e sem decisão de uma pessoa | BLOQUEANTE |
| P6 | Comportamento já documentado no ELM é **alterado** ou **reutilizado**, não duplicado: todo artefato tem a coluna "No ELM" preenchida (`reusa`, `altera` ou `novo (verificado <data>)`) com a decisão no `decisoes.md`; conceito novo sem verificação, ou com acerto `igual`/`sobrepõe` sem motivo registrado — conferir também no bundle (pelo `elm_buscar_req_local`) | BLOQUEANTE |
| P7 | Termos canônicos do glossário em todo o texto; nenhum sinônimo listado em "Evitar" | IMPORTANTE |
| P8 | Nenhuma decisão `em aberto` que mude comportamento | BLOQUEANTE |
| P9 | Sem caminho de arquivo, classe, SQL ou código | SUGESTÃO |
| P10 | Fora de escopo explícito | SUGESTÃO |
| P11 | Conceitos OKF v0.2 em `elm/` conformes (checklist "Conformidade" de `okf-elm.md` da `sdd-prd`): frontmatter que faz parse, `type` e `tags` do mapeamento do projeto, só chaves do OKF v0.2 (+ `id`), `status: draft` antes do GATE, HF ligando as suas REGs, links que resolvem, `index.md` completo | BLOQUEANTE |

Fecho: `RESULTADO: PRONTO` ou `RESULTADO: AJUSTAR`.

## L — Plano da fatia (`research.md`, `requirements.md`, `design.md`, `tasks.md`)

| # | Verificação | Severidade |
|---|---|---|
| L1 | Todo cenário que a fatia cobre (backlog `cobre`, ou os `C<n>` da ficha da fatia sem épico) tem critério de aceite em `requirements.md`, e nenhum critério sai do que a fatia cobre. Trilha rápida: o `bugfix.md` tem o comportamento atual com evidência, o esperado com fonte e o que não muda, como na ficha. **Todo valor visível ao usuário no "Então" do cenário** (texto, rótulo, mensagem, nome de arquivo, formato) aparece **igual, palavra por palavra**, no critério e no Esperado do contrato de pronto do `design.md` — nome de enum, código interno ou tradução não servem | BLOQUEANTE |
| L2 | Todo critério (ou item 2.x/3.x do `bugfix.md`) tem ao menos uma tarefa no `tasks.md` (`_Requirements: N.M_`); bugfix começa pelo teste da condição do defeito e pelos testes de preservação | BLOQUEANTE |
| L3 | Nenhuma regra de negócio que não esteja no PRD/ELM, no `decisoes.md` ou na ficha da fatia sem épico (Regras e Decisões). O plano muda a expectativa de um **teste existente** → está na seção "Testes existentes que mudam", com a fonte da decisão (pessoa, `D-nn`); o GATE segue a senioridade (`sdd-plano` Passo 5) | BLOQUEANTE |
| L4 | Os caminhos, classes e análogos citados existem (conferir com `glob`/`read`) — ou estão marcados "a criar" | BLOQUEANTE |
| L5 | O design segue o steering de tecnologia/estrutura, as regras críticas do `sdd.md` e as lições promovidas | BLOQUEANTE |
| L6 | Tarefas em ciclo de teste: cada comportamento começa por um teste que falha; corretiva começa pelo teste que reproduz o defeito | IMPORTANTE |
| L7 | Tarefas pequenas, na ordem de dependência, cada uma com o comando que prova que terminou | IMPORTANTE |
| L8 | Reexecução segura, transação e concorrência tratadas quando há escrita | BLOQUEANTE |
| L9 | Todo componente do design aparece em alguma tarefa, e vice-versa | IMPORTANTE |
| L10 | Nada fora do escopo da fatia (arquivos, refatorações oportunistas) | IMPORTANTE |

Fecho: `ANALISE: OK` ou `ANALISE: AJUSTAR`. Em cada achado diga se a falta é **do plano** (o codificador corrige)
ou **do PRD ou da ficha** (cenário ausente, regra contraditória → volta para o P.O. pela `sdd-prd`; na fatia sem
épico, pela `sdd-triar`).

## C — Código da fatia (diff contra a branch base)

Dois eixos, avaliados **separadamente** e relatados em seções próprias — um não compensa nem esconde o outro.
Reprovação em qualquer eixo é `REVISAR`.

**Eixo Spec** — o diff faz o que a fatia promete, e só isso:

| # | Verificação | Severidade |
|---|---|---|
| C1 | Cada critério de `requirements.md`/`bugfix.md` tem implementação (`critério → arquivo:linha`), citando a linha do critério | BLOQUEANTE |
| C2 | Cada cenário da fatia tem teste automatizado que o exercita pelo ponto de teste do `design.md` (`cenário → teste`), e o esperado do teste usa o valor visível do "Então" do cenário, igual | BLOQUEANTE |
| C3 | Os comandos de backpressure do `sdd.md` passam (compilar, testes, lint, cobertura se houver gate, medida no que o diff criou ou alterou — falta pré-existente fora do diff não reprova) — **executar** | BLOQUEANTE |
| C4 | Oráculo protegido: nenhum teste removido, desabilitado, ignorado, com assert vazio, enfraquecido ou tautológico (esperado recalculado como o código calcula); nenhuma exceção engolida. Expectativa de teste existente alterada só se está em "Testes existentes que mudam" do plano, com a decisão registrada | BLOQUEANTE |
| C5 | Reexecução segura: rodar de novo não duplica nem corrompe (chave, situação gravada, transação) | BLOQUEANTE |
| C6 | Tarefas `[x]` do `tasks.md` têm código correspondente no diff | BLOQUEANTE |
| C7 | Escopo: nada além da fatia — funcionalidade não pedida, arquivos fora do `design.md` (exceto testes e a pasta da fatia), refatoração oportunista | IMPORTANTE |

**Eixo Padrões** — o diff deixa o código pior para quem vem depois?

| # | Verificação | Severidade |
|---|---|---|
| C8 | Regras críticas do `sdd.md`, steering de tecnologia e regras aprendidas (mesmo arquivo) | BLOQUEANTE |
| C9 | Segurança: sem segredo no código ou em log, sem injeção (SQL, comando, HTML), dado sensível protegido | BLOQUEANTE |
| C10 | Modelo/entidade bate com o schema real (MCP de banco, somente leitura; sem o MCP de banco → `N/A`) | BLOQUEANTE |
| C11 | Segue o análogo e a forma do programa do `design.md`; nada de padrão novo sem decisão registrada | IMPORTANTE |
| C12 | Nomes do domínio = termos canônicos do glossário; nomes técnicos no padrão dos vizinhos | IMPORTANTE |
| C13 | Módulos profundos: interface pequena para o que esconde; sem abstração especulativa, camada a mais ou duplicação evitável | IMPORTANTE |
| C14 | Sem `TODO`/`FIXME`, print/log de depuração ou código comentado; registros obrigatórios da estrutura (rotas, menus, agendamentos, migrações) presentes | IMPORTANTE |
| C15 | Cada decisão do `design.md` com "Vira ADR? sim" tem o ADR no PR, em `.kiro/specs/<ft>-<slug>/adr/` (contexto · decisão · consequências · origem FT-nnn), e ele descreve o que o código faz; com a linha ET do `sdd.md` = `as-built no merge`, a ET em `elm/ET-<slug>.md` também está no PR e descreve o que o diff faz (interfaces, contratos, dados), nada além | IMPORTANTE |

Calibragem: seja cético (o autor tende a achar que terminou), mas aponte só o que afeta **correção, requisito,
segurança ou manutenção real**. Gosto pessoal e "eu faria diferente" são SUGESTÃO, quando muito — perseguir cada
achado leva a excesso de engenharia.

C3 falhando por ambiente (banco, rede, dependência fora do ar) → `AMBIENTE`, não conta como achado; diga o que
falhou.

**Drift de negócio** (não reprova; vai para a consolidação): na penúltima linha, `Drift de negócio: sim — <motivo>`
quando um achado aceito ou uma decisão técnica do `design.md` muda o comportamento visível ao usuário em relação
ao cenário ou à regra do PRD (ou da ficha); senão `Drift de negócio: não`. Fecho: `VEREDITO: APROVADO` ou
`VEREDITO: REVISAR`.

## Formato do relatório

```markdown
# Revisão <P | L | C> — <EP-xx | FT-xxx> · rodada <N>

## Resumo
<1–2 frases: o que foi revisado e a impressão geral>

## Achados
<!-- Rubrica C: uma tabela por eixo (Spec, Padrões). -->
| # | Severidade | Achado | Evidência | Correção | Origem (plano/PRD/código) |
|---|---|---|---|---|---|

## Verificações
| # | Resultado (✅ ❌ N/A AMBIENTE) | Observação |
|---|---|---|

<rubrica C, penúltima linha: Drift de negócio: não | sim — <motivo>>
<última linha: RESULTADO: … | ANALISE: … | VEREDITO: …>
```

A **última linha** é exatamente uma das linhas de fecho — quem chamou lê só ela para decidir.
