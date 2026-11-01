from chamber_sizing import chamber_sizing
from chamber_def import chamber_def
#from nozzle_sizing import nozzle_sizing
#from injector_sizing import injector_sizing
#from print_dictionaries import print_dictonary

g = 9.81
psi_to_Pa = 6894.75729      # psi * psi_to_Pa = Pa
rho = 786
dp_N2O = 15             # Pressure loss from tank to injector face
dp_IPA = 45
Cd = 0.4
p_tank = 465 * psi_to_Pa

ThrustMin = 420 # [lbf]
ThrustMax = 500    # [lbf]
Thrust_Range = [ThrustMin, ThrustMax]

Pc_step = 1
Pc_Low = 420
Pc_High = 520
Pc_Range = range(Pc_Low, Pc_High, Pc_step)

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
Af_Range = range(Af_Min, Af_Max, A_step)


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
counter = 0
resuls = []
Chamber_def = chamber_def(L_star)

results = chamber_sizing(Pc_Range, OF_Range, Thrust_Range, Aox_Range, Af_Range,p_tank, L_star, Pe, eta_cstar, eta_nozzle, eta_Cf)
print(results)