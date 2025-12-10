import os
import static_ffmpeg
from pydub import AudioSegment

def convert():
    print("Initializing static-ffmpeg...")
    static_ffmpeg.add_paths()
    
    wav_path = "tests/test_singing_with_noise.wav"
    mp3_path = "tests/test_singing_with_noise.mp3"
    
    if not os.path.exists(wav_path):
        print(f"Error: {wav_path} not found.")
        return

    print(f"Converting {wav_path} to {mp3_path}...")
    try:
        audio = AudioSegment.from_wav(wav_path)
        audio.export(mp3_path, format="mp3")
        print(f"Successfully created {mp3_path}")
    except Exception as e:
        print(f"Conversion failed: {e}")

if __name__ == "__main__":
    convert()
