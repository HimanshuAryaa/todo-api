# Todo API
A REST API built with Python and Flask with JWT Authentication.

## Features
- User registration and login
- JWT token authentication
- Get all todos
- Create a new todo
- Update a todo
- Delete a todo
- Protected routes — only authenticated users can access todos
- Each user can only see their own todos

## Tech Stack
- Python
- Flask
- SQLite
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt

## Setup
1. Clone the repository
2. Create virtual environment - 
    python -m venv venv
3. Activate virtual environment - 
    venv\Scripts\activate
4. Install dependencies - 
    pip install -r requirements.txt
5. Run the app - 
    python app.py

## API Endpoints

### Auth (No token required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and get JWT token |

### Todos (Token required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | Get current user's todos only |
| POST | `/todos` | Create a todo for current user |
| PUT | `/todos/<id>` | Update a todo |
| DELETE | `/todos/<id>` | Delete a todo |

## How to use authentication
1. Register a user via `/register`
2. Login via `/login` to get your token
3. Add the token to requests as Bearer Token in Authorization header
