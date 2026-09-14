"""Unit test voor eigenaarschap-validatie bij wijzigen/annuleren (T016, FR-007).

Moet falen totdat T018/T019 (wijzig_reservering/annuleer_reservering met
eigenaarschapscontrole) geimplementeerd zijn.
"""
from datetime import datetime, timedelta

import pytest

from app.models import Gebruiker, Vergaderruimte
from app.services.reservation_service import (
    AutorisatieError,
    annuleer_reservering,
    maak_reservering,
    wijzig_reservering,
)


def _morgen(uur: int, minuut: int = 0) -> datetime:
    morgen = datetime.utcnow().date() + timedelta(days=1)
    return datetime(morgen.year, morgen.month, morgen.day, uur, minuut)


@pytest.fixture()
def ruimte(db_session):
    r = Vergaderruimte(naam="Zaal D", capaciteit=6, locatie="Verdieping 1")
    db_session.add(r)
    db_session.commit()
    db_session.refresh(r)
    return r


@pytest.fixture()
def eigenaar(db_session):
    return db_session.query(Gebruiker).filter_by(demo_account_code="medewerker1").first()


@pytest.fixture()
def andere_medewerker(db_session):
    return db_session.query(Gebruiker).filter_by(demo_account_code="medewerker2").first()


def test_eigenaar_kan_eigen_reservering_wijzigen(db_session, ruimte, eigenaar):
    reservering = maak_reservering(db_session, ruimte.id, eigenaar.id, _morgen(10), _morgen(11))
    gewijzigd = wijzig_reservering(db_session, reservering, eigenaar.id, _morgen(12), _morgen(13))
    assert gewijzigd.status.value == "gewijzigd"


def test_andere_medewerker_kan_niet_wijzigen(db_session, ruimte, eigenaar, andere_medewerker):
    reservering = maak_reservering(db_session, ruimte.id, eigenaar.id, _morgen(10), _morgen(11))
    with pytest.raises(AutorisatieError):
        wijzig_reservering(db_session, reservering, andere_medewerker.id, _morgen(12), _morgen(13))


def test_eigenaar_kan_eigen_reservering_annuleren(db_session, ruimte, eigenaar):
    reservering = maak_reservering(db_session, ruimte.id, eigenaar.id, _morgen(10), _morgen(11))
    geannuleerd = annuleer_reservering(db_session, reservering, eigenaar.id)
    assert geannuleerd.status.value == "geannuleerd"


def test_andere_medewerker_kan_niet_annuleren(db_session, ruimte, eigenaar, andere_medewerker):
    reservering = maak_reservering(db_session, ruimte.id, eigenaar.id, _morgen(10), _morgen(11))
    with pytest.raises(AutorisatieError):
        annuleer_reservering(db_session, reservering, andere_medewerker.id)
