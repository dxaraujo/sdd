"""uv run --no-project python -m unittest test_gerar_agentes   (nesta pasta)"""
import json
import os
import re
import tempfile
import unittest
from fnmatch import fnmatchcase
from pathlib import Path

import gerar_agentes as g

BASE = json.loads((g.ASSETS / "papeis.json").read_text(encoding="utf-8"))
PAPEIS = BASE["papeis"]


def regras(a, cap, efeito):
    return [m for r in a["permissions"]["rules"] if r["capability"] == cap and r["effect"] == efeito for m in r.get("match", [])]


def efeito(a, cap, alvo):
    """Como o V3 decide: entre as regras com um `match` que pega o alvo e nenhum `exclude` que o pegue, vence a mais
    restritiva; sem regra, pergunta. `*` do fnmatch atravessa `/` (como o `like` do Cedar)."""
    pega = lambda padroes: any(fnmatchcase(alvo, p.removeprefix("./")) for p in padroes)
    efeitos = {r["effect"] for r in a["permissions"]["rules"]
               if r["capability"] == cap and pega(r.get("match", ["*"])) and not pega(r.get("exclude", []))}
    return next((e for e in ("deny", "ask", "allow") if e in efeitos), "ask")


class Gerar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        self.home, self.projeto = raiz / "home", raiz / "projeto"
        for s in {s for p in PAPEIS.values() for s in p["skills"]}:
            (self.home / "power/skills" / s).mkdir(parents=True)
            (self.home / "power/skills" / s / "SKILL.md").write_text("x")
        (self.projeto / ".kiro/steering").mkdir(parents=True)
        (self.projeto / ".kiro/steering/sdd.md").write_text("x")
        self.velho_home, os.environ["HOME"] = os.environ.get("HOME"), str(self.home)
        self.cfg = {"power": "~/power", "produto": ".kiro/planejamento", "glossario": "docs/glossario.md", "adr": "docs/adr",
                    "base": "develop", "bundle": "docs/elm/pa", "massa": None, "elm": True, "push_pr_no_loop": True,
                    "http_sh": True, "comandos": {"build": ["mvn test*"], "verificacao": ["mvn spring-boot:run*"]}}

    def tearDown(self):
        os.environ["HOME"] = self.velho_home
        self.tmp.cleanup()

    def gerar(self, **mudar):
        agentes = g.gerar(self.projeto, {**self.cfg, **mudar})
        self.assertEqual([e for a in agentes.values() for e in g.problemas(a, self.projeto)], [])
        return {k[4:-5]: a for k, a in agentes.items()}

    def test_seis_agentes_so_v3(self):
        agentes = self.gerar()
        self.assertEqual(sorted(agentes), sorted(PAPEIS))
        for nome, a in agentes.items():
            self.assertEqual(a["name"], f"sdd-{nome}")
            self.assertNotIn("allowedTools", a)
            self.assertNotIn("policies", a["permissions"])
            self.assertEqual(set(a.get("toolsSettings", {})) - {"subagent"}, set())
            self.assertNotIn("{{", json.dumps(a))
            self.assertNotIn("V2", a["prompt"])

    def test_comentar_e_anexar_na_propria_tarefa(self):
        agentes = self.gerar()
        for nome in ("produto", "codificador", "revisor", "verificador", "orquestrador"):
            for t in ("elm_comentar", "elm_anexo", "elm_transicao", "elm_lancar_horas"):
                self.assertIn(f"sdd/elm/{t}", regras(agentes[nome], "power", "ask"), nome)
                self.assertIn(f"@elm/{t}", agentes[nome]["tools"])
        self.assertIn("sdd/elm/elm_ligar", regras(agentes["codificador"], "power", "ask"))

    def test_pesquisador_so_le(self):
        p = self.gerar()["pesquisador"]
        self.assertEqual(regras(p, "power", "ask"), [])
        self.assertIn("sdd/elm/elm_comentar", regras(p, "power", "deny"))
        self.assertIn("sdd/gitlabpr/gitlab_criar_mr", regras(p, "power", "deny"))
        self.assertIn("*git push*", regras(p, "shell", "deny"))
        self.assertEqual(regras(p, "power", "allow"), [f"sdd/{t}" for t in g.expandir(["+elm-local"],
                                                                                      json.loads((g.ASSETS / "papeis.json").read_text())["grupos"])])

    def test_gitlab_so_em_quem_lida_com_pr(self):
        agentes = self.gerar()
        for nome in ("pesquisador", "verificador"):
            self.assertFalse([t for t in agentes[nome]["tools"] if t.startswith("@gitlabpr/")], nome)
            self.assertIn("sdd/gitlabpr/gitlab_obter_mr", regras(agentes[nome], "power", "deny"), nome)
        for nome in ("produto", "codificador", "revisor", "orquestrador"):
            self.assertIn("sdd/gitlabpr/gitlab_obter_mr", regras(agentes[nome], "power", "allow"), nome)
        self.assertIn("sdd/gitlabpr/gitlab_criar_mr", regras(agentes["produto"], "power", "deny"))

    def test_push_da_branch_nomeada_e_merge_so_no_codificador(self):
        agentes = self.gerar()
        for nome in ("codificador", "revisor", "verificador", "orquestrador"):
            self.assertIn("git push *", regras(agentes[nome], "shell", "ask"))
            self.assertEqual(efeito(agentes[nome], "shell", "git push -u origin feature/ft-031-x"), "ask", nome)
            for cmd in ("git push", "git push origin", "cd .kiro/local/wt/ft-031 && git push", "git push origin HEAD",
                        "git push -u origin HEAD:feature/ft-031-x", "git push origin @", "git push origin ft-031:develop",
                        "git push origin refs/heads/develop", "git push -f origin ft-031"):
                self.assertEqual(efeito(agentes[nome], "shell", cmd), "deny", (nome, cmd))
        for nome, a in agentes.items():
            self.assertIn("sdd/gitlabpr/gitlab_mesclar_mr", regras(a, "power", "ask" if nome == "codificador" else "deny"), nome)

    def test_registro_de_situacao_na_base(self):
        """Codificador e orquestrador gravam a situação da fatia (backlog e sprint) na base e dão o push com pergunta."""
        agentes = self.gerar()
        for nome in ("codificador", "orquestrador"):
            a = agentes[nome]
            for p in ("backlog.md", "sprints/2026/sprint-03.md"):
                self.assertEqual(efeito(a, "fs_write", f".kiro/planejamento/{p}"), "allow", (nome, p))
            for p in ("equipe.json", "acordos.md", "roadmap.md", "epicos/ep-03-x/prd.md", "fatias/FT-031.md",
                      "sustentacao/atendimento/AT-012-x.md", "aprendizado/licoes.md"):
                self.assertNotEqual(efeito(a, "fs_write", f".kiro/planejamento/{p}"), "allow", (nome, p))
            self.assertNotEqual(efeito(a, "fs_write", ".kiro/local/wt/ft-031/.kiro/planejamento/backlog.md"), "allow", nome)
            self.assertEqual(efeito(a, "shell", "git push origin develop"), "ask", nome)
            self.assertIn("git reset --keep origin/*", regras(a, "shell", "ask"), nome)
            self.assertEqual(efeito(a, "shell", "git reset --keep origin/develop --hard"), "deny", nome)
        for nome in ("revisor", "verificador"):
            self.assertEqual(efeito(agentes[nome], "shell", "git push origin develop"), "deny", nome)
            self.assertNotIn("git reset --keep origin/*", regras(agentes[nome], "shell", "ask"), nome)
        self.assertEqual(efeito(agentes["produto"], "shell", "git push origin develop"), "deny")

    def test_tool_do_elm_fora_do_papel_e_negada(self):
        catalogo = BASE["mcp_do_power"]["elm"]
        server = Path(__file__).resolve().parents[5] / "mcps/elm/mcp_elm/server.py"
        if server.exists():  # tool do mcp-elm fora do catálogo escaparia das regras dos agentes
            self.assertEqual(sorted(re.findall(r"^def (elm_\w+)\(", server.read_text(encoding="utf-8"), re.M)), sorted(catalogo))
        for nome, a in self.gerar().items():
            self.assertIn("sdd/elm/elm_backlog", regras(a, "power", "deny"), nome)

    def test_pa_schema_igual_ao_publicado(self):
        publicado = Path(__file__).resolve().parents[6] / "mcps/elm/pa.schema.json"
        if publicado.exists():  # a cópia do power e a publicada no repositório mcps
            self.assertEqual((Path(__file__).resolve().parents[1] / "assets/pa.schema.json").read_bytes(), publicado.read_bytes())

    def test_sem_elm(self):
        for a in self.gerar(elm=False).values():
            self.assertFalse([t for t in a["tools"] if t.startswith("@elm/")])
            self.assertEqual([m for m in regras(a, "power", "deny") if m.startswith("sdd/elm/")], ["sdd/elm/*"])

    def test_loop_sem_push_nem_pr(self):
        o = self.gerar(push_pr_no_loop=False)["orquestrador"]
        self.assertIn("*git push*", regras(o, "shell", "deny"))
        self.assertNotIn("git push *", regras(o, "shell", "ask"))
        self.assertIn("sdd/gitlabpr/gitlab_criar_mr", regras(o, "power", "deny"))

    def test_sem_glossario_nem_bundle(self):
        agentes = self.gerar(glossario=None, bundle=None)
        self.assertNotIn("docs/glossario.md", regras(agentes["produto"], "fs_write", "allow"))
        self.assertIn("glossário (`não há`)", agentes["produto"]["prompt"])
        self.assertFalse([m for m in regras(agentes["codificador"], "fs_read", "deny") if "elm/pa" in m])

    def test_extras_do_projeto(self):
        cfg = {"agentes": {"sdd-codificador": {"skills": ["skill://.kiro/skills/java/SKILL.md"], "mcp": ["banco/consultar"],
                                           "subagentes": [{"nome": "dba", "para": "consultas"}], "modelo": "m1"}}}
        (self.projeto / ".kiro/skills/java").mkdir(parents=True)
        (self.projeto / ".kiro/skills/java/SKILL.md").write_text("x")
        c = self.gerar(**cfg)["codificador"]
        self.assertTrue(c["includeMcpJson"])
        self.assertIn("@banco/consultar", c["tools"])
        self.assertIn("banco/consultar", regras(c, "mcp", "allow"))
        self.assertIn("dba", c["toolsSettings"]["subagent"]["availableAgents"])
        self.assertIn("Skills do projeto ligadas a você: `java`", c["prompt"])
        self.assertIn("`dba` (consultas)", c["prompt"])
        self.assertIn("mvn test*", regras(c, "shell", "allow"))
        self.assertIn("sh .kiro/sdd/http.sh *", regras(c, "shell", "allow"))
        self.assertEqual(c["model"], "m1")

    def test_resumo_mostra_o_que_cada_agente_recebeu(self):
        (self.projeto / ".kiro/skills/java").mkdir(parents=True)
        (self.projeto / ".kiro/skills/java/SKILL.md").write_text("x")
        cfg = {**self.cfg, "agentes": {"sdd-codificador": {"skills": ["skill://.kiro/skills/java/SKILL.md"],
                                                           "mcp": ["banco/consultar"]}}}
        linhas = {l.split("|")[1].strip(): l for l in g.resumo(g.gerar(self.projeto, cfg), cfg).splitlines()[2:]}
        self.assertIn("`java`", linhas["**sdd-codificador**"])
        self.assertIn("`banco/consultar`", linhas["**sdd-codificador**"])
        self.assertIn("🟢 só o bundle local", linhas["**sdd-pesquisador**"])
        self.assertIn("| ➖ |", linhas["**sdd-pesquisador**"])
        self.assertIn("🟢 consulta · 🟡 abrir e mesclar PR", linhas["**sdd-codificador**"])
        self.assertIn("🟡 pergunta", linhas["**sdd-codificador**"])
        self.assertTrue(linhas["**sdd-produto**"].rstrip(" |").endswith("🔴 negado"))

    def test_chave_sem_prefixo_falha(self):
        with self.assertRaises(ValueError):
            g.gerar(self.projeto, {**self.cfg, "agentes": {"codificador": {}}})

    def test_caminho_ruim_e_apontado(self):
        a = g.gerar(self.projeto, {**self.cfg, "agentes": {"sdd-revisor": {"skills": ["skill://.kiro/skills/nao/SKILL.md",
                                                                                     "skill:///abs/SKILL.md"]}}})
        erros = g.problemas(a["sdd-revisor.json"], self.projeto)
        self.assertEqual(len(erros), 2)

    def test_main_grava_e_diff_nao(self):
        conf = self.projeto / ".kiro/config/sdd/agentes.json"
        conf.parent.mkdir(parents=True)
        conf.write_text(json.dumps(self.cfg))
        self.assertEqual(g.main(["--projeto", str(self.projeto), "--diff"]), 0)
        self.assertFalse((self.projeto / ".kiro/agents").exists())
        self.assertEqual(g.main(["--projeto", str(self.projeto)]), 0)
        self.assertFalse((self.projeto / ".kiro/agents").exists())  # sem --gravar nada é gravado
        self.assertEqual(g.main(["--projeto", str(self.projeto), "--gravar"]), 0)
        self.assertEqual(len(list((self.projeto / ".kiro/agents").glob("sdd-*.json"))), 6)


if __name__ == "__main__":
    unittest.main()
