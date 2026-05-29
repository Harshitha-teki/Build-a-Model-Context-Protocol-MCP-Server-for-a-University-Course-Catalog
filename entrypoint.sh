#!/usr/bin/env bash
set -e

# Seed the database if needed
python -c "from data.seed_script.seed import seed_database; seed_database('./data/catalog.db')"

# Start the application
exec uvicorn src.main:app --host 0.0.0.0 --port 8080
