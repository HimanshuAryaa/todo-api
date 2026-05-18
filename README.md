# Todo API

A simple REST API built with Python and Flask.

## Features
- Get all todos
- Create a new todo
- Update a todo
- Delete a todo

## Tech Stack
- Python
- Flask

## Setup

1. Clone the repository
2. Create virtual environment
    python -m venv venv
3. Activate virtual environment
    venv\Scripts\activate
4. Install dependencies
    pip install -r requirements.txt
5. Run the app
    python app.py

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /todos | Get all todos |
| POST | /todos | Create a new todo |
| PUT | /todos/<id> | Update a todo |
| DELETE | /todos/<id> | Delete a todo |
