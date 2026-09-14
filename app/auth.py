"""Demo-account seed data en sessie-gebaseerde login/rolcontrole (T006, FR-011, FR-010)."""
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Gebruiker, Rol

# Trainings-scope: vaste demo-accounts, geen echte identity-provider (constitution V).
DEMO_ACCOUNTS = [
    {"naam": "Anna Medewerker", "rol": Rol.MEDEWERKER, "demo_account_code": "medewerker1"},
    {"naam": "Bram Medewerker", "rol": Rol.MEDEWERKER, "demo_account_code": "medewerker2"},
    {"naam": "Carla Beheerder", "rol": Rol.BEHEERDER, "demo_account_code": "beheerder1"},
]


def seed_demo_accounts(db: Session) -> None:
    for account in DEMO_ACCOUNTS:
        bestaat = (
            db.query(Gebruiker)
            .filter(Gebruiker.demo_account_code == account["demo_account_code"])
            .first()
        )
        if not bestaat:
            db.add(Gebruiker(**account))
    db.commit()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Gebruiker:
    demo_account_code = request.session.get("demo_account_code")
    if not demo_account_code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Niet ingelogd")
    gebruiker = (
        db.query(Gebruiker)
        .filter(Gebruiker.demo_account_code == demo_account_code)
        .first()
    )
    if gebruiker is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Onbekend account")
    return gebruiker


def require_beheerder(gebruiker: Gebruiker = Depends(get_current_user)) -> Gebruiker:
    if gebruiker.rol != Rol.BEHEERDER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Alleen beheerders mogen deze actie uitvoeren",
        )
    return gebruiker
