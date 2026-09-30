# OT Metal Plus — Quote Management System

## Overview

OT Metal Plus is a Django application for creating, managing and exporting commercial quotes for a metal trading business. The project is centered on a quotation workflow: the user fills in client information, adds product lines, applies a discount, and generates a PDF document ready to be sent to a customer.

## Business context

The application was built to automate the quotation process in a practical way. Instead of composing documents manually in a spreadsheet or a text editor, the platform centralizes the information in a database and produces a professional quote document based on the same business rules every time.

## Functional scope

- Quote creation with client metadata
- Product line management and validation
- Automatic subtotal, discount and VAT calculations
- Quote total calculation with FCFA or percentage discount rules
- PDF generation using a predefined template
- Historical quote listing
- Quote duplicate and delete operations

## Technologies

- Python 3
- Django 5
- SQLite
- ReportLab
- PyPDF

## Project structure

```text
E:\OT APP
├── README.md
├── requirements.txt
├── manage.py
├── .env.example
├── .gitignore
├── templates/
│   └── Devis_OT_Metal_Plus_demo.pdf
├── otmetal/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── quotes/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       ├── views.py
│       ├── services/
│       │   ├── calculations.py
│       │   └── pdf_generator.py
│       └── static/
└── docs/
```

## Configuration and environment

Secrets are loaded from environment variables instead of hardcoded values in source files.

Create a local `.env` file from the example provided:

```powershell
Copy-Item .env.example .env
```

Example:

```env
DJANGO_SECRET_KEY=replace-with-local-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=
```

## Installation

```powershell
cd "E:\OT APP"
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Database

The project uses SQLite for local development. The migration history is kept in the Django migration system; it should be used to rebuild the schema in a clean environment.

## PDF generation

The PDF document is generated from the anonymized `templates/Devis_OT_Metal_Plus_demo.pdf` template and a payload composed of quote data, pricing values and client details. The original business document is excluded from this portfolio project and retained in the local backup. The document logic is implemented in the Quote service layer and assembled with ReportLab and PyPDF-based processing.

## Tests

```powershell
py manage.py test
```

## Security notes

- Secret keys are not committed to the repository.
- `DJANGO_SECRET_KEY` and `DEBUG` are loaded from the local `.env` file or process environment.
- A development-only placeholder is used only when `DEBUG=True`; the app refuses to start with `DEBUG=False` and no configured key.
- Set `DEBUG=False` and configure an explicit `ALLOWED_HOSTS` value outside local development.
- Local generated PDF or debug artifacts are kept outside the tracked project state when preparing the portfolio.

## Future improvements

- User authentication and authorization
- PostgreSQL adoption for production-ready deployment
- More robust client and quote lifecycle management
- Export and API integrations for external systems

## License

No license has been selected for this project.
