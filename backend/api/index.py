"""
Vercel Serverless Entry Point for NextGent API
This file serves as the main entry point for Vercel serverless deployment.
"""
from app.main import app

# Vercel expects a variable named 'app' or a function named 'handler'
# We're exporting the FastAPI app directly for Vercel's Python runtime
# Vercel will automatically wrap it with the correct ASGI server

# This is the entry point for Vercel
__all__ = ['app']
