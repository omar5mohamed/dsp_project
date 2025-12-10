import streamlit as st
import numpy as np
import plotly.graph_objects as go
from core.frequency_analysis import compute_fft
from interface.common import render_header

def render():
    render_header("Fourier Analysis", "Frequency Domain Analysis")
    
    if 'audio_data' not in st.session_state:
        st.warning("No audio source detected. Please load a file in the Studio Home.")
        return

    data = st.session_state['audio_data']
    fs = st.session_state['fs']
    
    st.markdown("### 🔍 Signal Analysis")
    
    st.markdown("""
    **Fourier Analysis** breaks down complex waveforms into their elemental frequency components. 
    By converting the signal from the *Time Domain* to the *Frequency Domain*, we can visualize the spectral fingerprint of the audio.
    
    **Methodology**: We utilize the **Fast Fourier Transform (FFT)** algorithm to rapidly calculate the Discrete Fourier Transform (DFT), enabling real-time spectral analysis.
    """)
    
    st.latex(r"X[k] = \sum_{n=0}^{N-1} x[n] e^{-j2\pi \frac{kn}{N}}")
    
    st.markdown("""
    Here, $x[n]$ represents the discrete signal, $X[k]$ denotes the spectral coefficients, $N$ is the window length, and $k$ represents the frequency bin.
    
    **Understanding the Spectrum**:
    The plot below shows the **Magnitude Spectrum**, which represents the strength of each frequency component present in the signal. 
    - **Low frequencies** (bass) appear on the left.
    - **High frequencies** (treble) appear on the right.
    - The **height** of the curve indicates how loud that specific frequency is relative to others.
    """)
    
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
    
    st.markdown("### 🏔️ Peak Frequencies")
    
    if len(magnitude) > 1:
        mag_no_dc = magnitude[1:]
        freqs_no_dc = freqs[1:]
        
        top_indices = np.argsort(mag_no_dc)[-5:][::-1]
        top_freqs = freqs_no_dc[top_indices]
        top_mags = mag_no_dc[top_indices]
        
        cols = st.columns(5)
        for i, (f, m) in enumerate(zip(top_freqs, top_mags)):
            with cols[i]:
                if scale == "Linear":
                    mag_str = f"{m:.5f}"
                else:
                    mag_str = f"{m:.2f}"
                    
                st.markdown(f"""
                <div style="background: #1F2937; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #374151;">
                    <div style="color: #9CA3AF; font-size: 0.8rem;">Peak {i+1}</div>
                    <div style="font-weight: bold; color: #60A5FA;">{f:.1f} Hz</div>
                    <div style="font-size: 0.8rem;">{mag_str}</div>
                </div>
                """, unsafe_allow_html=True)

