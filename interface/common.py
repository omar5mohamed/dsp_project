import streamlit as st
import base64

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

        /* Uploader Customization */
        [data-testid="stFileUploader"] section {
            background-color: #161b22;
            border: 1px dashed #30363d;
        }
        [data-testid="stFileUploader"] section:hover {
            border-color: #00FF9D;
        }
        [data-testid="stFileUploader"] button {
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #0d1117; 
        }
        ::-webkit-scrollbar-thumb {
            background: #30363d; 
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00FF9D; 
        }
        
        </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle=""):
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem; border-bottom: 2px solid #30363d; padding-bottom: 1rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; color: #00FF9D; text-shadow: 0 0 10px rgba(0, 255, 157, 0.3);">{title}</h1>
            <p style="font-size: 1.2rem; color: #8b949e; font-family: 'Roboto Mono', monospace;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def get_audio_download_link(audio_data, fs, filename="processed_audio.wav"):
    import soundfile as sf
    import io
import streamlit as st
import base64

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

        /* Uploader Customization */
        [data-testid="stFileUploader"] section {
            background-color: #161b22;
            border: 1px dashed #30363d;
        }
        [data-testid="stFileUploader"] section:hover {
            border-color: #00FF9D;
        }
        [data-testid="stFileUploader"] button {
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: #0d1117; 
        }
        ::-webkit-scrollbar-thumb {
            background: #30363d; 
            border-radius: 5px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00FF9D; 
        }
        
        </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle=""):
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem; border-bottom: 2px solid #30363d; padding-bottom: 1rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; color: #00FF9D; text-shadow: 0 0 10px rgba(0, 255, 157, 0.3);">{title}</h1>
            <p style="font-size: 1.2rem; color: #8b949e; font-family: 'Roboto Mono', monospace;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

def get_audio_download_link(audio_data, fs, filename="processed_audio.wav"):
    import soundfile as sf
    import io
    
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, fs, format='WAV')
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    
    href = f'<a href="data:audio/wav;base64,{b64}" download="{filename}" style="text-decoration: none;"><button style="background: #10B981; color: white; border: none; padding: 10px 20px; border_radius: 5px; cursor: pointer; font_weight: bold;">Download Processed Audio</button></a>'
    return href

def convert_mp3_to_wav(mp3_file):
    """
    Converts an uploaded MP3 file to WAV format using pydub.
    Returns a BytesIO object containing the WAV data.
    """
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
    except ImportError:
        pass
        
    from pydub import AudioSegment
    import io
    
    audio = AudioSegment.from_mp3(mp3_file)
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io
