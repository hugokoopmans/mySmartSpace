"""Integration test: ruimtebeheer + rolcontrole beheerder (T026, Quickstart Scenario 5)."""
from datetime import datetime, timedelta

from tests.conftest import login


def _iso(uur: int) -> str:
    morgen = datetime.utcnow().date() + timedelta(days=1)
    return datetime(morgen.year, morgen.month, morgen.day, uur, 0).isoformat()


def test_beheerder_kan_ruimte_aanmaken_en_medewerker_kan_reserveren(client):
    login(client, "beheerder1")
    response = client.post(
        "/rooms/new", data={"naam": "Zaal J", "capaciteit": 8, "locatie": "Verdieping 6"}
    )
    assert response.status_code in (200, 303)
    client.post("/logout")

    login(client, "medewerker1")
    ruimtes = client.get("/rooms")
    assert "Zaal J" in ruimtes.text


def test_medewerker_mag_geen_ruimte_aanmaken(client):
    login(client, "medewerker1")
    response = client.post(
        "/rooms/new", data={"naam": "Zaal K", "capaciteit": 4, "locatie": "Verdieping 6"}
    )
    assert response.status_code == 403


def test_verwijderen_ruimte_met_toekomstreservering_geeft_conflict(client, db_session):
    from app.models import Vergaderruimte

    ruimte = Vergaderruimte(naam="Zaal L", capaciteit=4, locatie="Verdieping 7")
    db_session.add(ruimte)
    db_session.commit()
    db_session.refresh(ruimte)

    login(client, "medewerker1")
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _iso(9), "eindtijd": _iso(10)},
    )
    client.post("/logout")

    login(client, "beheerder1")
    response = client.post(f"/rooms/{ruimte.id}/delete")
    assert response.status_code == 409
