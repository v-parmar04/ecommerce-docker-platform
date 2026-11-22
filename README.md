# ecommerce-docker-platform

A focused FastAPI e-commerce API used as the application for the Docker engineering journey.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Health check |
| GET | `/products` | List products |
| GET | `/products/{product_id}` | Get one product |
| POST | `/orders` | Create an order |

Interactive API documentation is available at `/docs`.

## Run locally

Requirements: Python 3.12+

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r app\ecommerce\requirements.txt
python -m uvicorn ecommerce.main:app --app-dir app --reload
```

Open http://127.0.0.1:8000/docs

The application intentionally uses in-memory data and no database, authentication, payment system, or external service. This keeps the application focused and easy to explain while providing enough API behavior for the Docker engineering journey.

## Automated verification

Run the complete API test suite from the repository root:

```powershell
$env:PYTHONPATH="app"
pytest -q
```

The test suite covers successful requests, invalid input, missing resources, order creation, and the OpenAPI contract.
