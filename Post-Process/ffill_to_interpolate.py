import pandas as pd
import numpy as np

def ffill_to_interpolate(df, col_name, sample_factor):
    original_data_mask = df.index % sample_factor == 1

    # 2. Replace the forward-filled duplicates with NaN
    # We keep the value if it's an original row, otherwise we set it to NaN
    df[col_name] = df[col_name].where(original_data_mask, np.nan)

    # 3. Apply linear interpolation to fill the NaNs smoothly
    df[col_name] = df[col_name].interpolate(method='linear').ffill().bfill()
    return df[col_name]
