# Curso FastAPI Project

This is a simple FastAPI project developed as part of a course. It demonstrates basic FastAPI concepts including path parameters, Pydantic models, SQLModel integration, and dependency injection.

## Features

- **Root Endpoint**: Basic "Hello World" style endpoint.
- **Timezone Endpoint**: Get the current time for specific countries (Colombia, Mexico, Argentina, Brazil, Peru).
- **Customer Management**: Create and list customers (currently using in-memory storage).
- **Transaction & Invoice Models**: Data validation for transactions and invoices.

## Project Structure

- `main.py`: The main application file containing the FastAPI app and route definitions.
- `models.py`: Pydantic and SQLModel definitions for Customers, Transactions, and Invoices.
- `db.py`: Database connection and session management using SQLModel and SQLite.
- `requirements.txt`: List of project dependencies.

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, you can use the FastAPI CLI (included with `fastapi[standard]`):

```bash
fastapi dev main.py
```

Or run it directly with Python (uses uvicorn):

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`.

### Interactive Documentation

FastAPI provides automatic interactive documentation. Once the app is running, visit:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints

- `GET /`: Returns `{"message": "Hello, John!"}`.
- `GET /time/{timezone}`: Returns the current time for a given country code (e.g., `CO`, `MX`).
- `POST /customers`: Create a new customer.
- `GET /customers`: List all customers.
- `GET /customers/{customer_id}`: Get a specific customer by ID.
- `POST /transactions`: Create a transaction (validation only).
- `POST /invoices`: Create an invoice (validation only).
