# Schritt-für-Schritt-Anleitung

> 📸 = hier Screenshot für die PDF machen

## 1. GitHub-Account & Repository
1. Auf https://github.com registrieren (falls noch nicht geschehen).
2. **New repository** → Name z. B. `SWE3IL_CICD` → **Public** → *ohne* README/.gitignore anlegen → **Create repository**.

## 2. Code hochladen
Im Ordner `SWE3IL_CICD` (PowerShell):
```bash
git init -b main
git add .
git commit -m "Initial commit: Flask app + CI/CD pipeline"
git remote add origin https://github.com/MarkusErtl7/SWE3IL_CICD.git
git push -u origin main
```
Beim Push öffnet sich ein Browser-Login (Git Credential Manager). Die erste Pipeline wartet jetzt auf einen Runner („Waiting for a runner…“) – das ist korrekt.

## 3. Self-hosted Runner einrichten (Windows)
1. Im Repo: **Settings → Actions → Runners → New self-hosted runner** → **Windows / x64** wählen. 📸
2. Die dort angezeigten Befehle in **PowerShell** ausführen (nicht als Admin nötig), z. B. in `C:\actions-runner`:
   ```powershell
   mkdir C:\actions-runner; cd C:\actions-runner
   # Download + Extract: Befehle 1:1 von der GitHub-Seite kopieren (Version/Hash ändern sich)
   ./config.cmd --url https://github.com/MarkusErtl7/SWE3IL_CICD --token <TOKEN-VON-DER-SEITE>
   ```
   Bei den Fragen einfach Enter drücken (Default-Gruppe, Name = PC-Name, Labels Default).
   Bei *„Would you like to run the runner as service?“* → **N** (siehe Herausforderungen).
3. Runner starten:
   ```powershell
   ./run.cmd
   ```
   Ausgabe: `√ Connected to GitHub` / `Listening for Jobs`. 📸
4. In GitHub unter Settings → Actions → Runners steht der Runner jetzt als **Idle** (grün). 📸

## 4. Voraussetzungen auf dem Rechner
- **Python 3.11** im PATH (`python --version`)
- **Docker Desktop** gestartet (Linux-Container) – `docker version` muss Client *und* Server zeigen.

## 5. Pipeline ausführen
- Entweder neu pushen, oder im Repo **Actions → CI/CD Pipeline → Run workflow**.
- Im Runner-Fenster erscheint `Running job: Build & Test (CI)` … `Job ... completed with result: Succeeded`. 📸
- In GitHub Actions: beide Jobs grün ✅. 📸 (Job-Log öffnen → Schritt „Show runner info“ zeigt deinen PC-Namen) 📸
- Deploy prüfen: http://localhost:5000 im Browser öffnen bzw. `docker ps` zeigt `cicd-demo-app`. 📸

## 6. Abgabe
- Link: `https://github.com/MarkusErtl7/SWE3IL_CICD`
- PDF: `DOKUMENTATION.md` mit Screenshots ergänzen und als PDF exportieren.

## Typische Probleme
| Problem | Lösung |
|---|---|
| Job hängt bei „Waiting for a runner“ | `run.cmd` läuft nicht oder Runner im falschen Repo registriert |
| `python` nicht gefunden | Python-Installation mit „Add to PATH“; Runner neu starten |
| `docker: failed to connect ... dockerDesktopLinuxEngine` | Docker Desktop starten |
| Docker-Zugriff verweigert, wenn Runner als Dienst läuft | Dienst läuft als `NETWORK SERVICE` ohne Docker-Rechte → Runner per `run.cmd` als eigener User starten |
| Port 5000 belegt | Anderen Port in `ci-cd.yml` (`-p 5001:5000`) verwenden |
