# Next steps — MCP Production Readiness

## Prêt immédiatement

La V1 locale produit un score sur 100, un gate de release, un badge SVG, un rapport Markdown/JSON et un fichier de corrections guidées. Le workflow GitHub Actions exécute les tests et peut bloquer une release sous un seuil. Le système reste read-only, local-first et exige une autorisation explicite hors démo.

## À valider humainement

Le score et ses pondérations doivent être confrontés à des équipes qui construisent réellement des MCP. Les prix et les paliers doivent être testés par entretiens. Un juriste doit relire la formulation “readiness”, le badge, les rapports, les limites de responsabilité et la rétention des dépôts. Les règles de détection doivent être évaluées sur de vrais dépôts autorisés pour mesurer les faux positifs.

## Plan de validation sur 14 jours

| Période | Action | Résultat attendu |
|---|---|---|
| J1–J2 | Identifier 10–20 personnes ou entreprises qui construisent des MCP et qualifier leurs workflows GitHub/CI. | Liste de constructeurs actifs et problèmes récurrents. |
| J3–J4 | Mener cinq entretiens centrés sur les releases bloquées, les audits et les outils internes actuels. | Mesure de la douleur et des alternatives. |
| J5 | Montrer le score, le badge et le gate sur un dépôt d’exemple. | Objections et métriques jugées utiles. |
| J6–J7 | Proposer deux pilotes bornés, locaux et autorisés. | Premières preuves de valeur. |
| J8 | Comparer les résultats avec la revue humaine des équipes. | Faux positifs et pondérations à corriger. |
| J9–J10 | Tester les hypothèses de prix Developer, Team et audit accompagné. | Signal de volonté de payer. |
| J11 | Ajouter les contrôles demandés par les pilotes, sans élargir les permissions par défaut. | V1.1 priorisée par la demande réelle. |
| J12 | Tester le workflow CI sur une branche et documenter le seuil de gate. | Parcours d’installation reproductible. |
| J13 | Demander une recommandation ou une introduction à un autre constructeur MCP. | Début de canal commercial. |
| J14 | Décider : continuer les pilotes, ajuster l’offre ou arrêter une fonctionnalité non valorisée. | Décision fondée sur preuves plutôt que projection. |

## Roadmap conditionnelle

Si les pilotes confirment une demande récurrente, construire dans cet ordre : historique par commit, intégration GitHub enrichie, règles d’organisation, monitoring et alertes, puis SSO/déploiement privé. L’auto-fix doit d’abord produire des suggestions; toute création de PR doit être explicitement déclenchée et relue par un humain.
