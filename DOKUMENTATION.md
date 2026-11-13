# CI/CD Pipeline with a GitHub Self-Hosted Runner

**Name:** <your name> · **Date:** <date>
**Repository:** https://github.com/MarkusErtl7/SWE3IL_CICD

## 1. Goal
Recreate the CI/CD pipeline from the lecture with GitHub Actions. All jobs run on a
self-hosted runner on my own Windows 11 machine instead of on GitHub-hosted runners.

## 2. Project overview
- **Application:** small Python/Flask web service (`/`, `/health`, `/add/<a>/<b>`)
- **Tests:** pytest (4 unit tests), linting with flake8
- **Container:** Dockerfile based on `python:3.11-slim`
- **Pipeline:** `.github/workflows/ci-cd.yml`, triggered on push/PR to `main` and manually

| Stage | Job | Steps |
|---|---|---|
| CI | Build & Test | checkout → create venv & install deps → flake8 → pytest |
| CD | Docker Build & Deploy | build image (tagged with commit SHA + `latest`) → remove old container → start new container on port 5000 → smoke test `/health` |

The deploy job depends on the CI job (`needs: build-and-test`) and only runs if all tests pass. Both jobs use `runs-on: self-hosted`.

## 3. Steps
1. Created a GitHub account and a public repository `SWE3IL_CICD`.
2. Wrote the Flask app, tests, Dockerfile and workflow file and pushed them to `main`.
3. Registered a self-hosted runner: *Settings → Actions → Runners → New self-hosted runner* (Windows x64), downloaded the runner package, ran `config.cmd` with the registration token and started it with `run.cmd`.
   The runner is started from PowerShell with `cd C:\Users\Ertlz\actions-runner` and `.\run.cmd`.
   It connects to GitHub and waits for jobs. In the repository under *Settings → Actions → Runners*
   the runner `ADMIN` (labels `self-hosted`, `Windows`, `X64`) is listed with status **Idle**.

   ![Runner ADMIN with status Idle in GitHub and the PowerShell window running run.cmd](docs/screenshots/01-runner-idle-and-run-cmd.png)
   *Figure 1: Self-hosted runner registered in GitHub (Idle) and started locally with `run.cmd` ("Connected to GitHub", "Listening for Jobs").*
4. Started Docker Desktop and verified Python is on the PATH.
5. Triggered the pipeline (push / *Run workflow*).
   As soon as a job is picked up, the runner page in GitHub shows it as *Active Job* on `ADMIN`
   (status *In progress*), i.e. the job is executed on my local machine.

   ![Runner ADMIN in GitHub with active job "CI/CD Pipeline / Build & Test (CI)" in progress](docs/screenshots/05-runner-active-job.png)
   *Figure 2: Runner `ADMIN` (Windows x64, labels `self-hosted`, `Windows`, `X64`) currently executing the CI job.*

   The successful runs are listed in the Actions tab (see Figure 6).
   > 📸 Screenshot: job log step "Show runner info" with my computer name
6. Verified the deployment: `docker ps` shows `cicd-demo-app`, http://localhost:5000 returns the JSON response.
   > 📸 Screenshot: browser / `docker ps`

7. Tested the failure case: to check that the pipeline really stops broken code, I changed
   `test_add` in `tests/test_main.py` on purpose so that it expects a wrong result
   (`assert add(2, 3) == 6` instead of `== 5`) and pushed the change.

   ![test_main.py with the intentionally wrong assertion add(2, 3) == 6](docs/screenshots/02-failing-test.png)
   *Figure 3: Intentionally broken unit test in `tests/test_main.py` (line 5).*

   Result: the *Run tests (pytest)* step failed, the CI job turned red and the
   *Docker Build & Deploy* job was skipped because of `needs: build-and-test`. The previously
   deployed container kept running unchanged.

   The runner output on my machine shows both cases: the run for the previous, correct commit
   succeeded, the run for the broken commit failed. The deploy job at the end belongs to the earlier,
   correct run: a single self-hosted runner executes only one job at a time, so that deploy job
   waited in the queue until the CI job of the broken commit had finished.

   ![Runner terminal: Build & Test succeeded, then Build & Test failed, then Docker Build & Deploy](docs/screenshots/03-runner-succeeded-and-failed.png)
   *Figure 4: Local runner output – CI succeeded for the correct commit and failed for the broken one.*

   GitHub also sent an e-mail notification about the failed run: *Build & Test (CI)* failed,
   *Docker Build & Deploy (CD)* was skipped.

   ![GitHub e-mail: CI/CD Pipeline – Some jobs were not successful; Build & Test failed, Deploy skipped](docs/screenshots/04-failure-email.png)
   *Figure 5: E-mail notification from GitHub – the broken code was stopped before deployment.*

   Afterwards the test was reverted to `== 5` (commit *good Test*) and pushed. The Actions overview
   shows the result: run #4 (*break test*) failed, run #5 (*good Test*) succeeded, so the latest
   run on `main` is a successful CI/CD run.

   ![GitHub Actions overview: run #5 "good Test" succeeded, run #4 "break test" failed](docs/screenshots/06-actions-runs-overview.png)
   *Figure 6: Actions overview – the broken commit was stopped (#4), the fixed commit passed the whole pipeline (#5).*

## 4. Challenges and solutions
*(keep the ones that actually happened, add your own)*
- **First run failed at the first PowerShell step ("Process completed with exit code 1")** – the runner writes every `run:` step to a temporary `.ps1` file and runs it. Windows' default ExecutionPolicy (*Restricted*) blocks `.ps1` scripts, so the first run failed while the Node-based checkout step still worked. Fix: a custom shell in the workflow, `powershell -NoProfile -ExecutionPolicy Bypass -Command ". '{0}'"`, which only applies to the pipeline process and does not change the system-wide policy. The second run succeeded.
- **Job stuck on "Waiting for a runner"** – the runner was not running yet; starting `run.cmd` picked up the queued job.
- **Shell differences on Windows** – GitHub's examples use bash; on a Windows runner steps run in PowerShell, so the commands were written for PowerShell (`shell: powershell`, `.\.venv\Scripts\...`).
- **Docker daemon not reachable** – the deploy job failed with `failed to connect to the docker API` until Docker Desktop was started.
- **Runner as Windows service** – a service runs as `NETWORK SERVICE` and has no access to Docker Desktop, so the runner is started interactively with `run.cmd` under my user.
- **Replacing the running container** – a second deploy fails if a container with the same name already exists, so the pipeline removes the old container first.
- **Security** – self-hosted runners should only be used with private repos or trusted code, since a pull request from a fork could run code on my machine. The deploy job is therefore skipped for pull requests.

## 5. Result
The repository contains a successful pipeline run where both CI and CD jobs ran on my local machine (see screenshots).
