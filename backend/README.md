# SuaEscola \U0001F3EB

![Python](https://img.shields.io/badge/python-3.11+-blue) ![Flask](https://img.shields.io/badge/flask-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green)

A minimal MVP for school management: student and guardian CRUD with interactive API docs (Swagger) \U0001F4DA

## Table of contents \U0001F4C2

## Table of contents 📂

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Install \& Run](#install--run)
- [Formatting \& Linting](#formatting--linting)
- [API / Swagger](#api--swagger)
- [Endpoint Examples](#endpoint-examples)
- [Contributing](#contributing)
- [License](#license)

\U0001F4CB

A lightweight API showcasing student and guardian management, automatic OpenAPI/Swagger docs, and simple best-practice tooling.

## Features 

- Create, read, update and delete Students and add new Guardians  
- Associate students with guardians   
- Interactive API docs via Swagger UI   
- Code formatting with Black and linting with Ruff 

## Requirements 

- Windows 10/11  
- Python 3.11+  
- `venv` or any virtual environment manager

## Install & Run 

1. Create and activate a virtual environment (PowerShell):
   - `python -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`

2. Install dependencies:
   - `pip install -r requirements.txt`

3. Environment variables (example):
   - `set FLASK_APP=app.py`
   - `set FLASK_ENV=development`

4. Run the app:
   - `flask run --host 0.0.0.0 --port 5000 --reload`

5. Open in browser:
   - `http://localhost:5000/` — root redirects to the Swagger UI (e.g. `http://localhost:5000/swagger`) 

## Formatting & Linting

Keep code consistent with Black and Ruff.

- Install tools:
  - `pip install black ruff`

- Check and fix:
  - Check with Ruff: `ruff check .`  
  - Auto-fix with Ruff: `ruff check . --fix`  
  - Format with Black: `black .`

Tip: add `pre-commit` hooks to automate checks before commits 

## API / Swagger 

Swagger (OpenAPI) provides interactive documentation and testing. The root route (`/`) redirects to the Swagger UI for quick exploration. Look for the "Student" and "Guardian" sections to view schemas and try endpoints.

## Endpoint Examples 

- Get / search student (query params):
  - GET `/student?id=1`  
- Delete student (query params, same as GET):
  - DELETE `/student?id=1`

Curl examples:
- Get:
  - `curl "http://localhost:5000/student?id=1"`
- Delete:
  - `curl -X DELETE "http://localhost:5000/student?id=1"`

## Contributing 

1. Open an issue describing the improvement.  
2. Create a descriptive branch and make small commits.  
3. Send a Pull Request with clear description.

## License 

This project is licensed under the MIT License. See the `LICENSE` file for details. 