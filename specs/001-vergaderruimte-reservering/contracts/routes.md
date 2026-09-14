# Contracts: Vergaderruimte Reservering

De applicatie is een server-rendered webapp (geen publieke JSON-API); de
"contracten" hieronder zijn de HTTP-routes die de Jinja2-pagina's aansturen.
Vastgelegd zodat FR's herleidbaar zijn naar concrete endpoints voor
`/speckit-tasks`.

## Authenticatie

| Route | Methode | Rol | Beschrijving |
|---|---|---|---|
| `/login` | GET, POST | iedereen | Demo-account selecteren/inloggen (FR-011) |
| `/logout` | POST | ingelogd | Sessie beëindigen |

## Ruimtes

| Route | Methode | Rol | Beschrijving | FR |
|---|---|---|---|---|
| `/rooms` | GET | medewerker, beheerder | Lijst ruimtes + beschikbaarheid tonen | FR-001 |
| `/rooms/new` | GET, POST | beheerder | Nieuwe ruimte aanmaken | FR-009 |
| `/rooms/{id}/edit` | GET, POST | beheerder | Ruimte wijzigen (naam/capaciteit/locatie) | FR-009 |
| `/rooms/{id}/delete` | POST | beheerder | Ruimte verwijderen (geweigerd bij actieve toekomstreserveringen) | FR-009a |

## Reserveringen

| Route | Methode | Rol | Beschrijving | FR |
|---|---|---|---|---|
| `/reservations/new` | GET, POST | medewerker | Reservering aanmaken voor gekozen ruimte/tijd | FR-002, FR-003, FR-004, FR-004a, FR-004b |
| `/reservations` | GET | medewerker | Eigen overzicht (incl. historisch/geannuleerd) | FR-008 |
| `/reservations/{id}/edit` | GET, POST | medewerker (eigenaar) | Reservering wijzigen | FR-005, FR-007 |
| `/reservations/{id}/cancel` | POST | medewerker (eigenaar) | Reservering annuleren | FR-006, FR-007 |

## Foutresponses (alle schrijf-routes)

| Situatie | HTTP-status | FR |
|---|---|---|
| Overlappende reservering | 409 Conflict | FR-003 |
| Eindtijd ≤ begintijd | 422 Unprocessable Entity | FR-004 |
| Begintijd in verleden | 422 Unprocessable Entity | FR-004a |
| Buiten kantooruren (08:00–18:00) | 422 Unprocessable Entity | FR-004b |
| Wijzigen/annuleren andermans reservering | 403 Forbidden | FR-007 |
| Ruimte verwijderen met actieve toekomstreserveringen | 409 Conflict | FR-009a |
