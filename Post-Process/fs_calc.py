import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

def fs_calc(df):
    dt_sample = df['time_sec'].iloc[1]-df['time_sec'].iloc[0]
    fs = 1/dt_sample
    return fs
