#!/usr/bin/env bash
# One-command setup for anim8me.
# Creates an isolated venv with uv, installs all dependencies, and runs
# Django migrations so the app is immediately runnable afterward.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Creating venv (.venv) and installing dependencies with uv..."
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt

echo "==> Running Django migrations..."
.venv/bin/python anim8me/manage.py migrate

echo
echo "Setup complete. Run the app with:"
echo "  .venv/bin/python anim8me/manage.py runserver"
echo
echo "Or try the pose-estimation notebook with:"
echo "  .venv/bin/jupyter notebook pose_estimation_mediapipe.ipynb"
