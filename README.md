# conference-management-system
A web-based system for managing hotel bookings and conference facilities, designed to streamline the process for conference organizers and attendees.

## Continuous integration

CI runs on the Owner's Windows 11 machine through a self-hosted GitHub Actions runner
(labels: `self-hosted`, `Windows`, `X64`, `conference-management-system`). There are no
GitHub-hosted jobs. Because the repository is public, the workflow is limited to pushes to
`main` and manual `workflow_dispatch` runs: a self-hosted runner must never execute code
from untrusted pull requests.

The workflow `.github/workflows/ci.yml` installs `requirements.txt` into `.venv`,
byte-compiles the Python sources and runs `ci_smoke.py`, which loads the Flask app and
renders every route without a database. The project has no test suite and no linter yet,
so CI does not pretend to run them.

Run the same checks locally with PowerShell 7:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m compileall -q app.py ci_smoke.py init_db.py dummy_data.py conn_test.py new_staff.py
.\.venv\Scripts\python.exe ci_smoke.py
```

The PostgreSQL helper scripts read `PGHOST`, `PGDATABASE`, `PGUSER` and `PGPASSWORD` from
the environment; see `.env.example`. Never commit real credentials.
