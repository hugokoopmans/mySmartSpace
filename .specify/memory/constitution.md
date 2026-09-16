<!--
Sync Impact Report:
- Version change: 1.0.0 -> 1.1.0
- Modified principles: none
- Added principles: VI. Material Design UI
- Added sections: none
- Removed sections: none
- Deferred items: none
-->

# SmartSpace Constitution

## Core Principles

### I. Spec-First

Elke wijziging start met een bijgewerkte specificatie (`specs/*/spec.md`) vóórdat er
code wordt geschreven. De spec beschrijft *wat* en *waarom*, nooit *hoe* (geen
framework-, taal- of library-keuzes in de spec). Implementatiedetails volgen uit de
plan-fase (`/speckit-plan`), nooit andersom. Code die niet herleidbaar is tot een
requirement in de spec wordt niet gebouwd.

### II. Python/FastAPI Implementatie

De backend wordt gebouwd met FastAPI (Python); de gebruikersinterface is
server-rendered via Jinja2-templates. Er wordt geen aparte SPA-frontend gebouwd.
Deze keuze is een gedocumenteerde technische beslissing (voor dit trainingsproject),
losstaand van de spec, en mag bij een eventuele toekomstige .NET-implementatie voor
de klant volledig vervangen worden zonder dat de spec wijzigt.

### III. Eenvoud & Uitbreidbaarheid (YAGNI)

SQLite is de datastore; geen externe databaseserver. Er wordt geen functionaliteit
gebouwd die niet in de huidige release-scope zit (bijv. werkplekreserveringen,
Outlook/Teams/Graph-integratie). Het datamodel en de architectuur worden wel zo
ontworpen dat deze uitbreidingen later zonder herontwerp kunnen worden toegevoegd.

### IV. Test-First voor Businessregels (NON-NEGOTIABLE)

Kernbusinessregels (geen dubbele boekingen, eindtijd na begintijd, historische
reserveringen blijven raadpleegbaar) moeten voorzien zijn van geautomatiseerde tests
vóórdat de bijbehorende functionaliteit als voltooid geldt.

### V. Trainings-scope Authenticatie

Authenticatie gebeurt via vaste demo-accounts (rollen: Medewerker, Beheerder).
Er wordt geen echte identity-provider (SSO/Entra ID) geïmplementeerd. Dit is een
expliciete trainings-scope-beperking: de oplossing is in deze vorm niet geschikt
voor productiegebruik zonder aanvullende, echte authenticatie en autorisatie.

### VI. Material Design UI

De gebruikersinterface volgt Material Design-principes voor layout, componenten,
toegankelijkheid en interactie. Nieuwe en gewijzigde UI-elementen MOETEN
consistente componentpatronen, duidelijke visuele hiërarchie, bruikbare
toetsenbordinteractie en voldoende kleurcontrast bieden. Afwijkingen moeten in
het plan worden gemotiveerd.

## Taal & Doelgroep

De applicatie is Nederlandstalig en bedoeld voor lokaal/demo-gebruik (geen i18n,
geen schaal- of performance-eisen buiten single-user/demo-gebruik).

## Governance

Deze constitution staat boven alle andere projectafspraken. Wijzigingen aan de
principes vereisen een expliciete update van dit document (versie ophogen,
wijzigingsdatum bijwerken) en een korte motivatie. Elke spec, elk plan en elke
implementatie wordt getoetst aan deze principes; afwijkingen moeten expliciet
gemotiveerd worden (bijv. in de "Complexity Tracking"-sectie van een plan).

**Version**: 1.1.0 | **Ratified**: 2026-09-09 | **Last Amended**: 2026-09-16
