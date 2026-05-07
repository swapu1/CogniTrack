import streamlit as st
import requests
import json
import random
import os

# 1. Page Configuration
st.set_page_config(page_title="CogniTrack Pro", page_icon="🧠", layout="wide")

# 2. Premium CSS Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; min-width: 320px; }
    
    .status-card {
        padding: 12px; border-radius: 10px; margin-bottom: 8px; border: 1px solid #30363d;
        display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem;
    }
    .status-done { background-color: rgba(35, 134, 54, 0.15); border-left: 5px solid #238636; }
    .status-active { background-color: rgba(255, 170, 0, 0.1); border-left: 5px solid #ffaa00; }
    .status-pending { background-color: rgba(248, 81, 73, 0.1); border-left: 5px solid #30363d; opacity: 0.6; }
    
    .stMetric { background-color: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: 600; }
    
    .coming-soon {
        background-color: #1f6feb; color: white; padding: 4px 8px; 
        border-radius: 5px; font-size: 0.8rem; font-weight: bold; margin-left: 10px;
    }
    
    .disease-card {
        background-color: #1c2128; border: 1px solid #30363d; 
        padding: 15px; border-radius: 10px; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data & Task Loading
def load_all_data():
    if os.path.exists("score_history.json"):
        with open("score_history.json", "r") as f:
            h = json.load(f)
    else:
        h = []
    
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            t = json.load(f)
    else:
        t = [{"name": "The Cookie Theft", "image_file": "cookie_theft.png", "description": "Kitchen scene."}]
    return h, t

history, tasks = load_all_data()

if 'current_task' not in st.session_state:
    st.session_state.current_task = random.choice(tasks)

# 4. SIDEBAR
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-top: 20px;">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=90) 
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("🛡️ Patient Portal")
    st.write("**Patient:** Swapnil S.")
    st.write("**ID:** SW-2026-04")
    st.divider()
    
    st.subheader("🗓️ Clinical Progress")
    display_limit = max(4, len(history) + 3)
    
    for i in range(1, display_limit + 1):
        if len(history) >= i:
            st.markdown(f'<div class="status-card status-done"><span>Week {i}</span><strong style="color: #238636;">DONE</strong></div>', unsafe_allow_html=True)
        elif i == len(history) + 1:
            st.markdown(f'<div class="status-card status-active"><span>Week {i}</span><strong style="color: #ffaa00;">ACTIVE</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-card status-pending"><span>Week {i}</span><strong style="color: #6e7681;">LOCKED</strong></div>', unsafe_allow_html=True)
            
    st.divider()
    st.info(f"Total Database Tasks: **{len(tasks)} Images**")

# 5. MAIN INTERFACE
st.title("🧠 CogniTrack: Clinical Assessment")

tab1, tab2, tab3, tab4 = st.tabs(["📖 Introduction", "🚀 Current Assessment", "📈 Progress Graph", "🧬 Biometrics (Beta)"])

# --- UPDATED INTRODUCTION TAB ---
with tab1:
    st.markdown("### Welcome to Cognitive Tracking")
    st.write("Cognitive tracking is a proactive wellness monitor for your brain. By briefly analyzing subtle patterns, pacing, and vocabulary in your speech over time, CogniTrack monitors your cognitive vitality and detects early shifts long before they become noticeable.")
    
    col_stats, col_img = st.columns([1.5, 1], gap="large")
    
    with col_stats:
        st.markdown("#### 📊 Quick Global Statistics")
        st.markdown("""
        * **55 Million:** People living with significant cognitive decline globally.
        * **1 in 3 Seconds:** A new case is identified worldwide.
        * **75% Undiagnosed:** Most early-stage shifts go unnoticed without active tracking.
        * **Not Just Aging:** While age is a risk factor, severe cognitive decline is not a normal part of getting older.
        """)
        
    with col_img:
        try:
            st.image("intro_brain.png", use_container_width=True, caption="Longitudinal tracking detects subtle drifts.")
        except:
            st.info("🖼️ [Place 'intro_brain.png' in the directory]")

    st.divider()
    
    # Diseases Section
    st.markdown("### 🧠 Common Types of Cognitive Decline")
    st.write("Dementia is an umbrella term for conditions causing severe cognitive decline. Here are the most common specific conditions:")
    
    d1, d2 = st.columns(2, gap="large")
    
    with d1:
        st.markdown("""
        <div class="disease-card">
            <h4 style="color: #58a6ff;">1. Alzheimer's Disease (60-70%)</h4>
            <p>Caused by abnormal protein build-up (amyloid plaques and tau tangles) in the brain. It typically starts in the hippocampus, primarily affecting learning and short-term memory first.</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image("alzheimers_brain.png", use_container_width=True) # PLACEHOLDER IMAGE
        except:
            st.caption("[Add 'alzheimers_brain.png' here]")

        st.markdown("""
        <div class="disease-card">
            <h4 style="color: #58a6ff;">3. Lewy Body Dementia (5-10%)</h4>
            <p>Abnormal balloon-like clumps of protein develop inside nerve cells. Early signs include severe fluctuations in alertness, visual hallucinations, and Parkinson-like movement issues.</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image("lewy_body_brain.png", use_container_width=True) # PLACEHOLDER IMAGE
        except:
            st.caption("[Add 'lewy_body_brain.png' here]")

    with d2:
        st.markdown("""
        <div class="disease-card">
            <h4 style="color: #58a6ff;">2. Vascular Dementia (20%)</h4>
            <p>Occurs due to restricted blood flow to the brain, often linked to strokes, high blood pressure, or diabetes. It primarily impacts judgment, planning, and causes slowed thinking.</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image("vascular_brain.png", use_container_width=True) # PLACEHOLDER IMAGE
        except:
            st.caption("[Add 'vascular_brain.png' here]")

        st.markdown("""
        <div class="disease-card">
            <h4 style="color: #58a6ff;">4. Frontotemporal Dementia (FTD)</h4>
            <p>A leading cause of early-onset decline. It involves progressive nerve loss in the frontal and temporal lobes, causing drastic changes in personality, empathy, or language abilities.</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image("ftd_brain.png", use_container_width=True) # PLACEHOLDER IMAGE
        except:
            st.caption("[Add 'ftd_brain.png' here]")

    st.divider()
    
    st.markdown("### 🛡️ Prevention & Quality of Life")
    st.write("The brain is highly adaptable. You can actively build cognitive reserve and improve your quality of life through daily habits:")
    st.markdown("""
    * 🏃 **Stay Active:** Regular physical exercise increases blood flow and oxygen to the brain.
    * 🗣️ **Stay Social:** Engaging in daily conversations builds strong neural pathways.
    * 💤 **Rest Well:** 7-8 hours of quality sleep helps the brain clear out daily toxins.
    * 🥗 **Eat Smart:** Diets rich in Omega-3s and antioxidants support long-term mental clarity.
    """)

# --- ASSESSMENT TAB ---
with tab2:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        task = st.session_state.current_task
        st.subheader(f"Target Task: {task['name']}")
        
        try:
            st.image(task['image_file'], use_container_width=True)
        except:
            st.error(f"File '{task['image_file']}' missing in folder!")
            
        st.info(f"**Instructions:** {task.get('description', 'Describe this scene.')}")
        
        if st.button("🔄 Shuffle Picture (1 of 10)"):
            new_task = random.choice([t for t in tasks if t != st.session_state.current_task])
            st.session_state.current_task = new_task
            st.rerun()

    with col_right:
        st.subheader("🎙️ Voice Submission")
        audio = st.file_uploader("Upload .wav or .mp3", type=['wav', 'mp3'])
        
        if audio:
            with st.spinner("AI analyzing speech patterns..."):
                try:
                    res = requests.post("http://127.0.0.1:8000/process", 
                                        files={"file": (audio.name, audio.getvalue())})
                    
                    if res.status_code == 200:
                        data = res.json()
                        if "error" not in data:
                            score_val = float(data.get('score', 0))
                            st.metric("Wellness Score", f"{score_val}%")
                            st.progress(max(0.0, min(1.0, score_val / 100)))
                            
                            st.markdown("### Clinical Markers")
                            m = data.get('metrics', {})
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Pace (WPM)", m.get('wpm', 'N/A'))
                            c2.metric("MLU", m.get('mlu', 'N/A'))
                            c3.metric("Fillers", m.get('fillers', 'N/A'))
                            
                            with st.expander("📝 View Transcription Details"):
                                st.write(data.get('text', 'No text available.'))
                            
                            if st.button("✅ Confirm & Save Week"):
                                history.append(score_val)
                                with open("score_history.json", "w") as f:
                                    json.dump(history, f)
                                st.success(f"Week {len(history)} data successfully stored.")
                                st.rerun()
                        else:
                            st.error(f"AI Error: {data['error']}")
                    else:
                        st.error(f"Backend Server Error: {res.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend Not Running! Start 'backend.py' in your command prompt.")

# --- PROGRESS GRAPH TAB ---

with tab3:
    st.subheader("📈 Long-term Cognitive Stability")
    if len(history) > 0:
        st.line_chart(history)
        st.caption(f"Historical Trend for **Swapnil S.**")
    else:
        st.info("No data points available yet. Complete Week 1 to generate the graph.")
# --- BIOMETRICS TAB (Beta) ---
with tab4:
    st.markdown('<h3>🧬 Real-Time Physiological Tracking <span class="coming-soon">BETA TEST</span></h3>', unsafe_allow_html=True)
    st.write("This module integrates with external hardware to track physical stress and effort during cognitive load.")
    
    st.divider()
    
    col_bio1, col_bio2 = st.columns(2)
    
    with col_bio1:
        st.markdown("#### 💧 Galvanic Skin Response (GSR)")
        st.metric("Sweat Gland Activity", "--- µS", delta="Hardware Offline", delta_color="off")
        st.caption("Measures microscopic changes in sweat to detect frustration or high cognitive stress while attempting to describe complex scenes.")
        
    with col_bio2:
        st.markdown("#### ❤️ Pulse Oximetry")
        st.metric("Heart Rate / HRV", "--- BPM", delta="Hardware Offline", delta_color="off")
        st.caption("Tracks heart rate variability (HRV) and pulse spikes to identify anxiety related to word-finding difficulties (aphasia).")
        
    st.divider()
    st.info("🔌 **Arduino / Serial Interface Status:** Waiting for hardware connection on COM port...")
