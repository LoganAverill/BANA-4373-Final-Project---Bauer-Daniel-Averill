# Dashboard — How to Run

This dashboard is the Deliverable B companion to the team's BANA 4373 final project on oil price shocks and Texas energy employment. It runs locally on Windows, macOS, and Linux. Requires **Python 3.10 or newer**.

## Quick start (recommended: use a virtual environment)

A virtual environment avoids dependency conflicts with anything else on the grader's machine. The whole sequence below takes under a minute.

> Replace `<FOLDER>` in the first command with the actual path to wherever you saved this folder on your computer (e.g., `C:\Users\YourName\Downloads\Deliverable_B_Submission` on Windows, or `~/Downloads/Deliverable_B_Submission` on Mac).

### macOS / Linux

```bash
cd <FOLDER>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Windows (PowerShell)

```powershell
cd <FOLDER>
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

If PowerShell blocks the activation script, run it once as administrator:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Windows (Command Prompt)

```cmd
cd <FOLDER>
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
```

After the last command runs, you should see `Dash is running on http://127.0.0.1:8050/`. Open that URL in any browser.

## Quick start without a virtual environment

If the grader prefers to skip the venv, the same install works system-wide. Use whichever Python invocation is on the machine:

| OS | Python | Pip |
|---|---|---|
| macOS / Linux (most setups) | `python3` | `python3 -m pip` |
| Windows (after installer) | `python` | `python -m pip` |

So on a Mac without a venv:

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

If you see `error: externally-managed-environment` (common on macOS with Homebrew Python and recent pip), either use the venv approach above, or add `--user`:

```bash
python3 -m pip install --user -r requirements.txt
```

## What the dashboard does

Three interactive controls:

- **County dropdown** — switch between "All Texas" (panel average across 202 counties) and the top energy-employment counties (Harris, Midland, Ector, etc.).
- **Sample split** — full window, pre-2020 only, or post-2020 only. Used to test whether the oil-employme