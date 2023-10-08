def get_n1_index(signal_df, threshold=25):
    index = []
    index_series = []
    N = signal_df.shape[0]
    # # FIXED VARIABLE
    # threshold = 25

    for i in range(0, N, 1500):
        mxcount = 0
        count = 0
        try:
            for j in range(3000):
                if(abs(signal_df.iloc[i+j,0]) < threshold and abs(signal_df.iloc[i+j-1,0]) < threshold):
                    count += 1
                else:
                    if(count > mxcount):
                        mxcount = count
                    count = 0
            mxcount = max(mxcount, count)
        except:
            pass
        # print(i,mxcount)
        index_series.append(mxcount)
        if(mxcount > 1500):
            index.append(i)
    # len(index)
    return index