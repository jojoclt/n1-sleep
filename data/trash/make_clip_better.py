import pyedflib  # ref: https://pyedflib.readthedocs.io/en/latest/
import pandas as pd
import numpy as np
import os
import fnmatch
from datetime import timedelta

read_folder = "./sleep-cassette/"
write_folder = "./clips_better/"

os.makedirs(write_folder, exist_ok=True)

def clip_edf_data(signal, label, read_folder, write_folder):
    """
    Clips the PSG and hypnogram data to N1 segments saves the clipped data to a new file.

    Args:
        signal (str): The PSG file ID.
        label (str): The hypnogram file ID.
        read_folder (str): The folder path where the original PSG and hypnogram files are located.
        write_folder (str): The folder path where the clipped PSG and hypnogram files will be saved.

    Returns:
        None
    """
    signal_path = os.path.join(read_folder, signal)
    label_path = os.path.join(read_folder, label)

    # read data
    edf_signal = pyedflib.EdfReader(signal_path)
    edf_label = pyedflib.EdfReader(label_path)

    start_time = edf_signal.getStartdatetime()
    sig_labels, sig_freqs = (
        edf_signal.getSignalLabels(),
        edf_signal.getSampleFrequencies(),
    )
    data = []
    for ch_idx, sig_label, sig_freq in zip(enumerate(sig_labels), sig_freqs):
        sig = edf_signal.readSignal(chn=ch_idx)
        idx = pd.date_range(
            start=start_time, periods=len(sig), freq=pd.Timedelta(1 / sig_freq, unit="s")
        )
        data += [pd.Series(sig, index=idx, name=sig_label)]

    annotations = edf_label.readAnnotations()
    # create DataFrames
    annotations_df = pd.DataFrame(annotations)
    annotations_df = annotations_df.T
    annotations_df.rename(
        columns={0: "Onset", 1: "Duration", 2: "Annotations"}, inplace=True
    )

    for i, (prev, curr, next) in enumerate(
        zip(annotations_df, annotations_df[1:], annotations_df[2:])
    ):
        if (
            prev["Annotations"] == "Sleep stage W"
            and curr["Annotations"] == "Sleep stage 1"
        ):
            # if it is the first clip, shorten it to 10min
            if prev["Onset"] == 0.0:
                prev["Onset"] = curr["Onset"] - 600.0
                prev["Duration"] = 600.0
            # if it is the last clip, shorten it to 10min
            elif next["Duration"] > 600.0:
                next["Duration"] = 600.0
            
            duration = next["Onset"] + next["Duration"] - prev["Onset"]

            # write PSG clip to edf file from the prev, curr, next
            write_signal_path = os.path.join(
                write_folder, f"{signal[:-4]}_{i}-PSG.edf"
            )
            write_label_path = os.path.join(
                write_folder, f"{label[:-4]}_{i}-Hypnogram.edf"
            )
            write_edf_data(
                write_signal_path,
                write_label_path,
                prev["Onset"],
                duration,
                data,
                sig_labels,
                sig_freqs,
            )

            


if __name__ == "__main__":
    pattern1 = "*-PSG.edf"
    pattern2 = "*-Hypnogram.edf"

    psg_list = sorted(
        [f for f in os.listdir(read_folder) if fnmatch.fnmatch(f, pattern1)]
    )
    hypnogram_list = sorted(
        [f for f in os.listdir(read_folder) if fnmatch.fnmatch(f, pattern2)]
    )

    for signal, label in zip(psg_list, hypnogram_list):
        print("Signal:", signal)
        clip_edf_data(
            signal=signal,
            label=label,
            read_folder=read_folder,
            write_folder=write_folder,
        )
        break
