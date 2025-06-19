#!/bin/bash

# Development helper scripts for Faceless Agent Backend

cd "$(dirname "$0")/backend"

case "$1" in
    "format")
        echo "🎨 Formatting code with Black and isort..."
        poetry run black .
        poetry run isort .
        echo "✅ Code formatting complete!"
        ;;
    "lint")
        echo "🔍 Running linting checks..."
        poetry run flake8 .
        poetry run mypy .
        ;;
    "test")
        echo "🧪 Running tests..."
        poetry run pytest -v
        ;;
    "test-cov")
        echo "🧪 Running tests with coverage..."
        poetry run pytest --cov=app --cov-report=html --cov-report=term
        echo "📊 Coverage report generated in htmlcov/"
        ;;
    "dev")
        echo "🔧 Starting development server..."
        poetry run start
        ;;
    "shell")
        echo "🐚 Opening Poetry shell..."
        poetry shell
        ;;
    "install")
        echo "📦 Installing dependencies..."
        poetry install
        ;;
    "update")
        echo "⬆️  Updating dependencies..."
        poetry update
        ;;
    "add")
        if [ -z "$2" ]; then
            echo "❌ Please specify a package to add"
            echo "Usage: ./dev.sh add <package_name>"
            exit 1
        fi
        echo "➕ Adding package: $2"
        poetry add "$2"
        ;;
    "add-dev")
        if [ -z "$2" ]; then
            echo "❌ Please specify a dev package to add"
            echo "Usage: ./dev.sh add-dev <package_name>"
            exit 1
        fi
        echo "➕ Adding dev package: $2"
        poetry add --group dev "$2"
        ;;
    *)
        echo "🛠️  Faceless Agent Backend Development Helper"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  format     - Format code with Black and isort"
        echo "  lint       - Run linting (flake8 and mypy)"
        echo "  test       - Run tests"
        echo "  test-cov   - Run tests with coverage report"
        echo "  dev        - Start development server"
        echo "  shell      - Open Poetry shell"
        echo "  install    - Install dependencies"
        echo "  update     - Update dependencies"
        echo "  add        - Add a new package"
        echo "  add-dev    - Add a new dev package"
        echo ""
        echo "Examples:"
        echo "  $0 dev              # Start development server"
        echo "  $0 format           # Format all code"
        echo "  $0 test-cov         # Run tests with coverage"
        echo "  $0 add requests     # Add requests package"
        echo "  $0 add-dev pytest-mock # Add dev dependency"
        ;;
esac