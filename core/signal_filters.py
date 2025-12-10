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

