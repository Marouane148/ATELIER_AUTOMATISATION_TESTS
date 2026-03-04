# API Choice

- Étudiant : Étudiant ATELIER Automatisation
- API choisie : **Quotable** (Free quotes API)
- URL base : https://api.quotable.io
- Documentation officielle / README : https://github.com/lukePeavey/quotable
- Auth : **None** (pas d'authentification requise)
- Endpoints testés :
  - GET `/random` (quote aléatoire)
  - GET `/quotes?limit=5` (liste de 5 citations)
  - GET `/authors` (liste des auteurs)
- Hypothèses de contrat (champs attendus, types, codes) :
  - `GET /random` : HTTP 200, JSON avec fields: `_id` (string), `content` (string), `author` (string), `tags` (array[string]), `authorSlug` (string), `length` (int)
  - `GET /quotes?limit=5` : HTTP 200, JSON avec field `results` (array), chaque objet a les mêmes fields
  - `GET /authors` : HTTP 200, JSON avec field `results` (array), chaque objet a: `_id` (string), `name` (string), `slug` (string)
  - Codes attendus : 200 (OK), 404 (not found), 400 (bad request)
- Limites / rate limiting connu : ~500 req/day libre, pas de throttling strict documenté
- Risques (instabilité, downtime, CORS, etc.) : API très stable, CORS OK depuis localhost, downtime extrêmement rare
