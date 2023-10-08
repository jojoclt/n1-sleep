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
win_size = 7  # seconds
step_size = 2  # seconds

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
        freqs, psd[name] = signal.welch(window, fs=fs, nperseg=win_samples, nfft=2048)
        # Plot the PSD estimate
        mask = np.logical_and(freqs >= fmin, freqs < fmax)
        psd[name] = np.mean(psd[name][mask])
        freqs = freqs[:len(window)]
        # print(name)
    # break
        # Calculate LAMF, VSW, and SEM
        time_ticks = pd.date_range(start=signal_df.index.min(), end=signal_df.index.max(), freq='30S')
        lamf = np.mean(np.logical_and(window < 20, freqs > 10))
        
        diffs = np.diff(window) < -50
        diffs = np.append(0, diffs)
        vsw = np.mean(np.logical_and(window > 50, diffs))
        
        sem = np.mean(np.logical_and(window < 30, freqs < 3))

    # Check criteria for N1
    if psd['alpha'] < 0.1 * np.sum(list(psd.values())):
        if np.any(np.logical_and(freqs >= 4, freqs <= 7)):
            classif[i] = 1
        elif vsw > 0.5:
            classif[i] = 1
        elif sem > 0.5:
            classif[i] = 1
    elif lamf > 0.5:
        classif[i] = 0

    # Print the current classification
    if i % 10 == 0:
        print('Window {}: {}'.format(i, 'N1' if classif[i] == 1 else 'Non-N1'))
    """
    To implement a sliding window approach for real-time data, you can modify the previous code to continuously update the classification based on a fixed window size and step size. Here's an example implementation:

    """