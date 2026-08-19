# MCP Production Readiness — Offre

> **Positionnement.** La couche de validation avant publication des serveurs MCP : score, gate CI, badge, corrections guidées et dossier de preuve. Le produit n’est ni un audit de sécurité certifié, ni une certification de conformité, ni un conseil juridique.

## Hypothèses à valider par entretiens et pilotes

| Palier | Hypothèse | Livrables |
|---|---:|---|
| Gratuit / public | 0 € | Scan autorisé, score basique, cinq écarts principaux et badge expérimental |
| Developer | 19–29 €/mois | Scans récurrents, historique local, badge, intégration GitHub Actions et corrections guidées |
| Team | 99–299 €/mois | Plusieurs dépôts, règles CI, monitoring, alertes, rapports et historique d’équipe |
| Enterprise | 5 000–30 000 €/an | Audit MCP accompagné, règles personnalisées, SSO, déploiement privé, rapports sécurité et SLA |

Ces montants sont des **hypothèses de découverte**, jamais des prix garantis. Les pilotes doivent mesurer le coût évité, la fréquence des scans, les exigences de confidentialité et la volonté de payer avant d’investir dans une plateforme hébergée.

## Ce qui existe dans V1

Le CLI local analyse un dépôt autorisé en lecture seule, calcule un score pondéré sur 100, produit un gate `BLOCKED`, `REVIEW` ou `READY_WITHIN_CHECKLIST`, génère un badge SVG, un rapport Markdown/JSON et des corrections guidées. GitHub Actions peut bloquer un pipeline sous un seuil choisi.

## Roadmap à valider

La prochaine étape est un historique de scores par commit, puis une intégration GitHub plus riche, des règles personnalisées par organisation, un monitoring récurrent, des alertes et un mode privé. L’auto-fix doit rester borné à des suggestions ou à des pull requests explicitement approuvées; aucune mutation automatique de l’infrastructure cliente n’est acceptable par défaut.

## English positioning

**MCP Production Readiness** is a pre-publication validation standard for MCP servers: score, CI gate, badge, guided fixes and evidence pack. The current release is local-first and read-only. It is not a certified security audit, compliance certification, legal advice or guarantee.
