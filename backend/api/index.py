"""
Vercel Serverless Entry Point for NextGent API
This file serves as the main entry point for Vercel serverless deployment.
"""
from mangum import Mangum
from app.main import app

# Mangum handler for AWS Lambda/Vercel
handler = Mangum(app, lifespan="off")
