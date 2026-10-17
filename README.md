# Crash Guard Django Camera Panel

A small Django web dashboard for the configured-camera YOLO detection panel. This project contains only the web runtime, required detection and notification services, one YOLO model, and the configured sample video. It does not contain the old desktop GUI, training notebooks, presentation files, duplicate weights, local virtual environment, or Firebase credentials.

## Run locally on Windows

From this directory in PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py check
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Keep the terminal running. Press Ctrl+C to stop the server.

Edit `.env` locally. `FIREBASE_SERVICE_ACCOUNT_JSON` must be the full Firebase service-account JSON; put it on one line wrapped in single quotes or use a quoted multiline value. Never commit `.env` or share the key. Configure Cloudinary values to enable incident video uploads. AMD verification is disabled by default.

## Deploy to Render

Create a Python Web Service from this folder/repository root:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 3600 crashguard_site.wsgi:application`

Set `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY` to a generated random value, and `DJANGO_ALLOWED_HOSTS` to the Render service hostname. Add `FIREBASE_SERVICE_ACCOUNT_JSON` and the Cloudinary credentials in the Render environment settings. Do not commit secrets.

The detector state is in process memory and the service should run one application worker. The YOLO model and sample camera video are included in this project. Video processing, memory use, and provider pricing depend on the host's CPU/RAM plan.

## Deploy to Vercel

Vercel uses Python 3.12 as selected by `.python-version`. `pyproject.toml` pins `torch` and `torchvision` to the PyTorch CPU wheel index and resolves other packages from PyPI. Configure the Django and cloud-service environment variables in Vercel before deploying.

## Deploy as a container

The included Dockerfile builds a CPU-only Django/YOLO container. The service must provide `PORT`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and any required cloud credentials. Do not add `.env` or Firebase keys to the Docker image.

This dashboard has no user authentication. Do not expose it to the public internet without adding an access-control layer.
