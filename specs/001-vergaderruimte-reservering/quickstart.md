# Quickstart: Vergaderruimte Reservering

Validatiegids om end-to-end te bevestigen dat de feature werkt zoals
beschreven in [spec.md](spec.md). Verwijst naar [data-model.md](data-model.md)
en [contracts/routes.md](contracts/routes.md) voor details; bevat geen
implementatiecode.

## Vereisten

- Python 3.11+
- Dependencies uit `requirements.txt` (FastAPI, SQLAlchemy, Jinja2, Uvicorn, pytest)

## Opstarten (lokaal)

```bash
cd /home/hugo/zandbak/mySmartSpace
.venv/bin/uvicorn app.main:app --reload --port 8001
```

- Het project gebruikt een lokale SQLite-database (`smartspace.db`) in de repo-root.
- Bij eerste start wordt deze gevuld met seed-data: minimaal 2 demo-ruimtes en
  3 demo-accounts (2x rol `medewerker`, 1x rol `beheerder`).
- De app draait standaard op poort 8001 in deze demo-setup zodat een andere
  lokale service op 8000 niet in de weg zit.

## Validatiescenario's

### Scenario 1 — Reservering aanmaken (User Story 1, P1)

1. Log in als demo-medewerker via `/login`.
2. Ga naar `/rooms`, kies een ruimte, klik "Reserveren".
3. Vul een geldig tijdslot in binnen kantooruren (bijv. morgen 10:00–11:00).
4. **Verwacht**: reservering wordt aangemaakt en verschijnt op `/reservations`.
5. Herhaal stap 3 met exact hetzelfde tijdslot voor dezelfde ruimte.
6. **Verwacht**: 409-foutmelding, geen dubbele boeking (FR-003).

### Scenario 2 — Tijdvalidatie (FR-004/004a/004b)

1. Probeer een reservering met eindtijd vóór begintijd. **Verwacht**: 422.
2. Probeer een reservering met begintijd gisteren. **Verwacht**: 422.
3. Probeer een reservering om 19:00–20:00. **Verwacht**: 422 (buiten
   kantooruren 08:00–18:00).

### Scenario 3 — Wijzigen/annuleren (User Story 2, P2)

1. Wijzig een eigen reservering naar een ander vrij tijdslot.
   **Verwacht**: bijgewerkt, zichtbaar op `/reservations`.
2. Annuleer een eigen reservering. **Verwacht**: status `geannuleerd`, ruimte
   weer beschikbaar voor dat tijdslot.
3. Log in als een ander demo-medewerker-account en probeer de reservering van
   de eerste medewerker te wijzigen. **Verwacht**: 403 Forbidden (FR-007).

### Scenario 4 — Eigen overzicht incl. historie (User Story 3, P2)

1. Open `/reservations` als medewerker met minstens 1 actieve, 1 gewijzigde
   en 1 geannuleerde reservering.
2. **Verwacht**: alle drie zichtbaar met correcte status (FR-008).

### Scenario 5 — Ruimtebeheer (User Story 4, P3)

1. Log in als demo-beheerder, maak een nieuwe ruimte aan via `/rooms/new`.
2. **Verwacht**: ruimte direct zichtbaar/reserveerbaar op `/rooms` voor
   medewerkers.
3. Maak voor die ruimte een toekomstige reservering aan (als medewerker), en
   probeer daarna als beheerder de ruimte te verwijderen.
4. **Verwacht**: 409-foutmelding, verwijderen geweigerd (FR-009a).

## Geautomatiseerde tests

```bash
pytest
```

- `tests/unit/` dekt de businessregels uit `data-model.md` (overlap,
  kantooruren, verleden, verwijderregel) — verplicht vóór implementatie
  volgens constitution principe IV (Test-First, NON-NEGOTIABLE).
- `tests/integration/` dekt de 5 scenario's hierboven via de FastAPI
  TestClient.
