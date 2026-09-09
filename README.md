# mySmartSpace

trainings repo voor spec dirven developement project DIKW Academy

SmartSpace is een reserveringssysteem voor vergaderruimtes, gebouwd volgens een
spec-driven aanpak met [Spec Kit](https://github.com/github/spec-kit): eerst de
specificatie, dan het plan, dan de taken, en pas daarna de implementatie.

## Status

- Constitution: [.specify/memory/constitution.md](.specify/memory/constitution.md)
- Feature 001 - Vergaderruimte Reservering: [specs/001-vergaderruimte-reservering/](specs/001-vergaderruimte-reservering/)
  (spec, plan, research, data-model, contracts, quickstart, tasks)
- Implementatie: Python 3.11+ / FastAPI / Jinja2 / SQLite (zie
  [plan.md](specs/001-vergaderruimte-reservering/plan.md) voor de rationale)

## Lokaal draaien

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

Zie [quickstart.md](specs/001-vergaderruimte-reservering/quickstart.md) voor
validatiescenario's en demo-accounts.

## Tests

```bash
.venv/bin/pytest
```

## Extensions

Voer dit uit vanuit de root van je Spec Kit-repository:

bash
specify extension add git

Controleer daarna dat hij actief is:

bash
specify extension list

Je zou daar de git-extension als geïnstalleerd en enabled moeten zien. De extensie registreert vervolgens de bijbehorende agent-commands en hooks in je projectconfiguratie.
