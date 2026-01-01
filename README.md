# 🎬 Movie Rating System (Backend)

A backend RESTful API for managing movies and user ratings, built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, following a clean **layered architecture**.

---

## 🚀 Features

- Manage **Movies**, **Directors**, and **Genres**
- Add and retrieve **movie ratings**
- Calculate **average rating** per movie
- Pagination support for movie listing
- Clean layered architecture:
  - Controller
  - Service
  - Repository

---

## 🧱 Tech Stack

- **Python 3.13**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **Docker**
- **Poetry**

---

## 📁 Project Structure

```text
Movie_Rating/
├── alembic/                # Database migrations
│   ├── versions/
│   └── env.py
├── app/
│   ├── controller/         # API route handlers
│   ├── db/                 # Database engine & session
│   ├── exceptions/         # Custom HTTP exceptions
│   ├── models/             # SQLAlchemy models
│   ├── repositories/       # Data access layer
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic layer
│   └── main.py             # Application entry point
├── scripts/
│   └── seed_min.sql        # Minimal seed data
├── .env.example            # Environment variables example
├── alembic.ini
├── pyproject.toml
└── README.md



---

## ⚙️ Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:12345@localhost:5434/movierating

🐘 Run PostgreSQL with Docker
docker run -d \
  --name movie-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=12345 \
  -e POSTGRES_DB=movierating \
  -p 5434:5432 \
  postgres:16

🧬 Database Migration
poetry run alembic upgrade head

▶️ Run the Application
poetry run uvicorn app.main:app --reload

Open Swagger UI:
http://127.0.0.1:8000/docs

🧪 Seed Initial Data (Optional)
docker exec -i movie-postgres psql -U postgres -d movierating < scripts/seed_min.sql

📌 Example API Endpoints
Create Movie

POST /api/v1/movies/
{
  "title": "Inception",
  "director_id": 1,
  "release_year": 2010,
  "cast": "Leonardo DiCaprio",
  "genres": [4, 5]
}

List Movies

GET /api/v1/movies/?page=1&page_size=10

Add Rating

POST /api/v1/movies/{movie_id}/ratings

{
  "score": 8
}

👩‍💻 Author

Fatemeh Mehnati
