# Chatbot-Based Employee Management System

A Flask app that lets you create and manage employee records via a simple chatbot-style input and REST APIs. Employees are stored in MongoDB with sequential IDs like `EMP000001`.

**What it does**
- Chat endpoint that parses `Name, Department, Skill1/Skill2` and saves an employee.
- CRUD APIs for employees with pagination and search filters.
- Optional API key protection for write endpoints.
- MongoDB-backed sequential employee IDs and a migration script.

## Project Structure
- `app.py` Flask app and API routes.
- `chatbot.py` Chat flow that parses input and saves employees.
- `llm_parser.py` Input parser (comma-separated, flexible skill separators).
- `employee_service.py` Employee creation + logging.
- `database_mongo.py` MongoDB persistence + ID counter.
- `database_postgres.py` Legacy/optional Postgres insert helper (not used by Flask app).
- `migrate_employee_ids.py` Backfills sequential `employee_id` for existing Mongo docs.
- `templates/index.html` Basic UI for quick manual testing.

## Requirements
- Python 3.10+
- MongoDB running locally (default: `mongodb://localhost:27017/`)

Install dependencies:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Edit `config.py`:
- `MONGO_URI`: MongoDB connection string.
- `API_KEY`: If empty, auth is disabled. If set, clients must send `X-API-Key`.
- `POSTGRES_CONFIG`: Only used by `database_postgres.py` (not used by the Flask app).

## Run
```bash
python app.py
```
The app runs at `http://127.0.0.1:5000/`.

## API Usage
All JSON responses use snake_case fields:
```json
{
  "employee_id": "EMP000001",
  "name": "Rahul",
  "department": "IT",
  "skills": ["Python", "Flask"],
  "created_at": "2026-03-18T09:15:23.123456+00:00"
}
```

### Create via Chat
`POST /chat`
```json
{ "message": "Rahul, IT, Python/Flask" }
```

### Create via API
`POST /employees`
```json
{
  "name": "Asha",
  "department": "HR",
  "skills": ["Recruiting", "Onboarding"]
}
```

### List + Filter
`GET /employees?page=1&limit=20&name=rahul&department=it&skill=python`

Response:
```json
{
  "employees": [ ... ],
  "page": 1,
  "limit": 20,
  "total": 5
}
```

### Get One
`GET /employees/{employee_id}`

### Update
`PUT /employees/{employee_id}`
```json
{ "department": "Finance" }
```

### Delete
`DELETE /employees/{employee_id}`

## Notes
- `templates/index.html` is a minimal UI. It calls `/chat` but does not implement the “View All Employees” button yet.
- If `API_KEY` is set, send header `X-API-Key: <your-key>` for `POST/PUT/DELETE`.
- Skills can be split with `,` in the chat input, and within the third segment with `/`, `;`, or `|`.

## Migration Script
If you already have employee documents without `employee_id`, run:
```bash
python migrate_employee_ids.py
```
This assigns sequential IDs and updates the counter used for future inserts.
