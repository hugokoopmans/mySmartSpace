# Implementation Plan: Vergaderruimte Reservering

**Branch**: `001-vergaderruimte-reservering` | **Date**: 2026-09-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-vergaderruimte-reservering/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

Reserveringssysteem voor vergaderruimtes waarmee medewerkers ruimtes kunnen
raadplegen, reserveren, wijzigen en annuleren (met borging tegen dubbele
boekingen, kantooruren en reserveren-in-het-verleden), en beheerders ruimtes
kunnen configureren. Technische aanpak: een monolithische FastAPI-applicatie
met server-rendered Jinja2-templates en SQLite als datastore, conform de
projectconstitution.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI, Jinja2 (server-rendered templates),
Starlette test client, Uvicorn (ASGI-server), SQLAlchemy (ORM voor SQLite)

**Storage**: SQLite (bestandsgebaseerd, geen externe databaseserver)

**Testing**: pytest (unit + integratietests via FastAPI TestClient)

**Target Platform**: Lokale/single-host webserver (Linux), gebruikt via de browser

**Project Type**: web-service (single project, server-rendered, geen aparte SPA)

**Performance Goals**: Geen harde performance-eisen; reactietijden passend bij
lokaal/demo-gebruik (richtlijn: <500ms per pagina-load op localhost)

**Constraints**: Nederlandstalige UI; single-user/demo-schaal; geen externe
identity-provider (demo-accounts, zie constitution principe V)

**Scale/Scope**: Trainings-/demo-schaal: enkele tientallen ruimtes, enkele
demo-gebruikers, geen concurrency-eisen buiten correcte conflictafhandeling
bij gelijktijdige boekingspogingen (FR-003)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe (constitution.md) | Check | Status |
|---|---|---|
| I. Spec-First | Plan volgt uitsluitend uit spec.md; geen nieuwe scope toegevoegd | PASS |
| II. Python/FastAPI Implementatie | FastAPI-backend + Jinja2-templates, geen aparte SPA | PASS |
| III. Eenvoud & Uitbreidbaarheid (YAGNI) | SQLite, geen out-of-scope features (werkplekken/Outlook/Teams/Graph blijven buiten scope); datamodel houdt rekening met latere uitbreiding | PASS |
| IV. Test-First voor Businessregels (NON-NEGOTIABLE) | pytest verplicht voor FR-003/FR-004/FR-004a/FR-004b/FR-008/FR-009a vóórdat functionaliteit als voltooid geldt; tasks.md moet testtaken vóór implementatietaken plaatsen | PASS (te borgen in /speckit-tasks) |
| V. Trainings-scope Authenticatie | Vaste demo-accounts (Medewerker/Beheerder), geen echte identity-provider | PASS |

Geen constitution-schendingen; Complexity Tracking-sectie hieronder blijft leeg.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
app/
├── main.py                  # FastAPI app + route registratie
├── database.py              # SQLAlchemy engine/session (SQLite)
├── models.py                # ORM-modellen: Ruimte, Reservering, Gebruiker
├── auth.py                  # Demo-account login/sessiebeheer, rolcontrole
├── routers/
│   ├── rooms.py              # Ruimtes raadplegen + beheren (FR-001, FR-009, FR-009a)
│   └── reservations.py       # Reserveren/wijzigen/annuleren/overzicht (FR-002..FR-008)
├── services/
│   └── reservation_service.py  # Businessregels: overlap, kantooruren, verleden (FR-003/004/004a/004b)
├── templates/                # Jinja2-templates (server-rendered UI, NL)
│   ├── base.html
│   ├── rooms.html
│   └── reservations.html
└── static/
    └── css/

tests/
├── unit/                     # reservation_service businessregels (FR-003/004/004a/004b/009a)
├── integration/              # FastAPI TestClient end-to-end scenario's per user story
└── conftest.py                # Testfixtures: in-memory SQLite, demo-gebruikers
```

**Structure Decision**: Single project (Optie 1) — één FastAPI-applicatie met
server-rendered Jinja2-UI, geen aparte frontend/backend-scheiding nodig omdat
er geen SPA gebouwd wordt (constitution principe II).

## Complexity Tracking

> Geen gevulde rijen: er zijn geen constitution-schendingen die gerechtvaardigd
> moeten worden.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
