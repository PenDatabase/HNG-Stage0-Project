# HNG Stage 0 FastAPI Service

A simple FastAPI application for the HNG Stage 0 task. It exposes a `/me` endpoint that returns basic profile details along with a cat fact fetched from a third-party API. Requests are rate limited using SlowAPI, and the project is ready for deployment on Railway.

## Features
- FastAPI + Uvicorn ASGI stack
- Global CORS support for easy consumption
- `/me` endpoint with profile info and UTC timestamp
- Cat fact fetched from https://catfact.ninja/fact
- Rate limiting at 5 requests per minute per client via SlowAPI

## Requirements
- Python 3.10+
- Pip (or pipenv/poetry if you prefer)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/PenDatabase/HNG-Stage0-Project.git
cd HNG-Stage0-Project
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server locally
```bash
uvicorn main:app --reload
```

Visit http://127.0.0.1:8000/me to test the endpoint. Each response includes your profile data, a timestamp, and a cat fact. If the third-party service is unavailable, a friendly fallback message is returned instead.

## Deployment on Railway
The repository includes everything required to deploy on Railway:

- `Procfile` defines the start command for the web process: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- `railway.json` configures the Nixpacks builder, the start command, and an `/me` health check.

### Deploy via Railway CLI
```bash
railway login
railway link
railway up
```

### Deploy via Railway Dashboard
1. Create a new Railway project and connect this GitHub repo.
2. Railway auto-detects the Python environment through Nixpacks.
3. Deploy the `main` branch. Railway uses the `Procfile` start command and performs health checks on `/me`.

## Testing Rate Limits
Requests are limited to 5 per minute per client IP. Exceeding the limit returns HTTP 429 with a helpful message. Use a tool like `curl` or Postman to test:
```bash
curl http://127.0.0.1:8000/me
```

## Project Structure
```
main.py           # FastAPI application
requirements.txt # Python dependencies
Procfile          # Railway process definition
railway.json      # Railway build/deploy configuration
README.md         # Project documentation
```

## Contributing
1. Fork the repo and create a feature branch.
2. Make your changes and add tests if applicable.
3. Run the server to ensure everything works.
4. Submit a pull request describing your changes.

## License
This project is released under the MIT License. Feel free to use it as a reference or base for your own HNG tasks.
