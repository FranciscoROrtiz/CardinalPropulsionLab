import numpy as np

def calc_pressure_drop(p1, p2):
    """
    Inputs
        p1: array or float of upstream pressures
        p2: array or float of downstream pressures
    Output
        dp: array or float of pressure drops (p1 - p2)
    """
    # dp = [p1[i] - p2[i] for i in range(len(p1))]
    dp = p1 - p2
    dp[dp < 0] = 0

    return dp
