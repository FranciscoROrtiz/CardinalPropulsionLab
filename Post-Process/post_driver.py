"""

Overall workflow
get DATA
find noisy frequencies
    PSD
apply bandpass based on frequencies from ^

"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

from PSD_calc import PSD_calc
from lowpass_filter import lowpass_filter
from fs_calc import fs_calc
from parquet_process import parquet_process


"""
vvv FILE INPUTS vvv
"""
# Path to test data file
file = r"C:\Users\franc\Downloads\CPL - Post Processing Scripts\All Coldflow and Hotfire Data\BG_HF_2.parquet"

output = "LC_ox_tank"

# Find index for desired section of analysis
idx_start = 2400
idx_end = 2490

"""
^^^ FILE INPUTS ^^^
"""

df = parquet_process(file)
fs = fs_calc(df)

t = df["time_sec"].to_numpy()[idx_start:idx_end+1]
y = df[output].to_numpy()[idx_start:idx_end+1]


f, Pxx_den = PSD_calc(y, fs)
filtered_data = lowpass_filter(y, fs)
f_filt, Pxx_den_filt = PSD_calc(filtered_data, fs)

# IT'S PLOTTING TIME
plt.figure()
plt.semilogy(f, Pxx_den)
plt.semilogy(f_filt, Pxx_den_filt)
plt.figure()
plt.scatter(t, y, label="un")
plt.scatter(t, filtered_data, label="f")
plt.legend()
plt.show()
