import numpy as np
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from scipy.io import wavfile
import reverb
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/apply_reverb/")
async def apply_reverb(file: UploadFile = File(...), reverb_type: str = Form(...)):
    contents = await file.read()

    # Temporarily save the file to disk
    with open("audio.wav", "wb") as f:
        f.write(contents)
    
    # Separates file into sample rate and 1D integer array (format for our functions)
    sample_rate, audio = wavfile.read("audio.wav")

    audio = audio.astype(np.float32) / 32768  

    # Applies reverb depending on reverb_type with default values unless unknown
    if reverb_type == "simple":
        processed = reverb.simple(audio, sample_rate, 2, 10)
    elif reverb_type == "comb":
        processed = reverb.comb(audio, sample_rate, 10)
    elif reverb_type == "allpass":
        processed = reverb.allpass(audio, sample_rate, 10)
    elif reverb_type == "schroeder":
        processed = reverb.schroeder(audio, sample_rate, 10)
    elif reverb_type == "rir":
        BASE_DIR = Path(__file__).parent
        rir_path = BASE_DIR / "rir" / "rir.wav"
        processed = reverb.rir(audio, rir_path)
    else:
        return {"error": "Unknown reverb type"}
    
    reverbed = np.clip(processed, -1, 1)
    normalized = (reverbed * 2**15).astype(np.int16)

    # Writes the output to file
    wavfile.write(f"{file.filename}_{reverb_type}_reverb.wav", sample_rate, normalized)
    return FileResponse(f"{file.filename}_{reverb_type}_reverb.wav")