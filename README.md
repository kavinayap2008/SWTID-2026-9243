# SWTID-2026-9243
# 🏋️ FitBuddy – AI Fitness Plan Generator Using Gemini Models

FitBuddy is a web-based AI fitness application that generates personalized **7-day workout plans** and **nutrition/recovery tips** based on a user's age, weight, fitness goal, and preferred workout intensity.

The application is built using **Python, FastAPI, Google Gemini AI, SQLAlchemy, SQLite, Jinja2, HTML, and CSS**. Users can also provide feedback on an existing workout plan and generate an updated plan based on their requirements.

---

## ✨ Features

- 🤖 AI-generated personalized workout plans
- 📅 Complete 7-day fitness plan
- 🥗 Nutrition and recovery tips
- 🎯 Goal-based workout generation
- 💪 Low, Medium, and High workout intensity levels
- 🔄 Feedback-based workout plan updates
- 👥 User and workout-plan management
- 🗄️ SQLite database storage
- 🌐 Interactive web interface
- 🔌 REST API support
- 📚 Swagger API documentation
- ❤️ Health-check endpoint
- 🧪 Mock AI mode for local testing
- 🔁 Retry handling for temporary Gemini API errors

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Primary programming language |
| **FastAPI** | Web application and REST API framework |
| **Uvicorn** | ASGI development server |
| **Google Gemini AI** | AI workout and nutrition generation |
| **google-genai** | Google Gemini Python SDK |
| **Pydantic** | User input validation |
| **SQLAlchemy** | ORM and database operations |
| **SQLite** | Local relational database |
| **Jinja2** | Dynamic HTML template rendering |
| **HTML / CSS** | Frontend user interface |
| **Pytest** | Application testing |

---

## 🏗️ Application Architecture

```text
User / Browser
      │
      ▼
FastAPI Application
      │
      ▼
APIRouter / Routes
      │
      ├──────────────► Pydantic Validation
      │
      ├──────────────► Workout Generator
      │                      │
      │                      ▼
      │                Gemini Client
      │                      │
      │                      ▼
      │                Google Gemini API
      │
      ├──────────────► Nutrition Tip Generator
      │                      │
      │                      ▼
      │                Gemini Client
      │
      ├──────────────► Updated Plan Generator
      │                      │
      │                      ▼
      │                Gemini Client
      │
      ├──────────────► Database Helpers
      │                      │
      │                      ▼
      │                SQLAlchemy ORM
      │                      │
      │                      ▼
      │                 SQLite DB
      │
      └──────────────► Jinja2 Templates
                             │
                             ▼
                       User / Browser
```

---

## 🔄 Application Flow

```text
User Input
    ↓
FastAPI Form / JSON Route
    ↓
Pydantic Validation
    ↓
Workout Generator
    ↓
Gemini Client / Gemini API
    ↓
7-Day Workout Plan
    ↓
Nutrition / Recovery Tip Generator
    ↓
Save User + Workout Plan
    ↓
SQLAlchemy ORM
    ↓
SQLite Database
    ↓
Jinja2 Result Page / JSON Response
    ↓
User Feedback
    ↓
Updated Plan Generator
    ↓
Gemini AI
    ↓
Updated Workout Plan
```

---

## 📂 Project Structure

```text
FitBuddy-AI/
│
├── .env
├── .env.example
├── .gitignore
├── fitbuddy.db
├── pytest.ini
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_client.py
│   │   ├── gemini_generator.py
│   │   ├── gemini_flash_generator.py
│   │   └── updated_plan.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── styles.css
│   │
│   └── templates/
│       ├── all_users.html
│       ├── base.html
│       ├── index.html
│       └── result.html
│
└── tests/
    └── test_app.py
```

> `.venv` is a generated local virtual environment and should not be committed to the repository.

---

## ⚙️ How FitBuddy Works

### 1. User Input

The user enters:

