---
name: sdd-sync
description: "Sincroniza o bundle OKF do DOORS Next com o ELM nas duas vias, pelo MCP elm: plano (o que baixar, o que enviar, conflitos), baixar a versão oficial, enviar o que mudou no repositório e, depois de baixar, indexar a busca local (pergunta); e gera a visualização offline do bundle (explorar.html, galáxias 3D) sob pedido. Usa a pasta e a project area do pa_<nome>.json do projeto. Use em \"sincroniza o ELM\", \"baixa os requisitos\", \"atualiza o bundle\", \"envia os requisitos alterados\", \"sync do DOORS\", \"gera a visualização do bundle\", \"quero explorar o bundle\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.5.5"
---

# sdd-sync — Bundle do DOORS Next nas duas vias

O bundle (pasta `rm.download` do `pa`) é a cópia local, em OKF, dos requisitos oficiais: a `sdd-prd` e os similares
o leem pelas tools `elm_*_local` do MCP `elm`. Regras comuns: [../sdd/references/elm.md](../sdd/references/elm.md).

1. `elm_sync(projeto, pa, direcao "plano")` → mostre: a baixar (mudou no ELM), a enviar (mudou no bundle) e
   **conflitos** (mudou nos dois lados, com as duas datas).
2. Conflito → mostre o diff de cada um e pergunte qual fica (ELM → baixar aquele id; repositório → enviar). Nunca
   sobrescreva o ELM sem "sim".
3. Com "sim": `elm_sync(direcao "baixar", ids?)` e, se houver, `elm_sync(direcao "enviar", ids)`. Envio é escrita no
   ELM: um "sim" para o lote, com a lista.
4. Commit `ELM - Sincronizar bundle` com o que baixou (bundle no `.gitignore` → não há commit). Os agentes `sdd-*`
   não tocam no bundle pelo shell (`git add` com o caminho dele é negado): rode esta skill na sessão padrão do Kiro;
   num agente, entregue o comando do commit pronto e a pessoa o roda. Baixou algo → pergunte se indexa agora (a busca
   local e a visualização só veem o que está indexado): "sim" → `elm_indexar_local`, que roda em segundo plano e
   responde na hora; mostre `restantes` e siga. "não" → diga que a próxima busca local indexa o que mudou. Com o
   índice pronto, ofereça a visualização do bundle (passo 5).
5. **Visualização** ("gera a visualização do bundle", "quero explorar o bundle", ou o "sim" do passo 4):
   `elm_explorar_local(projeto, pa)` → gera o `explorar.html` na pasta do bundle, o bundle em galáxias num HTML único
   que abre no navegador sem internet (vista 3D ou 2D; busca e filtros por tipo, pasta e galáxia; Markdown):
   planeta = documento, lua = chunk do planeta selecionado. Mostra `path`, `documentos`, `chunks`, `galaxias`,
   `links` e `gerado_em`. Os documentos e vetores saem do índice em modo somente leitura: sem índice → `precondicao`
   com `campo: "indice"` → `elm_indexar_local` e rode de novo. Sem nada baixado → `nao_encontrado` com
   `campo: "bundle"` (mesma saída da consulta local: baixe no passo 3). Gerar de novo sobrescreve o `explorar.html`.

Saída: `🔄 Sync ELM · baixados <n> · enviados <n> · conflitos <n resolvidos> · bundle de <data>`.
Visualização: `🗺️ Bundle · <n> documentos · <n> chunks · <n> galáxias · <n> links · <path>`.
