"""Checagem do creditos.py: uv run --no-project python test_creditos.py"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from creditos import _ts, sessoes  # noqa: E402


def _sessao(kiro, sid, pasta, turnos):
    d = Path(kiro, "sessions", "h", f"sess_{sid}-0000")
    d.mkdir(parents=True)
    (d / "session.json").write_text(json.dumps({"workspacePaths": [pasta], "agentMode": "sdd-codificador", "title": sid}))
    linhas = [{"timestamp": ts, "payload": {"type": "usage_summary", "promptTurnSummaries": [{"unit": "credit", "usage": u}]}}
              for ts, u in turnos]
    linhas.append({"timestamp": "2026-10-21T10:00:00Z", "payload": {"type": "user"}})
    (d / "messages.jsonl").write_text("\n".join(map(json.dumps, linhas)) + "\nnão é json\n")


with tempfile.TemporaryDirectory() as k:
    repo, outro = str(Path(k, "repo")), str(Path(k, "outro"))
    _sessao(k, "aaaa", repo, [("2026-10-21T10:00:00.500Z", 1.5), ("2026-10-21T11:00:00Z", 2.0)])
    _sessao(k, "bbbb", outro, [("2026-10-21T12:00:00Z", 9.0)])
    _sessao(k, "cccc", str(Path(repo, "sub")), [("2026-10-21T13:00:00Z", 0.25)])

    r = sessoes(k, [repo])
    assert [x[1] for x in r] == ["cccc", "aaaa"], r  # filtra a pasta; a mais recente primeiro
    assert r[1][2] == 3.5, r
    # --desde igual ao "ate" gravado (segundos inteiros) não conta o mesmo turno de novo
    r = sessoes(k, [repo], _ts("2026-10-21T10:00:00Z"))
    assert [(x[1], x[2]) for x in r] == [("cccc", 0.25), ("aaaa", 2.0)], r
    assert sessoes(k, [repo], _ts("2026-10-21T14:00:00Z")) == []
print("ok")
