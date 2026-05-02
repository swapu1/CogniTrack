ai based early cognitive decline tracker front and backend
# 🧠 CogniTrack: Setup Guide

Welcome to CogniTrack! This guide will help you get the project running on your computer. Please follow the steps carefully based on whether you are using a Mac or Windows.

---

## 📂 1. The Exact File Structure
Before you do anything, make sure your downloaded folder looks **exactly** like this. If files are missing or in the wrong place, the app will crash.
```text
CogniTrack/
│
├── app.py                 
├── backend(1).py          
├── tasks.json             
├── score_history.json     
├── requirements.txt       
│
└── /images                
    ├── cookie_theft.png
    ├── picnic.png
    ├── circus.png
    ├── park.png
    ├── grocery.png
    ├── street.png
    ├── library.png
    ├── garden.png
    ├── beach.png
    └── classroom.png

    ***

### A Quick Note Before You Upload:
Make sure you actually create a `requirements.txt` file in your folder before pushing to GitHub. Just make a text file, name it `requirements.txt`, and paste this inside it:

```text
streamlit
fastapi
uvicorn
openai-whisper
librosa
numpy
plotly
spacy
fpdf
pyserial
pyaudio

🍎 2. Setup Instructions for MAC Users
Step 1: Install System Audio Tools
Open your Terminal app. You need an app called Homebrew to install the audio decoder. If you don't have Homebrew, install it from brew.sh first. Then run this command:
brew install ffmpeg portaudio
Step 2: Install Python Libraries
In the same Terminal, navigate to the CogniTrack folder (using cd /path/to/CogniTrack) and run these two commands one after the other:
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm


Step 3: Run the App (Requires TWO Terminals)
You must open two separate Terminal windows. Make sure both are inside the CogniTrack folder.

Terminal 1 (Start the Brain): Run python3 "backend(1).py"

Terminal 2 (Start the Face): Run python3 -m streamlit run app.py

(Note: Your Mac might ask for Microphone permissions the first time you run it. Click "Allow".)

🪟 3. Setup Instructions for WINDOWS Users 
Step 1: The FFmpeg Audio Tool
Windows needs a special file to understand audio.

Ask the project creator to send you the ffmpeg.exe file.

Place that ffmpeg.exe file directly inside the main CogniTrack folder (right next to app.py).

Here is the simplified, no-nonsense README.md file. It lists the exact 10 images you used and gives foolproof, separate instructions for Windows and Mac.

You can copy everything inside the box below and paste it directly into your GitHub repository.

Markdown
# 🧠 CogniTrack: Setup Guide

Welcome to CogniTrack! This guide will help you get the project running on your computer. Please follow the steps carefully based on whether you are using a Mac or Windows.

---

## 📂 1. The Exact File Structure
Before you do anything, make sure your downloaded folder looks **exactly** like this. If files are missing or in the wrong place, the app will crash.
```text
CogniTrack/
│
├── app.py                 
├── backend(1).py          
├── tasks.json             
├── score_history.json     
├── requirements.txt       
│
└── /images                
    ├── cookie_theft.png
    ├── picnic.png
    ├── circus.png
    ├── park.png
    ├── grocery.png
    ├── street.png
    ├── library.png
    ├── garden.png
    ├── beach.png
    └── classroom.png
🍎 2. Setup Instructions for MAC Users
Step 1: Install System Audio Tools
Open your Terminal app. You need an app called Homebrew to install the audio decoder. If you don't have Homebrew, install it from brew.sh first. Then run this command:

Bash
brew install ffmpeg portaudio
Step 2: Install Python Libraries
In the same Terminal, navigate to the CogniTrack folder (using cd /path/to/CogniTrack) and run these two commands one after the other:

Bash
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
Step 3: Run the App (Requires TWO Terminals)
You must open two separate Terminal windows. Make sure both are inside the CogniTrack folder.

Terminal 1 (Start the Brain): Run python3 "backend(1).py"

Terminal 2 (Start the Face): Run python3 -m streamlit run app.py

(Note: Your Mac might ask for Microphone permissions the first time you run it. Click "Allow".)

🪟 3. Setup Instructions for WINDOWS Users
Step 1: The FFmpeg Audio Tool
Windows needs a special file to understand audio.

Ask the project creator to send you the ffmpeg.exe file.

Place that ffmpeg.exe file directly inside the main CogniTrack folder (right next to app.py).

Step 2: Install Python Libraries
Open Command Prompt, use cd C:\path\to\CogniTrack to get inside your folder, and run these two commands:

DOS
pip install -r requirements.txt
py -m spacy download en_core_web_sm

Here is the simplified, no-nonsense README.md file. It lists the exact 10 images you used and gives foolproof, separate instructions for Windows and Mac.

You can copy everything inside the box below and paste it directly into your GitHub repository.

Markdown
# 🧠 CogniTrack: Setup Guide

Welcome to CogniTrack! This guide will help you get the project running on your computer. Please follow the steps carefully based on whether you are using a Mac or Windows.

---

## 📂 1. The Exact File Structure
Before you do anything, make sure your downloaded folder looks **exactly** like this. If files are missing or in the wrong place, the app will crash.
```text
CogniTrack/
│
├── app.py                 
├── backend(1).py          
├── tasks.json             
├── score_history.json     
├── requirements.txt       
│
└── /images                
    ├── cookie_theft.png
    ├── picnic.png
    ├── circus.png
    ├── park.png
    ├── grocery.png
    ├── street.png
    ├── library.png
    ├── garden.png
    ├── beach.png
    └── classroom.png
🍎 2. Setup Instructions for MAC Users
Step 1: Install System Audio Tools
Open your Terminal app. You need an app called Homebrew to install the audio decoder. If you don't have Homebrew, install it from brew.sh first. Then run this command:

Bash
brew install ffmpeg portaudio
Step 2: Install Python Libraries
In the same Terminal, navigate to the CogniTrack folder (using cd /path/to/CogniTrack) and run these two commands one after the other:

Bash
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
Step 3: Run the App (Requires TWO Terminals)
You must open two separate Terminal windows. Make sure both are inside the CogniTrack folder.

Terminal 1 (Start the Brain): Run python3 "backend(1).py"

Terminal 2 (Start the Face): Run python3 -m streamlit run app.py

(Note: Your Mac might ask for Microphone permissions the first time you run it. Click "Allow".)

🪟 3. Setup Instructions for WINDOWS Users
Step 1: The FFmpeg Audio Tool
Windows needs a special file to understand audio.

Ask the project creator to send you the ffmpeg.exe file.

Place that ffmpeg.exe file directly inside the main CogniTrack folder (right next to app.py).

Step 2: Install Python Libraries
Open Command Prompt, use cd C:\path\to\CogniTrack to get inside your folder, and run these two commands:

DOS
pip install -r requirements.txt
py -m spacy download en_core_web_sm


Step 3: Run the App (Requires TWO Command Prompts)
You must open two separate Command Prompt windows. Make sure both are inside the CogniTrack folder.

Window 1 (Start the Brain): Run py "backend(1).py"

Window 2 (Start the Face): Run py -m streamlit run app.py



📦 Appendix: What goes in requirements.txt?
If you haven't made the requirements.txt file yet, simply create a text file with that exact name, and paste this list inside it:


streamlit
fastapi
uvicorn
openai-whisper
librosa
numpy
plotly
spacy
pyaudio
pyserial
fpdf
