import os
import sys
import json
import librosa
import numpy as np
import spacy
import whisper
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# Since DLLs are now in the same folder, we just need to tell Python to look "here"
os.add_dll_directory(os.getcwd())

print("🤖 Loading AI models... this will take a moment.")
whisper_model = whisper.load_model("base")
nlp = spacy.load("en_core_web_sm")
HISTORY_FILE = "score_history.json"

def analyze_speech(audio_path):
    try:
        # 1. Transcription
        result = whisper_model.transcribe(audio_path)
        text = result.get('text', "No speech detected.")
        
        # 2. Audio Loading
        y, sr = librosa.load(audio_path, duration=60)
        intervals = librosa.effects.split(y, top_db=25) 
        pause_count = max(0, len(intervals) - 1)
        
        # 3. Score Calculation
        # Start at 100, subtract for pauses
        score = 100 - (pause_count * 3)
        final_score = min(max(score, 10), 100)
        
        # 4. History Tracking
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        
        history.append(float(final_score))
        with open(HISTORY_FILE, "w") as f:
            json.dump(history[-10:], f)
            
        return {"text": text, "score": final_score, "history": history}
        
    except Exception as e:
        # If it hits this, it prints the REAL error in your black CMD window
        print(f"❌ Actual Error: {e}")
        return {"error": str(e), "score": 0, "history": []}

@app.post("/process")
async def process_audio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        return analyze_speech(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)