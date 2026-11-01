import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

def lowpass_filter(data, fs, fc=None, order=5):
    # Filter
    if fc == None:
        fc = fs/10
    # lp_filter(fs, data, critical frequency, order=5)
    sos = signal.butter(order, fc, btype='low', fs=fs, output='sos')
    if len(data)<49:
        filtered_data = signal.sosfiltfilt(sos, data, padlen=len(data)-1)
    else:
        filtered_data = signal.sosfiltfilt(sos, data)
    return filtered_data
