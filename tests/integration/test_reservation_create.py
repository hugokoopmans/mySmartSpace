"""Integration test: reservering aanmaken + conflictafhandeling (T011, FR-002/FR-003).

Dekt Quickstart Scenario 1 & 2. Moet falen totdat T013/T014 geimplementeerd zijn.
"""
from datetime import datetime, timedelta

from tests.conftest import login


def _morgen_iso(uur: int) -> str:
    morgen = datetime.utcnow().date() + timedelta(days=1)
    return datetime(morgen.year, morgen.month, morgen.day, uur, 0).isoformat()


def test_medewerker_kan_ruimte_reserveren(client, db_session):
    from app.models import Vergaderruimte

    ruimte = Vergaderruimte(naam="Zaal B", capaciteit=4, locatie="Verdieping 2")
    db_session.add(ruimte)
    db_session.commit()
    db_session.refresh(ruimte)

    login(client, "medewerker1")
    response = client.post(
        "/reservations/new",
        data={
            "ruimte_id": ruimte.id,
            "begintijd": _morgen_iso(10),
            "eindtijd": _morgen_iso(11),
        },
    )
    assert response.status_code in (200, 303)

    overzicht = client.get("/reservations")
    assert overzicht.status_code == 200
    assert "Zaal B" in overzicht.text


def test_overlappende_reservering_geeft_conflictfout(client, db_session):
    from app.models import Vergaderruimte

    ruimte = Vergaderruimte(naam="Zaal C", capaciteit=4, locatie="Verdieping 2")
    db_session.add(ruimte)
    db_session.commit()
    db_session.refresh(ruimte)

    login(client, "medewerker1")
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _morgen_iso(10), "eindtijd": _morgen_iso(11)},
    )
    response = client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _morgen_iso(10), "eindtijd": _morgen_iso(11)},
    )
    assert response.status_code == 409
