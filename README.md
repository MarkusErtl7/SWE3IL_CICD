# SWE3IL_CICD – GitHub Actions mit Self-Hosted Runner

Kleine Flask-App mit einer CI/CD-Pipeline, die auf einem **self-hosted Runner** (eigener Windows-PC) läuft.

## Pipeline
1. **CI – Build & Test**: Checkout → venv + Dependencies → Lint (flake8) → Tests (pytest)
2. **CD – Deploy**: Docker-Image bauen → alten Container stoppen → neuen Container starten → Smoke-Test auf `/health`

Trigger: Push / Pull Request auf `main` sowie manuell (`workflow_dispatch`).

## Lokal starten
```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements-dev.txt
.venv\Scripts\pytest -v
.venv\Scripts\python -m app.main
```
Nach erfolgreichem Deploy erreichbar unter http://localhost:5000
