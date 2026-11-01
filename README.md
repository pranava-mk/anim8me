# 🏃 anim8me

> Real-time pose estimation on your webcam, built with MediaPipe + Django.

A Django app that runs live pose tracking on a webcam feed or video file,
plus a Jupyter notebook demo of the underlying pose-capture / replay logic.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-092E20)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.21-00B2A9)
![License](https://img.shields.io/badge/license-none%20specified-lightgrey)

---

## ✨ What it does

- Runs **MediaPipe Pose** on a video feed and streams the annotated result
  live as MJPEG over HTTP
- Captures pose landmarks as structured JSON via a small DRF API
- A standalone notebook captures webcam pose landmarks, pickles them, and
  replays them on a blank canvas — a minimal end-to-end pose-tracking demo

## 🚀 Getting Started

One command installs everything — uses [uv](https://docs.astral.sh/uv/) to
create an isolated virtualenv, no system-wide installs, no sudo:

```bash
./setup.sh
```

This creates `.venv/`, installs every dependency from `requirements.txt`, and
runs Django migrations. You're ready to run right after.

### Requirements

- Python 3.11
- [uv](https://docs.astral.sh/uv/) (for `./setup.sh`)
- A webcam, for the live-capture paths (`/webcam/`, the notebook)

## 🖥️ Usage

**Run the Django app:**

```bash
.venv/bin/python anim8me/manage.py runserver
```

| Route | What it does |
|---|---|
| `/` | Home page |
| `/webcam/` | Webcam UI |
| `/pose_estimation/` | MJPEG stream with live pose landmarks over `mainapp/video.mp4` |
| `/motion_visualization/` | Motion visualization page |
| `/api/landmarks/` | JSON API exposing the most recently captured landmarks |

Swap the hardcoded `cv2.VideoCapture(...)` back to `cv2.VideoCapture(0)` in
`views.py` to use a live webcam instead of the bundled demo video.

**Run the notebook:**

```bash
.venv/bin/jupyter notebook pose_estimation_mediapipe.ipynb
```

Opens a live `cv2.imshow` window reading from your webcam — press `q` in that
window to stop. It captures frames, runs MediaPipe Pose on each, pickles the
landmark history, then replays the saved landmarks on a blank canvas.

## 🗂️ Project Structure

```
anim8me/
├── setup.sh                        # one-command uv-based install
├── requirements.txt
├── pose_estimation_mediapipe.ipynb # standalone pose-capture/replay demo
└── anim8me/                        # Django project
    ├── anim8me/                    # settings, urls, wsgi/asgi
    └── mainapp/
        ├── views.py                # pose estimation, streaming, API
        ├── views_api.py            # DRF landmark API
        ├── urls.py
        └── video.mp4               # bundled demo video
```

## 🧠 Notes

- `mediapipe` is pinned to `0.10.21` — newer `mediapipe` releases (1.x)
  dropped the legacy `mp.solutions` API this code depends on
- Generated artifacts (`db.sqlite3`, `*.pkl`, `*.avi`, `.venv/`) are gitignored;
  `setup.sh` regenerates what's needed

## 📦 Deployment

This needs a real server (Python runtime, webcam/video I/O, SQLite) — it
**can't run on GitHub Pages**, which only serves static files. There's no
hosted demo link for that reason. Run it locally with `./setup.sh` +
`runserver`, or deploy it to any host that runs a Python/Django process
(Render, Railway, a VM, etc.) if you want it live on the web.
