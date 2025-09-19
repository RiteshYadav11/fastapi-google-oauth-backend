Perfect 👍
I’ll format everything properly into a **single markdown file** (`README.md`) with all styling, headings, tables, and code blocks — so you can directly copy-paste into your repo.

Here it is:

---

```markdown
# 🚀 FastAPI Google OAuth Backend

A comprehensive **FastAPI-based backend** for a food ordering platform with **Google OAuth authentication**, **database management**, and **analytical reporting** capabilities.  

---

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
- [Demo](#-demo)  

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
├── migrations/              # Alembic migration files
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
# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=fastapi_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:your_secure_password@localhost:5432/fastapi_db

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Session
SESSION_SECRET=your_session_secret_key
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

# Run migrations
alembic upgrade head
```

#### 3. Start the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
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

---

## 🎉 Application Ready!

* API Base URL → `http://localhost:8000`
* Swagger Docs → `http://localhost:8000/docs`
* ReDoc Docs → `http://localhost:8000/redoc`

---

## 📖 API Documentation

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

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
* `GET /auth/me` – Get current user profile

### 🔹 Orders

* `POST /orders/` – Create new order (requires payment validation)
* `GET /orders/` – Get user’s orders
* `GET /orders/{order_id}` – Get order details

### 🔹 Payments

* `POST /payments/` – Process payment
* `GET /payments/{transaction_id}` – Get payment status

### 🔹 Analytics & Reports

* `GET /restaurants/mumbai-earnings` – Total earnings in Mumbai (last month)
* `GET /restaurants/bangalore-veg-earnings` – Veg item earnings in Bangalore
* `GET /restaurants/top-customers` – Top 3 customers by orders
* `GET /restaurants/daily-revenue` – Daily revenue for past 7 days
* `GET /restaurants/{restaurant_id}/summary` – Order summary for restaurant

---

## 📌 Example API Calls

### 1. Login with Google

```bash
curl -X GET "http://localhost:8000/auth/login"
```

### 2. Create Order

```bash
curl -X POST "http://localhost:8000/orders/" \
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
curl -X GET "http://localhost:8000/restaurants/mumbai-earnings" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🐳 Docker Deployment

### 🔹 Development

```bash
docker-compose up --build
docker-compose logs -f web
docker-compose down
```

### 🔹 Production

```bash
docker build -t fastapi-backend .
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

---

## 🎥 Demo

👉 [Demo Video Link Here](#) *(to be added after recording)*

---

```

---

Do you want me to also add **badges (Python, FastAPI, Docker, PostgreSQL)** at the top of README for extra polish?
```
