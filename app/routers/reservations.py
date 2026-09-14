"""Router voor reserveringen (T014/T020/T023): aanmaken, wijzigen, annuleren, overzicht."""
from datetime import datetime

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Gebruiker, Reservering, Vergaderruimte
from app.services.reservation_service import (
    AutorisatieError,
    ReserveringConflictError,
    ReserveringValidatieError,
    annuleer_reservering,
    maak_reservering,
    wijzig_reservering,
)

router = APIRouter(prefix="/reservations", tags=["reservations"])


def _get_templates(request: Request):
    from app.main import templates

    return templates


@router.get("/new")
def nieuw_formulier(
    request: Request,
    ruimte_id: int | None = None,
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(get_current_user),
):
    templates = _get_templates(request)
    ruimtes = db.query(Vergaderruimte).filter(Vergaderruimte.verwijderd.is_(False)).all()
    return templates.TemplateResponse(
        request,
        "reservations_new.html",
        {"user": user, "ruimtes": ruimtes, "ruimte_id": ruimte_id},
    )


@router.post("/new")
def nieuw_aanmaken(
    request: Request,
    ruimte_id: int = Form(...),
    begintijd: str = Form(...),
    eindtijd: str = Form(...),
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(get_current_user),
):
    templates = _get_templates(request)
    try:
        maak_reservering(
            db, ruimte_id, user.id, datetime.fromisoformat(begintijd), datetime.fromisoformat(eindtijd)
        )
    except ReserveringValidatieError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except ReserveringConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return RedirectResponse(url="/reservations", status_code=303)


@router.get("")
def overzicht(
    request: Request,
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(get_current_user),
):
    templates = _get_templates(request)
    reserveringen = (
        db.query(Reservering)
        .filter(Reservering.medewerker_id == user.id)
        .order_by(Reservering.begintijd.desc())
        .all()
    )
    return templates.TemplateResponse(
        request, "reservations.html", {"user": user, "reserveringen": reserveringen}
    )


def _get_eigen_reservering(db: Session, reservering_id: int, user: Gebruiker) -> Reservering:
    reservering = db.get(Reservering, reservering_id)
    if reservering is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservering niet gevonden")
    return reservering


@router.get("/{reservering_id}/edit")
def wijzig_formulier(
    reservering_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(get_current_user),
):
    templates = _get_templates(request)
    reservering = _get_eigen_reservering(db, reservering_id, user)
    return templates.TemplateResponse(
        request, "reservations_edit.html", {"user": user, "reservering": reservering}
    )


@router.post("/{reservering_id}/edit")
def wijzig_indienen(
    reservering_id: int,
    request: Request,
    begintijd: str = Form(...),
    eindtijd: str = Form(...),
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(get_current_user),
):
    templates = _get_templates(request)
    reservering = _get_eigen_reservering(db, reservering_id, user)
    try:
        wijzig_reservering(
            db, reservering, user.id, datetime.fromisoformat(begintijd), datetime.fromisoformat(eindtijd)
        )
    except AutorisatieError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ReserveringValidatieError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except ReserveringConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return RedirectResponse(url="/reservations", status_code=303)


@router.post("/{reservering_id}/cancel")
def annuleren(
    reservering_id: int,
    db: Session = Depends(get_db),
    user: Gebruiker = Depends(get_current_user),
):
    reservering = _get_eigen_reservering(db, reservering_id, user)
    try:
        annuleer_reservering(db, reservering, user.id)
    except AutorisatieError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    return RedirectResponse(url="/reservations", status_code=303)

