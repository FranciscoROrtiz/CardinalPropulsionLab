from ffill_to_interpolate import ffill_to_interpolate
import pandas as pd

def ffill_to_interpolate_all_sensor_type(df, downsampled_sensor_prefix, fs_downsampled, fs_goal):
    for col in df.columns:
        if col.startswith(downsampled_sensor_prefix):
            df[col] = ffill_to_interpolate(df, col, int(fs_goal/fs_downsampled))
    return df
