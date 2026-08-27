# Expense Tracker API

A FastAPI-based expense tracking application for managing personal income and expense records with user authentication.

## Features

- User registration and login
- JWT-based authentication
- Create, read, update, and delete transactions
- Filter transactions by type, category, and amount range
- User-specific data isolation
- SQLAlchemy database models

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL (production config)
- JWT authentication
- Pytest

## Project Structure

```text
Expanse_Tracker/
├── main.py                 # FastAPI app entry point
├── database.py             # Database configuration and session setup
├── models.py               # SQLAlchemy models for users and transactions
├── schemas.py              # Pydantic request/response schemas
├── security.py             # Auth logic, password hashing, JWT generation
├── requirements.txt        # Python dependencies
├── routers/
│   ├── __init__.py
│   ├── auth.py             # Register/login endpoints
│   └── transactions.py     # Transaction CRUD and filtering endpoints
├── tests/
│   ├── conftest.py         # Test database and fixtures
│   └── test_transactions.py
├── .env                    # Local environment variables
└── .gitignore
```

## Environment Variables

Create a `.env` file in the project root with:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/expense_tracker
SECRET_KEY=your_secret_key_here
```

The app requires both values to start.

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Endpoints

### Authentication

- `POST /auth/register` - Create a new user
- `POST /auth/login` - Login and receive JWT token

### Transactions

- `POST /transactions` - Create a transaction
- `GET /transactions` - Get all transactions for the logged-in user
- `GET /transactions/filter` - Filter transactions
- `GET /transactions/{transaction_id}` - Get one transaction
- `PUT /transactions/{transaction_id}` - Update a transaction
- `DELETE /transactions/{transaction_id}` - Delete a transaction

## Testing

Run tests with:

```bash
pytest
```

This project uses an in-memory SQLite database for test execution.

## Notes

- Authentication is required for transaction endpoints.
- Each transaction is tied to its owner via `owner_id`.
- The app uses JWT tokens in the `Authorization` header as a Bearer token.


## Author : Muiz Sarwar