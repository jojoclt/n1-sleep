import numpy as np
import matplotlib.pyplot as plt
import os
import mne
from mne.preprocessing import ICA
from scipy import signal
from asrpy import ASR
from scipy.fft import fft, fftfreq
import fnmatch
import shutil
import pyedflib

def denoise(psg_id, read_folder, filter_write_folder, asr_write_folder):

    signal_path = os.path.join(read_folder, f'{psg_id}-PSG.edf')

    raw = mne.io.read_raw_edf(signal_path, preload=True)
    raw.set_channel_types({'EOG horizontal': 'eog'})
    raw.set_channel_types({'EMG submental': 'emg'})
    raw.drop_channels(['Resp oro-nasal', 'Temp rectal', 'Event marker'])

    montage = mne.channels.make_standard_montage('standard_1005')
    channel_pos_fzcz = montage.get_positions()['ch_pos']['Fz']
    channel_pos_pzoz = montage.get_positions()['ch_pos']['Pz']
    montage = mne.channels.make_dig_montage({ 'EEG Fpz-Cz': channel_pos_fzcz, 'EEG Pz-Oz': channel_pos_pzoz }, coord_frame='head')
    raw.set_channel_types({ 'EEG Fpz-Cz': 'eeg', 'EEG Pz-Oz': 'eeg' })
    raw.set_montage(montage)

    sampling_rate = 1000  # Sampling rate in Hz
    low_freq = 1  # 低频截止频率
    high_freq = 49.9  # 高频截止频率
    filter_order = 4  # 滤波器阶数

    filtered_file = os.path.join(filter_write_folder, f'{psg_id}-filter-PSG.edf')
    raw_filtered = raw.copy()
    raw_filtered.load_data()
    raw_filtered.filter(low_freq, high_freq, fir_design='firwin', filter_length='auto', l_trans_bandwidth='auto', h_trans_bandwidth='auto', method='fir', phase='zero', fir_window='hamming', verbose=True)
    print(filtered_file)
    mne.export.export_raw(filtered_file, raw_filtered, "edf", overwrite=True)

    asr_file = os.path.join(asr_write_folder, f'{psg_id}-asr-PSG.edf')
    sfreq = raw.info["sfreq"]
    asr = ASR(sfreq=sfreq, cutoff=5)
    asr.fit(raw_filtered)
    asr_filtered_data = asr.transform(raw)
    print(asr_file)
    mne.export.export_raw(asr_file, asr_filtered_data, "edf", overwrite=True)


read_folder = './clips/'
pattern1 = '*-PSG.edf'
pattern2 = '*-Hypnogram.edf'

psg_list = sorted([f for f in os.listdir(read_folder) if fnmatch.fnmatch(f, pattern1)])
hypnogram_list = sorted([f for f in os.listdir(read_folder) if fnmatch.fnmatch(f, pattern2)])
cnt = []

for i in range(len(psg_list)):
    try:
        denoise(
            psg_id=psg_list[i][0:10],
            read_folder = read_folder,
            filter_write_folder = './bands/',
            asr_write_folder = './asrs'
        )
    except:
        cnt.append(psg_list[i][0:10])
        continue
    # shutil.copy2(read_folder+hypnogram_list[i], './annotations')