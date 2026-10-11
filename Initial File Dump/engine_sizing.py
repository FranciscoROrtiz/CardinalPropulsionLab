from chamber_sizing import chamber_sizing
from nozzle_sizing import nozzle_sizing
from injector_sizing import injector_sizing
from print_dictionaries import print_dictonary

from engine_design_dictionaries import create_design_dictionaries
from engine_save_results import save_results

"""
vvv Inputs vvv
"""

# System Top-Level Requirements
ThrustMin = 1 # [lbf]
ThrustMax = 1    # [lbf]
Thrust_Range = [ThrustMin, ThrustMax]

Pc_step = 1
Pc_Low = 420
Pc_High = 520
PC_Range = range(Pc_Low, Pc_High, Pc_step)

#Isp = 165   # Specific Impulse
OFMin = 2.8
OFMax = 3.2  # Oxidizer_mass_flow_rate / Fuel_mass_flow_rate
OF_Range = [OFMin, OFMax];

A_step = .0000001

Aox_Min = .000035       #Oxidizer injector area
Aox_Max = .000055
Aox_Range = range(Aox_Min, Aox_Max, A_step)

Af_Min = .000009         #Fuel injector area
Af_Max = .000029
Af_range = range(Af_Min, Af_Max, A_step)


# Tank Pressure
p_tank_low = 465        # [psi] What is the initial N2O pressure in the tank
dp_N2O = 15             # Pressure loss from tank to injector face
dp_IPA = 45             # Pressure loss from tank to injector face

# Chamber
#Pc = 350        # [psi]
L_star = 0.635      # 25 [in] for N2O/IPA, dependant on propellant combination
alpha = 15          # Conical nozzle expansion angle
eta_cstar = 0.85
eta_nozzle = 0.98
eta_Cf = .95

# Expansion Pressure
Pe = 101325         # Nozzle exit pressure design point

# Injector
stiffness = 0.2         # (feed_pressure - chamber_pressure) / chamber pressure
Cd_ox = 0.4
Cd_fuel = 0.4
rho_IPA = 785       # kg/m^3
film_cooling_percentage = 0.5      # mdot_fuel_film / mdot_fuel
film_cooling_percentage = 0.10      # mdot_fuel_film / mdot_tot
smallest_drill = 62     # Smallest allowable drill bit for film cooling holes (ex. 61 = #61)


"""
^^^ Inputs ^^^
"""

# Input Dictionary

inputs = {
    "Thrust_lbf": Thrust,
    "Isp_s": Isp,
    "OF": OF,

    "p_tank_low_psi": p_tank_low,
    "dp_N2O_psi": dp_N2O,
    "dp_IPA_psi": dp_IPA,

    "Pc_psi": Pc,
    "L_star_m": L_star,
    "alpha_deg": alpha,

    "Pe_Pa": Pe,

    "stiffness": stiffness,
    "Cd_ox": Cd_ox,
    "Cd_fuel": Cd_fuel,
    "rho_IPA_kg_m3": rho_IPA,
    "film_cooling_percentage": film_cooling_percentage,
    "smallest_drill": smallest_drill}


# Chamber Sizing
chamber_def, combustion_gas_properties, epsilon_e, chamber_dimensions, mass_flow_rates = chamber_sizing(
    Thrust, Isp, OF, p_tank_low, stiffness,
    L_star, Pc, Pe, film_cooling_percentage, eta_cstar, eta_nozzle
)


# Nozzle Sizing
nozzle_angles, nozzle_def, nozzle_dimensions = nozzle_sizing(
    chamber_def,
    combustion_gas_properties,
    epsilon_e,
    chamber_dimensions,
    mass_flow_rates
)


# Injector Sizing
injector_areas, pintle_geometry, annulus_geometry, film_geometry = injector_sizing(
    mass_flow_rates,
    p_tank_low,
    dp_N2O,
    dp_IPA,
    Cd_ox,
    Cd_fuel,
    rho_IPA,
    film_cooling_percentage,
    chamber_dimensions["diameter"],
    Pc,
    smallest_drill
)


# Organize Design Data

inputs, results = create_design_dictionaries(
    inputs=inputs,

    chamber_def=chamber_def,
    combustion_gas_properties=combustion_gas_properties,
    epsilon_e=epsilon_e,
    chamber_dimensions=chamber_dimensions,
    mass_flow_rates=mass_flow_rates,

    nozzle_angles=nozzle_angles,
    nozzle_def=nozzle_def,
    nozzle_dimensions=nozzle_dimensions,

    injector_areas=injector_areas,
    pintle_geometry=pintle_geometry,
    annulus_geometry=annulus_geometry,
    film_geometry=film_geometry
)


# Save Results

csv_filename = save_results(
    inputs=inputs,
    results=results,
    filename_prefix="CPL_engine_design_Analysis"
)

# Print Results
print("#"*40)
print("Combustion Chamber Results")
print("#"*40)
print("Mass Flow Rates")
print_dictonary(mass_flow_rates)
print("\n")

print("Chamber Definition")
print_dictonary(chamber_def)
print('\n')

print('Chamber Dimensions')
print_dictonary(chamber_dimensions)
print('\n')

print('Combustion Gas Properties')
print_dictonary(combustion_gas_properties)
print('\n')



print("#"*40)
print("Nozzle Results")
print("#"*40)

print('Nozzle Definition')
print_dictonary(nozzle_def)
print(f"  epsilon_e = {epsilon_e}")
print('\n')

print('Nozzle Dimensions')
print_dictonary(nozzle_dimensions)
print('\n')


print("#"*40)
print("Injector Results")
print("#"*40)
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
print('\n')

print('Film Geometry')
print_dictonary(film_geometry)