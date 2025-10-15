import numpy as np
from scipy.io import wavfile
import scipy.signal as signal

def simple(audio, sample_rate, d1, d2):
    """
    Apply a simple delay-based reverb simulating a single wall reflection.

    Parameters:
        audio (np.ndarray): Mono input audio waveform.
        sample_rate (int): Sampling rate of the audio in Hz.
        d1 (float): Distance from microphone to source in meters.
        d2 (float): Distance from microphone to wall in meters.

    Returns:
        np.ndarray: Audio with a single delayed echo added.
    """
    print("Applying simple reverb")
    output = np.zeros( len(audio))
    speed_of_sound = 343
    delay = int((d1 + d2*2) * sample_rate / speed_of_sound)
    
    for n in range(delay, len(audio)):
        output[n] = audio[n] + 0.5 *  audio[n - delay]

    output = normalize(output)
    
    return output

def schroeder(audio, sample_rate, d):
    """
    Apply a Schroeder reverb using multiple comb and allpass filters.

    Parameters:
        audio (np.ndarray): Mono input audio waveform.
        sample_rate (int): Sampling rate of the audio in Hz.
        d (float): Base distance in meters (used in filter delays).

    Returns:
        np.ndarray: Reverberated audio with a more natural decay.
    """

    print("Applying schroeder reverb")
    combs = comb( audio, sample_rate, 5)
    combs = comb( audio, sample_rate, 3)
    combs = comb( audio, sample_rate, 10)

    output = 5 * audio

    allpasses = allpass(combs, sample_rate, 10)
    allpasses = allpass(allpasses, sample_rate, 5)
    
    output += allpasses

    # Normalize audio
    output = normalize(output)

    return output

# SCHROEDER HELPER FUNCTIONS
def comb(audio, sample_rate, d):
    """
    Apply a comb filter to create multiple decaying echoes.

    Parameters:
        audio (np.ndarray): Mono input audio waveform.
        sample_rate (int): Sampling rate of the audio in Hz.
        d (float): Distance in meters (controls delay length).

    Returns:
        np.ndarray: Audio with repeated echoes.
    """
    print("Applying comb filter")
    output = np.zeros( len(audio))
    delay = int(2 * d * sample_rate / 343)
    
    for n in range(delay, len(audio)):
        output[n] = audio[n] + 0.5 *  output[n - delay]
    
    return output

def allpass(audio, sample_rate, d):
    """
    Apply an allpass filter to smear echoes while keeping overall loudness.

    Parameters:
        audio (np.ndarray): Mono input audio waveform.
        sample_rate (int): Sampling rate of the audio in Hz.
        d (float): Distance in meters (controls delay length).

    Returns:
        np.ndarray: Audio with phase-modified echoes.
    """
    print("Applying allpass filter")
    output = np.zeros( len(audio))
    delay = int(2 * d * sample_rate / 343)
    
    for n in range(delay, len(audio)):
        output[n] = 0.5 * audio[n] + audio[n - delay] - 0.5 * output[n - delay]
    
    return output

def rir(audio, rir_path):
    print("Applying rir filter")
    _, rir = wavfile.read(rir_path)

    left = signal.fftconvolve(audio, rir[:, 0], mode='full')
    right = signal.fftconvolve(audio, rir[:, 1], mode='full')

    output = np.stack((left, right)).T
    output_trimmed = output[:, :len(audio)]

    output_trimmed = normalize(output_trimmed)

    return output_trimmed

def normalize(audio):
    max_val = np.max(np.abs(audio))

    if max_val > 0:
        audio = audio / max_val * 0.9

    return audio