- Name
- User ID
- Age
- Weight
- Fitness goal
- Workout intensity

Workout intensity can be:

- `low`
- `medium`
- `high`

Pydantic validates the supplied information before it reaches the AI and database layers.

### 2. AI Workout Generation

FitBuddy prepares a prompt using the user's:

- Age
- Weight
- Fitness goal
- Workout intensity

The prompt is sent to the configured **Google Gemini model**.

Gemini generates a personalized **7-day workout plan** containing appropriate workout and recovery guidance.

### 3. Nutrition / Recovery Tip

FitBuddy also generates a short nutrition or recovery tip according to the user's fitness goal.

The guidance is designed to complement the generated workout plan.

### 4. Feedback-Based Plan Update

After receiving a workout plan, the user can provide feedback.

For example:

```text
Include light-weight dumbbell workouts in my plan.
```

FitBuddy retrieves the original plan and sends the original plan together with the user's feedback to the AI service.

Gemini then generates a revised 7-day workout plan while the original plan remains stored separately.

### 5. Database Storage

FitBuddy uses:

```text
SQLAlchemy ORM
       ↓
SQLite
       ↓
fitbuddy.db
```

The database contains two main tables:

```text
users
workout_plans
```

The `users` table stores user profile information.

The `workout_plans` table stores:

- Original workout plan
- Updated workout plan
- Latest user feedback

---

# 🚀 Installation and Setup

## Prerequisites

Before running FitBuddy, install:

- Python
- VS Code
- Git
- A Google Gemini API key for real AI mode

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Move into the project directory:

```bash
cd YOUR-REPOSITORY
```

---

## 2. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Major dependencies include:

```text
fastapi
uvicorn
jinja2
sqlalchemy
python-multipart
python-dotenv
google-genai
pydantic
pydantic-settings
httpx
pytest
```

---

# 🔑 Environment Configuration

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Configure `.env` with the required settings.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_WORKOUT_MODEL=your_configured_workout_model
GEMINI_TIP_MODEL=your_configured_tip_model
DATABASE_URL=sqlite:///./fitbuddy.db
MOCK_AI=false
```

> ⚠️ **Important:** Never upload your real `.env` file or Gemini API key to GitHub.

Make sure `.env` is included in `.gitignore`.

---

# ▶️ Running the Application

From the project root directory, run:

```bash
uvicorn app.main:app --reload
```

The command means:

```text
uvicorn      → Starts the ASGI server

app.main     → Loads app/main.py

:app         → Uses the FastAPI object named "app"

--reload     → Automatically restarts the development server
               when source code changes
```

After startup, open:

```text
http://127.0.0.1:8000/
```

---

# 🌐 Application URLs

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/` | FitBuddy web application |
| `http://127.0.0.1:8000/view-all-users` | User/workout-plan dashboard |
| `http://127.0.0.1:8000/docs` | Swagger API documentation |
| `http://127.0.0.1:8000/health` | Application health check |
| `http://127.0.0.1:8000/api/users` | User and workout-plan JSON data |

---

# 🔌 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Display user input form |
| `POST` | `/generate-workout` | Generate workout plan |
| `POST` | `/submit-feedback` | Update workout plan from feedback |
| `GET` | `/view-all-users` | Display users and plans |
| `POST` | `/delete-user/{user_id}` | Delete a user |
| `POST` | `/api/workouts` | Generate workout using JSON |
| `POST` | `/api/feedback` | Update plan using JSON |
| `GET` | `/api/users` | Retrieve users and plans |
| `GET` | `/health` | Application health check |
| `GET` | `/docs` | Swagger API documentation |

---

# 📡 API Example

## Generate Workout Plan

### Request

```http
POST /api/workouts
```

Example JSON:

```json
{
  "user_id": 101,
  "username": "Demo User",
  "age": 30,
  "weight": 70,
  "goal": "general wellness",
  "intensity": "medium"
}
```

