import math

def nozzle_def(alpha, theta_n, theta_e, chamber_def):

    Rt = (chamber_def['A_throat']/math.pi)**0.5
    R = 0.382*Rt

    nozzle_def = {
        "alpha": alpha,
        "theta_n": theta_n,
        "theta_e": theta_e,
        "Rt": Rt,
        "R": R
    }
    return nozzle_def