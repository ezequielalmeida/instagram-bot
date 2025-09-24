# Contributing Guide

Este documento define las convenciones y el flujo de trabajo para contribuir al proyecto **Instagram Bot (FastAPI)**.  
La idea es mantener el repositorio claro, ordenado y fácil de mantener en el tiempo.

---

## Flujo de trabajo con ramas

- **main**  
  Rama estable. Contiene únicamente código listo para producción/deploy.

- **dev**  
  Rama de integración. Antes de llegar a `main`, todos los cambios deben pasar por acá.  

- **feature/***  
  Para nuevas funcionalidades. Ejemplo:  
  - `feature/webhook-verification`  
  - `feature/auto-responder`  

- **fix/***  
  Para corregir errores o bugs. Ejemplo:  
  - `fix/hmac-check`  
  - `fix/env-loader`  

- **chore/***  
  Para tareas de mantenimiento (dependencias, configs, CI/CD). Ejemplo:  
  - `chore/update-precommit`

---

## Convenciones de commits

Se utiliza el estándar **[Conventional Commits](https://www.conventionalcommits.org/)**.  
Formato:  

