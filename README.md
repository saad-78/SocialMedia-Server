# SocialBooster Demo (Django + Neon + DRF)

A demo full-stack web app built for a Full Stack Developer assignment: Django + PostgreSQL (Neon) with REST CRUD APIs, a third‑party API integration (HN Algolia), and a simple reporting + Chart.js dashboard. [web:109]

## Features

- REST CRUD APIs (DRF):
  - `Keyword`: tracked search terms.
  - `Mention`: stored results (manual or fetched).
- Third‑party integration:
  - Sync mentions from Hacker News Algolia Search API via a dedicated endpoint. [web:109]
- Reporting + visualization:
  - Aggregated “mentions per day” report endpoint backed by the database.
  - `/dashboard/` page showing a Chart.js line chart.

## Tech stack

- Python + Django
- Django REST Framework (DRF)
- PostgreSQL on Neon
- Chart.js (frontend chart)
- `requests` (HN Algolia integration)

## Setup (local)

### Prerequisites
- Python 3.12+
- Git
- A Neon Postgres database (or any Postgres)

### 1) Clone and install
git clone <YOUR_GITHUB_REPO_URL>
cd socialbooster-demo

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt


### 2) Configure environment variables
Create a `.env` file in the project root:

touch .env
nano .env


Example `.env`:

Django
DEBUG=1
SECRET_KEY=dev-only-change-me
ALLOWED_HOSTS=127.0.0.1,localhost

Postgres (Neon)
Use your Neon connection string here.
For migrations, Neon recommends using a direct (non-pooled) connection string.​
DATABASE_URL="postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require"


Optional (recommended best practice with Neon):
- Use **direct** connection string for migrations and **pooled** for runtime; pooled hosts usually contain `-pooler`. [web:86]

### 3) Run migrations
python manage.py makemigrations
python manage.py migrate


### 4) Run the server
python manage.py runserver


App URLs:
- API root: http://127.0.0.1:8000/api/
- Dashboard: http://127.0.0.1:8000/dashboard/
- Admin: http://127.0.0.1:8000/admin/

## API endpoints

### CRUD
- `GET /api/keywords/`
- `POST /api/keywords/`
- `GET /api/keywords/{id}/`
- `PATCH /api/keywords/{id}/`
- `DELETE /api/keywords/{id}/`

- `GET /api/mentions/`
- `POST /api/mentions/`
- `GET /api/mentions/{id}/`
- `PATCH /api/mentions/{id}/`
- `DELETE /api/mentions/{id}/`

### HN Algolia sync
Sync mentions for a keyword from the HN Algolia Search API using `search_by_date` + `tags=story`. [web:109]

- `POST /api/keywords/{id}/sync_hn/?hitsPerPage=20&page=0`

### Reporting
- `GET /api/reports/mentions_daily/?keyword_id={id}&days=30`
- Optional: `&source=hn_algolia`

## Quick demo (curl)

### 1) Create a keyword
curl -X POST http://127.0.0.1:8000/api/keywords/
-H "Content-Type: application/json"
-d '{"term":"django"}'


### 2) Sync mentions from HN Algolia
curl -X POST "http://127.0.0.1:8000/api/keywords/1/sync_hn/?hitsPerPage=20&page=0"


### 3) List mentions
curl http://127.0.0.1:8000/api/mentions/


### 4) Get daily report data
curl "http://127.0.0.1:8000/api/reports/mentions_daily/?keyword_id=1&days=365"


## Deployment notes

This project is deployable to any Django-friendly platform (Render/Railway/Fly.io/etc.).
Minimum required environment variables in production:
- `SECRET_KEY`
- `DEBUG=0`
- `ALLOWED_HOSTS=<your-domain>`
- `DATABASE_URL=<neon postgres url>`

Run migrations during deployment:
python manage.py migrate


Neon note: use a direct connection string for migrations if you run into pooling-related migration issues. [web:6][web:86]

## License
MIT (or replace with your preferred license)