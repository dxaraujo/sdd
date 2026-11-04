# Equipe — <nome do projeto>

> **Formato:** Markdown (alternativo ao `equipe.json`).  
> **Atualizado:** AAAA-MM-DD  
> **Duração da sprint:** N semanas  
> **Início (sprint 1):** AAAA-MM-DD  

---

## Pessoas

> Colunas obrigatórias: Login, Nome, Papéis, Horas/semana (e Senioridade, para Dev).  
> Papéis (um ou mais, separados por vírgula): `P.O.` · `Especificador` · `Dev` · `QA` · `SM` — exatamente um P.O. e um SM ativos (a mesma pessoa pode ter os dois; o SM é o dono da [GB])  
> Senioridade (obrigatória para Dev): `Júnior` (fatias sempre HITL) · `Pleno` (modo pelos critérios da fatia) · `Sênior` (AFK por padrão; a [REV] é sempre de um Dev Sênior); `—` para quem não é Dev  
> Atende: `true` = faz Sustentação (toda categoria: [ATD], [IMPL]…); `false` ou em branco = não. A reserva (Sustentação + retrabalho) é das horas do time inteiro.  
> Ativo: `false` = saiu (histórico preservado).

| Login | Nome | Papéis | Senioridade | Horas/semana | Horas revisão/semana | Horas especificação/semana | Atende | Ativo |
|---|---|---|---|---|---|---|---|---|
| joao.lima | João Lima | Dev | Sênior | 40 | 6 | 0 | false | true |
| maria.silva | Maria Silva | QA, Especificador | — | 40 | 8 | 2 | true | true |

---

## Ausências planejadas

> Genérico de propósito: sem dado pessoal (nada de saúde ou motivo particular).  
> Motivo: `férias` · `folga` · `treinamento` · `outro`

| Login | Início | Fim | Motivo |
|---|---|---|---|

---

## Histórico de sprints

> Gravado na virada de cada sprint. Sprint: a chave `<pai>/Sprint <nn>` (`2026/Sprint 03`).  
> Horas (DEV/REV/APR/VER/ESP/Sustentação) vêm do relatório de horas da virada (`elm_horas(iteracao)`).

| Sprint | Fatias concluídas | Lead time médio (dias) | Horas DEV | Horas REV | Horas APR | Horas VER | Horas ESP | Horas Sustentação | Reserva Sustentação (%) |
|---|---|---|---|---|---|---|---|---|---|
