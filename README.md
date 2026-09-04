# Sign to Speech — Happy Mother's Day 💐

A simple real-time hand gesture recognition app that plays audio clips of Mother's Day phrases using OpenCV, cvzone (Teachable Machine), and Pygame.

## Gestures

| Label | Audio |
| :--- | :--- |
| `Netral` | *(silent)* |
| `Happy` | `audio/Happy.wav` |
| `Moms` | `audio/Moms.wav` |
| `Day` | `audio/Day.wav` |
| `ILoveYou` | `audio/ILoveYou.wav` |
| `Mom` | `audio/Mom.wav` |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Or with Conda:
```bash
conda env create -f environment.yml
conda activate hariibu
```

## Run

```bash
python main.py
```

Press **`q`** to quit.

> **Note:** The default camera index is `1` (DroidCam). If you're using a built-in webcam, change `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)` in `main.py`.
