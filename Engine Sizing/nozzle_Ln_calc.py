import math

def nozzle_Ln_calc(nozzle_def, epsilon_e):
    Ln = (nozzle_def['Rt']*(math.sqrt(epsilon_e)-1) + nozzle_def['R']*(1/math.cos((math.radians(nozzle_def['alpha'])))-1))/(math.tan(math.radians(nozzle_def['alpha'])))

    return Ln