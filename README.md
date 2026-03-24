# FastAPI Notes Backend

Backend API для управления заметками с аутентификацией и авторизацией.

## Функции
- FastAPI
- SQLAlchemy ORM
- JWT Authentication
- Password hashing (bcrypt)
- Ownership-based access control
- CRUD operations

## Endpoints
- POST /users — create user
- POST /login — get JWT token
- GET /notes — get user notes
- POST /notes — create note
- PUT /notes/{id} — update note
- DELETE /notes/{id} — delete note

## Стек
- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