The API returns the validated user information together with the generated workout plan and nutrition tip.

---

## Update Workout Using Feedback

### Request

```http
POST /api/feedback
```

Example:

```json
{
  "user_id": 101,
  "feedback": "Add more mobility and one recovery session"
}
```

The API generates and returns an updated workout plan.

---

# 📚 Swagger API Documentation

FastAPI automatically generates interactive Swagger documentation.

Start the application and open:

```text
http://127.0.0.1:8000/docs
```

You can test the REST API endpoints directly from the browser.

---

# 🗄️ Database

FitBuddy uses a local SQLite database:

```text
fitbuddy.db
```

Main tables:

```text
users
workout_plans
```

Database relationship:

```text
users
  │
  │ 1
  │
  │ 0..1
  ▼
workout_plans
```

SQLAlchemy ORM handles communication between the Python application and SQLite.

---

# 🤖 Mock AI Mode

FitBuddy supports a mock AI mode for local development and testing without making real Gemini API calls.

Set:

```env
MOCK_AI=true
```

For real Gemini execution:

```env
MOCK_AI=false
```

and configure a valid:

```env
GEMINI_API_KEY=your_api_key
```

---

# 🧪 Testing

Run the automated tests with:

```bash
pytest -q
```

The test suite covers the main end-to-end API workflow, including:

- Application health check
- Workout generation
- Feedback submission
- User API

---

# 🛡️ Security Notes

The project already uses environment-based configuration for the Gemini API key and validates user input using Pydantic.

For production use, additional security should be implemented, including:

- Authentication
- Role-based authorization
- CSRF protection
- API rate limiting
- HTTPS
- Secure secret management
- Protected admin endpoints
- Structured logging
- Production-grade database configuration

> The current admin dashboard and related endpoints should not be considered production-secure without authentication and authorization.

---

# ⚠️ Fitness Disclaimer

FitBuddy provides **AI-generated general fitness and nutrition information** for educational purposes.

The generated content should not be considered medical advice, diagnosis, treatment, or a substitute for guidance from qualified healthcare or fitness professionals.

---

# 🔮 Future Enhancements

Possible future improvements include:

- User authentication and login
- Role-based access control
- Coach/Admin accounts
- Server-generated user IDs
- PostgreSQL database support
- Workout history
- Feedback history
- Progress tracking
- Exercise analytics
- Database migrations with Alembic
- Asynchronous AI processing
- Docker support
- CI/CD pipeline
- Centralized logging and monitoring
- Improved health and safety checks
- Local/private LLM support for privacy-sensitive deployments

---

# 📖 Project Workflow Summary

```text
User
 ↓
Web Interface
 ↓
FastAPI
 ↓
Pydantic Validation
 ↓
Gemini AI
 ↓
7-Day Workout Plan
 ↓
Nutrition / Recovery Tip
 ↓
SQLAlchemy
 ↓
SQLite Database
 ↓
Jinja2 Result Page
 ↓
User Feedback
 ↓
Gemini AI
 ↓
Updated Workout Plan
```

---

# 🎓 Project Information

**Project Name:**  
FitBuddy – AI Fitness Plan Generator Using Gemini Models

**Project Type:**  
Generative AI / Web Application

**Purpose:**  
To demonstrate how Generative AI can be integrated with a modern Python web application to generate personalized fitness plans and update them according to user feedback.

---

# 📄 License

This project was developed for educational and academic purposes.

If you intend to distribute or reuse the project publicly, add an appropriate open-source license such as MIT after reviewing the licensing requirements of the project and its dependencies.

---

## ⭐ About FitBuddy

FitBuddy demonstrates the integration of:

**Generative AI + FastAPI + REST API + Pydantic + SQLAlchemy + SQLite + Jinja2**

to build an interactive AI-powered fitness planning application.

The project provides both a user-friendly browser interface and REST APIs, making it useful for learning modern Python web development and Generative AI integration.
