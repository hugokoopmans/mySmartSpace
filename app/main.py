"""FastAPI-app, Jinja2- en static-configuratie (T007)."""
from fastapi import Depends, FastAPI, Form, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from app.database import SessionLocal, get_db, init_db
from app.auth import DEMO_ACCOUNTS, seed_demo_accounts
from app.models import Gebruiker

app = FastAPI(title="SmartSpace - Vergaderruimte Reservering")
app.add_middleware(SessionMiddleware, secret_key="training-repo-demo-secret")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


def _render_error_page(request: Request, status_code: int, title: str, message: str):
    return templates.TemplateResponse(
        request,
        "errors.html",
        {"user": None, "status_code": status_code, "title": title, "message": message},
        status_code=status_code,
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    mapping = {
        401: ("Niet ingelogd", exc.detail or "Je bent niet ingelogd."),
        403: ("Geen toegang", exc.detail or "Je hebt geen rechten voor deze actie."),
        404: ("Niet gevonden", exc.detail or "De gevraagde pagina of resource bestaat niet."),
        409: ("Conflict", exc.detail or "Er is een conflict met de huidige status."),
        422: ("Ongeldige invoer", exc.detail or "Controleer je invoer en probeer het opnieuw."),
    }
    title, message = mapping.get(exc.status_code, ("Fout", exc.detail or "Er is iets misgegaan."))
    return _render_error_page(request, exc.status_code, title, message)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return _render_error_page(
        request,
        422,
        "Ongeldige invoer",
        "Controleer de invoer en probeer het opnieuw.",
    )


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    db = SessionLocal()
    try:
        seed_demo_accounts(db)
    finally:
        db.close()


@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(
        request, "login.html", {"accounts": DEMO_ACCOUNTS, "user": None}
    )


@app.post("/login")
def login_submit(
    request: Request,
    demo_account_code: str = Form(...),
    db: Session = Depends(get_db),
):
    gebruiker = (
        db.query(Gebruiker)
        .filter(Gebruiker.demo_account_code == demo_account_code)
        .first()
    )
    if gebruiker is None:
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "accounts": DEMO_ACCOUNTS,
                "user": None,
                "fout": "Onbekend demo-account",
            },
            status_code=422,
        )
    request.session["demo_account_code"] = gebruiker.demo_account_code
    return RedirectResponse(url="/rooms", status_code=303)


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


from app.routers import rooms, reservations  # noqa: E402

app.include_router(rooms.router)
app.include_router(reservations.router)

