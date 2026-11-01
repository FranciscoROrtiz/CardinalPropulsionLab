from define_conditions_fuel import define_conditions_fuel
from calc_mass_flux_rate import calculate_mass_flux_rate

def calc_fuel_mass_flow_rate(A, Pc, p_tank, dp, Cd, rho):
    p1 = p_tank - dp
    IPA = define_conditions_fuel(p1, Pc,rho)
    G = calculate_mass_flux_rate(IPA)
    mdot_fuel = Cd * A * G
    return mdot_fuel