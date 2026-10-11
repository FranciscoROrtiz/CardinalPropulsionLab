from define_conditions_ox import define_conditions_ox
from calc_mass_flux_rate import calculate_mass_flux_rate

def calc_ox_mass_flow_rate(A, Pc, p_tank, dp, Cd,rho):
    p1 = p_tank - dp
    N2O = define_conditions_ox(p1, Pc)
    G = calculate_mass_flux_rate(N2O)
    mdot_ox = Cd * A * G
    return mdot_ox