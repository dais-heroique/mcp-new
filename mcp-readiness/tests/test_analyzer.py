from pathlib import Path
from mcp_readiness.analyzer import analyze
ROOT = Path(__file__).parents[1]
def finding(data, dimension): return next(f for f in data["findings"] if f["dimension"] == dimension)
def test_clean_server():
    data = analyze(ROOT / "examples" / "clean-server")
    assert finding(data, "transport")["status"] == "OK"
    assert finding(data, "observability")["status"] == "OK"
def test_legacy_server():
    data = analyze(ROOT / "examples" / "legacy-server")
    assert finding(data, "transport")["status"] == "Bloquant"
    assert finding(data, "authorization")["status"] == "À surveiller"
    assert finding(data, "risk-surface")["status"] == "À surveiller"
def test_ambiguous_server():
    data = analyze(ROOT / "examples" / "ambiguous-server")
    assert finding(data, "transport")["status"] == "À surveiller"
    assert finding(data, "authorization")["status"] == "Bloquant"
