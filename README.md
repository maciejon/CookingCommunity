# Project Overview

-----------------
CookingCommunity is a full-stack recipe-sharing platform demonstrating a production-like separation of concerns: a Svelte frontend, a Django REST backend, and a small Go microservice for image handling.

Roles & Responsibilities
------------------------
- Frontend: maciejon — implemented the Svelte + TypeScript UI, routing, components, and client-side integration with the API.
- Backend & Image Server: jaian400 — implemented the Django REST API and the Go-based image microservice for upload/serving.

Key Features
------------
- Browse and search recipes by category
- Create, edit and review recipes with step-by-step instructions
- Upload and serve recipe images via a dedicated Go microservice
- User registration and authentication
- Responsive UI built with Svelte

Tech Stack
----------
- Frontend: Svelte, TypeScript
- Backend: Python, Django, Django REST Framework, SQL
- Image service: Go

Architecture (overview)
-----------------------
User ↔ Frontend (Svelte) ↔ Backend API (Django REST) ↔ Image microservice (Go)

Run locally (development)
-------------------------
1. Backend (Django)

```bash
# create/activate venv, install requirements (if not present)
python3 -m venv .venv
source .venv/bin/activate
cd projekt/backend_bizon
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

2. Frontend (Svelte)

```bash
cd projekt/frontend_bizon
npm install
npm run dev
```

3. Image microservice (Go)

```bash
cd projekt/image_bizon
go run main.go
```

Notes
-----
- The project includes a development SQLite DB for convenience.

Contact / Attribution
---------------------
- Frontend (UI & client): maciejon
- Backend & Image service: jaian400

