# 🚀 Django + React + TypeScript Initial Code (with JWT Authentication)

This project is a **starter template** for building modern web applications using:

* **Backend:** Django + Django REST Framework (with JWT authentication)
* **Frontend:** React + TypeScript

It comes with authentication, environment-based configurations, and ready-to-extend integrations.

## ✨ Features

🛠️ **Pre-configuration:**

* ✅ Django backend with custom user model (email login)
* ✅ JWT authentication (access + refresh tokens)
* ✅ React + TypeScript setup
* ✅ Environment-based configs for development & production
* ✅ Integration ready (PostgreSQL, Redis, Celery, OAuth, etc.)

🔧 **Features currently supported:**

* Authentication: registration, login, logout, password reset, email verification, Google OAuth
* API: RESTful endpoints with error handling & standardized responses
* Background Tasks: Celery with Redis support
* Database: SQLite (default), PostgreSQL (production-ready)
* Frontend: React with TypeScript, `.env` config support

## 📦 Requirements

* Python 3.10+
* Node.js v22.16.0
* npm
* SQLite (default) / PostgreSQL (prod)

## ⚙️ Setup Instructions

### 🔹 Backend (Django)

1. Clone the repository:

   ```bash
   git clone git@github.com:shaileshpandit141/drts-init.git
   cd drts-init
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Configure environment variables:
   Create `.env` in the backend directory:

   ```dotenv
   # Django
   SECRET_KEY=your_django_secret_key
   ENVIRONMENT=dev  # or prod
   ALLOWED_HOSTS=["localhost", "127.0.0.1"]

   # JWT
   TOKEN_ACTIVE_KEY_ID=v1
   TOKEN_PRIVATE_KEY_v1=-----BEGIN PRIVATE KEY-----your_private_key-----END PRIVATE KEY-----

   # PostgreSQL (Production)
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432

   # Redis (Production)
   REDIS_CACHE_LOCATION=redis://127.0.0.1:6379/1

   # Email (Production)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=example@gmail.com
   EMAIL_HOST_PASSWORD=your_password
   EMAIL_DEFAULT_FROM_EMAIL=example@gmail.com

   # Google OAuth2
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

   # Celery
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```

4. Apply migrations:

   ```bash
   uv run manage.py migrate
   ```

5. Create a superuser:

   ```bash
   uv run manage.py createsuperuser
   ```

6. Run the dev server:

   ```bash
   uv run manage.py runserver
   ```

### 🔹 Frontend (React + TypeScript)

1. Navigate to frontend:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Configure environment variables:
   Create `.env` in the frontend root:

   ```dotenv
   REACT_APP_BASE_API_URL=http://localhost:8000
   REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
   ```

4. Run React dev server:

   ```bash
   npm start
   ```

## 🔑 Authentication API Endpoints

Base URL:

```bash
http://localhost:8000/api/v1/auth
```

Available endpoints:

* **POST** `/signup/` → Register new account (email/password)
* **POST** `/account-verification/` → Request account verification
* **POST** `/account-verification/confirm/` → Confirm account verification
* **POST** `/token/` → Obtain access + refresh tokens
* **POST** `/token/refresh/` → Refresh access token
* **POST** `/token/block/` → Sign out (invalidate refresh token)
* **POST** `/password/change/` → Change password
* **POST** `/password/reset/` → Request password reset
* **POST** `/password/reset/confirm/` → Confirm password reset
* **POST** `/account-deactivation/` → Deactivate account
* **GET** `/user/` → Fetch user profile
* **GET** `/google/signin/` → Start Google OAuth flow
* **POST** `/google/callback/` → Handle Google OAuth callback

## ⚠️ Error Responses (Standardized)

Examples of default response structures:

* **400 Bad Request** → `{ "field": ["Invalid input"] }`
* **401 Unauthorized** → `{ "detail": "Authentication credentials were not provided." }`
* **403 Forbidden** → `{ "detail": "You do not have permission." }`
* **404 Not Found** → `{ "detail": "Not found." }`
* **405 Method Not Allowed** → `{ "detail": "Method not allowed." }`
* **500 Server Error** → `{ "detail": "A server error occurred." }`

## 🎨 Frontend Integration

* Store tokens in **localStorage** (or cookies for security).
* Attach `Authorization: Bearer <token>` header to protected requests.
* Use **TypeScript interfaces** for request/response payloads.

## 🤝 Contributing

Contributions are welcome! Please open an issue or PR for improvements.

## 📜 License

MIT License — See [LICENSE](LICENSE).

## 👤 Author

Created by **Shailesh Pandit**
📧 [shaileshpandit141@gmail.com](mailto:shaileshpandit141@gmail.com)
