import math
import numpy as np

def calc_cstar_ideal(R, Tc, gamma, g=9.81):
    Tau = np.sqrt(gamma * ( ( gamma + 1)/2 ) ** (-(gamma + 1)/(gamma - 1)))
    cstar_ideal = np.sqrt(R * Tc) / Tau
    return cstar_ideal
