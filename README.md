# Planora — Professional Project Workspace

Planora is a full-stack project and task management app with a polished monochrome interface: a deep-black navigation rail, white workspace, restrained grey borders, subtle shadows, responsive layouts, hover feedback, and page transitions. It is built with React + TypeScript + Vite and Django REST Framework + SQLite.

## Included pages and features

- **Authentication:** account registration, JWT sign-in, sign-out, and per-user workspace data.
- **Overview:** KPI cards, project progress, focus summary, and recent tasks.
- **Projects:** project cards, due dates, progress indicators, create and delete actions.
- **My Tasks:** searchable task list with status filtering and task creation/deletion.
- **Board:** Kanban-style status columns with status updates.
- **Calendar:** upcoming task deadlines.
- **Team:** workspace members and their task/project context.
- **Reports:** completion metrics, status distribution, project progress, CSV export.
- **Activity:** recent project/task events.
- **Settings:** profile summary, workspace preferences, and sign-out.
- **Usability:** responsive mobile navigation, useful empty states, error messages, toast feedback, modal forms, and reduced-motion support.

Newly registered accounts receive a small, editable starter workspace with sample projects and tasks. This is real data stored in the local SQLite database, not hard-coded demo cards; users can update or delete it.

## Requirements

- Windows 10/11
- Python 3.10 or newer (Python 3.11 is a safe choice)
- Node.js 20 or newer and npm
- Internet access on first setup to download dependencies

## Run in VS Code on Windows

### 1. Open the project

In VS Code, choose **File → Open Folder** and select the extracted `Planora-Black-White-FullStack` folder.

### 2. Start the backend

Open **Terminal → New Terminal** and run:

```powershell
cd backend
.\start-backend.ps1
```

The script creates a clean `.planora-venv` environment (separate from any old `.venv`), installs the pinned dependencies, applies database migrations, and starts Django. Keep this terminal open.

If PowerShell blocks the script, run this once in the same terminal and retry the script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start-backend.ps1
```

Backend API: `http://127.0.0.1:8000/api/`

### 3. Start the frontend

Open a **second terminal** in VS Code:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL Vite prints, normally `http://localhost:5173/`.

You can also double-click `frontend/start-frontend.cmd` to install and start the frontend on Windows.

### 4. Create your account

On the Planora sign-in screen, choose **Create one**, register with a username, email, and password (at least 8 characters), then sign in. A starter workspace is created for the new account. Use your own credentials; there is no shared default password.

## API overview

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET/POST /api/projects/`
- `GET/POST /api/tasks/`
- `GET /api/dashboard/`
- `GET /api/team/`
- `GET /api/activity/`

Project and task detail routes support the standard Django REST Framework update and delete methods. JWT authentication is required for workspace data.

## Troubleshooting

- **Do not reuse a broken or locked virtual environment.** The backend script uses `.planora-venv`, so it does not need the old `.venv` or `.venv_new` folders.
- If the first `pip install` fails, read the final error line and confirm internet access. Retry the script after the network is restored. If Windows reports a file is in use, close other terminals running Python for this project and restart VS Code before retrying.
- If `npm install` fails, confirm Node.js/npm are installed with `node -v` and `npm -v`, then retry after internet access is available.
- Keep the backend terminal running while using the frontend.
- If port `8000` or `5173` is already in use, stop the other development server or adjust its port.

## Notes

This is a local development project, not a production deployment. Before public deployment, replace the development secret key, set `DEBUG = False`, configure allowed hosts and HTTPS, and review authentication, rate limits, backups, and privacy requirements.
