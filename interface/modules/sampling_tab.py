import streamlit as st
import numpy as np
import plotly.graph_objects as go
from core.signal_digitization import sample_signal, quantize_signal
from core.frequency_analysis import compute_fft
from interface.common import render_header, get_audio_download_link

def render():
    render_header("Digital Conversion", "ADC Simulation")
    
    if 'audio_data' not in st.session_state:
        st.warning("No audio source detected. Please load a file in the Studio Home.")
        return

    data = st.session_state['audio_data']
    fs = st.session_state['fs']
    
    # Calculate Nyquist Rate
    f_orig, mag_orig, _ = compute_fft(data, fs, window_type='Hann', scale='Linear')
    threshold = 0.01 * np.max(mag_orig)
    significant_freqs = f_orig[mag_orig > threshold]
    f_max = np.max(significant_freqs) if len(significant_freqs) > 0 else 0
    nyquist_rate = 2 * f_max
    
    st.markdown("### 📊 Signal Processing & Visualization")
    
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
    
    zoom_range = st.slider("Zoom (Samples)", 0, len(data), (0, 1000))
    start_idx, end_idx = zoom_range
    
    st.markdown(f"""
    <div class="metric-container" style="margin-top: 10px; margin-bottom: 20px; display: flex; gap: 2rem;">
        <div>
            <div style="font-size: 0.9rem; color: #9CA3AF;">Quantization Levels (L)</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #00FF9D;">{2**n_bits}</div>
        </div>
        <div>
            <div style="font-size: 0.9rem; color: #9CA3AF;">Nyquist Rate</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #00FF9D;">{nyquist_rate:.0f} Hz</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    resampled_signal, t_resampled = sample_signal(data, fs, new_fs)
    
    quantized_signal, error = quantize_signal(resampled_signal, n_bits)
    
    ratio = new_fs / fs
    start_res = int(start_idx * ratio)
    end_res = int(end_idx * ratio)
    
    fig = go.Figure()
    
    t_orig = np.arange(start_idx, end_idx) / fs
    y_orig = data[start_idx:end_idx]
    
    max_plot_points = 5000
    if len(t_orig) > max_plot_points:
        step = int(np.ceil(len(t_orig) / max_plot_points))
        t_plot = t_orig[::step]
        y_plot = y_orig[::step]
        st.caption(f"⚠️ Visualizing 1 out of every {step} samples for performance.")
    else:
        t_plot = t_orig
        y_plot = y_orig

    fig.add_trace(go.Scatter(
        x=t_plot, 
        y=y_plot,
        mode='lines',
        name='Original Signal',
        line=dict(color='#3B82F6', width=2),
        opacity=0.7
    ))
    
    t_new = t_resampled[start_res:end_res]
    y_new = quantized_signal[start_res:end_res]
    
    if len(t_new) > max_plot_points:
        step_new = int(np.ceil(len(t_new) / max_plot_points))
        t_new_plot = t_new[::step_new]
        y_new_plot = y_new[::step_new]
    else:
        t_new_plot = t_new
        y_new_plot = y_new
    
    fig.add_trace(go.Scatter(
        x=t_new_plot, 
        y=y_new_plot,
        mode='lines+markers',
        name=f'Sampled ({new_fs}Hz) & Quantized ({n_bits}-bit)',
        line=dict(color='#EF4444', width=2, shape='hv'), # 'hv' for step-like
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title="Waveform Comparison",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
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
    
    st.plotly_chart(fig, use_container_width=True)
