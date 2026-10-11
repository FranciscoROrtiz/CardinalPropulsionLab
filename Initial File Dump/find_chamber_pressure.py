def find_chamber_pressure(p_tank_low, stiffness):
    Pc = p_tank_low / (stiffness + 1)       # [psi]
    return Pc