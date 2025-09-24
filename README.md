# Instagram Bot (Python + FastAPI)

Proyecto base para un bot de Instagram
## Requisitos
- Python 3.11+
- Git
- (Opcional) Make / PowerShell

## Setup r√°pido
```bash
# crear y activar entorno
python -m venv .venv
# Windows (CMD/Powershell)
.venv\Scripts\activate
# instalar deps y herramientas de desarrollo (definidas en pyproject.toml)
pip install -e .[dev]
# instalar hooks de pre-commit
pre-commit install
# correr chequeos a mano (opcional)
pre-commit run --all-files -v
```

## ConfiguraciÛn 12-factor
Este proyecto sigue el principio 12-factor: toda la configuraciÛn proviene de variables de entorno. El loader en `app/core/config.py` primero lee `.env` (si existe), y despuÈs `.env.<entorno>` (`.env.dev`, `.env.staging`, etc.) sobreescribiendo lo que corresponda.

### Entornos soportados
- `default`: entorno base/local (valor por defecto cuando no hay variable definida).
- `dev`: desarrollo con `DEBUG` encendido.
- `staging`: pre-producciÛn, mismo cÛdigo que prod pero con recursos aislados.
- `prod`: producciÛn. Us· este valor para instancias p˙blicas.

DefinÌ el entorno exportando `IG_ENVIRONMENT`, `IG_ENV`, `APP_ENV` o `ENVIRONMENT`. Ejemplo en PowerShell:
```powershell
$Env:IG_ENVIRONMENT = 'dev'
uvicorn app.main:api --reload --port 8000
```

### Variables disponibles (prefijo `IG_` opcional)
- `IG_APP_NAME` / `APP_NAME` (`instagram-bot`)
- `IG_API_PREFIX` / `API_PREFIX` (`/`)
- `IG_DEBUG` / `DEBUG` (`false` por defecto, pero se habilita si el entorno es `default` o `dev`)
- `IG_LOG_LEVEL` / `LOG_LEVEL` (`INFO`)
- `IG_DATABASE_URL` / `DATABASE_URL`
- `IG_REDIS_URL` / `REDIS_URL`
- `IG_INSTAGRAM_APP_ID` / `INSTAGRAM_APP_ID`
- `IG_INSTAGRAM_APP_SECRET` / `INSTAGRAM_APP_SECRET`
- `IG_WEBHOOK_VERIFY_TOKEN` / `WEBHOOK_VERIFY_TOKEN`
- `IG_DOCS_URL` / `DOCS_URL` (`/docs`)
- `IG_REDOC_URL` / `REDOC_URL` (`/redoc`)
- `IG_OPENAPI_URL` / `OPENAPI_URL` (`/openapi.json`)

PodÈs extender la configuraciÛn agregando campos en `AppSettings`. Para leerla en cualquier mÛdulo:
```python
from app.core.config import get_settings

settings = get_settings()
print(settings.environment)
```
## Ejecutar en desarrollo
```bash
uvicorn app.main:api --reload --port 8000
# healthcheck
curl http://localhost:8000/ping
```

## Estructura del repo
```
app/
  main.py                # FastAPI app (punto de entrada)
  # (luego) server/webhook.py, server/middleware.py, core/, adapters/, etc.
tests/
  # tests unitarios y de integraci√≥n
.pre-commit-config.yaml  # hooks de calidad (ruff/black)
pyproject.toml           # deps y config (ruff/black/mypy/pytest)
.gitignore               # ignora venv, caches y builds
```

## Calidad y pruebas
```bash
# lint y formato
ruff check .
black --check .
# tipos
mypy app
# tests
pytest -q
```

> Consejos: commits chicos con mensajes claros (Conventional Commits), correr linters y tests antes del commit para feedback r√°pido.

## Workflow (resumen)
1. Crear rama de feature: `git checkout -b feature/<nombre>`  
2. Codear en bloques chicos + correr `pre-commit`/tests local.  
3. `git add` ‚Üí `git commit -m "feat(scope): ..."`  
4. `git push -u origin feature/<nombre>` y abrir PR hacia `main`.  
5. Revisar PR (lint/tests) y mergear cuando est√© verde.  
6. Mantener `README`/docs actualizados si cambia algo relevante.

## GitHub remoto (sincronizaci√≥n)
```bash
git branch -M main
git remote add origin https://github.com/<tu-usuario>/instagram-bot.git
git push -u origin main
```

## Normalizar finales de l√≠nea (opcional recomendable)
Crear `.gitattributes` con:
```
* text=auto eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
*.sh  text eol=lf
*.png binary
*.jpg binary
*.pdf binary
*.zip binary
```
Luego:
```bash
git add .gitattributes
git commit -m "chore: normalize EOL and mark binaries"
```

## Pr√≥ximos pasos sugeridos
- Agregar endpoints `/webhook` y verificaci√≥n de firma HMAC (raw body + HMAC-SHA256).
- Tests unitarios del verificador de firma.
- Estado en Redis (idempotencia) y cola (Celery/RQ) para tareas diferidas.
- M√©tricas (`/metrics`) y logs estructurados.
- CI (GitHub Actions) cuando lo subas a GitHub.

---

¬© 2025

