"""ORM-modellen per data-model.md: Gebruiker, Vergaderruimte, Reservering (T005)."""
import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Rol(str, enum.Enum):
    MEDEWERKER = "medewerker"
    BEHEERDER = "beheerder"


class ReserveringStatus(str, enum.Enum):
    ACTIEF = "actief"
    GEWIJZIGD = "gewijzigd"
    GEANNULEERD = "geannuleerd"


class Gebruiker(Base):
    __tablename__ = "gebruikers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    naam: Mapped[str] = mapped_column(String(100), nullable=False)
    rol: Mapped[Rol] = mapped_column(Enum(Rol), nullable=False)
    demo_account_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )


class Vergaderruimte(Base):
    __tablename__ = "vergaderruimtes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    naam: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    capaciteit: Mapped[int] = mapped_column(Integer, nullable=False)
    locatie: Mapped[str] = mapped_column(String(100), nullable=False)
    verwijderd: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    reserveringen: Mapped[list["Reservering"]] = relationship(back_populates="ruimte")


class Reservering(Base):
    __tablename__ = "reserveringen"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ruimte_id: Mapped[int] = mapped_column(
        ForeignKey("vergaderruimtes.id"), nullable=False
    )
    medewerker_id: Mapped[int] = mapped_column(
        ForeignKey("gebruikers.id"), nullable=False
    )
    begintijd: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    eindtijd: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ReserveringStatus] = mapped_column(
        Enum(ReserveringStatus), default=ReserveringStatus.ACTIEF, nullable=False
    )
    aangemaakt_op: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    ruimte: Mapped["Vergaderruimte"] = relationship(back_populates="reserveringen")
    medewerker: Mapped["Gebruiker"] = relationship()
