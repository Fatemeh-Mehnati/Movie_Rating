🎬 Movie Rating System (Backend)

A backend RESTful API for managing movies and user ratings, built with FastAPI, PostgreSQL, and SQLAlchemy, following a clean layered architecture (Repository / Service / Controller).

🚀 Features

Manage Movies, Directors, Genres

Assign multiple genres to a movie

Add ratings (1–10) to movies

Automatically calculate:

Average rating

Ratings count

Pagination for movie listing

Fully documented API with Swagger UI

Database migrations with Alembic

🧱 Tech Stack

Python 3.13

FastAPI

PostgreSQL

SQLAlchemy ORM

Alembic (migrations)

Pydantic (data validation)

Docker (PostgreSQL container)

📂 Project Structure
Movie_Rating/
│
├── alembic/                # Database migrations
│
├── app/
│   ├── controller/         # API route handlers
│   ├── db/                 # Database engine & session
│   ├── exceptions/         # Custom HTTP exceptions
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic layer
│   └── main.py             # Application entry point
│
├── scripts/
│   └── seed_min.sql        # Minimal seed data
│
├── .env.example            # Environment variables example
├── alembic.ini
├── pyproject.toml
└── README.md

⚙️ Environment Setup
1️⃣ Clone repository
git clone <repository-url>
cd Movie_Rating

2️⃣ Create virtual environment & install dependencies
poetry install

3️⃣ Environment variables

Create .env file based on .env.example:

DATABASE_URL=postgresql+psycopg2://postgres:12345@localhost:5434/movierating

🐘 Database Setup (PostgreSQL with Docker)
docker run -d \
  --name movie-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345 \
  -e POSTGRES_DB=movierating \
  -p 5434:5432 \
  postgres:16

🔄 Database Migrations
poetry run alembic upgrade head

🌱 Seed Initial Data (optional)
docker exec -i movie-postgres psql -U postgres -d movierating < scripts/seed_min.sql


This adds:

Sample Directors

Sample Genres

▶️ Run the Application
poetry run uvicorn app.main:app --reload


Application will be available at:

API: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

📌 API Endpoints Overview
🎥 Movies
Method	Endpoint	Description
POST	/api/v1/movies/	Create a new movie
GET	/api/v1/movies/	List movies (paginated)
⭐ Ratings
Method	Endpoint	Description
POST	/api/v1/movies/{movie_id}/ratings	Add rating to a movie
🧠 Architecture Overview

This project follows Clean Architecture principles:

Controller: Handles HTTP requests & responses

Service: Business logic and validations

Repository: Database access abstraction

Models: Database schema (SQLAlchemy)

Schemas: Input/output validation (Pydantic)

Benefits:

High maintainability

Testability

Clear separation of concerns

✅ Example API Response
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Inception",
    "release_year": 2010,
    "director": {
      "id": 1,
      "name": "Christopher Nolan"
    },
    "genres": ["Sci-Fi", "Thriller"],
    "average_rating": 8.0,
    "ratings_count": 1
  }
}

🧪 Validation Rules

Rating score must be between 1 and 10

Invalid inputs return HTTP 422

Non-existent resources return HTTP 404

📄 License

This project is developed for educational purposes.

✨ Author

Developed by Fatemeh Mehnati
Backend Developer | FastAPI | PostgreSQL