from chamber_sizing import chamber_sizing
from nozzle_def import nozzle_def
from nozzle_dimensions_calc import nozzle_dimensions_calc
from print_dictionaries import print_dictonary
from nozzle_rao_parabola_angles import calculate_parabolic_angles

"""
vvv Inputs vvv
"""
# Thrust = 450
# Isp = 150
# OF = 3

# p_tank_low = 450
# stiffness = 0.2

# L_star = 0.635      # 25 [in]
# epsilon_c = 5

# Pe = 101325

#alpha = 15
#theta_n = 22.5
#theta_e = 14

"""
^^^ Inputs ^^^
"""

# chamber_def, combustion_gas_properties, epsilon_e, chamber_dimensions, mass_flow_rates = size_a_good_portion_of_engine(Thrust, Isp, OF, p_tank_low, stiffness, L_star, epsilon_c, Pe)

def nozzle_sizing(chamber_def, epsilon_e,alpha):
    nozzle = {}
    nozzle_angles = calculate_parabolic_angles(epsilon_e)
    n_def = nozzle_def(alpha, nozzle_angles['theta_n'], nozzle_angles['theta_e'], chamber_def)
    nozzle_dimensions = nozzle_dimensions_calc(n_def, epsilon_e)  # Nozzle Length
    return nozzle_angles, n_def, nozzle_dimensions



"""
# Step 4: Nozzle
nozzle_angles = calculate_parabolic_angles(epsilon_e)
nozzle_def = nozzle_def(alpha, nozzle_angles['theta_n'], nozzle_angles['theta_e'], chamber_def)
nozzle_dimensions = nozzle_dimensions_calc(nozzle_def, epsilon_e) # Nozzle Length


print('Nozzle Definition')
print_dictonary(nozzle_def)
print('\n')

print('Nozzle Dimensions')
print_dictonary(nozzle_dimensions)
print('\n')
"""