"""Integration test: Nederlandse foutpagina's voor 403/409/422."""

from datetime import datetime, timedelta

from tests.conftest import login


def test_403_page_is_html_and_includes_nl_message(client):
    login(client, "medewerker1")
    response = client.post(
        "/rooms/new",
        data={"naam": "Zaal V", "capaciteit": 4, "locatie": "Verdieping 9"},
    )
    assert response.status_code == 403
    assert response.headers["content-type"].startswith("text/html")
    assert "Geen toegang" in response.text or "403" in response.text


def test_409_page_is_html_and_includes_nl_message(client, db_session):
    from app.models import Vergaderruimte

    ruimte = Vergaderruimte(naam="Zaal W", capaciteit=4, locatie="Verdieping 10")
    db_session.add(ruimte)
    db_session.commit()
    db_session.refresh(ruimte)

    login(client, "medewerker1")
    morgen = datetime.utcnow().date() + timedelta(days=1)
    client.post(
        "/reservations/new",
        data={
            "ruimte_id": ruimte.id,
            "begintijd": datetime(morgen.year, morgen.month, morgen.day, 9, 0).isoformat(),
            "eindtijd": datetime(morgen.year, morgen.month, morgen.day, 10, 0).isoformat(),
        },
    )
    client.post("/logout")

    login(client, "beheerder1")
    response = client.post(f"/rooms/{ruimte.id}/delete")
    assert response.status_code == 409
    assert response.headers["content-type"].startswith("text/html")
    assert "conflict" in response.text.lower() or "403" in response.text or "409" in response.text


def test_422_page_is_html_and_includes_nl_message(client):
    login(client, "medewerker1")
    response = client.post(
        "/reservations/new",
        data={
            "ruimte_id": 1,
            "begintijd": "2025-01-01T12:00:00",
            "eindtijd": "2025-01-01T11:00:00",
        },
    )
    assert response.status_code == 422
    assert response.headers["content-type"].startswith("text/html")
    assert "invoer" in response.text.lower() or "422" in response.text
