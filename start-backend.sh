#!/bin/bash

# Faceless Agent Backend Setup Script (Poetry Version)

echo "🚀 Starting Faceless Agent Backend Setup with Poetry..."

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed!"
    echo "Please install Poetry first:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    echo "or visit: https://python-poetry.org/docs/#installation"
    exit 1
fi

echo "✅ Poetry found: $(poetry --version)"

# Install dependencies
echo "📋 Installing dependencies with Poetry..."
poetry install

# Check if .env file exists
if [ ! -f "../.env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your GROQ_API_KEY"
    echo "You can copy from .env.sample and add your API key:"
    echo "  cp ../.env.sample ../.env"
    echo "  # Then edit ../.env and add your GROQ_API_KEY"
    echo ""
fi

# Check if GROQ_API_KEY is set
if [ -f "../.env" ]; then
    if ! grep -q "GROQ_API_KEY=.*[^[:space:]]" "../.env"; then
        echo "⚠️  Warning: GROQ_API_KEY appears to be empty in .env file"
        echo "Please add your Groq API key to the .env file"
        echo "Get your API key from: https://console.groq.com"
        echo ""
    fi
fi

# Run the backend
echo "🎯 Starting FastAPI backend server with Poetry..."
echo "Backend will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo "Interactive docs at: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

poetry run start