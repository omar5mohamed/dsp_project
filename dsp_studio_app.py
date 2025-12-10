import streamlit as st
import os
import sys
from interface.common import load_css, render_header, convert_mp3_to_wav
from interface.modules import sampling_tab, fft_tab, denoise_tab
import soundfile as sf
import numpy as np

st.set_page_config(
    page_title="Audio Signal Studio",
    page_icon="🎚️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

with st.sidebar:
    st.title("🎚️ Studio Controls")
    
    page = st.radio(
        "Navigate",
        ["Studio Home", "Digital Conversion", "Fourier Analysis", "Noise Reduction"],
        index=0
    )
    
    st.markdown("---")


if page == "Studio Home":
    render_header("Audio Signal Studio", "Advanced Signal Processing Suite")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📤 Upload Audio File")
        
        uploaded_file = st.file_uploader("Upload Audio", type=['wav', 'mp3'], label_visibility="collapsed")
        
        if uploaded_file:
            st.session_state['uploaded_file'] = uploaded_file
            
            if uploaded_file.name.lower().endswith('.mp3'):
                with st.spinner("Converting MP3 to WAV..."):
                    wav_io = convert_mp3_to_wav(uploaded_file)
                    data, fs = sf.read(wav_io)
                    st.success(f"Converted & Loaded: {uploaded_file.name}")
            else:
                data, fs = sf.read(uploaded_file)
                st.success(f"Loaded: {uploaded_file.name}")
            
            if len(data.shape) > 1:
                data = data.mean(axis=1)
                
            st.session_state['audio_data'] = data
            st.session_state['fs'] = fs
            st.session_state['current_file'] = uploaded_file.name
            
            st.audio(uploaded_file)
            
    if 'current_file' in st.session_state:
        st.info(f"Currently analyzing: **{st.session_state['current_file']}**")

elif page == "Digital Conversion":
    sampling_tab.render()

elif page == "Fourier Analysis":
    fft_tab.render()

elif page == "Noise Reduction":
    denoise_tab.render()
