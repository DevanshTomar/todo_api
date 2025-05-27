# Todo API

A robust, modular, and secure Todo API built with FastAPI and SQLAlchemy. This project provides endpoints for user authentication, todo management, and user profile management, leveraging modern Python best practices and a clean architecture.

---

## Features

- **User Authentication**: Secure login and registration with JWT-based authentication and password hashing (bcrypt).
- **Todo Management**: Create, read, update, and delete todos. Todos are associated with users and support priorities, completion status, and descriptions.
- **User Profile Management**: Endpoints for retrieving user details and changing passwords.
- **Role Management**: Users can have roles for future extensibility (admin, user, etc.).
- **Environment Configuration**: Uses `.env` for environment variables and database connection.

---

## Tech Stack

- **Framework**: FastAPI 0.115.12
- **ORM**: SQLAlchemy 2.0.28
- **Database**: Configurable via `.env` (e.g., PostgreSQL, SQLite, etc.)
- **Authentication**: JWT (python-jose), Passlib (bcrypt)
- **Migration**: Alembic 1.16.1
- **Environment**: Python 3.10+
- **Other**: Pydantic 2.6.3, python-dotenv 1.1.0, uvicorn 0.34.2

---

## Project Structure

```
/ (root)
├── main.py              # FastAPI app entrypoint, router registration
├── database.py          # SQLAlchemy engine/session setup
├── models.py            # ORM models for Users and Todos
├── routers/
│   ├── auth.py          # Authentication endpoints (login, register, JWT)
│   ├── todos.py         # CRUD endpoints for todos
│   ├── users.py         # User profile and password management
│   └── admin.py         # (Optional) Admin endpoints
├── alembic/             # Database migration files
│   ├── versions/        # Migration version scripts
│   └── env.py           # Alembic environment configuration
├── alembic.ini          # Alembic configuration file
├── .env                 # Environment variables (DB connection, secrets)
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd todo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   The requirements include:
   - fastapi==0.115.12
   - uvicorn==0.34.2
   - sqlalchemy==2.0.28
   - python-dotenv==1.1.0
   - pydantic==2.6.3
   - alembic==1.16.1
   - python-jose[cryptography]==3.3.0
   - passlib[bcrypt]==1.7.4
   - starlette==0.46.2
   - typing-extensions==4.13.2

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your database URL and any secrets.
   - Example `.env`:
     ```env
     DATABASE_URL=sqlite:///./test.db
     SECRET_KEY=your_secret_key
     ALGORITHM=HS256
     ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the interactive API docs:**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## Example API Usage

### Authentication
- `POST /login` — Obtain a JWT access token
- `POST /register` — Register a new user

### Todos
- `GET /todos/` — List all todos for the authenticated user
- `POST /todos/todo` — Create a new todo
- `PUT /todos/todo/{todo_id}` — Update an existing todo
- `DELETE /todos/todo/{todo_id}` — Delete a todo

### Users
- `GET /users/` — Get current user profile
- `PUT /users/password` — Change password
- `PUT /users/phone` — Change phone number

---

## Models Overview

### Users
- `id`: Integer, primary key
- `email`: String, unique
- `username`: String, unique
- `first_name`, `last_name`: String
- `hashed_password`: String (bcrypt hashed)
- `is_active`: Boolean
- `role`: String (for future role-based access)
- `phone_number`: String

### Todos
- `id`: Integer, primary key
- `title`: String
- `description`: String
- `priority`: Integer (1-5)
- `complete`: Boolean
- `owner_id`: Foreign key to Users

---

## Security Notes
- Passwords are hashed using bcrypt and never stored in plaintext.
- JWTs are used for authentication and should be kept secure.
- Environment variables are used for all secrets and configuration.
