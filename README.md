# Instagram Bot (Python + FastAPI)

Proyecto base para un bot de Instagram
## Requisitos
- Python 3.11+
- Git
- (Opcional) Make / PowerShell

## Setup rápido
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
  # tests unitarios y de integración
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

> Consejos: commits chicos con mensajes claros (Conventional Commits), correr linters y tests antes del commit para feedback rápido.

## Workflow (resumen)
1. Crear rama de feature: `git checkout -b feature/<nombre>`  
2. Codear en bloques chicos + correr `pre-commit`/tests local.  
3. `git add` → `git commit -m "feat(scope): ..."`  
4. `git push -u origin feature/<nombre>` y abrir PR hacia `main`.  
5. Revisar PR (lint/tests) y mergear cuando esté verde.  
6. Mantener `README`/docs actualizados si cambia algo relevante.

## GitHub remoto (sincronización)
```bash
git branch -M main
git remote add origin https://github.com/<tu-usuario>/instagram-bot.git
git push -u origin main
```

## Normalizar finales de línea (opcional recomendable)
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

## Próximos pasos sugeridos
- Agregar endpoints `/webhook` y verificación de firma HMAC (raw body + HMAC-SHA256).
- Tests unitarios del verificador de firma.
- Estado en Redis (idempotencia) y cola (Celery/RQ) para tareas diferidas.
- Métricas (`/metrics`) y logs estructurados.
- CI (GitHub Actions) cuando lo subas a GitHub.

---

© 2025
