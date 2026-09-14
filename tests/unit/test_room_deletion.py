"""Unit test voor verwijderregel (T025, FR-009a).

Verwijderen van een ruimte MOET geweigerd worden zolang er nog actieve
toekomstige reserveringen bestaan.
"""
from datetime import datetime, timedelta

import pytest

from app.models import Gebruiker, Vergaderruimte
from app.services.reservation_service import maak_reservering
from app.services.room_service import RuimteVerwijderConflictError, verwijder_ruimte


def _morgen(uur: int) -> datetime:
    morgen = datetime.utcnow().date() + timedelta(days=1)
    return datetime(morgen.year, morgen.month, morgen.day, uur, 0)


@pytest.fixture()
def ruimte(db_session):
    r = Vergaderruimte(naam="Zaal I", capaciteit=4, locatie="Verdieping 5")
    db_session.add(r)
    db_session.commit()
    db_session.refresh(r)
    return r


@pytest.fixture()
def medewerker(db_session):
    return db_session.query(Gebruiker).filter_by(demo_account_code="medewerker1").first()


def test_verwijderen_zonder_reserveringen_slaagt(db_session, ruimte):
    verwijder_ruimte(db_session, ruimte.id)
    db_session.refresh(ruimte)
    assert ruimte.verwijderd is True


def test_verwijderen_met_actieve_toekomstreservering_wordt_geweigerd(db_session, ruimte, medewerker):
    maak_reservering(db_session, ruimte.id, medewerker.id, _morgen(10), _morgen(11))
    with pytest.raises(RuimteVerwijderConflictError):
        verwijder_ruimte(db_session, ruimte.id)
