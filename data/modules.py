from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# region
# def eeg_n1_dynamic(signal_df, k=10):
#     """
#     Returns the index of the signal where the signal is below a threshold for a long time
#     This function will consider the dynamic threshold (amplitude) of the last k-window

#     Parameters
#     ----------
#     signal_df : pandas.DataFrame
#         The signal dataframe
#     k : int (default=10)
#         The window size

#     Returns
#     -------
#     index : int
#         The index of the signal where the signal is below a threshold for a long time
#     """

#     index = -1
#     N = signal_df.shape[0]

#     # 1 STEP = 0.01s (100Hz)
#     # i -> sliding window in 1500 steps
#     for i in range(0, N, 1500):
#         mxcount = 0
#         count = 0
#         # Going to try consecutive 50 steps (0.5s) and check if the signal is below a threshold
#         # If it is in 50 steps, then the count will be increased by 50 and so on...
#         for j in range(i, i + 3000):
#             if signal_df.iloc[j]['amplitude'] < signal_df.iloc[j]['threshold']:
#                 count += 1
#             else:
#                 if count > mxcount:
#                     mxcount = count
#                 count = 0
#     return index
# endregion

def eeg_n1_static(signal_df, thres = 25):
    index = []
    N = signal_df.shape[0]
    CONSECUTIVE_STEPS = 50
    # 1 STEP = 0.01s (100Hz)
    # i -> sliding window in 1500 steps
    for i in range(0, N, 3000):
        count = 0
        inner_count = 0
        # Going to try consecutive 50 steps (0.5s) and check if the signal is below a threshold
        # If it is in 50 steps, then the count will be increased by 50 and so on...
        for j in range(i, min(N, i + 3000)):
            if abs(signal_df.iloc[j]) < thres:
                inner_count += 1
            else:
                if inner_count >= CONSECUTIVE_STEPS-1:
                    count += inner_count
                inner_count = 0
        
        if count >= 1500:
            index.append(i)
        
        # there is some case that there are separate intervals
        if len(index) and index[-1] != i:
            index.append(index[-1] + 3000)
            break
    return index

def eog_n1_predict(signal_df, window = 10, ratio = 0.3):
    # window = moving average window
    # ratio = if max value * ratio < all seen values in the interval, then N1
    N = signal_df.shape[0]
    # FIXED VARIABLE
    max_arr = []
    seen = 0 # how many intervals passed

    for i in range(0, N, 3000):
        max_len = min(i+3000, N)
        cur_max = signal_df.iloc[i:max_len].max()
        if seen > window:
            avg = sum(max_arr[-window:])/window
            if avg * ratio > cur_max:
                # print("FOUND")
                return i
            # else:
            #     print(f"cur_max: {cur_max}, avg: {avg}")
        else:
            max_arr.append(cur_max)
        seen += 1
    
    return -1
    
def get_n1_eeg(signal_df, eeg_index, eog_index):
    start = pd.to_datetime(signal_df.index[0])

    def check_sleep_stage_predict(row, start_index, duration):
        start_time = start + timedelta(seconds = start_index)
        end_time = start + timedelta(seconds = start_index) + timedelta(seconds = duration)
        if start_time <= pd.to_datetime(row.name) < end_time:
            return int(1)
        else:
            return int(0)

    if len(eeg_index) == 0:
        pass
    else:
        signal_df['N1_predict_EEG'] = signal_df.apply(check_sleep_stage_predict, args=(int(eeg_index[0]/100), int((eeg_index[-1]-eeg_index[0])/100)), axis=1)    

    if eog_index == -1:
        pass
    else:
        eog_index = [eog_index]
        signal_df['N1_predict_EOG'] = signal_df.apply(check_sleep_stage_predict, args=(int(eog_index[0]/100), int(max(eog_index)/100) + 1.5), axis=1) 
    empty_EEG = signal_df.get('N1_predict_EEG').eq(0).all()
    empty_EOG = signal_df.get('N1_predict_EOG') & signal_df.get('N1_predict_EOG').eq(0).all()
    if (not empty_EEG and not empty_EOG):
        v = signal_df['N1_predict_EEG']&signal_df['N1_predict_EOG']
        signal_df['N1_predict'] = v
        # signal_df['N1_predict'] = signal_df.apply(check_sleep_stage_predict, args=(v/100, 0.01), axis=1)
        if signal_df['N1_predict'].eq(0).all():
            signal_df['N1_predict'] = signal_df['N1_predict_EOG']
    if not empty_EEG:
        signal_df['N1_predict'] = signal_df['N1_predict_EEG']
    elif not empty_EOG:
        signal_df['N1_predict'] = signal_df['N1_predict_EOG']
    return signal_df

def lol(signal_df, write_folder, psg_id, save_fig=False):
    num_columns = len(signal_df.columns)

    fig, axes = plt.subplots(num_columns, 1, figsize=(20, 12), sharex=True)

    # 迴圈遍歷每個欄位
    for i, column in enumerate(signal_df.columns):
        # 取得目前的軸
        ax = axes[i]

        # 繪製折線圖
        ax.plot(signal_df.index, signal_df[column])
        
        # 繪製虛線
        start_time = signal_df.index[0]
        end_time = signal_df.index[-1]
        interval = pd.Timedelta(seconds=30)
        current_time = start_time + interval
        while current_time < end_time:
            ax.axvline(x=current_time, linestyle='--', color='gray')
            current_time += interval

        # 設定軸的標籤
        ax.set_ylabel(column)
        loc = mdates.MinuteLocator(interval=1)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # 設定圖表標題和共用 x 軸標籤
    fig.suptitle('Signal Visualization')
    axes[-1].set_xlabel('Time')
    # 調整子圖之間的間距
    plt.tight_layout()
    plt.ylim(0,10)
    # 顯示圖表
    if save_fig:
        plt.savefig(write_folder + psg_id.split('.')[0],bbox_inches='tight')
    else:
        plt.show()
