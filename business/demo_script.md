# Démo et vente — MCP Readiness Audit

## Objectif

La démo doit vendre un premier audit borné, pas une plateforme SaaS imaginaire. La question d’ouverture est : **« Pouvez-vous publier ce MCP en confiance ? »**

## Déroulé de 15 minutes

De 0 à 3 minutes, montrer le flow GitHub repository → score → findings → gate → badge. De 3 à 6 minutes, lancer `mcp-readiness --demo --output /tmp/mcp-demo --preview-fixes --test-command "python -m pytest -q"`. De 6 à 9 minutes, ouvrir le score, le gate, le rapport, le badge et les écarts. De 9 à 12 minutes, ouvrir `fixes.patch`, `fix-preview.md`, `pr-body.md` et `fix-manifest.json`; expliquer que les tests ont tourné sur une copie et que le dépôt source n’a pas été modifié. De 12 à 15 minutes, proposer l’audit payant et demander : **« Voulez-vous que ce check tourne automatiquement sur chaque PR ? »**

## Offre de sortie

Proposer un MCP Readiness Audit à 149–499 € comme hypothèse de lancement, avec dépôt autorisé, score, rapports, badge, corrections guidées et restitution. Après un premier résultat utile, proposer le check CI récurrent plutôt qu’un dashboard complet.

## Objections

**« Est-ce un pentest ? »** Non. C’est une revue de release-readiness statique et non destructive.

**« L’outil corrige-t-il automatiquement le code ? »** Non. Il prépare un preview de diff et un corps de PR. Un humain inspecte, adapte, teste et approuve toute modification.

**« Pouvez-vous garantir la conformité ? »** Non. Le score est un signal d’alignement avec une checklist, pas une certification.

**« Pourquoi pas un SaaS complet maintenant ? »** Le premier objectif est de valider la volonté de payer auprès de 10–20 constructeurs MCP et d’obtenir 3–5 premiers paiements avant d’investir dans le monitoring, le SSO ou l’infrastructure hébergée.
