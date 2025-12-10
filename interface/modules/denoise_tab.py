import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import spectrogram
from core.signal_filters import apply_lowpass
from core.frequency_analysis import compute_fft
from interface.common import render_header, get_audio_download_link

def render():
    render_header("Noise Reduction", "Advanced Filtering Engine")
    
    if 'audio_data' not in st.session_state:
        st.warning("No audio source detected. Please load a file in the Studio Home.")
        return

    data = st.session_state['audio_data']
    fs = st.session_state['fs']
    
    st.markdown("### 📘 Filter Characteristics")
    st.markdown("""
    **Low-Pass Filtering** allows low-frequency components to pass through while attenuating frequencies above a specified cutoff point. This is essential for removing high-frequency noise.
    """)
    
    st.latex(r"|H(j\omega)| = \frac{1}{\sqrt{1 + (\frac{\omega}{\omega_c})^{2n}}}")
    

    
    st.markdown(r"""
    By carefully selecting the cutoff frequency $\omega_c$, we can target the noise floor while preserving the intelligibility and richness of the original signal.
    """)
    
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
        # download icon
        import io
        import base64
        buffer = io.BytesIO()
        import soundfile as sf
        sf.write(buffer, processed_data, fs, format='WAV')
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        filename = f"cleaned_{method.lower().replace(' ', '_')}.wav"
        
        href = f'<a href="data:audio/wav;base64,{b64}" download="{filename}" style="text-decoration: none; display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; background: #00FF9D; color: #0d1117; font-size: 24px; font-weight: bold;">↓</a>'
        st.markdown(href, unsafe_allow_html=True)
    

        
    st.markdown("### 📉 Magnitude Response Comparison")
    
    freqs_orig, mag_orig, _ = compute_fft(data, fs, window_type='Hann', scale='Log')
    freqs_proc, mag_proc, _ = compute_fft(processed_data, fs, window_type='Hann', scale='Log')
    
    fig_spec = go.Figure()
    
    fig_spec.add_trace(go.Scatter(
        x=freqs_orig,
        y=mag_orig,
        mode='lines',
        name='Original Signal',
        line=dict(color='#3B82F6', width=1.5),
        opacity=0.6
    ))
    
    fig_spec.add_trace(go.Scatter(
        x=freqs_proc,
        y=mag_proc,
        mode='lines',
        name='Processed Signal',
        line=dict(color='#10B981', width=1.5),
        opacity=0.9
    ))
    
    fig_spec.update_layout(
        title="Magnitude Spectrum Comparison (Log Scale)",
        xaxis_title="Frequency (Hz)",
        yaxis_title="Magnitude (dB)",
        template="plotly_dark",
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_spec, use_container_width=True)
