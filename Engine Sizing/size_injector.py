from calculate_injector_Area import calculate_injector_Area
from calculate_mass_flux_rate import calculate_mass_flux_rate
from Mercury.define_conditions_ox import define_conditions
from define_conditions_fuel import define_conditions_fuel
"""
vvv INPUTS vvv
"""

p_tank_low = 400            # [psi]
stiffness = 0.2             # ex. 0.2 = 20% stiffness

# Oxidizer inputs
mdot_ox = 1.0202        # kg/s
Cd_ox = 0.4

# Fuel inputs
mdot_fuel = 0.3401      # kg/s
Cd_fuel = 0.4
rho_IPA = 785       # kg/m^3
film_cooling_percentage = 0.2      # mdot_fuel_film / mdot_fuel


"""
^^^ INPUTS ^^^
"""

# Constants
psi_to_Pa = 6894.75729      # psi * psi_to_Pa = Pa
mdot_fuel_comb = mdot_fuel * (1 - film_cooling_percentage)
mdot_fuel_film = mdot_fuel * film_cooling_percentage


# Calculate chamber pressure
pc = p_tank_low / (stiffness + 1)

# Convert pressures to SI Units [Pa]
p_1 = p_tank_low * psi_to_Pa    # Pressure upstream of injector face
p_2 = pc * psi_to_Pa            # Pressure downstream of injector face (chamber pressure)

# Define propellants
N2O = define_conditions(p_1,p_2)
IPA = define_conditions_fuel(p_1, p_2, rho_IPA)

# Calculate Injector Areas

# Nitrous
G_N2O = calculate_mass_flux_rate(N2O)
A_N2O = calculate_injector_Area(G_N2O, mdot_ox, Cd_ox)

# IPA
G_IPA = calculate_mass_flux_rate(IPA)
A_IPA_comb = calculate_injector_Area(G_IPA, mdot_fuel_comb, Cd_fuel)
A_IPA_film = calculate_injector_Area(G_IPA, mdot_fuel_film, Cd_fuel)


print(f"A_ox = {A_N2O}")
print(f"A_fuel_comb = {A_IPA_comb}")
print(f"A_fuel_film = {A_IPA_film}")
