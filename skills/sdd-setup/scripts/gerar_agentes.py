"""Gera .kiro/agents/sdd-<papel>.json (Kiro IDE e CLI V3) a partir de assets/agents/papeis.json, dos prompts
assets/agents/sdd-<papel>.md e da configuração do projeto em .kiro/config/sdd/agentes.json.

    uv run --no-project python gerar_agentes.py --projeto <raiz>            # só mostra o diff e a tabela
    uv run --no-project python gerar_agentes.py --projeto <raiz> --gravar   # grava (só depois do "ok" da pessoa)

Sai com 1 se algum caminho citado não existe ou sobrou um {{…}} (nada é gravado). Termina com a tabela do que
cada agente recebeu (skills, MCPs, ELM, subagentes, push), lida dos agentes gerados.
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "agents"
PH = re.compile(r"\{\{([A-Z_]+)\}\}")


def expandir(itens, grupos):
    """Lista com '+grupo' trocado pelo conteúdo do grupo (recursivo), sem repetir."""
    out = []
    for i in itens:
        for j in (expandir(grupos[i[1:]], grupos) if i.startswith("+") else [i]):
            if j not in out:
                out.append(j)
    return out


def preencher(padroes, valores):
    """Troca os {{X}}; padrão cujo valor é None (não há) sai."""
    out = []
    for p in padroes:
        nomes = PH.findall(p)
        if any(valores.get(n) is None for n in nomes):
            continue
        out.append(PH.sub(lambda m: valores[m.group(1)], p))
    return out


def regra(cap, efeito, match=None, exclude=None):
    r = {"capability": cap, "effect": efeito}
    if match is not None:
        r["match"] = match
    if exclude:
        r["exclude"] = exclude
    return r


def agente(nome, p, base, cfg):
    valores = {"POWER": cfg["power"], "PRODUTO": cfg["produto"], "GLOSSARIO": cfg.get("glossario"), "ADR": cfg.get("adr"),
               "BASE": cfg["base"], "BUNDLE": cfg.get("bundle"), "MASSA": cfg.get("massa")}
    extra = cfg.get("agentes", {}).get(f"sdd-{nome}", {})
    grupos, sh = base["grupos"], base["shell"]

    libera = expandir(p.get("mcp_libera", []), grupos)
    pergunta = expandir(p.get("mcp_pergunta", []), grupos)
    if p.get("push") == "loop" and not cfg.get("push_pr_no_loop", True):
        pergunta = [t for t in pergunta if t != "gitlabpr/gitlab_criar_mr"]
    if not cfg.get("elm", True):
        libera = [t for t in libera if not t.startswith("elm/")]
        pergunta = [t for t in pergunta if not t.startswith("elm/")]
    # o que o papel não usa é negado: a IDE chama tool de power pelo kiro_powers, fora do filtro de `tools`
    nega = [f"{s}/{t}" for s, ts in base["mcp_do_power"].items() for t in ts
            if f"{s}/{t}" not in libera + pergunta and (s != "elm" or cfg.get("elm", True))]
    if not cfg.get("elm", True):
        nega.append("elm/*")

    subagentes = p.get("subagentes", []) + [s["nome"] for s in extra.get("subagentes", [])]
    mcp_extra = extra.get("mcp", [])

    regras = [regra("fs_read", "allow", preencher(base["ler"]["permitir"], valores) + extra.get("ler", [])),
              regra("fs_read", "deny", preencher(base["ler"]["negar"], valores)),
              regra("fs_write", "allow", preencher(p["escreve"], valores))]
    if p.get("nao_escreve"):  # o `exclude` (V3) tira da negação o que o papel grava dentro de uma pasta negada
        regras.append(regra("fs_write", "deny", preencher(p["nao_escreve"], valores),
                            preencher(p.get("nao_escreve_exceto", []), valores)))
    for g in p["shell"]:
        regras.append(regra("shell", "allow", sh[g]["comandos"], sh[g].get("exceto")))
    soltos = p.get("shell_permitir", []) + [c for k in p.get("comandos", []) for c in cfg.get("comandos", {}).get(k, [])]
    if p.get("http_sh") and cfg.get("http_sh"):
        soltos.append("sh .kiro/sdd/http.sh *")
    if soltos:
        regras.append(regra("shell", "allow", soltos))
    push = p.get("push")
    if push == "loop":
        push = "perguntar" if cfg.get("push_pr_no_loop", True) else "negar"
    perguntar = (["git push *"] if push == "perguntar" else []) + p.get("shell_perguntar", [])
    if perguntar:
        regras.append(regra("shell", "ask", perguntar))
    negar = sh["negar"] + (sh["push-perigoso"] if push == "perguntar" else ["*git push*"]) + p.get("shell_negar", [])
    regras.append(regra("shell", "deny", preencher(negar, valores)))
    if subagentes:
        regras.append(regra("subagent", "allow", subagentes))
    for efeito, ts in (("allow", libera), ("ask", pergunta), ("deny", nega)):
        if ts:
            regras.append(regra("power", efeito, [f"sdd/{t}" for t in ts]))
    if mcp_extra:
        regras.append(regra("mcp", "allow", [m if "/" in m else f"{m}/*" for m in mcp_extra]))
    regras.append(regra("skill", "allow"))

    skills_extras = [Path(s.removeprefix("skill://")).parent.name for s in extra.get("skills", [])]
    prompt = (ASSETS / f"sdd-{nome}.md").read_text(encoding="utf-8")
    prompt = prompt.replace("{{SKILLS_EXTRAS}}", f"Skills do projeto ligadas a você: {', '.join(f'`{s}`' for s in skills_extras)}"
                            " — carregue a do artefato antes de escrevê-lo." if skills_extras else "")
    subs_projeto = extra.get("subagentes", [])
    prompt = prompt.replace("{{SUBAGENTES}}", "Subagentes do projeto: " + ", ".join(f"`{s['nome']}` ({s['para']})" for s in subs_projeto)
                            if subs_projeto else "")
    prompt = re.sub(r"\n{3,}", "\n\n", PH.sub(lambda m: valores.get(m.group(1)) or "não há", prompt)).rstrip() + "\n"

    a = {"name": f"sdd-{nome}", "description": p["description"], "prompt": prompt,
         "tools": ["read", "write", "shell"] + [f"subagent/{s}" for s in subagentes]
                  + [f"@{t}" for t in libera + pergunta] + [f"@{m}" for m in mcp_extra],
         "resources": ["file://.kiro/steering/sdd.md"] + cfg.get("steering", [])
                      + [f"skill://{cfg['power']}/skills/{s}/SKILL.md" for s in p["skills"]] + extra.get("skills", []),
         "includeMcpJson": bool(mcp_extra), "includePowers": True, "welcomeMessage": p["welcomeMessage"],
         "permissions": {"rules": regras}}
    if subagentes:  # o V3 ainda lê a lista de subagentes daqui (o resto do toolsSettings saiu)
        a["toolsSettings"] = {"subagent": {"availableAgents": subagentes, "trustedAgents": subagentes}}
    if extra.get("modelo"):
        a["model"] = extra["modelo"]
    return a


def problemas(a, projeto):
    texto = json.dumps(a, ensure_ascii=False)
    out = [f"{a['name']}: sobrou {m}" for m in sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", texto)))]
    for r in a["resources"]:
        caminho = r.split("://", 1)[1]
        if caminho.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", caminho) or "\\" in caminho or "$" in caminho:
            out.append(f"{a['name']}: caminho absoluto ou com variável: {r}")
            continue
        alvo = Path.home() / caminho[2:] if caminho.startswith("~/") else projeto / caminho
        # o sdd.md é gravado pela setup no mesmo passo, depois do "ok" ao resumo
        if "*" not in caminho and r != "file://.kiro/steering/sdd.md" and not alvo.is_file():
            out.append(f"{a['name']}: não existe: {r}")
    return out


def resumo(agentes, cfg):
    """Tabela markdown do que cada agente recebeu, lida dos agentes gerados; ícones da legenda de references/wizard.md."""
    fluxo = f"skill://{cfg['power']}/skills/"
    linhas = ["| Agente | Skills do fluxo | Skills do projeto | MCPs do projeto | ELM | GitLab | Subagentes | Push |",
              "|---|---|---|---|---|---|---|---|"]
    for a in agentes.values():
        skills = [r.removeprefix("skill://") for r in a["resources"] if r.startswith("skill://")]
        do_fluxo = [Path(s).parent.name.removeprefix("sdd-") for s in skills if f"skill://{s}".startswith(fluxo)]
        do_projeto = [Path(s).parent.name for s in skills if not f"skill://{s}".startswith(fluxo)]
        mcps = [t[1:] for t in a["tools"] if t.startswith("@") and not t.startswith(("@elm/", "@gitlabpr/"))]
        do_elm = [t for t in a["tools"] if t.startswith("@elm/")]
        escreve = any(r["capability"] == "power" and r["effect"] == "ask" and any(m.startswith("sdd/elm/") for m in r["match"])
                      for r in a["permissions"]["rules"])
        elm = ("➖" if not do_elm else "🟢 só o bundle local" if all(t.endswith("_local") for t in do_elm)
               else "🟢 consulta · 🟡 escrita" if escreve else "🟢 consulta")
        do_gitlab = {t.removeprefix("@gitlabpr/") for t in a["tools"] if t.startswith("@gitlabpr/")}
        gitlab = ("➖" if not do_gitlab else "🟢 consulta · 🟡 abrir e mesclar PR" if "gitlab_mesclar_mr" in do_gitlab
                  else "🟢 consulta · 🟡 abrir PR" if "gitlab_criar_mr" in do_gitlab else "🟢 consulta")
        subs = a.get("toolsSettings", {}).get("subagent", {}).get("availableAgents", [])
        push = "🟡 pergunta" if any(r["capability"] == "shell" and r["effect"] == "ask" and "git push *" in r["match"]
                                 for r in a["permissions"]["rules"]) else "🔴 negado"
        cel = lambda xs: ", ".join(f"`{x}`" for x in xs) or "➖"
        linhas.append(f"| **{a['name']}** | {cel(do_fluxo)} | {cel(do_projeto)} | {cel(mcps)} | {elm} | {gitlab} | {cel(subs)} | {push} |")
    return "\n".join(linhas) + "\n"


def gerar(projeto: Path, cfg: dict) -> dict:
    base = json.loads((ASSETS / "papeis.json").read_text(encoding="utf-8"))
    # a chave é o nome do agente (sdd-<papel>); desconhecida nunca é ignorada em silêncio
    nomes = [f"sdd-{n}" for n in base["papeis"]]
    if desconhecidos := sorted(set(cfg.get("agentes", {})) - set(nomes)):
        raise ValueError(f"agentes.json: agente desconhecido {desconhecidos}; use {nomes}")
    return {f"sdd-{n}.json": agente(n, p, base, cfg) for n, p in base["papeis"].items()}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--projeto", type=Path, default=Path("."))
    ap.add_argument("--config", type=Path, help="padrão: <projeto>/.kiro/config/sdd/agentes.json")
    ap.add_argument("--saida", type=Path, help="padrão: <projeto>/.kiro/agents")
    # gravar é opt-in: rodar sem flag nunca grava nada antes do "ok" da pessoa
    ap.add_argument("--gravar", action="store_true", help="grava os agentes (sem ela, só mostra o diff)")
    ap.add_argument("--diff", action="store_true", help="o padrão: mostra o diff e não grava")
    args = ap.parse_args(argv)
    projeto = args.projeto.resolve()
    cfg = json.loads((args.config or projeto / ".kiro/config/sdd/agentes.json").read_text(encoding="utf-8"))
    try:
        agentes = gerar(projeto, cfg)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    erros = [e for a in agentes.values() for e in problemas(a, projeto)]
    if erros:
        print("\n".join(erros), file=sys.stderr)
        return 1
    saida = args.saida or projeto / ".kiro/agents"
    for arquivo, a in agentes.items():
        novo = json.dumps(a, ensure_ascii=False, indent=2) + "\n"
        alvo = saida / arquivo
        antigo = alvo.read_text(encoding="utf-8") if alvo.exists() else ""
        if not args.gravar:
            sys.stdout.writelines(difflib.unified_diff(antigo.splitlines(True), novo.splitlines(True), str(alvo), str(alvo)))
        elif novo != antigo:
            saida.mkdir(parents=True, exist_ok=True)
            alvo.write_text(novo, encoding="utf-8")
            print(f"gravado {alvo}")
    print("\n" + resumo(agentes, cfg), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
