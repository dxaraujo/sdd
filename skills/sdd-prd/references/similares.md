# Similares no ELM (antes de criar HF, REG ou GL — só leitura)

Chamado pela `sdd-prd`, pela `sdd-triar` (regra da ficha de uma fatia sem épico) e pela publicação de um conceito
novo. Não pede confirmação. Entrada: por artefato proposto, a sigla (`HF` | `REG` | `GL`), o título provisório e 3–6
palavras-chave do domínio (termos do glossário, sinônimos da entrevista, atores, valores).

1. **Bundle** (pasta `rm.download` do `pa`), pelo `elm_buscar_req_local`: um pelo título e um por palavra-chave
   (sem bundle baixado → erro `nao_encontrado` campo `bundle`: diga isso, ofereça a `sdd-sync` e siga só no passo 2).
   Anote a data do último sincronismo (`sdd-sync`).
2. **Ao vivo:** `elm_buscar_req(texto)` pelo título e por palavra-chave, filtrando o resultado pelos tipos das
   siglas do `pa`. Sem o MCP `elm` → só o bundle, e a saída diz `ao vivo: pendente`.
3. **Classifique** cada acerto (corpo pelo `elm_ler_req_local` ou `elm_ler_req`): **igual** (mesmo comportamento,
   mesma regra com o mesmo valor, mesmo termo) · **sobrepõe** (parte do comportamento, mesma regra com outro valor,
   mesmo termo com outra definição) · **relacionado** (mesmo assunto, comportamento diferente). Só palavra em comum
   → descarte.
4. **Saída**, um bloco por artefato:

   ```
   🔎 Similares no ELM — EP-<nn> · bundle de <data> · ao vivo: <sim | pendente>
   | Proposto | No ELM (id · título · tipo · pasta) | Relação | Recomendação |
   |---|---|---|---|
   | REG-01 Limite de tentativas | 2101 · REG - Tentativas de login · Regra · 04-Regras | igual | reutilizar 2101 |
   ```

   **igual → reutilizar** (HF embute a REG existente, cita a HF, linka o termo pelo id) · **sobrepõe → alterar** o
   existente (caminho "Alteração" da `sdd-prd`) · **relacionado → criar novo**, citando o existente em `## Relações`
   · **nenhum → criar novo** (`novo (verificado <data>)`). A decisão é da pessoa.
