import math

def calculate_mass_flow_rates(Thrust, Ue, eta_nozzle, OF, film_cooling_percentage):
    lbf_to_N = 4.44822162       # lbf * lbf_to_N = N

    T = Thrust * lbf_to_N
    mass_flow_rates = {}
    mass_flow_rates['mdot_tot'] = T /(Ue * math.sqrt(eta_nozzle))
    mass_flow_rates['mdot_fuel_comb'] = mass_flow_rates['mdot_tot'] * (1 - film_cooling_percentage) / (OF + 1)
    mass_flow_rates['mdot_fuel_film'] = film_cooling_percentage * mass_flow_rates['mdot_tot']
    mass_flow_rates['mdot_ox'] = OF * mass_flow_rates['mdot_fuel_comb']
    # mass_flow_rates['mdot_fuel_comb'] = mass_flow_rates['mdot_tot'] / (OF + 1.25)
    # mass_flow_rates['mdot_fuel_film'] = 0.25 * mass_flow_rates['mdot_fuel_comb']



    return mass_flow_rates