#!/bin/bash
# Starts backend (:8001) and frontend (:3000), stops both on Ctrl+C.
set -e
cd "$(dirname "$0")"

cleanup() {
  echo "Stopping servers..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
}
trap cleanup EXIT INT TERM

(cd backend && source .venv/bin/activate && python manage.py runserver 0.0.0.0:8001) &
BACKEND_PID=$!

(cd frontend && npm run dev) &
FRONTEND_PID=$!

echo "Backend:  http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop both."

wait
