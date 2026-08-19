from pathlib import Path
from mcp_readiness.analyzer import analyze
from mcp_readiness.fixflow import create_preview
ROOT = Path(__file__).parents[1]
def finding(data, dimension): return next(f for f in data["findings"] if f["dimension"] == dimension)
def test_clean_server():
    data = analyze(ROOT / "examples" / "clean-server")
    assert finding(data, "transport")["status"] == "OK"
    assert finding(data, "observability")["status"] == "OK"
    assert 0 <= data["score"]["score"] <= 100
    assert data["score"]["gate"] in {"BLOCKED", "REVIEW", "READY_WITHIN_CHECKLIST"}
def test_legacy_server():
    data = analyze(ROOT / "examples" / "legacy-server")
    assert finding(data, "transport")["status"] == "Bloquant"
    assert finding(data, "authorization")["status"] == "À surveiller"
    assert finding(data, "risk-surface")["status"] == "À surveiller"
def test_ambiguous_server():
    data = analyze(ROOT / "examples" / "ambiguous-server")
    assert finding(data, "transport")["status"] == "À surveiller"
    assert finding(data, "authorization")["status"] == "Bloquant"
    assert data["score"]["gate"] == "BLOCKED"

def test_fix_preview_is_non_destructive(tmp_path):
    repo = ROOT / "examples" / "clean-server"
    before = (repo / "server.py").read_text()
    data = analyze(repo)
    manifest = create_preview(data, repo, tmp_path, "python -c \"print('candidate tests passed')\"")
    assert manifest["test"]["status"] == "passed"
    assert (tmp_path / "fixes.patch").exists()
    assert (tmp_path / "pr-body.md").exists()
    assert (repo / "server.py").read_text() == before
