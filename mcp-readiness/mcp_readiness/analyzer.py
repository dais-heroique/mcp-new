from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

BASELINE = "2026-07-28"

@dataclass
class Finding:
    dimension: str
    status: str
    title: str
    justification: str
    evidence: list[str]
    remediation: str
    owner: str = "Engineering / Security"
    reference: str = "https://modelcontextprotocol.io/"

    def to_dict(self):
        return asdict(self)


def _files(root: Path) -> Iterable[Path]:
    ignored = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__", ".next"}
    for path in root.rglob("*"):
        if path.is_file() and not any(part in ignored for part in path.parts) and path.suffix.lower() in {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".toml", ".yaml", ".yml", ".md", ".go", ".rs", ".cs"}:
            yield path


def _read(paths: Iterable[Path]) -> dict[str, str]:
    result = {}
    for path in paths:
        try:
            result[str(path)] = path.read_text(encoding="utf-8", errors="ignore")[:500_000]
        except OSError:
            pass
    return result


def _evidence(texts: dict[str, str], patterns: list[str]) -> list[str]:
    return [filename for filename, text in texts.items() if any(re.search(pattern, text, re.I | re.M) for pattern in patterns)][:12]


def analyze(root: str | Path) -> dict:
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"Target is not a directory: {root}")
    texts = _read(_files(root)); all_text = "\n".join(texts.values()); findings: list[Finding] = []
    streamable = _evidence(texts, [r"StreamableHTTP", r"streamable.?http", r"createMcpHandler", r"streamable_http"])
    legacy = _evidence(texts, [r"HTTP.?SSE", r"SseServerTransport", r"SSEServerTransport", r"/sse", r"ServerSentEvent"])
    stdio = _evidence(texts, [r"StdioServerTransport", r"stdio_server", r"run_stdio", r"stdio"])
    if streamable and legacy: status, title, why = "À surveiller", "Streamable HTTP présent avec vestiges HTTP+SSE", "Le dépôt contient un transport moderne et des marqueurs legacy; vérifiez le chemin réellement exposé."
    elif legacy: status, title, why = "Bloquant", "Transport HTTP+SSE legacy détecté", "HTTP+SSE est déprécié dans la baseline 2026-07-28; planifier la migration."
    elif streamable or stdio: status, title, why = "OK", "Transport MCP identifiable", "Un transport stdio ou Streamable HTTP est identifiable."
    else: status, title, why = "À surveiller", "Transport non déterminé", "Aucun motif de transport standard n'a été trouvé; revue manuelle requise."
    findings.append(Finding("transport", status, title, why, list(dict.fromkeys(streamable + legacy + stdio)), "Documenter Streamable HTTP stateless pour le distant; conserver stdio pour le local et retirer HTTP+SSE après validation.", reference="https://modelcontextprotocol.io/specification/2026-07-28/basic/transports"))
    dcr = _evidence(texts, [r"Dynamic Client Registration", r"dynamic.?client.?registration", r"register_client", r"/register"])
    cimd = _evidence(texts, [r"CIMD", r"client.?metadata.?document", r"client_id_metadata"])
    oauth = _evidence(texts, [r"OAuth", r"oauth", r"authorization", r"Bearer", r"JWKS", r"issuer"])
    ema = _evidence(texts, [r"enterprise.?managed", r"EMA", r"ID.?JAG", r"enterprise-managed-authorization", r"identity assertion"])
    if ema: auth_status, auth_title, auth_why = "OK", "Signaux EMA détectés", "Le dépôt contient des marqueurs EMA; vérifier issuer, audience, signature, expiry et scopes."
    elif oauth or dcr: auth_status, auth_title, auth_why = "À surveiller", "Signal d'autorisation sans preuve EMA", "Un mécanisme OAuth ou d'enregistrement client semble présent, mais EMA et validations complètes ne sont pas identifiables."
    else: auth_status, auth_title, auth_why = "Bloquant", "Autorisation non détectée", "Aucun mécanisme d'autorisation identifiable."
    findings.append(Finding("authorization", auth_status, auth_title, auth_why, list(dict.fromkeys(oauth + ema + cimd + dcr)), "Ajouter OAuth avec validation issuer/audience/expiration/scopes; documenter EMA et la révocation IdP.", reference="https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization"))
    findings.append(Finding("registration", "À surveiller" if dcr and not cimd else ("OK" if cimd else "À surveiller"), "Enregistrement client", "DCR détecté sans CIMD." if dcr and not cimd else "CIMD détecté ou choix à documenter.", list(dict.fromkeys(cimd + dcr)), "Préférer les clients pré-enregistrés ou CIMD; garder DCR comme fallback documenté.", reference="https://blog.modelcontextprotocol.io/posts/2026-07-28/"))
    tools = _evidence(texts, [r"@(?:mcp\.)?tool", r"register_tool", r"server\.tool", r"tools/list", r"Tool\(", r"tools\s*="])
    resources = _evidence(texts, [r"@(?:mcp\.)?resource", r"register_resource", r"server\.resource", r"resources/list"])
    risky = {"file access": r"open\(|pathlib|readFile|writeFile|fs\.", "command execution": r"subprocess|child_process|exec\(|spawn\(|os\.system|shell=True", "network egress": r"requests\.|httpx\.|fetch\(|urllib|axios|socket", "database write": r"INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM|\.execute\(|\.save\("}
    risk_evidence = {name: _evidence(texts, [pattern]) for name, pattern in risky.items()}; risk_hits = [name for name, ev in risk_evidence.items() if ev]
    findings.append(Finding("exposure", "OK" if tools else "À surveiller", f"Surface exposée: {len(tools)} fichier(s) avec outils, {len(resources)} avec ressources", "Les déclarations et preuves sont listées.", list(dict.fromkeys(tools + resources + [p for ev in risk_evidence.values() for p in ev])), "Réduire les permissions, décrire chaque outil, valider les entrées et confirmer les actions à impact.", reference="https://modelcontextprotocol.io/docs"))
    if risk_hits: findings.append(Finding("risk-surface", "À surveiller", "Capacités sensibles potentiellement exposées", "Motifs détectés: " + ", ".join(risk_hits) + ". Revue humaine requise.", list(dict.fromkeys([p for ev in risk_evidence.values() for p in ev])), "Ajouter allowlists, scopes par outil, validation, timeouts, audit et tests non destructifs.", reference="https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization"))
    logging = _evidence(texts, [r"logging", r"logger", r"audit.?log", r"audit.?trail", r"structlog", r"winston", r"pino"])
    findings.append(Finding("observability", "OK" if logging else "À surveiller", "Journalisation et audit trail", "Des marqueurs sont présents." if logging else "Aucune journalisation explicite trouvée.", logging, "Journaliser identité, outil, résultat, durée et corrélation sans secrets.", reference="https://modelcontextprotocol.io/specification/2026-07-28/"))
    sdk = _evidence(texts, [r"modelcontextprotocol", r"@modelcontextprotocol", r"mcp-server", r"mcp>=", r"mcp=="])
    findings.append(Finding("sdk", "À surveiller" if sdk else "Bloquant", "Version SDK", "Référence SDK trouvée; comparaison exacte à confirmer." if sdk else "Aucune dépendance SDK MCP identifiable.", sdk, "Épingler un SDK compatible avec la baseline et exécuter les tests d'interopérabilité.", reference="https://github.com/modelcontextprotocol/python-sdk"))
    return {"schema_version": "1.0", "baseline": BASELINE, "target": str(root), "findings": [f.to_dict() for f in findings], "evidence_summary": {"files_scanned": len(texts)}}


