from injector_areas import injector_areas
from injector_pintle_sizing import optimize_pintle_geometry
from injector_pintle_annulus_sizing import injector_annulus_sizing
from injector_film_cooling_orifices_arrangement import optimize_film_cooling_holes

"""
vvv INPUTS vvv
"""

Thrust = 450
Isp = 150
g = 9.81
OF = 3

p_tank_low = 465            # [psi]
dp_N2O = 15
dp_IPA = 45

# Oxidizer inputs
Cd_ox = 0.4

# Fuel inputs     # kg/s
Cd_fuel = 0.4
rho_IPA = 785       # kg/m^3
film_cooling_percentage = 0.2      # mdot_fuel_film / mdot_fuel

# Chamber geometry
d_chamber = 0.0736132291262     # [m]
Pc = 350

############################33
#d_chamber = 0.0635      # NOT REAL CHAMBER DIAMETER


"""
^^^ INPUTS ^^^
"""

def injector_sizing(mass_flow_rates, p_tank_low, dp_N2O, dp_IPA, Cd_ox, Cd_fuel, rho_IPA, film_cooling_percentage, d_chamber, Pc, smallest_drill):

    p_N2O = p_tank_low - dp_N2O
    p_IPA = p_tank_low - dp_IPA

    # Calculate injector areas
    injector_areas_dict = injector_areas(p_N2O, p_IPA, Pc, mass_flow_rates['mdot_ox'], Cd_ox, mass_flow_rates['mdot_fuel_comb'], mass_flow_rates['mdot_fuel_film'], Cd_fuel, rho_IPA)

    # Calculate Pintle Drill Bit Holes
    pintle_geometry = optimize_pintle_geometry(injector_areas_dict['A_N2O'], d_chamber)

    # Calculate Annulus Size
    annulus_geometry = injector_annulus_sizing(mass_flow_rates['mdot_fuel_comb'], injector_areas_dict['A_IPA_comb'], pintle_geometry['pintle_diameter'])

    # Calculate Film Cooling Drill Bit Holes
    film_geometry = optimize_film_cooling_holes(injector_areas_dict['A_IPA_film'], smallest_drill)

    return injector_areas_dict, pintle_geometry, annulus_geometry, film_geometry

# Print Results
"""
print('Mass Flow Rates')
print_dictonary(mass_flow_rates)
print('\n')

print('Injector Areas')
print_dictonary(injector_areas)
print('\n')

print('Pintle Geometry')
print_dictonary(pintle_geometry)
print('\n')

print('Annulus Geometry')
print_dictonary(annulus_geometry)
"""

