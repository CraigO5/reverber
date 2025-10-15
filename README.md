# Reverber

Reverber is a web application that allows users to apply various reverb effects to `.wav` audio files. It includes multiple types of reverberation, such as simple delay, Schroeder reverb, and convolution with room impulse responses (RIRs).

---

## Features

- Upload `.wav` audio files
- Apply different reverb effects:
  - Simple
  - Schroeder
  - RIR (Room Impulse Response)
- Download the processed audio
- FastAPI backend with real-time audio processing
- Next.js frontend with drag-and-drop support

---

## Tech Stack

- **Frontend:** Next.js, React, Tailwind CSS, React Dropzone
- **Backend:** FastAPI, Python, SciPy, NumPy
- **Audio Processing:** Custom Python reverb functions, convolution-based RIR

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- `pip` and `npm` installed

### Backend Setup

Navigate to the backend folder:

```bash
cd backend
```
Create and activate a virtual environment:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```
Install dependencies:
```
pip install -r requirements.txt
```
Run the backend server:
```
uvicorn main:app --reload
```
The API will run on http://127.0.0.1:8000.
### Frontend Setup

Navigate to the frontend folder:
```
cd frontend
```
Install dependencies:
```
npm install
```
Run the frontend server:
```
npm run dev
```
The app will run on http://localhost:3000.

## Usage

Open the app in your browser.

Drag and drop a .wav file into the upload area.

Select the desired reverb type.

Click Apply Reverb to process the audio.

Download the reverberated file when prompted.

Git Ignore Recommendations

Make sure your .gitignore includes:
```
# Python
venv/
__pycache__/

# Audio files
*.wav
*.zip
```
This prevents large files or virtual environments from being committed.
License

This project is MIT licensed.
