# Tasks: Vergaderruimte Reservering

**Input**: Design documents from `/specs/001-vergaderruimte-reservering/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/routes.md](contracts/routes.md), [quickstart.md](quickstart.md)

**Tests**: Test-taken zijn VERPLICHT (niet optioneel) voor de businessregels
FR-003, FR-004, FR-004a, FR-004b, FR-007 en FR-009a — conform constitution
principe IV (Test-First, NON-NEGOTIABLE). Elke test-taak MOET falen vóór de
bijbehorende implementatietaak wordt uitgevoerd.

**Organization**: Taken zijn gegroepeerd per user story (spec.md) zodat elke
story onafhankelijk gebouwd, getest en opgeleverd kan worden.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Kan parallel uitgevoerd worden (ander bestand, geen onderlinge afhankelijkheid)
- **[Story]**: Bij welke user story deze taak hoort (US1, US2, US3, US4)
- Elke beschrijving bevat het exacte bestandspad

## Path Conventions

Single project structuur per [plan.md](plan.md): `app/` (applicatiecode), `tests/` (unit + integratie).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Projectinitialisatie en basisstructuur

- [X] T001 Create project directory structure per plan.md (`app/`, `app/routers/`, `app/services/`, `app/templates/`, `app/static/`, `tests/unit/`, `tests/integration/`)
- [X] T002 Initialize Python-project met dependencies in `requirements.txt` (fastapi, uvicorn, sqlalchemy, jinja2, python-multipart, pytest, httpx)
- [X] T003 [P] Configureer pytest in `pyproject.toml` (testpaths = tests/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Kerninfrastructuur die MOET bestaan vóór enige user story gebouwd wordt

**⚠️ CRITICAL**: Geen user-story-werk mag starten vóór deze fase compleet is

- [X] T004 Setup SQLAlchemy engine + sessiebeheer voor SQLite in `app/database.py`
- [X] T005 Implement ORM-modellen Gebruiker, Vergaderruimte, Reservering (incl. status-enum) per `data-model.md` in `app/models.py`
- [X] T006 Implement demo-account seed data + sessie-gebaseerde login/rolcontrole (FR-011, FR-010) in `app/auth.py`
- [X] T007 Create FastAPI-app instance, Jinja2Templates- en StaticFiles-configuratie in `app/main.py`
- [X] T008 [P] Create basis Jinja2-template met navigatie/rolweergave in `app/templates/base.html`
- [X] T009 Create pytest-fixtures (in-memory SQLite engine, demo-gebruikers, FastAPI TestClient) in `tests/conftest.py`

**Checkpoint**: Foundation gereed — user story-implementatie kan beginnen.

---

## Phase 3: User Story 1 - Vergaderruimte reserveren (Priority: P1) 🎯 MVP

**Goal**: Medewerker kan beschikbare ruimtes raadplegen en reserveren, met borging tegen overlap, ongeldige tijden en reserveren buiten kantooruren/verleden.

**Independent Test**: Als medewerker een vrije ruimte zoeken, reserveren, en de reservering terugzien in eigen overzicht; een overlappende tweede poging moet geweigerd worden.

- [X] T010 [US1] Write failing unit tests voor businessregels overlap (FR-003), eindtijd-na-begintijd (FR-004), begintijd-in-toekomst (FR-004a) en kantooruren (FR-004b) in `tests/unit/test_reservation_rules.py`
- [X] T011 [P] [US1] Write failing integration test voor reservering aanmaken + conflictafhandeling (Quickstart Scenario 1 & 2) in `tests/integration/test_reservation_create.py`
- [X] T012 [US1] Implement `reservation_service.maak_reservering()` met overlap-/tijd-/kantoorurenvalidatie (maakt T010 groen) in `app/services/reservation_service.py`
- [X] T013 [US1] Implement ruimtelijst + beschikbaarheidsquery voor GET `/rooms` (FR-001) in `app/routers/rooms.py`
- [X] T014 [US1] Implement GET/POST `/reservations/new` endpoint dat `reservation_service` aanroept (maakt T011 groen, FR-002) in `app/routers/reservations.py`
- [X] T015 [P] [US1] Create Jinja2-templates `app/templates/rooms.html` (ruimtelijst) en `app/templates/reservations_new.html` (reserveringsformulier)

**Checkpoint**: User Story 1 volledig werkend en onafhankelijk testbaar (MVP).

---

## Phase 4: User Story 2 - Reservering wijzigen of annuleren (Priority: P2)

**Goal**: Medewerker kan een eigen reservering wijzigen of annuleren; alleen de eigenaar mag dit.

**Independent Test**: Eigen reservering wijzigen naar vrij tijdslot en apart annuleren; poging tot wijzigen van andermans reservering wordt geweigerd.

- [X] T016 [US2] Write failing unit test voor eigenaarschap-validatie (FR-007) in `tests/unit/test_reservation_ownership.py`
- [X] T017 [P] [US2] Write failing integration test voor wijzigen/annuleren + 403 bij andermans reservering (Quickstart Scenario 3) in `tests/integration/test_reservation_edit_cancel.py`
- [X] T018 [US2] Implement `reservation_service.wijzig_reservering()` (hergebruikt overlap-/tijdvalidatie uit T012, status → `gewijzigd`) in `app/services/reservation_service.py`
- [X] T019 [US2] Implement `reservation_service.annuleer_reservering()` (status → `geannuleerd`, eigenaarschapscontrole, maakt T016 groen) in `app/services/reservation_service.py`
- [X] T020 [US2] Implement GET/POST `/reservations/{id}/edit` en POST `/reservations/{id}/cancel` endpoints (maakt T017 groen, FR-005/FR-006/FR-007) in `app/routers/reservations.py`
- [X] T021 [P] [US2] Create Jinja2-template `app/templates/reservations_edit.html`

**Checkpoint**: User Story 2 werkend, bovenop US1.

---

## Phase 5: User Story 3 - Eigen reserveringen overzien (Priority: P2)

**Goal**: Medewerker kan al zijn reserveringen (incl. historische/geannuleerde) inzien.

**Independent Test**: Meerdere reserveringen met verschillende statussen aanmaken en controleren dat ze allemaal zichtbaar zijn in het overzicht.

- [X] T022 [P] [US3] Write failing integration test voor overzicht incl. historische/geannuleerde reserveringen (Quickstart Scenario 4, FR-008) in `tests/integration/test_reservation_overview.py`
- [X] T023 [US3] Implement overzichtsquery (alle statussen, gesorteerd op tijd) voor GET `/reservations` (maakt T022 groen) in `app/routers/reservations.py`
- [X] T024 [P] [US3] Create Jinja2-template `app/templates/reservations.html` (overzicht met statuslabel)

**Checkpoint**: User Story 3 werkend, bovenop US1.

---

## Phase 6: User Story 4 - Vergaderruimtes beheren (Priority: P3)

**Goal**: Beheerder kan ruimtes aanmaken/wijzigen en verwijderen (met verwijderregel FR-009a).

**Independent Test**: Als beheerder een ruimte aanmaken en direct reserveerbaar zien; verwijderen van een ruimte met toekomstige reservering wordt geweigerd.

- [ ] T025 [P] [US4] Write failing unit test voor verwijderregel (FR-009a: weigeren bij actieve toekomstreservering) in `tests/unit/test_room_deletion.py`
- [ ] T026 [P] [US4] Write failing integration test voor ruimte aanmaken/wijzigen/verwijderen incl. rolcontrole beheerder (Quickstart Scenario 5) in `tests/integration/test_room_management.py`
- [ ] T027 [US4] Implement GET/POST `/rooms/new` en GET/POST `/rooms/{id}/edit` met beheerder-rolcontrole (FR-009, FR-010) in `app/routers/rooms.py`
- [ ] T028 [US4] Implement POST `/rooms/{id}/delete` met verwijderregel (maakt T025 groen) in `app/routers/rooms.py`
- [ ] T029 [P] [US4] Create Jinja2-templates `app/templates/rooms_new.html` en `app/templates/rooms_edit.html`

**Checkpoint**: User Story 4 werkend; alle user stories nu compleet.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Afronding na alle user stories

- [ ] T030 [P] Create foutpagina-template met NL-meldingen voor 403/409/422-responses in `app/templates/errors.html`
- [ ] T031 [P] Verifieer en actualiseer opstartinstructies in `quickstart.md` op basis van de daadwerkelijke implementatie
- [ ] T032 Run volledige `pytest`-suite en bevestig dat alle FR-001 t/m FR-011 gedekt zijn door minstens één test (constitution principe IV gate)

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** → **Phase 2 (Foundational)**: blokkerend, geen user story kan starten vóór T004–T009 klaar zijn.
- **Phase 3 (US1, P1)**: kan direct na Phase 2 starten; dit is de MVP.
- **Phase 4 (US2, P2)** en **Phase 5 (US3, P2)**: beide bouwen voort op de reservation_service uit US1 (T012); kunnen onderling parallel gebouwd worden ná US1.
- **Phase 6 (US4, P3)**: onafhankelijk van US2/US3, maar in de praktijk handiger ná US1 omdat US1 al ruimtes uitleest; kan technisch ook parallel aan US2/US3.
- **Phase 7 (Polish)**: pas nadat alle gewenste user stories opgeleverd zijn.

## Parallel Execution Examples

- Binnen Phase 2: T008 (template) kan parallel met T004–T007/T009 (andere bestanden).
- Binnen Phase 3: T011 (integratietest, ander bestand) kan parallel met T010; T015 (templates) kan parallel met T012–T014.
- Binnen Phase 4: T017 kan parallel met T016; T021 kan parallel met T018–T020.
- Binnen Phase 6: T025 en T026 kunnen parallel (verschillende testbestanden).

## Implementation Strategy

1. **MVP eerst**: Phase 1 → Phase 2 → Phase 3 (US1). Dit levert een werkend, demonstreerbaar reserveringssysteem op (kernwaarde van de spec).
2. **Incrementeel uitbreiden**: Phase 4 (US2) en Phase 5 (US3) toevoegen voor volledige medewerkersflow.
3. **Beheerfunctionaliteit**: Phase 6 (US4) toevoegen zodra beheerders zelf ruimtes moeten kunnen configureren (tot dan toe kan seed-data in T005/T006 volstaan als tijdelijke vervanging, zoals genoemd in spec.md).
4. **Afronden**: Phase 7 voor foutafhandeling en validatie van de volledige testsuite.
