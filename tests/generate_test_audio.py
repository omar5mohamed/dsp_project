import numpy as np
import scipy.io.wavfile as wavfile
import os
from pydub import AudioSegment
import static_ffmpeg

def generate_synthetic_singing():
    # Initialize static-ffmpeg to ensure binaries are found
    print("Initializing static-ffmpeg...")
    static_ffmpeg.add_paths()
    
    print("Generating synthetic singing...")
    fs = 44100
    duration = 10
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # "Singing" - Vibrato
    # Fundamental frequency 440Hz (A4) with 5Hz vibrato
    vibrato = 5 * np.sin(2 * np.pi * 5 * t)
    f0 = 440 + vibrato
    
    # Generate phase
    phase = 2 * np.pi * np.cumsum(f0) / fs
    
    # Harmonics for "voice" like sound
    signal = 0.5 * np.sin(phase) + 0.3 * np.sin(2 * phase) + 0.2 * np.sin(3 * phase)
    
    # Add Noise (White Noise)
    print("Adding noise...")
    noise = np.random.normal(0, 0.05, len(t))
    
    mixed = signal + noise
    
    # Normalize
    mixed = mixed / np.max(np.abs(mixed))
    
    # Save as WAV first
    wav_path = "tests/test_singing_with_noise.wav"
    print(f"Saving WAV to {wav_path}...")
    wavfile.write(wav_path, fs, (mixed * 32767).astype(np.int16))
    
    # Convert to MP3
    mp3_path = "tests/test_singing_with_noise.mp3"
    print(f"Converting to MP3: {mp3_path}...")
    try:
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format="mp3")
        print(f"Successfully generated {mp3_path}")
    except Exception as e:
        print(f"Failed to convert to MP3: {e}")
        print("Ensure ffmpeg is installed or static-ffmpeg is working.")

if __name__ == "__main__":
    generate_synthetic_singing()
