"""Integration test: overzicht incl. historische/geannuleerde reserveringen (T022, FR-008).

Dekt Quickstart Scenario 4.
"""
from datetime import datetime, timedelta

from tests.conftest import login


def _iso(uur: int, dagen: int = 1) -> str:
    dag = datetime.utcnow().date() + timedelta(days=dagen)
    return datetime(dag.year, dag.month, dag.day, uur, 0).isoformat()


def test_overzicht_toont_actief_gewijzigd_en_geannuleerd(client, db_session):
    from app.models import Vergaderruimte

    ruimte = Vergaderruimte(naam="Zaal H", capaciteit=4, locatie="Verdieping 4")
    db_session.add(ruimte)
    db_session.commit()
    db_session.refresh(ruimte)

    login(client, "medewerker1")

    # Actieve reservering
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _iso(9), "eindtijd": _iso(10)},
    )
    # Gewijzigde reservering
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _iso(11), "eindtijd": _iso(12)},
    )
    # Geannuleerde reservering
    client.post(
        "/reservations/new",
        data={"ruimte_id": ruimte.id, "begintijd": _iso(13), "eindtijd": _iso(14)},
    )

    overzicht = client.get("/reservations")
    assert overzicht.status_code == 200
    ids = [int(x) for x in __import__("re").findall(r"/reservations/(\d+)/edit", overzicht.text)]
    assert len(ids) == 3

    # Wijzig de tweede, annuleer de derde
    client.post(
        f"/reservations/{ids[1]}/edit", data={"begintijd": _iso(15), "eindtijd": _iso(16)}
    )
    client.post(f"/reservations/{ids[2]}/cancel")

    overzicht_na = client.get("/reservations")
    assert overzicht_na.text.count("actief") >= 1
    assert "gewijzigd" in overzicht_na.text
    assert "geannuleerd" in overzicht_na.text
