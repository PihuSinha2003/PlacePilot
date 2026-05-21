# PlacePilot

> *PlacePilot — Campus Career Hub : Django Campus Job Portal with Smart Matching & Placement Dashboard*

Your co-pilot for campus placements. Students discover internships and jobs, save opportunities, track applications, and get personalized recommendations. Placement cells post openings, notices, and interview schedules from a dedicated admin panel.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![DRF](https://img.shields.io/badge/DRF-API-red)

---

## Why this project

Campus placements are still messy — job posts land in WhatsApp groups, emails, and notice boards, and students have no single place to track what they've applied to or what's closing soon.

PlacePilot brings that into one portal. Students can find roles matched to their skills and batch, save openings for later, and follow deadlines from a personal dashboard. Placement cells get a lightweight admin panel to publish jobs, notices, and interview schedules without juggling spreadsheets.

It is built around a real campus workflow, not a tutorial clone — practical enough to use during placement season, and strong enough to show Django, authentication, CRUD, filtering, file uploads, and a REST API in one cohesive product.

---

## Features

### For students
- Sign up, login, and build a profile with skills, branch, batch year, and resume upload
- Browse and search jobs/internships with filters (role, location, batch year, type, experience)
- Apply to roles or save them for later
- Dashboard with applied/saved/shortlisted counts and deadline reminders
- Personalized job recommendations based on skills, batch, and experience

### For placement admins
- Post and manage job/internship openings
- Publish campus notices (with pin support)
- Schedule interviews with date, time, and venue

### API
- `GET /api/jobs/` — paginated job list with search and filters
- `GET /api/jobs/<id>/` — single job detail

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5, Django REST Framework |
| Database | SQLite (default), PostgreSQL-ready |
| Frontend | HTML, Bootstrap 5, minimal JavaScript |
| Filters | django-filter |
| Auth | Django built-in authentication |

---

## Project structure

```
PlacePilot/
├── accounts/          # Signup, login, student profiles
├── jobs/              # Listings, apply, save, dashboard, admin jobs
├── notices/           # Announcements and interview schedules
├── api/               # REST endpoints for job listings
├── templates/         # Bootstrap UI templates
├── static/            # CSS and JS
└── campus_career_hub/ # Django project settings and URLs
```

---

## Getting started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
# Clone or download the project, then:
cd PlacePilot

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

# Environment config
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux

python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Demo accounts

| Role | Username | Password |
|------|----------|----------|
| Student | `student` | `student123` |
| Placement Admin | `placement` | `placement123` |

Create a superuser for Django admin:

```bash
python manage.py createsuperuser
```

Django admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## API usage

List jobs with filters:

```
GET /api/jobs/?role=developer&location=bangalore&batch_year=2026&search=python
```

Get a single job:

```
GET /api/jobs/1/
```

Response is JSON with pagination on list endpoints.

---

## PostgreSQL (optional)

Update `campus_career_hub/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'placepilot',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run `python manage.py migrate`.

---

## Resume bullet points

Copy-paste ready for your resume or LinkedIn:

- Built **PlacePilot**, a Django campus job portal with role-based dashboards for students and placement cells
- Implemented job search, multi-filter listings, apply/save workflows, and a skill-based recommendation engine
- Designed REST API with Django REST Framework for programmatic job listing retrieval
- Added placement admin panel for posting opportunities, notices, and interview schedules

---
