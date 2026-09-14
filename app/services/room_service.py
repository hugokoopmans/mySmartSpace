"""Businesslogica voor ruimtebeheer (T027/T028): aanmaken, wijzigen, verwijderen (FR-009, FR-009a)."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Reservering, ReserveringStatus, Vergaderruimte


class RuimteVerwijderConflictError(Exception):
    """Ruimte heeft nog actieve toekomstreserveringen — leidt tot HTTP 409."""


def maak_ruimte(db: Session, naam: str, capaciteit: int, locatie: str) -> Vergaderruimte:
    ruimte = Vergaderruimte(naam=naam, capaciteit=capaciteit, locatie=locatie)
    db.add(ruimte)
    db.commit()
    db.refresh(ruimte)
    return ruimte


def wijzig_ruimte(
    db: Session, ruimte: Vergaderruimte, naam: str, capaciteit: int, locatie: str
) -> Vergaderruimte:
    ruimte.naam = naam
    ruimte.capaciteit = capaciteit
    ruimte.locatie = locatie
    db.commit()
    db.refresh(ruimte)
    return ruimte


def _heeft_actieve_toekomstreservering(db: Session, ruimte_id: int) -> bool:
    query = db.query(Reservering).filter(
        Reservering.ruimte_id == ruimte_id,
        Reservering.status != ReserveringStatus.GEANNULEERD,
        Reservering.eindtijd > datetime.utcnow(),
    )
    return db.query(query.exists()).scalar()


def verwijder_ruimte(db: Session, ruimte_id: int) -> None:
    if _heeft_actieve_toekomstreservering(db, ruimte_id):
        raise RuimteVerwijderConflictError(
            "Ruimte heeft nog actieve toekomstige reserveringen en kan niet verwijderd worden."
        )  # FR-009a
    ruimte = db.get(Vergaderruimte, ruimte_id)
    ruimte.verwijderd = True
    db.commit()
