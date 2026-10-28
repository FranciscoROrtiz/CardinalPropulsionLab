import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

def PSD_calc(data, fs):
    f, Pxx_den = signal.welch(data, fs)
    return f, Pxx_den
