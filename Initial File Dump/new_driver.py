from chamber_sizing import chamber_sizing
from chamber_def import chamber_def
import numpy as np
from rocketCEA_run import rocketCEA_run
from nozzle_sizing import nozzle_sizing
import matplotlib.pyplot as plt
#from injector_sizing import injector_sizing
#from print_dictionaries import print_dictonary

g = 9.81
psi_to_Pa = 6894.75729      # psi * psi_to_Pa = Pa
rho = 786
Cd = 0.4
p_tank = 500 * psi_to_Pa

lbf_to_N = 4.44822    # lbf * lbf_to_N = N

ThrustMin = 445 * lbf_to_N    # [N]
ThrustMax = 650 * lbf_to_N    # [N]
Thrust_Range = [ThrustMin, ThrustMax]

Pc_step = 1 * psi_to_Pa
Pc_Low = 340 * psi_to_Pa
Pc_High = 360 * psi_to_Pa
Pc_Range = np.arange(Pc_Low, Pc_High, Pc_step)
err_Pc = 0.01;

#Isp = 165   # Specific Impulse
OFMin = 2.8
OFMax = 3.2  # Oxidizer_mass_flow_rate / Fuel_mass_flow_rate
OF_Range = [OFMin, OFMax];

A_step = .0000003

Aox_Min = .000055       #Oxidizer injector area
Aox_Max = .000075
Aox_Range = np.arange(Aox_Min, Aox_Max, A_step)

Af_Min = .000009         #Fuel injector area
Af_Max = .000029
Af_Range = np.arange(Af_Min, Af_Max, A_step)


# Tank Pressure
#p_tank_low = 465 * psi_to_Pa        #  What is the initial N2O pressure in the tank
dp_N2O = 15 * psi_to_Pa              # Pressure loss from tank to injector face
dp_IPA = 45 * psi_to_Pa             # Pressure loss from tank to injector face

# Chamber
#Pc = 350        # [psi]
L_star = 0.635      # 25 [in] for N2O/IPA, dependant on propellant combination
alpha = 15          # Conical nozzle expansion angle
eta_cstar = 0.85
eta_nozzle = 0.98
eta_Cf = .95

# Expansion Pressure
Pe = 101325         # Nozzle exit pressure design point




results,nozzle_inputs, results_max = chamber_sizing(Pc_Range, OF_Range, Thrust_Range, Aox_Range, A_step,p_tank, L_star, Pe, eta_cstar, eta_nozzle, eta_Cf, dp_IPA, Cd, rho, dp_N2O,err_Pc)
nozzle_angles, n_def, nozzle_dimensions = nozzle_sizing(nozzle_inputs['Chamber_def'], nozzle_inputs['epsilon_e'],alpha)
#inj_to_throat = results['Cyl Length'] + 1.5*n_def['Rt'] 

#print("Injector to Throat Length:", inj_to_throat)
print("Results at Max Fuel Area:", results_max)
#print("Nozzle Inputs:", nozzle_inputs)                                                                            
#print("Nozzle Angles:", nozzle_angles)
#print("Nozzle Def:", n_def)

