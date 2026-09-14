"""Router voor vergaderruimtes (T013/T027/T028)."""
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user, require_beheerder
from app.database import get_db
from app.models import Gebruiker, Vergaderruimte
from app.services.room_service import (
    RuimteVerwijderConflictError,
    maak_ruimte,
    verwijder_ruimte,
    wijzig_ruimte,
)

router = APIRouter(prefix="/rooms", tags=["rooms"])


def _get_templates(request: Request):
    from app.main import templates

    return templates


@router.get("")
def lijst_ruimtes(
    request: Request,
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(get_current_user),
):
    templates = _get_templates(request)
    ruimtes = db.query(Vergaderruimte).filter(Vergaderruimte.verwijderd.is_(False)).all()
    return templates.TemplateResponse(
        request, "rooms.html", {"user": user, "ruimtes": ruimtes}
    )


@router.get("/new")
def nieuwe_ruimte_formulier(
    request: Request,
    user: Gebruiker = Depends(require_beheerder),
):
    templates = _get_templates(request)
    return templates.TemplateResponse(request, "rooms_new.html", {"user": user})


@router.post("/new")
def nieuwe_ruimte_aanmaken(
    naam: str = Form(...),
    capaciteit: int = Form(...),
    locatie: str = Form(...),
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(require_beheerder),
):
    maak_ruimte(db, naam, capaciteit, locatie)
    return RedirectResponse(url="/rooms", status_code=303)


@router.get("/{ruimte_id}/edit")
def wijzig_ruimte_formulier(
    ruimte_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(require_beheerder),
):
    templates = _get_templates(request)
    ruimte = db.get(Vergaderruimte, ruimte_id)
    if ruimte is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ruimte niet gevonden")
    return templates.TemplateResponse(request, "rooms_edit.html", {"user": user, "ruimte": ruimte})


@router.post("/{ruimte_id}/edit")
def wijzig_ruimte_indienen(
    ruimte_id: int,
    naam: str = Form(...),
    capaciteit: int = Form(...),
    locatie: str = Form(...),
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(require_beheerder),
):
    ruimte = db.get(Vergaderruimte, ruimte_id)
    if ruimte is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ruimte niet gevonden")
    wijzig_ruimte(db, ruimte, naam, capaciteit, locatie)
    return RedirectResponse(url="/rooms", status_code=303)


@router.post("/{ruimte_id}/delete")
def ruimte_verwijderen(
    ruimte_id: int,
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(require_beheerder),
):
    try:
        verwijder_ruimte(db, ruimte_id)
    except RuimteVerwijderConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return RedirectResponse(url="/rooms", status_code=303)


