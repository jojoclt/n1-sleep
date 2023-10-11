import numpy as np
from scipy import signal
import pyedflib
import os
import matplotlib.pyplot as plt

print(os.getcwd())
# Load the EEG data
f = pyedflib.EdfReader('./clips/SC400100E0-PSG.edf')
eeg_data = f.readSignal(0)
fs = f.getSampleFrequency(0)

# Define the frequency bands of interest
freq_bands = {'delta': (0.5, 4),
              'theta': (4, 8),
              'alpha': (8, 12),
              'beta': (12, 30)}

# Define the window size and step size
win_size = 20  # seconds
step_size = 5  # seconds

# Calculate the number of samples per window and step
win_samples = int(win_size * fs)
step_samples = int(step_size * fs)

# Initialize the classification matrix
n_windows = int(np.ceil((eeg_data.shape[0] - win_samples) / step_samples) + 1)
classif = np.zeros(n_windows)
# Loop over windows and classify based on criteria
for i in range(n_windows):
    # Extract window data
    start = i * step_samples
    end = start + win_samples
    if end > eeg_data.shape[0]:
        end = eeg_data.shape[0]
    window = eeg_data[start:end]

    # Calculate PSD for each frequency band
    psd = {}
    for name, (fmin, fmax) in freq_bands.items():
        freqs, psd[name] = signal.welch(window, fs=fs, nperseg=win_samples,nfft=4096)
        # Plot the PSD estimate
        mask = np.logical_and(freqs >= fmin, freqs < fmax)
        psd[name] = np.mean(psd[name][mask])
        freqs = freqs[:len(window)]
    
    # Check if Alpha power is low
    alpha_power = psd['alpha']
    other_power = sum([psd[name] for name in freq_bands if name != 'alpha'])
    if alpha_power < other_power:
        # Calculate LAMF and check if it is greater than 50%
        lamf = np.mean(np.logical_and(window < 20, freqs > 10))
        if lamf > 0.5:
            # Classify window as N1
            print('N1')
        else:
            # Classify window as not N1
            print('Not N1')
    else:
        # Check if there is EEG activity in the range of 4-7 Hz
        theta_power = psd['theta']
        if theta_power > 0:
            # Check if there are Vertex Sharp Waves or Slow Eye Movements
            if np.any(np.logical_or(window > 50, window < -50)):
                # Classify window as N1
                print('N1')
            else:
                # Classify window as not N1
                print('Not N1')
        else:
            # Classify window as not N1
            print('Not N1')