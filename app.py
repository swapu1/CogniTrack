import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="CogniTrack", layout="wide")
st.title("🧠 CogniTrack: Cognitive Wellness Tracker")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Weekly Task")
    st.image("cookie_theft.png", use_container_width=True)

with col2:
    st.subheader("Recording Upload")
    uploaded_file = st.file_uploader("Upload your recording", type=['wav', 'mp3', 'm4a'])

    if uploaded_file:
        with st.spinner("Analyzing speech patterns..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post("http://localhost:8000/process", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.metric("Wellness Score", f"{data['score']}/100")
                    
                    # Display the Weekly Trend
                    st.subheader("Weekly Progress")
                    history_df = pd.DataFrame(data['history'], columns=["Wellness Score"])
                    st.line_chart(history_df)
                    
                    if data['score'] < 75:
                        st.warning("Note: Your score is lower than usual. Consider sharing this with a professional.")
                else:
                    st.error("Backend Error. Make sure Terminal 1 is running.")
            except Exception as e:
                st.error(f"Connection failed: {e}")