def markdown_report(data: dict) -> str:
    fs = data["findings"]; blockers = sum(f["status"] == "Bloquant" for f in fs); watch = sum(f["status"] == "À surveiller" for f in fs)
    lines = ["# MCP Release Readiness — Rapport statique", "", "> **Disclaimer.** Ce document est une checklist heuristique. Il ne constitue ni un audit de sécurité certifié, ni un conseil juridique, et n'affirme jamais la conformité.", "", f"**Baseline :** `{data['baseline']}`  \n**Cible :** `{data['target']}`  \n**Fichiers analysés :** {data['evidence_summary']['files_scanned']}", "", "## Résumé exécutif", "", f"L'analyse a relevé **{blockers} Bloquant(s)** et **{watch} point(s) À surveiller**. Une validation humaine reste nécessaire.", "", "## Matrice des écarts", "", "| Dimension | Statut | Écart / justification | Propriétaire |", "|---|---|---|---|"]
    for f in fs: lines.append(f"| {f['dimension']} | **{f['status']}** | {f['title']} — {f['justification']} | {f['owner']} |")
    lines += ["", "## Preuves et remédiations", ""]
    for f in fs:
        lines += [f"### {f['dimension']} — {f['title']}", f"**Preuves :** {', '.join(f['evidence']) if f['evidence'] else 'Aucune preuve textuelle détectée'}", f"**Remédiation proposée :** {f['remediation']}", f"**Référence :** [{f['reference']}]({f['reference']})", ""]
    lines += ["## Plan d'action daté", "", "| Échéance | Action | Responsable |", "|---|---|---|", "| J+1 | Confirmer les preuves et le transport réellement exposé | Équipe technique cliente |", "| J+3 | Prioriser les Bloquants | Engineering / Security |", "| J+7 | Tester la migration en préproduction | Engineering |", "| J+14 | Rejouer le scanner et archiver la preuve | Engineering / Security |"]
    return "\n".join(lines) + "\n"


def write_reports(data: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "report.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "report.md").write_text(markdown_report(data), encoding="utf-8")
