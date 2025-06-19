# Faceless Agent Backend

A persona-shifting AI chat agent backend powered by Groq and LangChain.

## Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Groq API key

## Installation

### 1. Install Poetry

If you don't have Poetry installed, install it:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or on macOS with Homebrew:
```bash
brew install poetry
```

### 2. Install Dependencies

Navigate to the backend directory and install dependencies:

```bash
cd backend
poetry install
```

This will create a virtual environment and install all dependencies.

### 3. Environment Setup

Create a `.env` file in the project root (one level up from backend):

```bash
cp ../.env.sample ../.env
```

Then edit the `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from: https://console.groq.com

## Running the Application

### Development Mode

```bash
poetry run start
```

Or alternatively:
```bash
poetry shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
poetry run start-prod
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Development Tools

### Code Formatting

```bash
# Format code with Black
poetry run black .

# Sort imports with isort
poetry run isort .

# Lint with flake8
poetry run flake8 .

# Type checking with mypy
poetry run mypy .
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=app

# Run specific test file
poetry run pytest tests/test_api.py
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /generate_persona` - Generate random persona
- `GET /personas` - Get all personas
- `POST /add_persona` - Add custom persona
- `POST /chat` - Send chat message
- `DELETE /personas/{id}` - Delete custom persona

## Database

The application uses SQLite with 30 pre-loaded personas. The database file (`personas.db`) is created automatically on first run.

## Architecture

- **FastAPI**: Web framework
- **LangChain**: AI orchestration
- **Groq**: LLM provider
- **SQLite**: Database
- **Pydantic**: Data validation
- **Poetry**: Dependency management