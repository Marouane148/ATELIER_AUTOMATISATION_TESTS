# API Choice

- Étudiant : Étudiant ATELIER Automatisation
- API choisie : **JSONPlaceholder** (Fake JSON API for testing)
- URL base : https://jsonplaceholder.typicode.com
- Documentation officielle / README : https://jsonplaceholder.typicode.com
- Auth : **None** (pas d'authentification requise)
- Endpoints testés :
  - GET `/posts/1` (post unique)
  - GET `/posts?_limit=5` (liste de 5 posts)
  - GET `/users` (liste des utilisateurs)
- Hypothèses de contrat (champs attendus, types, codes) :
  - `GET /posts/1` : HTTP 200, JSON avec fields: `userId` (int), `id` (int), `title` (string), `body` (string)
  - `GET /posts?_limit=5` : HTTP 200, JSON array avec les mêmes fields
  - `GET /users` : HTTP 200, JSON array, chaque user a: `id` (int), `name` (string), `email` (string)
  - Codes attendus : 200 (OK), 404 (not found)
- Limites / rate limiting connu : Aucun, API fake pour tests
- Risques (instabilité, downtime, CORS, etc.) : API ultra-stable (service professionnel), CORS OK, 99.9% uptime garanti
