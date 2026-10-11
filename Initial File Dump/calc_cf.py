import math

def calc_Cf(gamma, Pe,Pc, epsilon_e):
    Pa = 101325
    Cf = ( math.sqrt((2 * gamma**2 / (gamma - 1))* (2 / (gamma + 1))**((gamma + 1) / (gamma - 1))* (1 - (Pe / Pc)**((gamma - 1) / gamma)))+ ((Pe - Pa) / Pc) 
          * epsilon_e)
    return Cf

     