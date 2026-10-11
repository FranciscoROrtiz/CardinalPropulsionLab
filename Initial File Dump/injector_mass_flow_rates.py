def injector_mass_flow_rates(Thrust, Isp, g, OF, film_cooling_percentage):
    lbf_to_N = 4.44822162       # lbf * lbf_to_N = N

    T = Thrust * lbf_to_N
    mass_flow_rates = {}
    mass_flow_rates['mdot_tot'] = T /(Isp * g)
    mass_flow_rates['mdot_fuel_comb'] = mass_flow_rates['mdot_tot'] / (OF + 1.25)
    mass_flow_rates['mdot_fuel_film'] = 1.25 * film_cooling_percentage * mass_flow_rates['mdot_fuel_comb']
    mass_flow_rates['mdot_ox'] = OF * mass_flow_rates['mdot_fuel_comb']


    return mass_flow_rates