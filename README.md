# asset-management-system
FastAPI Asset Management System with JWT Authentication, Asset Management, Asset Allocation, Reports, Search, SQLAlchemy ORM, Pagination, and Docker Support.
# Asset Management System

## Features

- JWT Authentication
- Asset Management (CRUD)
- Asset Allocation
- Search, Filter & Pagination
- Asset Assignment Reports
- SQLAlchemy ORM
- SQLite Database
- Docker Support
- Logging
- Basic Unit Tests



## Project Setup

### 1. Install dependencies


pip install -r requirements.txt


### 2. Run the application


uvicorn main:app --reload


Swagger URL


http://127.0.0.1:8000/docs


## Environment Variables


SECRET_KEY=asset_secret_key
ALGORITHM=HS256




## Authentication Flow

1. Register User
2. Login
3. Receive JWT Token
4. Access Protected APIs



## API Examples

### Register

POST /auth/register

### Login

POST /auth/login

### Create Asset

POST /assets

### Allocate Asset

POST /allocations



## Deployment

### Docker


docker build -t asset-management .
docker run -p 8000:8000 asset-management


## Assumptions

- Asset Tag is unique.
- One asset can be assigned to only one employee at a time.
- Returned assets become available again.
- Soft delete is implemented using `is_active`.
