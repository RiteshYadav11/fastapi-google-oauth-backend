# 🚀 FastAPI Google OAuth Backend

A comprehensive **FastAPI-based backend** for a food ordering platform with **Google OAuth authentication**, **database management**, and **analytical reporting** capabilities.  

## 📋 Table of Contents
 
- [Project Overview](#-project-overview)  
- [Features](#-features)  
- [Tech Stack](#-tech-stack)  
- [Project Structure](#-project-structure)  
- [Prerequisites](#-prerequisites)  
- [Installation & Setup](#-installation--setup)  
- [Environment Variables](#-environment-variables)  
- [Running the Application](#-running-the-application)  
- [API Documentation](#-api-documentation)  
- [Database Schema](#-database-schema)  
- [Authentication Flow](#-authentication-flow)  
- [API Endpoints](#-api-endpoints)  
- [Docker Deployment](#-docker-deployment)  
- [Example API Calls](#-example-api-calls)  

---


## 🎯 Project Overview

This backend system manages a food ordering platform with the following core functionalities:

- 🔐 **Google OAuth 2.0 Authentication** – Secure user login and registration  
- 💳 **Payment Processing** – Handle UPI and card payments with status tracking  
- 🍽️ **Order Management** – Complete order lifecycle with payment validation  
- 🏨 **Restaurant Management** – Multi-location restaurant data  
- 📊 **Analytics & Reporting** – Complex queries for business insights  

---

## ✨ Features

- 🔐 Google OAuth Integration – Seamless login with Google accounts  
- 💳 Payment Gateway – Support for UPI and card payments  
- 🍽️ Order System – Complete order management with validation  
- 🏪 Multi-Restaurant Support – Restaurants across Mumbai and Bangalore  
- 📊 Analytics APIs – Revenue reports, customer insights, and performance metrics  
- 🐳 Docker Support – Easy deployment with Docker and Docker Compose  
- 📝 Auto-Documentation – Interactive API docs with Swagger UI  
- 🗃️ Database Migrations – Alembic for schema versioning  

---

## 🛠️ Tech Stack

- **Framework:** FastAPI  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Authentication:** Google OAuth 2.0 + JWT  
- **Migration:** Alembic  
- **Containerization:** Docker & Docker Compose  
- **Documentation:** Swagger UI (Auto-generated)  

---

## 📁 Project Structure

```

fastapi-google-oauth-backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for request/response
│   ├── database.py          # Database configuration and connection
│   ├── utils.py             # Utility functions (JWT, OAuth helpers)
│   └── routers/
│       ├── auth.py          # Authentication routes (Google OAuth)
│       ├── orders.py        # Order management routes
│       ├── payments.py      # Payment processing routes
│       └── restaurants.py   # Restaurant and analytics routes
├── migrations/              # Alembic migrations 
|       ├── versions/
│       ├── env.py
|       ├── script.py.mako     
├── requirements.txt         # Python dependencies
├── alembic.ini              # Alembic configuration
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Multi-container Docker setup
├── .env.example             # Environment variables template
├── sql\_schema.sql           # Database schema (optional)
└── README.md                # Project documentation

````

---

## 📋 Prerequisites

- **Python 3.11+**  
- **PostgreSQL 15+**  
- **Docker & Docker Compose** (optional)  
- **Google Cloud Console account** (for OAuth setup)  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/fastapi-google-oauth-backend.git
cd fastapi-google-oauth-backend
````

### 2️⃣ Google OAuth Setup

1. Go to **Google Cloud Console**
2. Create a new project (or select existing)
3. Enable **Google+ API**
4. Create OAuth 2.0 credentials:

   * Go to **Credentials → Create Credentials → OAuth 2.0 Client ID**
   * Application type: **Web application**
   * Authorized redirect URIs: `http://localhost:8000/auth/callback`
5. Save the **Client ID** and **Client Secret**

### 3️⃣ Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configurations
nano .env
```

---

## 🔧 Environment Variables

Example `.env` file:

```env
# Database configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_db

# Google OAuth2 configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Security
JWT_SECRET=your_jwt_secret_here
SESSION_SECRET=your_session_secret_here
```

---

## 🏃‍♂️ Running the Application

### 🔹 Method 1: Local Development

#### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Setup Database

```bash
# Start PostgreSQL (if not running)
createdb fastapi_db

# Generate initial migration
alembic revision --autogenerate -m "initial tables"

# Run migrations
alembic upgrade head
```

#### 3. Start the Application

Local Development
```bash
# Run with auto-reload (default: host=127.0.0.1, port=8000)
uvicorn app.main:app --reload
```

Access the app at: http://127.0.0.1:8000

Production / Docker
```bash
# Run with host 0.0.0.0 so it's accessible from outside
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Useful when running inside Docker or exposing the app to other devices on your network.

Access via: http://<your-ip>:8000
```

---

### 🔹 Method 2: Docker Deployment

#### 1. Build & Run with Docker Compose

```bash
docker-compose up --build
# Or run in background
docker-compose up -d --build
```

#### 2. Run Database Migrations

```bash
docker-compose exec web alembic upgrade head
```

#### 3. Run Database Migrations (Option B: Automatic)

You can also configure migrations to run automatically every time the container starts.
Comment out this line in `docker-compose.yml`:
```bash
command: uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Uncomment and use this in your docker-compose.yml under the web service:
```bash
command: >
  bash -c "alembic upgrade head &&
           uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
```

With this setup, Alembic migrations are applied before launching the FastAPI app.


---

## 🎉 Application Ready!

* API Base URL → `http://127.0.0.1:8000`
* Swagger Docs → `http://127.0.0.1:8000/docs`
* ReDoc Docs → `http://127.0.0.1:8000/redoc`

---

## 📖 API Documentation

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
<a name="-database-schema"></a>
## 🗄️ Database Schema

### Customers

| Field      | Type    | Description                |
| ---------- | ------- | -------------------------- |
| id         | UUID PK | Unique customer identifier |
| name       | VARCHAR | Customer full name         |
| google\_id | VARCHAR | Google OAuth identifier    |
| age        | INT     | Customer age               |

### Payments

| Field           | Type      | Description                     |
| --------------- | --------- | ------------------------------- |
| transaction\_id | UUID PK   | Unique transaction identifier   |
| status          | ENUM      | Payment status (`pass`, `fail`) |
| payment\_type   | ENUM      | Payment method (`UPI`, `card`)  |
| created\_at     | TIMESTAMP | Payment timestamp               |

### Orders

| Field           | Type      | Description             |
| --------------- | --------- | ----------------------- |
| order\_id       | UUID PK   | Unique order identifier |
| food\_item      | ENUM      | Food item ordered       |
| transaction\_id | UUID FK   | Reference to payment    |
| restaurant\_id  | UUID FK   | Reference to restaurant |
| created\_at     | TIMESTAMP | Order timestamp         |

### Restaurants

| Field            | Type    | Description                      |
| ---------------- | ------- | -------------------------------- |
| restaurant\_id   | UUID PK | Unique restaurant identifier     |
| restaurant\_name | VARCHAR | Restaurant name                  |
| area             | ENUM    | Location (`Mumbai`, `Bangalore`) |

---

## 🔐 Authentication Flow

1. **Login Request** → User clicks *Login with Google*
2. **OAuth Redirect** → Google OAuth consent screen
3. **Authorization** → User grants permissions
4. **Callback** → Google redirects with authorization code
5. **Token Exchange** → Backend exchanges code for token
6. **User Info** → Fetch details from Google API
7. **User Creation** → Insert user if new
8. **JWT Generation** → Return JWT token
9. **Authenticated Requests** → Use JWT for protected APIs

---

## 🔗 API Endpoints

### 🔹 Authentication

* `GET /auth/login` – Initiate Google OAuth login
* `GET /auth/callback` – Handle OAuth callback
* `GET /auth/verify-token` – Verify JWT token

### 🔹 Restaurants

* `POST /restaurants/` – Create new restaurant  
* `GET /restaurants/{restaurant_id}` – Get restaurant details  

### 🔹 Orders

* `POST /orders/` – Create new order (requires payment validation)
* `GET /orders/debug/test_order_type` - Debug Order Type

### 🔹 Payments

* `POST /payments/` – Process payment
* `GET /payments/{transaction_id}` – Get payment status

### 🔹 Analytics & Reports

* `GET /orders/reports/mumbai/last_month` – Total earnings in Mumbai (last month)  
* `GET /orders/reports/bangalore/veg_earnings` – Veg item earnings in Bangalore  
* `GET /orders/reports/top_customers` – Top 3 customers by orders  
* `GET /orders/reports/daily_revenue_7days` – Daily revenue for past 7 days  
* `GET /orders/reports/restaurant/{restaurant_id}/summary` – Order summary for a restaurant  

---

## 📌 Example API Calls

### 1. Login with Google

```bash
curl -X GET "http://127.0.0.1:8000/auth/login"
```

### 2. Create Order

```bash
curl -X POST "http://127.0.0.1:8000/orders/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "food_item": "veg manchurian",
    "transaction_id": "payment_uuid_here",
    "restaurant_id": "restaurant_uuid_here"
  }'
```

### 3. Get Mumbai Earnings

```bash
curl -X GET "http://127.0.0.1:8000/orders/reports/mumbai/last_month" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🐳 Docker Deployment

### 🔹 Development (using Docker Compose)

```bash
# Build and start all services (web + db)
docker-compose up --build

# Follow logs for the FastAPI web container
docker-compose logs -f web

# Stop and remove containers, networks, volumes
docker-compose down
```

### 🔹 Production

```bash
# Build image
docker build -t fastapi-backend .

# Run container with environment variables from .env
docker run -d --name fastapi-app \
  -p 8000:8000 \
  --env-file .env \
  fastapi-backend
```

### 🔹 Useful Commands

```bash
# View running containers
docker-compose ps

# Open container shell
docker-compose exec web bash

# View DB logs
docker-compose logs db

# Reset everything
docker-compose down -v
docker-compose up --build
```
