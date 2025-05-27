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

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: Configurable via `.env` (e.g., PostgreSQL, SQLite, etc.)
- **Authentication**: JWT, Passlib (bcrypt)
- **Environment**: Python 3.10+
- **Other**: Pydantic, python-dotenv

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
   *(Create a `requirements.txt` if not present, with FastAPI, SQLAlchemy, python-dotenv, passlib[bcrypt], pydantic, and uvicorn)*
   ```bash
   pip install fastapi sqlalchemy python-dotenv passlib[bcrypt] pydantic uvicorn
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your database URL and any secrets.
   - Example `.env`:
     ```env
     DATABASE_URL=sqlite:///./test.db
     SECRET_KEY=your_secret_key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

5. **Run the application:**
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

---

## Contribution
Pull requests are welcome! Please open an issue first to discuss major changes.

---

## License
This project is licensed under the MIT License.
