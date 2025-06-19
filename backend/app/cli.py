#!/usr/bin/env python3
"""
Entry point script for starting the Faceless Agent backend server.
"""
import uvicorn

def main():
    """Start the FastAPI server in development mode."""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

def main_prod():
    """Start the FastAPI server in production mode."""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    main()