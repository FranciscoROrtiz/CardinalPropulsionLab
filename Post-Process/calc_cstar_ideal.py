import math

def calc_cstar_ideal(R, g, Tc, gamma):
    Tau = math.sqrt(gamma * ( ( gamma + 1)/2 ) ** (-(gamma + 1)/(gamma - 1)))
    cstar_ideal = math.sqrt(R * g * Tc) / Tau
    return cstar_ideal  