from chamber_sizing import size_a_good_portion_of_engine
from print_dictionaries import print_dictonary

"""
vvv Inputs vvv
"""
Thrust = 450
Isp = 150
OF = 3

p_tank_low = 420
stiffness = 0.2

L_star = 0.635      # 25 [in]
epsilon_c = 5

Pe = 101325


"""
^^^ Inputs ^^^
"""

chamber_def, combustion_gas_properties, epsilon_e, chamber_dimensions, mass_flow_rates = size_a_good_portion_of_engine(Thrust, Isp, OF, p_tank_low, stiffness, L_star, epsilon_c, Pe)

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

print(f"epsilon_e = {epsilon_e}")
