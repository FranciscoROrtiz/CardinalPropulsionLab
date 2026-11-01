from define_conditions_fuel import define_conditions_fuel
from calculate_mass_flux_rate import calculate_mass_flux_rate

def calc_fuel_area(mdot, Pc, p_tank, dp, Cd, rho):
    p1 = p_tank - dp
    IPA = define_conditions_fuel(p1, Pc, rho)
    G = calculate_mass_flux_rate(IPA)
    A_fuel = mdot / (Cd * G)
    return A_fuel