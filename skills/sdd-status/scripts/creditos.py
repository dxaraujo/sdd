"""Créditos do Kiro por sessão, lidos do ~/.kiro desta máquina (só leitura).

Uso: uv run --no-project python creditos.py [--pasta <dir>]... [--desde <AAAA-MM-DDTHH:MM:SS>]

Uma linha por sessão do Kiro aberta numa das pastas, com créditos depois de --desde (hora local), a mais recente
primeiro: sessao=<id curto> creditos=<x.xx> ate=<último turno, hora local> modo=<agente> titulo=<título>.
Nenhuma sessão com consumo → código 1.
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def _norm(p):
    return os.path.normcase(os.path.abspath(p))


def _dentro(a, b):
    a, b = _norm(a), _norm(b)
    return a == b or a.startswith(b.rstrip(os.sep) + os.sep)


def _ts(s):
    # Kiro grava em UTC com Z; --desde sem fuso é hora local. Compara em segundos inteiros, porque a linha
    # gravada no status.md tem segundos e o turno dela não pode contar de novo.
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (d if d.tzinfo else d.astimezone()).astimezone().replace(microsecond=0)


def sessoes(kiro, pastas, desde=None):
    # ponytail: o turno em curso não entra (o usage_summary é gravado no fim do turno); a skill lê na resposta a
    # uma pergunta, e o turno do registro fica para o próximo fechamento
    out = []
    for meta in Path(kiro, "sessions").glob("*/sess_*/session.json"):
        try:
            s = json.loads(meta.read_text(encoding="utf-8"))
            msgs = (meta.parent / "messages.jsonl").read_text(encoding="utf-8").splitlines()
        except (OSError, ValueError):
            continue
        wps = s.get("workspacePaths") or []
        if not any(_dentro(w, p) or _dentro(p, w) for w in wps for p in pastas):
            continue
        total, ate = 0.0, None
        for linha in msgs:
            try:
                r = json.loads(linha)
            except ValueError:
                continue
            p = r.get("payload") or {}
            if p.get("type") != "usage_summary":
                continue
            t = _ts(r["timestamp"])
            if desde and t <= desde:
                continue
            total += sum(x.get("usage", 0) for x in p.get("promptTurnSummaries", []) if x.get("unit") == "credit")
            ate = max(ate, t) if ate else t
        if ate:
            sid = meta.parent.name.removeprefix("sess_").split("-")[0]
            out.append((ate, sid, total, s.get("agentMode", "—"), s.get("title", "—")))
    return sorted(out, reverse=True)


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--pasta", action="append")
    a.add_argument("--desde")
    a.add_argument("--kiro", default=os.environ.get("KIRO_HOME", str(Path.home() / ".kiro")))
    o = a.parse_args(argv)
    r = sessoes(o.kiro, o.pasta or [os.getcwd()], _ts(o.desde) if o.desde else None)
    for ate, sid, total, modo, titulo in r:
        print(f"sessao={sid} creditos={total:.2f} ate={ate.strftime('%Y-%m-%dT%H:%M:%S')} modo={modo} titulo={titulo}")
    if not r:
        print("nenhuma sessão do Kiro com consumo nesta pasta (pergunte o número à pessoa)", file=sys.stderr)
    return 0 if r else 1


if __name__ == "__main__":
    sys.exit(main())
