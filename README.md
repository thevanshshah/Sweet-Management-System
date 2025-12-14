# Sweet Shop Management System

**A modern, full-stack Sweet Shop Management System built with a security-first mindset and a Test-Driven Development (TDD) approach.**

---

## 📋 Table of Contents
1. [What is This System?](#-what-is-this-system)
2. [Who Can Use This?](#-who-can-use-this)
3. [Key Features](#-key-features)
4. [Technical Architecture](#-technical-architecture)
5. [Quick Start Guide](#-quick-start-guide)
6. [API Reference](#-api-reference)
7. [Testing & TDD](#-testing--tdd)
8. [My AI Usage](#-my-ai-usage)

---

## 🧐 What is This System?

The Sweet Shop Management System is a digital backbone for a confectionery business. It replaces manual spreadsheets with a secure, automated inventory and sales system.

It acts as an intelligent store manager that:
* **Tracks Inventory:** Maintains accurate stock counts for sweets and snacks.
* **Prevents Overselling:** Blocks purchases when stock reaches zero.
* **Improves Experience:** Displays visually appealing product cards using smart image mapping.

### 🏪 Real-World Example
Imagine you run **“Royal Sweets & Snacks”**:
1.  You have **20 Samosas** in stock.
2.  A customer logs in and purchases **5 Samosas**.
3.  The system atomically updates the stock to **15**.
4.  Another customer tries to buy 16 — the system **rejects the purchase** to maintain inventory correctness.

---

## 👥 Who Can Use This?

**1️⃣ Shop Owner (Admin Role)**
* Add new sweets
* Update prices and categories
* Restock inventory
* Delete discontinued items
* View exact warehouse stock counts

**2️⃣ Customer (User Role)**
* Browse available sweets
* Search by name or category
* See stock-aware messages like *“Hurry! Only 2 left!”*
* Purchase sweets securely

---

## 🌟 Key Features

### 🔐 Security & Access Control
* **JWT-based authentication** (JSON Web Tokens).
* **Role-Based Access Control (RBAC):** All admin-only actions (Restock, Delete) are validated server-side.
* **Security First:** Frontend role checks are cosmetic; backend enforcement is authoritative.

### 📦 Inventory Management
* **Atomic Operations:** Purchase and restock operations are race-condition safe.
* **Zero-Stock Protection:** Purchases are strictly blocked when stock = 0.
* **Data Integrity:** Quantity always remains non-negative.

### 🎨 User Experience
* **Smart Image Engine:** Frontend automatically selects appetizing images based on product names (e.g., "Vadapav", "Cake").
* **Responsive UI:** Clean interface built with React & Vite.
* **Clear Distinctions:** Distinct views for Customers vs. Admins.

---

## 🛠️ Technical Architecture
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python (FastAPI) | RESTful API with JWT security |
| **Database** | SQLite (via SQLAlchemy ORM) | Type-safe relational storage |
| **Frontend** | React + Vite | SPA consuming backend APIs |
| **Styling** | CSS Modules | Custom responsive "Premium" theme |
| **Testing** | Pytest | Backend unit and integration tests |

## 🚀 Quick Start Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/thevanshshah/Sweet-Management-System.git
cd Sweet-Management-System
```
### Step 2: Backend Setup
```bash
cd backend

# Create & Activate Virtual Environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Run Server
uvicorn main:app --reload
```
- API runs at: http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs

### Step 3: Frontend Setup
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```
- Frontend runs at: http://localhost:5173

## API Reference
### Authentication
| Method | Endpoint | Access |
| :--- | :--- | :--- |
| **POST** | /api/auth/register | Public |
| **POST** | /api/auth/login | Public |

### Sweets
| Method | Endpoint | Access |
| :--- | :--- | :--- |
| **GET** | /api/sweets | Public |
| **POST** | /api/sweets | Admin |
| **DELETE** | /api/sweets/{id} | Admin |

### Inventory
| Method | Endpoint | Access |
| :--- | :--- | :--- |
| **POST** | /api/sweets/{id}/purchase | User |
| **POST** | /api/sweets/{id}/restock | Admin |

## 🧪 Testing & TDD
This project strictly follows Test-Driven Development (TDD) principles. Tests were written before core logic to ensure backend correctness and security.

Coverage Includes:

- Authentication & JWT Validations
- Role-based access (403 Forbidden checks)
- Purchase logic & Stock decrements
- Out-of-stock handling

### Run tests
```bash
cd backend
pytest --cov
```
## 🤖 My AI Usage

### 🛠️ AI Tools Used
* **ChatGPT**
* **Google Gemini**

### 📊 Development Approach (80/20 Rule)
This project followed an **80/20 development approach** to ensure full ownership and understanding of the system:
* **80% Manual Implementation:** Core architecture, business logic, security, and UI behavior.
* **20% AI Assistance:** Debugging, reasoning validation, and documentation refinement.

### 🧠 How AI Was Used
AI tools were used **strictly as a support mechanism**, primarily for:
* **Debugging:** Interpreting specific error messages and stack traces (e.g., authentication issues, ORM-related errors) that temporarily blocked progress.
* **Clarification:** Resolving framework- or syntax-level doubts without relying on generated solutions.
* **Reasoning Review:** Validating manually written logic for edge cases, acting as a second pair of eyes rather than a code author.
* **Documentation:** Improving clarity, structure, and readability of README content.

**AI was NOT used to design system architecture, database models, or core business logic.**

### ✍️ What Was Implemented Manually
The following components were designed, written, and validated independently:

* **Backend Business Logic:** Purchase flow, stock decrement logic, restocking mechanism, and validation rules ensuring data integrity.
* **Security & Access Control:** JWT-based authentication, role-based access control (Admin vs User), and server-side authorization checks.
* **Database Design & API Contracts:** Schema design, entity relationships, and REST API behavior.
* **Frontend State & UI Logic:** Authentication flow (login/register toggle), role-aware UI rendering, and inventory-driven UI state.
* **Testing & Validation:** Test cases covering authentication, authorization failures (403), inventory updates, and edge cases.

### 💭 Reflection
AI tools acted as **debugging assistants** and **productivity enhancers**, not as decision-makers or code generators.

All critical architectural decisions, security mechanisms, and business rules were fully owned, implemented, and verified by me, ensuring deep understanding and long-term maintainability of the system.

## 📸 Screenshots
1. Login & Registration
2. Customer Shop View
3. Admin Panel

### Made with care by Vansh Shah
