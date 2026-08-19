from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class ScoreDimension:
    key: str
    label: str
    weight: int
    status: str
    points: int
    rationale: str


def _points(status: str) -> int:
    return {"OK": 100, "À surveiller": 55, "Bloquant": 0}.get(status, 25)


def calculate_score(findings: list[dict]) -> dict:
    weights = {
        "transport": (20, "Protocol compatibility"),
        "authorization": (20, "Authentication"),
        "exposure": (15, "Tool schemas and exposure"),
        "risk-surface": (15, "Security surface"),
        "observability": (10, "Error handling and audit trail"),
        "sdk": (10, "SDK and dependency readiness"),
        "registration": (10, "Client registration"),
    }
    dimensions = []
    for finding in findings:
        if finding["dimension"] not in weights:
            continue
        weight, label = weights[finding["dimension"]]
        dimensions.append(ScoreDimension(finding["dimension"], label, weight, finding["status"], _points(finding["status"]), finding["justification"]))
    total_weight = sum(d.weight for d in dimensions) or 1
    score = round(sum(d.weight * d.points for d in dimensions) / total_weight)
    blockers = sum(d.status == "Bloquant" for d in dimensions)
    watches = sum(d.status == "À surveiller" for d in dimensions)
    gate = "BLOCKED" if blockers else ("REVIEW" if watches else "READY_WITHIN_CHECKLIST")
    return {
        "score": score,
        "max_score": 100,
        "gate": gate,
        "blockers": blockers,
        "watch_items": watches,
        "dimensions": [d.__dict__ for d in dimensions],
        "disclaimer": "Score heuristique d’alignement avec une checklist; ce résultat ne constitue ni certification, ni audit de sécurité certifié, ni conseil juridique.",
    }
