#!/bin/bash
echo "===== Waiting 5s to ensure DB is ready ====="
sleep 5
echo "===== Running db.create_all() for Recomendations-Query ====="
python -c 'import sys, os; from src.app import create_app; app = create_app(); ctx = app.app_context(); ctx.push(); from src.models import db; db.create_all(); ctx.pop()' || {
  echo "ERROR: db.create_all() failed!"
  exit 1
}
echo "===== Starting Flask Server for Recomendations-Query ====="
flask run --host=0.0.0.0 --port=8080