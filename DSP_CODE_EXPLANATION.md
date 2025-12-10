# DSP Code Explanation (Beginner's Guide)

This guide explains the "Brain" of the application—the Digital Signal Processing (DSP) code.

**What is DSP?**
Imagine audio as a continuous wave, like a string vibrating. To change this sound with a computer (digital), we must first turn it into numbers (digits), process those numbers, and then turn them back into sound. That's Digital Signal Processing.

---

## 1. `core/frequency_analysis.py`

**The Goal:** To understand what frequencies (pitches) make up a sound. Think of a musical chord; it sounds like one thing, but it's made of several individual notes. This code helps us find those notes.

### `compute_fft` Function

This function uses the **Fast Fourier Transform (FFT)** to break a sound wave (Time Domain) into its frequency ingredients (Frequency Domain).

```python
import numpy as np
from scipy.fft import rfft, rfftfreq

def compute_fft(signal, fs, window_type='None', scale='Linear'):
    """
    Computes the FFT of the signal.
    
    Args:
        signal (np.array): Input signal.
        fs (int): Sampling rate.
        window_type (str): Window function ('None', 'Hann', 'Hamming').
        scale (str): Magnitude scale ('Linear', 'Log').
        
    Returns:
        np.array: Frequency axis (positive half).
        np.array: Magnitude spectrum (positive half).
        np.array: Phase spectrum (positive half).
    """
    N = len(signal)
    
    if window_type == 'Hann':
        window = np.hanning(N)
        signal = signal * window
    elif window_type == 'Hamming':
        window = np.hamming(N)
        signal = signal * window
        
    yf = rfft(signal)
    xf = rfftfreq(N, 1/fs)
    
    freqs = xf
    
    magnitude = np.abs(yf)
    
    magnitude = magnitude / N
    
    if scale == 'Log':
        magnitude = 20 * np.log10(magnitude + 1e-10)
        
    phase = np.angle(yf)
    
    return freqs, magnitude, phase
```

**Line-by-Line Breakdown**:

- `import numpy as np`: Importing "NumPy", a fast calculator for lists of numbers.
- `from scipy.fft import rfft, rfftfreq`: Borrowing the FFT tool from a scientific library. `rfft` breaks the sound apart.
- `def compute_fft(...)`: Defines our "recipe". It needs the audio `signal` and sampling rate `fs`.
- `N = len(signal)`: We count the total number of audio samples.
- `if window_type == 'Hann': ...`: **Analogy**: If you cut audio abruptly, it clicks. A "Window" smooths the edges to zero to prevent this.
- `yf = rfft(signal)`: **The Core Step**: This runs the math to turn time-based audio into frequency numbers.
- `xf = rfftfreq(N, 1/fs)`: Calculates graph labels (e.g., "This bin is 20Hz").
- `magnitude = np.abs(yf)`: Calculates the volume (strength) of each frequency.
- `magnitude = magnitude / N`: Divides by total samples to keep numbers consistent for any song length.
- `if scale == 'Log': ...`: Converts volume to Decibels (dB) because human ears hear loudness exponentially, not linearly.
- `return freqs, magnitude, phase`: Sends back the Pitch list, Volume list, and Timing list.

---

## 2. `core/signal_digitization.py`

**The Goal:** To simulate how real-world sound turns into computer data (ADC - Analog to Digital Conversion).

### `sample_signal` Function

**Concept: Sampling**
Real sound is smooth. Computers use rapid snapshots (samples). This is like a flip-book; enough pages make it look smooth.

```python
import numpy as np
from scipy.signal import resample

def sample_signal(signal, original_fs, new_fs):
    """
    Resamples the signal from original_fs to new_fs.
    
    Args:
        signal (np.array): The input signal.
        original_fs (int): Original sampling rate.
        new_fs (int): Target sampling rate.
        
    Returns:
        np.array: Resampled signal.
        np.array: Time axis for the resampled signal.
    """
    if new_fs == original_fs:
        t = np.arange(len(signal)) / original_fs
        return signal, t
    
    num_samples = int(len(signal) * new_fs / original_fs)
    
    resampled_signal = resample(signal, num_samples)
    
    t = np.arange(num_samples) / new_fs
    
    return resampled_signal, t
```

**Line-by-Line Breakdown**:
- `if new_fs == original_fs:`: If we aren't changing speed, return original audio.
- `num_samples = ...`: Calculate how many "pages" our new flip-book needs. Lower quality = fewer pages.
- `resampled_signal = resample(...)`: Smart tool that throws away data to simulate low-quality recording.
- `t = np.arange(...)`: Creates new timestamps for the new, fewer samples.

### `quantize_signal` Function

**Concept: Quantization**
Sampling creates the "Time" grid. Quantization creates the "Loudness" grid. Imagine measuring a wave's height. It might be 1.2345 meters. A computer might only store "1.2". This rounding creates "digital noise".

```python
def quantize_signal(signal, n_bits):
    """
    Quantizes the signal to n_bits.
    
    Args:
        signal (np.array): Input signal (assumed to be normalized between -1 and 1 or similar).
        n_bits (int): Number of bits for quantization.
        
    Returns:
        np.array: Quantized signal.
        np.array: Quantization error.
    """
    L = 2 ** n_bits
    
    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal, np.zeros_like(signal)
        
    norm_signal = signal / max_val
    
    scaled = (norm_signal + 1) * (L - 1) / 2
    quantized_levels = np.round(scaled)
    
    quantized_levels = np.clip(quantized_levels, 0, L - 1)
    
    quantized_norm = (quantized_levels * 2 / (L - 1)) - 1
    
    quantized_signal = quantized_norm * max_val
    
    error = signal - quantized_signal
    
    return quantized_signal, error
```

**Line-by-Line Breakdown**:
- `L = 2 ** n_bits`: "Bits" are storage space. 8 bits = 256 volume levels.
- `max_val = np.max(...)`: Finding the loudest part of the song.
- `norm_signal = signal / max_val`: Shrinking song so the loudest part is exactly 1.0 (easier math).
- `scaled = ...`: Stretching small signal to fit our levels (0 to 255).
- `quantized_levels = np.round(scaled)`: **The Crucial Step**: Forcing precise values to the nearest whole number. This rounding *is* the quality loss.
- `error = ...`: Calculating exactly what we lost (the difference between perfect original and blocky copy).

---

## 3. `core/signal_filters.py`

**The Goal:** To clean up audio by removing unwanted sounds.

### `apply_lowpass` Function

**Concept: Low-Pass Filter**
Like a bouncer at a club. It lets "Low" frequencies (Bass) in, but stops "High" frequencies (Treble/Hiss).

```python
import numpy as np
from scipy.signal import butter, lfilter

def apply_lowpass(signal, fs, cutoff, order=5):
    """
    Applies a low-pass Butterworth filter.
    
    Args:
        signal (np.array): Input signal.
        fs (int): Sampling rate.
        cutoff (float): Cutoff frequency in Hz.
        order (int): Filter order.
        
    Returns:
        np.array: Filtered signal.
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, signal)
    return y
```

**Line-by-Line Breakdown**:
- `nyquist = 0.5 * fs`: The "Speed Limit" of digital audio. Always half the sampling rate.
- `normal_cutoff = ...`: Converting our target frequency (e.g., 5000Hz) into a percentage (0 to 1) of the speed limit.
- `b, a = butter(...)`: "Butterworth" is a smooth, flat filter type. `b` and `a` are the math numbers describing its shape.
- `y = lfilter(...)`: Running the audio through the filter math to get clean output `y`.
