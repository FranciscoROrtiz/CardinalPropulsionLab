import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

def parquet_process(file):
    df = pd.read_parquet(file)
    # Convert native timestamp to regular seconds
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    df['time_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()
    return df
