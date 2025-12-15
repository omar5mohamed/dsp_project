# interface/common.py

import streamlit as st
import base64
import io
import soundfile as sf

def load_css():
    """
    Custom CSS for clean modern light mode
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
        }

        .main .block-container {
            background-color: #ffffff;
            padding-top: 2rem;
            padding-bottom: 3rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            margin-top: 1rem;
            max-width: 1200px;
        }

        h1, h2, h3 {
            font-weight: 700;
            color: #2563eb;
        }

        h1 {
            font-size: 2.8rem;
        }

        .stButton > button {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.65rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }

        .stButton > button:hover {
            background-color: #1d4ed8;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
        }

        [data-testid="stFileUploader"] section {
            background-color: #f1f5f9;
            border: 2px dashed #cbd5e1;
            border-radius: 10px;
            padding: 1rem;
        }

        [data-testid="stFileUploader"] section:hover {
            border-color: #2563eb;
            background-color: #e0eaff;
        }

        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle=""):
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 3rem;">
            <h1 style="font-size: 3.2rem; color: #2563eb; margin-bottom: 0.8rem;">
                {title}
            </h1>
            <p style="font-size: 1.3rem; color: #64748b; max-width: 800px; margin: 0 auto;">
                {subtitle}
            </p>
        </div>
        <hr style="border: 0; height: 2px; background: linear-gradient(to right, transparent, #e2e8f0, transparent); margin: 3rem 0;">
    """, unsafe_allow_html=True)

def get_audio_download_link(audio_data, fs, filename="processed_audio.wav"):
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, fs, format='WAV')
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
   
    href = f'''
    <a href="data:audio/wav;base64,{b64}" download="{filename}" style="text-decoration: none;">
        <button style="
            background: #10b981; 
            color: white; 
            border: none; 
            padding: 14px 28px; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: bold;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        ">
            📥 تحميل الملف المعالج
        </button>
    </a>
    '''
    return href

# سيب دالة convert_mp3_to_wav زي ما هي إذا كانت موجودة
