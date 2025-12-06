Understood.
Here is the **FULL, FINAL, CLEAN, PRODUCTION-READY README.md** — you can copy-paste it directly into your repo *as is*.

---

# ✅ **Task Management API – Backend (FastAPI + MongoDB + Beanie)**

A fully functional **Task Management Backend** built using **FastAPI**, designed for the Atlys Backend Engineer Assessment.
This project implements:

✔ User Registration & Login (JWT Authentication)
✔ Role-based Authorization
✔ Task CRUD operations
✔ Advanced Task Filtering
✔ Bulk Update of Tasks
✔ Task Analytics (overdue tasks, distribution)
✔ Clean Architecture (Routes → Service → UseCases → Repository → DB)
✔ MongoDB + Beanie ORM
✔ Singleton DB initialization
✔ Logger (Singleton, Rotating File Handler)

---

## 📌 **Table of Contents**

* [Features](#features)
* [Selected Optional Features & Justification](#selected-optional-features--justification)
* [Tech Stack](#tech-stack)
* [Project Structure](#project-structure)
* [Setup & Installation](#setup--installation)
* [Environment Variables](#environment-variables)
* [Running the Server](#running-the-server)
* [API Endpoints](#api-endpoints)
* [Authentication Flow](#authentication-flow)
* [Architecture & Design Patterns](#architecture--design-patterns)
* [Future Improvements](#future-improvements)

---

# 🚀 **Features**

## 🔐 **Authentication**

* User registration with email + password
* Password hashing (bcrypt)
* JWT token generation & verification
* Role-based authorization (Admin/User)
* Protected routes using middleware

## 👥 **User Management**

* Register user
* Login user
* Get current authenticated user (`/me`)
* Get all users (protected)

## 📝 **Task Management**

* Create, Read, Update, Delete tasks
* Tasks include:

  * title
  * description
  * status
  * priority
  * assignee
  * due_date
  * tags
  * collaborators
  * subtasks

## 🔍 **Advanced Task Filtering**

Filter tasks using:

* status
* priority
* assignee
* date range
* tags
  Supports **AND/OR logic**.

## 📊 **Analytics**

* Overdue tasks per user
* Task distribution per user (pie-chart friendly data)

## 📦 **Bulk Operations**

* Bulk update multiple tasks at once (status, assignee, etc.)

---

# ⭐ **Selected Optional Features & Justification**

From the 4 given optional features, **I implemented the following 3**:

### ✅ **1. Filtering tasks by multiple criteria**

Useful for real-world dashboards, improves user productivity.

### ✅ **2. Task distribution & overdue tasks analytics**

Important for performance tracking & workload management.

### ❌ Not Implemented: *Timeline of task changes*

Reason:
This feature requires event sourcing or audit logs, which is more time-intensive.
Due to the assignment time constraint, I prioritized implementing features that provide higher functional value with cleaner implementation.

---

# 🧰 **Tech Stack**

| Layer            | Technology                              |
| ---------------- | --------------------------------------- |
| Language         | Python 3.x                              |
| Framework        | FastAPI                                 |
| Database         | MongoDB (Atlas or Local)                |
| ODM              | Beanie                                  |
| Auth             | JWT + bcrypt                            |
| Architecture     | Clean Architecture + Repository Pattern |
| Deployment-ready | Uvicorn server                          |

---

# 📂 **Project Structure**

```
server/
│── app.py
│── logger.py
│── settings.py
│── .env
│
├── auth/
│   ├── middleware/
│   │     ├── authentication_middleware.py
│   │     ├── role_check_middleware.py
│   └── usecase/
│         ├── generate_token_usecase.py
│         ├── verify_jwt_usecase.py
│         ├── hash_password_usecase.py
│         ├── verify_password_usecase.py
│
├── user/
│   ├── routes/
│   ├── schema/
│   ├── models/
│   ├── repository/
│   ├── use_case/
│   ├── abstract_repository/
│
├── task/
│   ├── routes/
│   ├── schema/
│   ├── models/
│   ├── repository/
│   ├── use_case/
│
├── database/
│   ├── mongo_config.py
│   ├── db_factory.py
│   ├── db_initialize.py
│
└── logs/
     └── app.log
```

---

# ⚙ **Setup & Installation**

```bash
git clone https://github.com/sudarshan24-10/task_management_backend_Atlys_assesment.git

cd task_management_backend_Atlys_assesment
cd server

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

# 🔑 **Environment Variables**

Create a `.env` file inside **/server**:

```
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net
DB_NAME=task_management
JWT_SECRET=<your-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Ensure `.env` is included in `.gitignore`.

---

# ▶ **Running the Server**

```bash
uvicorn app:app --reload
```

API Docs URL:

👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**
👉 **[http://localhost:8000/redoc](http://localhost:8000/redoc)**

---

# 📡 **API Endpoints**

---

## 🔐 **Auth Endpoints**

### **Register User**

```
POST /user/auth/register
```

### **Login User**

```
POST /user/auth/login
```

Returns:

```json
{
  "message": "Login successful",
  "access_token": "<JWT_TOKEN>"
}
```

### **Get Current User**

```
GET /user/auth/me
Authorization: Bearer <token>
```

### **Get All Users**

```
GET /user/auth/users
Authorization: Bearer <token>
```

---

## 📝 **Task Endpoints**

### Create Task

```
POST /tasks/
```

### Get All Tasks

```
GET /tasks/
```

### Get Task by ID

```
GET /tasks/{task_id}
```

### Update Task

```
PUT /tasks/{task_id}
```

### Delete Task

```
DELETE /tasks/{task_id}
```

---

## 🔍 **Task Filtering**

```
GET /tasks/filter?status=OPEN&priority=HIGH&assignee=userId&tags=python,backend
```

---

## 📦 **Bulk Update**

```
PUT /tasks/bulk-update
```

Body example:

```json
{
  "task_ids": ["id1", "id2"],
  "status": "IN_PROGRESS"
}
```

---

## 📊 **Analytics Endpoints**

### Overdue tasks per user

```
GET /tasks/analytics/overdue
```

### Task distribution

```
GET /tasks/analytics/distribution
```

---

# 🔐 **Authentication Flow**

1. User registers
2. Logs in → receives JWT token
3. Sends requests with:

```
Authorization: Bearer <token>
```

4. Middleware verifies token → loads user → injects into endpoint

---

# 🧱 **Architecture & Design Patterns**

### ✔ Clean Architecture

* Routes (FastAPI)
* Service Layer
* Use Cases (Business Logic)
* Repository Layer (MongoDB/Postgres interchangeable)
* Database Layer (Singleton Beanie init)

### ✔ Repository Pattern

Makes database swappable (MongoDB → Postgres).

### ✔ Factory Pattern

To initialize databases cleanly.

### ✔ Singleton Logger

Used across the entire application.

---

# 🚀 **Future Improvements**

* Add task dependency feature
* Add subtasks support fully
* Add pagination to heavy endpoints
* Add background workers for notifications
* Add rate-limiting middleware
* Add unit & integration tests
* Dockerize entire project

---

# 📝 **Final Notes**

This backend was implemented following the Atlys Backend Engineering assignment requirements, with emphasis on:

* scalability
* clean architecture
* separation of concerns
* production-level patterns
* extensibility for future features

---

