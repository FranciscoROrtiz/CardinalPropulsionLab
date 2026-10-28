def calc_pressure_drop(p1, p2):
    """
    Inputs
        p1: List of upstream pressures
        p2: List of downstream pressures
    Output
        dp: List of pressure drops (p1 - p2)
    """
    dp = [p1[i] - p2[i] for i in range(len(p1))]
    
    return dp