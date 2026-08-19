# Trame de démo client — 15 minutes

> La démo utilise un dépôt local d’exemple. Aucun serveur tiers n’est scanné. Le produit n’est pas un audit certifié.

## Déroulé

De 0 à 2 minutes, présenter le changement de baseline : cœur stateless, Streamable HTTP et dépréciation HTTP+SSE/DCR. De 2 à 4 minutes, montrer le dépôt local, l’autorisation écrite, la version et les exclusions. De 4 à 7 minutes, lancer `mcp-readiness --demo --output /tmp/mcp-demo-report`, puis ouvrir `report.md` et `report.json`. De 7 à 10 minutes, parcourir les statuts, les preuves et les remédiations. De 10 à 12 minutes, expliquer la valeur du JSON rejouable et de la seconde passe. De 12 à 15 minutes, proposer un pilote sur un dépôt non critique avec consentement écrit et restitution.

## Objections

**« Est-ce un pentest ? »** Non. C’est une analyse statique non destructive; un pentest séparé peut être confié à un prestataire qualifié.

**« Pouvez-vous garantir la conformité ? »** Non. Le rapport exprime un alignement avec une checklist et doit être relu par les équipes et le conseil juridique du client.

**« Pourquoi ne pas scanner directement notre URL MCP ? »** Par sécurité et par conception : cette version accepte uniquement un chemin local et exige un consentement explicite hors démo.

**« Le rapport dit-il qu’un outil est dangereux ? »** Non. Il signale une capacité sensible potentielle et demande une revue du code, des scopes et des contrôles.
