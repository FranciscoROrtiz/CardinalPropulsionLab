import math

def calc_Cf(gamma, Pe,Pc, epsilon_e):
    Cf = (math.sqrt(2 * gamma**2 / (g - 1) * (2 / (gamma + 1))**((gamma + 1) / (gamma - 1))
                * (1 - Pe**((gamma - 1) / gamma))) + (Pe - 101325 / Pc) * epsilon_e)
    return Cf

