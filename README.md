# Playwright Python E-commerce Project 

This repository starts with Day 1 only: a UI catalogue smoke test and a product API smoke test against the same Toolshop practice application. Build the later layers yourself with the workbook, then review and debug each change before committing it.

Start with [the five-day workbook](docs/five_day_workbook.md) and [today's guided task](docs/day_01.md).

## Install on macOS or Linux

Use Python 3.11 or newer for this project's type hints. Open this folder itself in VS Code, rather than its parent.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
```

In VS Code, install the recommended Python and Python Debugger extensions. Run **Python: Select Interpreter** and select `.venv/bin/python`. The Python extension discovers pytest tests in the Testing panel. The Microsoft Playwright Test extension's Node test-runner workflow is not needed for this Python suite.

Windows PowerShell: use `py -m venv .venv`, activate with `.venv\Scripts\Activate.ps1`, and select `.venv\Scripts\python.exe` in VS Code. The remaining `python -m ...` commands are the same; copy `.env.example` using `Copy-Item .env.example .env`.

## Run

```bash
python -m pytest tests/api -v
python -m pytest tests/ui -v --headed
python -m pytest -m smoke -v
```

No login, real payment or account creation occurs on Day 1. API-only tests use a standalone request context and do not launch Chromium.

If your network needs an explicit HTTP proxy, put its server URL in `PW_PROXY_SERVER` in your local `.env`. Leave it empty on a normal direct connection. Both UI contexts and standalone API contexts use this optional setting.

## Debug and trace

Put a VS Code breakpoint on the UI navigation line or the API `response.json()` line. Choose a Day 1 debug configuration and press F5. Inspect `response.status`, `body`, and `products` in the API debug session.

```bash
PWDEBUG=1 python -m pytest tests/ui/test_catalog_smoke.py -s
python -m pytest tests/ui --tracing on -v
python -m playwright show-trace <actual-path-to-trace.zip>
```

Replace the trace placeholder with the real file under `test-results/`. `--tracing on` keeps successful UI traces for learning; `retain-on-failure` is the normal configuration. The browser plugin flags do not automatically trace our separately created API request context. Learn API debugging through breakpoints now; add sanitized API logs and reports on Day 5.

## Dependencies

`requirements.in` lists the packages we intentionally chose. `requirements.txt` pins the resolved dependency versions used to validate this starter. Install the pins; update them deliberately in a clean virtual environment and rerun the suite when upgrading.

## Daily Git habit

For a **new, empty GitHub repository**:

```bash
git init -b main
git status --short
git add README.md requirements.in requirements.txt pytest.ini conftest.py config tests docs .env.example .gitignore .vscode
git diff --cached
git commit -m "Day 1: add Playwright Python UI and API smoke tests"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Replace the placeholders with your actual repository. GitHub authentication is through your Git credential manager or GitHub CLI, not a token inside the remote URL. If the repository already contains files, clone it first and add this starter on a new branch; do not initialize an unrelated repository and force-push over its history.

Check staged files before each commit. `.env`, authentication state, virtual environments, screenshots and traces are ignored. Keep the real handbook PDF outside this repo unless you intentionally want to include it.

## What comes next

- Day 2: extract a catalogue POM and parameterize search tests from JSON.
- Day 3: introduce API transport/domain clients, response models and negative tests.
- Day 4: use API-selected product data in a UI cart flow; practice isolation and traces.
- Day 5: add GitHub Actions, failure artifacts and a reviewed AI-assisted test workflow.

See `docs/validation.md` for what was actually checked in the preparation environment.
