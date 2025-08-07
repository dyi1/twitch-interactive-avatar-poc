# Twitch IA - FastAPI Integration

A basic FastAPI application with CRUD operations for the Twitch IA project.

## Features

- ✅ FastAPI with automatic API documentation
- ✅ CORS middleware for cross-origin requests
- ✅ Pydantic models for request/response validation
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Error handling with HTTP exceptions
- ✅ Health check endpoint
- ✅ Hot reload for development

## Setup

### Prerequisites
- Python 3.8+ 
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies with uv

```bash
# Install all dependencies
uv sync

# Install with dev dependencies
uv sync --extra dev
```

### 3. Run the Application

```bash
# Method 1: Using the helper scripts (recommended)
uv run python scripts.py dev      # Development with hot reload
uv run python scripts.py start    # Production server

# Method 2: Using uv run with uvicorn directly
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Method 3: Using Python directly
uv run python main.py
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Available Endpoints

### Core Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check

### Items CRUD
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get specific item
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

## Example Usage

### Create an Item
```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Sample Item",
       "description": "This is a test item",
       "price": 29.99,
       "is_active": true
     }'
```

### Get All Items
```bash
curl -X GET "http://localhost:8000/items"
```

### Get Specific Item
```bash
curl -X GET "http://localhost:8000/items/1"
```

### Update Item
```bash
curl -X PUT "http://localhost:8000/items/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Updated Item",
       "description": "Updated description",
       "price": 39.99,
       "is_active": true
     }'
```

### Delete Item
```bash
curl -X DELETE "http://localhost:8000/items/1"
```

## Project Structure

```
twitch-ia/
├── main.py           # Main FastAPI application
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Development with uv

### Quick Commands

```bash
# Development commands using scripts.py
uv run python scripts.py dev           # Start development server
uv run python scripts.py start         # Start production server
uv run python scripts.py format        # Format code with black
uv run python scripts.py lint          # Lint code with flake8
uv run python scripts.py sort-imports  # Sort imports with isort
uv run python scripts.py test          # Run tests
uv run python scripts.py install-dev   # Install with dev dependencies
uv run python scripts.py help          # Show available commands

# Direct uv commands
uv add package-name           # Add new dependencies
uv add --dev package-name     # Add dev dependencies
uv sync                       # Update dependencies
uv sync --extra dev           # Install with dev dependencies
uv run pytest                # Run tests directly
```

### Project Structure with uv

```
twitch-ia/
├── pyproject.toml     # Project configuration and dependencies
├── uv.lock           # Locked dependency versions (auto-generated)
├── .python-version   # Python version specification
├── .venv/            # Virtual environment (auto-created by uv)
├── main.py          # Main FastAPI application
├── scripts.py       # Helper scripts for common tasks
├── requirements.txt # Legacy support (optional)
└── README.md       # This file
```

## Development Notes

- The current implementation uses in-memory storage for simplicity
- Project is configured for Python 3.8+ with uv package management
- All dependencies are managed through `pyproject.toml`
- Development tools (black, flake8, isort) are included as optional dependencies
- For production, replace with a proper database (PostgreSQL, MongoDB, etc.)
- Configure CORS properly for production environments

## Next Steps

1. Add database integration (SQLAlchemy, MongoDB, etc.)
2. Implement authentication (JWT, OAuth)
3. Add comprehensive tests with pytest
4. Add logging and monitoring
5. Create Docker configuration
6. Set up CI/CD pipeline with uv
