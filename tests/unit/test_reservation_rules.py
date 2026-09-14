"""Unit tests voor reservation_service businessregels (T010).

Dekt FR-003 (overlap), FR-004 (eindtijd>begintijd), FR-004a (begintijd in
toekomst), FR-004b (kantooruren 08:00-18:00). Deze tests MOETEN falen totdat
T012 (reservation_service.maak_reservering) geimplementeerd is.
"""
from datetime import datetime, timedelta

import pytest

from app.models import Gebruiker, Vergaderruimte
from app.services.reservation_service import (
    ReserveringConflictError,
    ReserveringValidatieError,
    maak_reservering,
)


def _morgen(uur: int, minuut: int = 0) -> datetime:
    morgen = datetime.utcnow().date() + timedelta(days=1)
    return datetime(morgen.year, morgen.month, morgen.day, uur, minuut)


@pytest.fixture()
def ruimte(db_session):
    r = Vergaderruimte(naam="Zaal A", capaciteit=6, locatie="Verdieping 1")
    db_session.add(r)
    db_session.commit()
    db_session.refresh(r)
    return r


@pytest.fixture()
def medewerker(db_session):
    return db_session.query(Gebruiker).filter_by(demo_account_code="medewerker1").first()


def test_reservering_binnen_kantooruren_slaagt(db_session, ruimte, medewerker):
    reservering = maak_reservering(
        db_session, ruimte.id, medewerker.id, _morgen(10), _morgen(11)
    )
    assert reservering.id is not None


def test_overlappende_reservering_wordt_geweigerd(db_session, ruimte, medewerker):
    maak_reservering(db_session, ruimte.id, medewerker.id, _morgen(10), _morgen(11))
    with pytest.raises(ReserveringConflictError):
        maak_reservering(db_session, ruimte.id, medewerker.id, _morgen(10, 30), _morgen(11, 30))


def test_aansluitende_reservering_is_toegestaan(db_session, ruimte, medewerker):
    maak_reservering(db_session, ruimte.id, medewerker.id, _morgen(10), _morgen(11))
    # eindtijd van eerste = begintijd van tweede -> geen overlap
    reservering2 = maak_reservering(db_session, ruimte.id, medewerker.id, _morgen(11), _morgen(12))
    assert reservering2.id is not None


def test_eindtijd_voor_begintijd_wordt_geweigerd(db_session, ruimte, medewerker):
    with pytest.raises(ReserveringValidatieError):
        maak_reservering(db_session, ruimte.id, medewerker.id, _morgen(11), _morgen(10))


def test_begintijd_in_verleden_wordt_geweigerd(db_session, ruimte, medewerker):
    verleden = datetime.utcnow() - timedelta(days=1)
    with pytest.raises(ReserveringValidatieError):
        maak_reservering(db_session, ruimte.id, medewerker.id, verleden, verleden + timedelta(hours=1))


def test_reservering_buiten_kantooruren_wordt_geweigerd(db_session, ruimte, medewerker):
    with pytest.raises(ReserveringValidatieError):
        maak_reservering(db_session, ruimte.id, medewerker.id, _morgen(19), _morgen(20))
