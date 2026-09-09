# Research: Vergaderruimte Reservering

Geen `NEEDS CLARIFICATION`-markers resterend in de Technical Context (alle
technische keuzes zijn al vastgelegd via de constitution). Dit document legt
de rationale vast voor de gekozen technologieën.

## Decision: FastAPI + Jinja2 (server-rendered), geen SPA

- **Rationale**: Vastgelegd in constitution principe II. FastAPI geeft
  moderne async-ondersteuning en automatische request-validatie (Pydantic),
  wat goed aansluit bij de businessregels rond tijdvalidatie (FR-004/004a/004b).
  Server-rendered Jinja2 houdt de trainingsopzet eenvoudig: één proces, geen
  losse build-pipeline voor een frontend.
- **Alternatives considered**: Django (meer batteries-included maar zwaarder
  dan nodig voor deze scope); losse SPA + REST-API (meer bewegende delen,
  onnodige complexiteit voor een single-user/demo-toepassing — afgewezen op
  basis van constitution principe III, YAGNI).

## Decision: SQLite via SQLAlchemy

- **Rationale**: Constitution principe III schrijft SQLite voor als datastore
  zonder externe databaseserver. SQLAlchemy geeft een ORM-laag die
  overlap-constraints en statusbeheer voor reserveringen overzichtelijk houdt.
- **Alternatives considered**: Rauwe SQL via `sqlite3`-module (minder
  onderhoudbaar naarmate het datamodel groeit); PostgreSQL (buiten scope,
  vereist externe server — expliciet uitgesloten door de constitution).

## Decision: Overlapdetectie en conflictafhandeling (FR-003)

- **Rationale**: Overlappende reserveringen voor dezelfde ruimte worden
  voorkomen door bij het aanmaken/wijzigen van een reservering binnen dezelfde
  databasetransactie te controleren op overlappende actieve reserveringen
  voor die ruimte, en de tweede gelijktijdige aanvraag af te wijzen met een
  duidelijke foutmelding (per Clarifications-sessie: "eerste aanvraag wint").
  Dit wordt afgedwongen op serviceniveau (`reservation_service.py`), niet in
  de UI, zodat de regel niet omzeild kan worden.
- **Alternatives considered**: Optimistic locking op applicatieniveau zonder
  transactie-isolatie (risico op race conditions bij gelijktijdige aanvragen);
  afgewezen omdat SQLite transacties met `BEGIN IMMEDIATE` dit eenvoudiger en
  betrouwbaarder afdwingen voor deze schaal.

## Decision: Demo-authenticatie (FR-011)

- **Rationale**: Constitution principe V schrijft vaste demo-accounts voor
  (rollen Medewerker/Beheerder), geen echte identity-provider. Dit wordt
  geïmplementeerd als een eenvoudige sessie-gebaseerde login met een vaste
  set gebruikers (seed-data), zonder wachtwoord-hashing-complexiteit die bij
  productiegebruik wel vereist zou zijn.
- **Alternatives considered**: Microsoft Entra ID/SSO (buiten scope voor
  trainingsrepo; expliciet uitgesloten, zie constitution principe V en
  Assumptions in spec.md).

**Output**: Alle technische onbekenden zijn opgelost; klaar voor Phase 1.
