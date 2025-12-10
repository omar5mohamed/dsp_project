# Frontend Code Explanation (Beginner's Guide)

This guide explains the "Face" of the application—the User Interface (UI).

---

## 1. `dsp_studio_app.py`

**The Goal:** The "Main Manager" of the app. It decides what page to show and handles the initial file upload.

```python
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
```

**Key Parts Explained**:
- `st.set_page_config(...)`: Tells the browser tab name and to use a "Wide" layout.
- `with st.sidebar: ... st.radio(...)`: Creates the side menu. Whatever you click (e.g., "Noise Reduction") gets saved in `page`.
- `if page == ...`: The Traffic Cop. It checks what `page` is active and runs that specific code.
- `st.session_state`: The app's "Short-Term Memory". It remembers your uploaded song when you switch tabs, so you don't have to upload it again.

---

## 2. `interface/common.py`

**The Goal:** The "Stylist". It makes the app look Premium.

### `load_css` Function

```python
def load_css():
    """
    Injects custom CSS for a premium look.
    """
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;400;600;700&display=swap');

        /* Global Styles */
        html, body, [class*="css"] {
            font-family: 'Roboto Mono', monospace;
            background-color: #0d1117;
            color: #e6edf3;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #00FF9D;
        }
        
        /* Buttons */
        .stButton > button {
            background: transparent;
            color: #00FF9D;
            border: 2px solid #00FF9D;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
        }
        
        .stButton > button:hover {
            background: #00FF9D;
            color: #0d1117;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.6);
            transform: translateY(-2px);
        }

        /* ... scrollbar and uploader styles ... */
        </style>
    """, unsafe_allow_html=True)
```

**Key Parts Explained**:
- `st.markdown("<style>...</style>")`: Streamlit normally doesn't let you hack the design. We "trick" it by injecting raw HTML code (CSS) that overrides the default colors with our dark theme and green highlights.

---

## 3. `interface/modules/denoise_tab.py`

**The Goal:** The Noise Reduction Page.

### `render` Function

```python
def render():
    render_header("Noise Reduction", "Advanced Filtering Engine")
    
    if 'audio_data' not in st.session_state:
        st.warning("No audio source detected. Please load a file in the Studio Home.")
        return

    data = st.session_state['audio_data']
    fs = st.session_state['fs']
    
    # ... explanatory text ...
    
    st.markdown("### 🎛️ Parameter Adjustment")
    
    method = "Low-pass Filter"
    
    cutoff = st.slider(
        "Cutoff Frequency (Hz)",
        min_value=100,
        max_value=int(fs/2)-100,
        value=3000,
        step=100
    )
    processed_data = apply_lowpass(data, fs, cutoff)
            
    st.markdown("### 🎧 A/B Monitoring")
    
    st.markdown("**Original Signal**")
    st.audio(data, sample_rate=fs)
    
    st.markdown("**Processed Signal**")
    
    col_audio, col_dl = st.columns([6, 1])
    
    with col_audio:
        st.audio(processed_data, sample_rate=fs)
        
    with col_dl:
        # ... download button code ...
        pass
```

**Key Parts Explained**:
- `cutoff = st.slider(...)`: Creates the knob you slide.
- `processed_data = apply_lowpass(...)`: Instantly sends your audio + knob position to the DSP "Brain" to get the cleaned audio.
- `st.audio(...)`: Creates the two music players so you can hear "Before" vs "After".

---

## 4. `interface/modules/fft_tab.py`

**The Goal:** The Frequency Visualizer.

### `render` Function

```python
def render():
    # ... header and explanations ...

    st.markdown("### 🎛️ Controls")
    scale = st.radio(
        "Magnitude Scale",
        ["Linear", "Log"],
        horizontal=True,
        label_visibility="collapsed"
    )
        
    freqs, magnitude_linear, phase = compute_fft(data, fs, window_type='Hann', scale='Linear')

    if scale == "Log":
        magnitude = 20 * np.log10(magnitude_linear + 1e-10)
    else:
        magnitude = magnitude_linear
    
    st.markdown("### 📊 Spectrum")
    
    fig_mag = go.Figure()
    
    fig_mag.add_trace(go.Scatter(
        x=freqs,
        y=magnitude,
        mode='lines',
        name='Magnitude',
        line=dict(color='#8B5CF6', width=1.5),
        fill='tozeroy',
        fillcolor='rgba(139, 92, 246, 0.2)'
    ))
    
    fig_mag.update_layout(
        title="Magnitude Spectrum",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude (dB)" if scale == "Log" else "Magnitude",
        template="plotly_dark",
        height=500
    )
    
    st.plotly_chart(fig_mag, use_container_width=True)
```

**Key Parts Explained**:
- `scale = st.radio(...)`: simple toggle switch for "Linear" vs "Log" view.
- `compute_fft(...)`: Calls the math library to analyze the sound.
- `go.Figure()` ... `st.plotly_chart(...)`: Draws the interactive purple graph on the screen.

---

## 5. `interface/modules/sampling_tab.py`

**The Goal:** The Retro Simulator (ADC).

### `render` Function

```python
def render():
    # ... setup ...
    
    new_fs = st.slider(
        "Sampling Rate (Hz)", 
        min_value=1000, 
        max_value=44100, 
        value=fs if fs <= 44100 else 44100,
        step=1000
    )
    
    n_bits = st.slider(
        "Quantization Bits", 
        min_value=2, 
        max_value=16, 
        value=8
    )
    
    # ... calculations ...

    resampled_signal, t_resampled = sample_signal(data, fs, new_fs)
    
    quantized_signal, error = quantize_signal(resampled_signal, n_bits)
    
    # ... plotting code ...
    
    fig.add_trace(go.Scatter(
        x=t_new_plot, 
        y=y_new_plot,
        mode='lines+markers',
        name=f'Sampled ({new_fs}Hz) & Quantized ({n_bits}-bit)',
        line=dict(color='#EF4444', width=2, shape='hv'), # 'hv' for step-like
        marker=dict(size=4)
    ))
```

**Key Parts Explained**:
- `new_fs`: Controls "Time" quality (muffled sound).
- `n_bits`: Controls "Volume" precision (static noise).
- `shape='hv'`: Tells the graph to draw "Steps" instead of lines, proving that digital audio is blocky!
