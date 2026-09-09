"""Businesslogica voor reserveringen (T012): overlap-, tijd- en kantoorurenvalidatie.

Implementeert FR-002, FR-003, FR-004, FR-004a, FR-004b.
"""
from datetime import datetime, time

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Reservering, ReserveringStatus

KANTOOR_START = time(8, 0)
KANTOOR_EIND = time(18, 0)


class ReserveringValidatieError(Exception):
    """Ongeldige invoer (tijd, kantooruren) — leidt tot HTTP 422."""


class ReserveringConflictError(Exception):
    """Overlappende reservering — leidt tot HTTP 409."""


class AutorisatieError(Exception):
    """Actie op reservering van iemand anders — leidt tot HTTP 403."""


def _valideer_tijden(begintijd: datetime, eindtijd: datetime) -> None:
    if eindtijd <= begintijd:
        raise ReserveringValidatieError("Eindtijd moet na de begintijd liggen.")  # FR-004
    if begintijd <= datetime.utcnow():
        raise ReserveringValidatieError("Begintijd moet in de toekomst liggen.")  # FR-004a
    if not (KANTOOR_START <= begintijd.time() and eindtijd.time() <= KANTOOR_EIND):
        raise ReserveringValidatieError(
            "Reservering moet binnen kantooruren (08:00-18:00) vallen."
        )  # FR-004b


def _heeft_overlap(db: Session, ruimte_id: int, begintijd: datetime, eindtijd: datetime, exclude_id: int | None = None) -> bool:
    query = db.query(Reservering).filter(
        Reservering.ruimte_id == ruimte_id,
        Reservering.status != ReserveringStatus.GEANNULEERD,
        and_(Reservering.begintijd < eindtijd, Reservering.eindtijd > begintijd),
    )
    if exclude_id is not None:
        query = query.filter(Reservering.id != exclude_id)
    return db.query(query.exists()).scalar()


def maak_reservering(
    db: Session, ruimte_id: int, medewerker_id: int, begintijd: datetime, eindtijd: datetime
) -> Reservering:
    _valideer_tijden(begintijd, eindtijd)
    if _heeft_overlap(db, ruimte_id, begintijd, eindtijd):
        raise ReserveringConflictError(
            "Ruimte is al gereserveerd voor (een deel van) dit tijdslot."
        )  # FR-003
    reservering = Reservering(
        ruimte_id=ruimte_id,
        medewerker_id=medewerker_id,
        begintijd=begintijd,
        eindtijd=eindtijd,
        status=ReserveringStatus.ACTIEF,
    )
    db.add(reservering)
    try:
        db.commit()
    except IntegrityError as exc:  # tweede gelijktijdige aanvraag verliest (FR-003)
        db.rollback()
        raise ReserveringConflictError("Ruimte is zojuist door iemand anders geboekt.") from exc
    db.refresh(reservering)
    return reservering


def wijzig_reservering(
    db: Session,
    reservering: Reservering,
    medewerker_id: int,
    begintijd: datetime,
    eindtijd: datetime,
) -> Reservering:
    if reservering.medewerker_id != medewerker_id:
        raise AutorisatieError("Alleen de eigenaar mag deze reservering wijzigen.")  # FR-007
    _valideer_tijden(begintijd, eindtijd)
    if _heeft_overlap(db, reservering.ruimte_id, begintijd, eindtijd, exclude_id=reservering.id):
        raise ReserveringConflictError(
            "Ruimte is al gereserveerd voor (een deel van) dit tijdslot."
        )
    reservering.begintijd = begintijd
    reservering.eindtijd = eindtijd
    reservering.status = ReserveringStatus.GEWIJZIGD
    db.commit()
    db.refresh(reservering)
    return reservering


def annuleer_reservering(db: Session, reservering: Reservering, medewerker_id: int) -> Reservering:
    if reservering.medewerker_id != medewerker_id:
        raise AutorisatieError("Alleen de eigenaar mag deze reservering annuleren.")  # FR-007
    reservering.status = ReserveringStatus.GEANNULEERD
    db.commit()
    db.refresh(reservering)
    return reservering
