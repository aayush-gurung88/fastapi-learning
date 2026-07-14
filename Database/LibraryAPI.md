# 📚 Library Book API

A simple Book Management REST API built using **FastAPI** and **SQLModel**.  
It supports full CRUD operations with proper validation, filtering, pagination, and clean response models.
  
---

## 🚀 Features

- Create a book
- Get all books (with pagination + optional author filter)
- Get a single book by ID
- Update a book partially (PATCH)
- Delete a book
- Proper HTTP status codes
- 404 error handling with clear messages
- Organized API documentation using tags
- Clean public response (no sensitive data like ISBN exposed)

---

## 🧠 Project Structure (Concept)

### Models

- **BookBase**
  - Shared fields: `title`, `author`, `year`
  - Used as a base for other models

- **Book (Table Model)**
  - Database table
  - Adds: `id`, `isbn`

- **BookCreate**
  - Used for creating books
  - Includes all fields + `isbn`

- **BookUpdate**
  - Used for PATCH requests
  - All fields are optional for partial updates

- **BookPublic**
  - Response model
  - Excludes sensitive fields like `isbn`

---

## 🛠️ Why Models Are Separated

We use multiple models instead of one because:

- **Security** → Hide sensitive fields like ISBN in public API
- **Flexibility** → PATCH updates only provided fields
- **Clarity** → Separate purpose for create, update, and response
- Could be done in one model, but would reduce control and safety

---

## ⚙️ Database Approach

- Uses **SQLModel (ORM + Pydantic combined)**
- SQLite database
- Session handled using FastAPI dependency injection

### Query Style Used
- `select(Book)` + `session.exec()` for queries
- `session.get()` could also be used, but `select()` is more flexible for filtering and scaling

---

## 🔄 PATCH Update Logic

- Uses:
  - `model_dump(exclude_unset=True)`
- Only updates fields sent by user
- Uses `setattr()` to dynamically update object fields
- Ensures partial update without overwriting existing data

---

## 📌 API Endpoints
POST 
GET
PATCH 
DELETE



---

## ⚡ How to Run

### 1. Install dependencies
```bash
pip install fastapi sqlmodel uvicorn

### 2. Run server
uvicorn main:app --reload

### 3. Open docs
http://127.0.0.1:8000/docs

Example Request
Create Book
{
  "title": "Harry Potter",
  "author": "J.K. Rowling",
  "year": 2001,
  "isbn": "123-456-789"
}