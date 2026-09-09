"""Router voor vergaderruimtes (T013/T027/T028)."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Gebruiker, Vergaderruimte

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

