import os
import json
import librosa
import spacy
import whisper
from fastapi import FastAPI, UploadFile, File

# DLL Fix for Windows
try:
    os.add_dll_directory(os.getcwd())
except Exception:
    pass

app = FastAPI()

print("🤖 Clinical AI Engine Loading...")
# 'base' is the best balance of speed and accuracy for your PC
whisper_model = whisper.load_model("base")
nlp = spacy.load("en_core_web_sm")
HISTORY_FILE = "score_history.json"

def analyze_speech(audio_path):
    try:
        # 1. AI Transcription (Handled with Tokenizer stability)
        result = whisper_model.transcribe(audio_path)
        text = result.get('text', "")
        
        # 2. Linguistic Processing
        doc = nlp(text)
        words = [token.text.lower() for token in doc if not token.is_punct]
        sentences = list(doc.sents)
        
        # MLU (Complexity) & Fillers (Stalling)
        mlu = len(words) / max(1, len(sentences))
        fillers = ["um", "uh", "ah", "er", "hm", "like"]
        filler_count = sum(1 for word in words if word in fillers)
        
        # 3. Audio Timing (Pace)
        duration = librosa.get_duration(path=audio_path)
        wpm = (len(words) / (duration / 60)) if duration > 0 else 0
        
        # 4. Scoring Formula (100 - clinical penalties)
        score = 100.0
        if wpm < 115: score -= (115 - wpm) * 0.4
        if mlu < 7: score -= (7 - mlu) * 2.5
        score -= (filler_count * 1.5)
        final_score = min(max(round(score, 1), 10), 100)

        # 5. Save Score to History
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        
        history.append(float(final_score))
        with open(HISTORY_FILE, "w") as f:
            json.dump(history[-10:], f)

        return {
            "text": text,
            "score": final_score,
            "metrics": {"wpm": round(wpm), "mlu": round(mlu, 1), "fillers": filler_count},
            "history": history
        }
    except Exception as e:
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
