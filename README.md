# Blog App

A backend-only blog application built with **FastAPI** that focuses on anime content. The application automatically generates and publishes **three AI-written anime blogs every hour** using **Gemini Flash**, while also allowing authenticated users to create and manage their own blog posts.

> **Note:** This repository contains only the backend API. A frontend has not been implemented yet.

---

## Features

* OAuth2 authentication
* User registration and login
* Automatic AI-generated anime blog publishing
* Three AI-generated blogs published every hour
* User-created blog posts
* Full CRUD operations for blogs
* Users can edit and delete only their own blogs
* PostgreSQL database
* Automatic API documentation with Swagger UI
* Docker support
* Database migrations with Alembic

---

## Tech Stack

| Technology   | Purpose                     |
| ------------ | --------------------------- |
| FastAPI      | Web framework               |
| PostgreSQL   | Database                    |
| SQLAlchemy   | ORM                         |
| Pydantic     | Data validation and schemas |
| Celery       | Background task processing  |
| Gemini Flash | AI blog generation          |
| OAuth2       | Authentication              |
| Alembic      | Database migrations         |
| Docker       | Containerization            |
| uv           | Package management          |

---

## AI Blog Generation

The application automatically generates **three anime-related blog posts every hour** using **Gemini Flash**.

The generation process runs as a scheduled **Celery** background task, allowing AI-generated content to be published independently of user requests.

Currently, only **anime** blogs are generated automatically.

---

## Authentication

The API uses **OAuth2** authentication to secure protected endpoints.

Authenticated users can:

* Create blogs
* Update their own blogs
* Delete their own blogs
* View blog data

Users cannot modify blogs created by other users.

---

## Blog Operations

Currently supported operations include:

* Create a blog
* Retrieve a blog by ID
* Update your own blog
* Delete your own blog

At the moment, blog retrieval is supported **by blog ID**.

---

## API Documentation

After starting the server, interactive API documentation is available at:

* `/docs` — Swagger UI
* `/redoc` — ReDoc

---

## Installation

### Clone the repository

```bash
git clone <your-repository-url>
cd blog-app
```

### Install dependencies

```bash
uv sync
```

### Configure environment variables

Create a `.env` file in the project root and configure the required environment variables.

Example:

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

GEMINI_API_KEY=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
```

Configure additional variables as required by your project.

---

## Database Migration

Run the database migrations using Alembic.

```bash
alembic upgrade head
```

---

## Running the Application

Start the FastAPI server:

```bash
uv run uvicorn app.main:app --reload
```

Start the Celery worker:

```bash
celery -A app.celery worker --loglevel=info
```

Start the Celery Beat scheduler:

```bash
celery -A app.celery beat --loglevel=info
```

> Replace `app.main` and `app.celery` with your actual module paths if they differ.

---

## Docker

The project includes Docker support for running the application and its services in containers.

Build and start the services using Docker Compose:

```bash
docker compose up --build
```

---

## Project Structure

```text
.
├── alembic/
├── app/
│   ├── api/
│   ├── auth/
│   ├── crud/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   ├── database.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

The exact structure may vary depending on your implementation.

---

## Future Improvements

* Search blogs by title
* Filtering and pagination
* Categories and tags
* Blog images
* AI-generated summaries
* Comments
* Likes
* Bookmarks
* Rich text editor support
* Full-text search
* Frontend application

---

## License

This project currently does not have a license.

---

## Author

Developed as a backend learning project using FastAPI, PostgreSQL, SQLAlchemy, Celery, and Google's Gemini Flash.
