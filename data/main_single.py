import pyedflib # ref: https://pyedflib.readthedocs.io/en/latest/
import pandas as pd
import numpy as np
import os
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import fnmatch
from modules import *
from tqdm import tqdm

file = '4112'
read_folder = './clips/'
write_folder = f'./plots_sleep_cas/'
os.makedirs(write_folder, exist_ok=True)
pattern1 = f'*{file}*-PSG.edf'
pattern2 = f'*{file}*-Hypnogram.edf'

psg_list = sorted([f for f in os.listdir(read_folder) if fnmatch.fnmatch(f, pattern1)])
hypnogram_list = sorted([f for f in os.listdir(read_folder) if fnmatch.fnmatch(f, pattern2)])
psg_iter = iter(psg_list)
hypnogram_iter = iter(hypnogram_list)

channels = ['EEG Fpz-Cz', 'EEG Pz-Oz', 'EOG horizontal']
channel = channels[1]

for i, (psg_id, hypnogram_id) in enumerate(zip(psg_iter, hypnogram_iter)):
    print(f"{i}/{len(psg_list)}", end="\r")
    signal_path = os.path.join(read_folder, psg_id)
    label_path = os.path.join(read_folder, hypnogram_id)
    edf_signal = pyedflib.EdfReader(signal_path)
    edf_label = pyedflib.EdfReader(label_path)
    annotations = edf_label.readAnnotations()
    start = edf_signal.getStartdatetime()
    signals, frequencies = edf_signal.getSignalLabels(), edf_signal.getSampleFrequencies()
    
    data = []
    for ch_idx, sig_name, freq in zip( range(len(signals)), signals, frequencies,):
        sig = edf_signal.readSignal(chn=ch_idx)
        idx = pd.date_range(  start=start, periods=len(sig), freq=pd.Timedelta(1 / freq, unit="s") )
        data += [pd.Series(sig, index=idx, name=sig_name)]
    # create DataFrames
    annotations_df = pd.DataFrame(annotations)
    annotations_df = annotations_df.T
    annotations_df.rename(columns={0: "Onset", 1: "Duration", 2:"Annotations"}, inplace=True)
    signal_df =pd.concat(data[0:3], axis=1)

    def check_sleep_stage(row):
        start_time = start + timedelta(seconds = int(annotations_df['Onset'].iloc[1]))
        end_time = start + timedelta(seconds = int(annotations_df['Onset'].iloc[1])) + timedelta(seconds = int(annotations_df['Duration'].iloc[1]))
        if start_time <= pd.to_datetime(row.name) < end_time:
            return int(1)
        else:
            return int(0)
    signal_df['N1'] = signal_df.apply(check_sleep_stage, axis=1)

    
    eeg_index = eeg_n1_static(signal_df[channels[0]], thres = 25)
    # eeg_index = np.array([])
    eog_index = eog_n1_predict(signal_df[channels[2]], window = 10, ratio = 0.5)
    # print(i, eeg_index)
    signal_df = get_n1_eeg(signal_df, eeg_index, eog_index)
    lol(signal_df, write_folder, psg_id, save_fig=True)

    