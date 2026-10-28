import math

def calc_Cf_ideal(gamma, Pe,Pc, epsilon_e):
    Cf = ( math.sqrt((2 * gamma**2 / (gamma - 1))* (2 / (gamma + 1))**((gamma + 1) / (gamma - 1))* (1 - (Pe / Pc)**((gamma - 1) / gamma)))+ ((Pe - Pa) / Pc) 
          * epsilon_e)
    return Cf

     