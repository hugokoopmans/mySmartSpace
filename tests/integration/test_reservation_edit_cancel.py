"""Integration test: wijzigen/annuleren + 403 bij andermans reservering (T017).

Dekt Quickstart Scenario 3 (FR-005, FR-006, FR-007).
Moet falen totdat T020 (edit/cancel-endpoints) geimplementeerd is.
"""
from datetime import datetime, timedelta

from tests.conftest import login


def _morgen_iso(uur: int) -> str:
    morgen = datetime.utcnow().date() + timedelta(days=1)
    return datetime(morgen.year, morgen.month, morgen.day, uur, 0).isoformat()


def _maak_ruimte(db_session, naam: str):
    from app.models import Vergaderruimte

    ruimte = Vergaderruimte(naam=naam, capaciteit=4, locatie="Verdieping 2")
    db_session.add(ruimte)
    db_session.commit()
    db_session.refresh(ruimte)
    return ruimte


def test_medewerker_kan_eigen_reservering_wijzigen(client, db_session):
    ruimte = _maak_ruimte(db_session, "Zaal E")
    login(client, "medewerker1")
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _morgen_iso(9), "eindtijd": _morgen_iso(10)},
    )
    reservering = db_session.query(__import__("app.models", fromlist=["Reservering"]).Reservering).first()

    response = client.post(
        f"/reservations/{reservering.id}/edit",
        data={"begintijd": _morgen_iso(11), "eindtijd": _morgen_iso(12)},
    )
    assert response.status_code in (200, 303)


def test_medewerker_kan_eigen_reservering_annuleren(client, db_session):
    ruimte = _maak_ruimte(db_session, "Zaal F")
    login(client, "medewerker1")
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _morgen_iso(9), "eindtijd": _morgen_iso(10)},
    )
    reservering = db_session.query(__import__("app.models", fromlist=["Reservering"]).Reservering).first()

    response = client.post(f"/reservations/{reservering.id}/cancel")
    assert response.status_code in (200, 303)

    overzicht = client.get("/reservations")
    assert "geannuleerd" in overzicht.text


def test_andere_medewerker_krijgt_403_bij_wijzigen(client, db_session):
    ruimte = _maak_ruimte(db_session, "Zaal G")
    login(client, "medewerker1")
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _morgen_iso(9), "eindtijd": _morgen_iso(10)},
    )
    reservering = db_session.query(__import__("app.models", fromlist=["Reservering"]).Reservering).first()

    login(client, "medewerker2")
    response = client.post(
        f"/reservations/{reservering.id}/edit",
        data={"begintijd": _morgen_iso(11), "eindtijd": _morgen_iso(12)},
    )
    assert response.status_code == 403
