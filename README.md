# anim8me

A Django app that runs real-time pose estimation (via MediaPipe + OpenCV) on a
webcam feed or a video file, with a Jupyter notebook demo of the underlying
pose-tracking / replay logic.

## Setup

One command installs everything (uses [uv](https://docs.astral.sh/uv/) to create
an isolated virtualenv — no system-wide installs, no sudo):

```bash
./setup.sh
```

This creates `.venv/`, installs all dependencies from `requirements.txt`, and
runs Django migrations. After it finishes you're ready to run the app.

## Run the Django app

```bash
.venv/bin/python anim8me/manage.py runserver
```

Then visit:

- `/` — home page
- `/webcam/` — webcam UI
- `/pose_estimation/` — MJPEG stream with live pose landmarks drawn over `anim8me/mainapp/video.mp4`
  (swap the hardcoded `cv2.VideoCapture(0)` back in `views.py` to use a real webcam instead)
- `/motion_visualization/` — motion visualization page
- `/api/landmarks/` — JSON API exposing the most recently captured landmarks

## Run the notebook

```bash
.venv/bin/jupyter notebook pose_estimation_mediapipe.ipynb
```

The notebook opens a live `cv2.imshow` window reading from your **webcam**
(not a file) — press `q` in that window to stop each cell. It:

1. Captures webcam frames, runs MediaPipe Pose on each, and pickles the
   landmark history to `pose_landmarks_history.pkl`.
2. Replays the saved landmarks on a blank canvas as a sanity check.

## Requirements

- Python 3.11
- [uv](https://docs.astral.sh/uv/) (for `./setup.sh`)
- A webcam, for the live-capture paths (`/webcam/`, the notebook)

## Notes

- `mediapipe` is pinned to `0.10.21` — newer `mediapipe` releases (1.x)
  dropped the legacy `mp.solutions` API this code depends on.
- Generated artifacts (`db.sqlite3`, `*.pkl`, `*.avi`, `.venv/`) are gitignored;
  `setup.sh` regenerates what's needed.
