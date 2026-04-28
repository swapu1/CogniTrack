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
    
    /* Coming Soon Badge */
    .coming-soon {
        background-color: #1f6feb; color: white; padding: 4px 8px; 
        border-radius: 5px; font-size: 0.8rem; font-weight: bold; margin-left: 10px;
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

# 4. SIDEBAR: INFINITE WEEKLY TRACKER
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

# --- I ADDED THE THIRD TAB HERE ---
tab1, tab2, tab3 = st.tabs(["🚀 Current Assessment", "📈 Progress Graph", "🧬 Biometrics (Beta)"])

with tab1:
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
                    st.error("Backend Not Running! Start 'backend(1).py' in your command prompt.")

with tab2:
    st.subheader("📈 Long-term Cognitive Stability")
    if len(history) > 0:
        st.line_chart(history)
        st.caption(f"Historical Trend for **Swapnil S.**")
    else:
        st.info("No data points available yet. Complete Week 1 to generate the graph.")

# --- HERE IS YOUR NEW HARDWARE MENU ---
with tab3:
    st.markdown('<h3>🧬 Real-Time Physiological Tracking <span class="coming-soon">COMING SOON</span></h3>', unsafe_allow_html=True)
    st.write("This module will integrate with external hardware to track physical stress and effort during cognitive load.")
    
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
