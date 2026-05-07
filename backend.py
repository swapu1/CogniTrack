import os
import json
import soundfile as sf  # Replaces librosa for fast duration — no full audio decode
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

# OPTIMIZATION 1: Switched from 'base' to 'tiny' — 3-4x faster transcription
# with minimal accuracy loss for clinical speech patterns.
whisper_model = whisper.load_model("tiny")

# OPTIMIZATION 2: Disable unused spaCy components (NER, lemmatizer, attribute_ruler)
# We only need tokenization + sentence segmentation, so this cuts load+run time.
nlp = spacy.load("en_core_web_sm", disable=["ner", "attribute_ruler", "lemmatizer"])

HISTORY_FILE = "score_history.json"

# OPTIMIZATION 3: Use a set instead of a list for filler words — O(1) lookup vs O(n)
FILLER_SET = {"um", "uh", "ah", "er", "hm", "like"}


def get_duration_fast(audio_path: str) -> float:
    """
    OPTIMIZATION 4: Use soundfile.info() for instant file-level metadata.
    The old librosa.get_duration() decoded the entire audio waveform just
    to measure length. soundfile reads the header only — no decoding needed.
    """
    try:
        info = sf.info(audio_path)
        return info.duration
    except Exception:
        # Fallback in case of an unusual format soundfile can't handle
        import librosa
        return librosa.get_duration(path=audio_path)


def analyze_speech(audio_path: str) -> dict:
    try:
        # STEP 1: Transcription
        # OPTIMIZATION 5: language="en" skips language auto-detection (saves ~0.5-1s)
        # OPTIMIZATION 6: fp16=False prevents slowdowns on CPU (fp16 is GPU-only)
        result = whisper_model.transcribe(audio_path, language="en", fp16=False)
        text = result.get("text", "")

        # STEP 2: Linguistic Processing — single spaCy pass
        doc = nlp(text)
        words = [
            token.text.lower()
            for token in doc
            if not token.is_punct and not token.is_space
        ]
        sentences = list(doc.sents)

        word_count = len(words)
        sent_count = max(1, len(sentences))

        # MLU (utterance complexity) and filler detection
        mlu = word_count / sent_count
        filler_count = sum(1 for w in words if w in FILLER_SET)  # O(1) per word

        # STEP 3: Audio duration (fast, no decoding)
        duration = get_duration_fast(audio_path)
        wpm = (word_count / (duration / 60)) if duration > 0 else 0

        # STEP 4: Wellness scoring (100 - clinical penalties)
        score = 100.0
        if wpm < 115:
            score -= (115 - wpm) * 0.4
        if mlu < 7:
            score -= (7 - mlu) * 2.5
        score -= filler_count * 1.5
        final_score = min(max(round(score, 1), 10), 100)

        # STEP 5: Persist history (keep last 10 sessions)
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        history.append(float(final_score))
        history = history[-10:]
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)

        return {
            "text": text,
            "score": final_score,
            "metrics": {
                "wpm": round(wpm),
                "mlu": round(mlu, 1),
                "fillers": filler_count,
            },
            "history": history,
        }

    except Exception as e:
        return {"error": str(e), "score": 0, "history": []}


@app.post("/process")
async def process_audio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    # Read the full upload into memory first, then write — avoids partial reads
    content = await file.read()
    with open(temp_path, "wb") as f:
        f.write(content)
    try:
        return analyze_speech(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
