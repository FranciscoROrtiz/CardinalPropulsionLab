
from rocketCEA_run import rocketCEA_run
from nozzle_contraction_ratio import calculate_contraction_ratio
from throat_area_calc import throat_area_calc
from area_to_diameter import area_to_diameter
from chamber_dimensions_calc import chamber_dimensions_calc
from nozzle_epsilon_e_calc import nozzle_epsilon_e_calc
from calc_OF import calc_OF
from calc_fuel_mass_flow_rate import calc_fuel_mass_flow_rate
from calc_ox_mass_flow_rate import calc_ox_mass_flow_rate
from calc_pc_star import calc_pc_star
from calc_cf import calc_Cf
from calc_thrust import calc_thrust
from chamber_def import chamber_def
from calc_fuel_area import calc_fuel_area
import numpy as np
import matplotlib.pyplot as plt


def chamber_sizing(Pc_Range, OF_Range, Thrust_Range, Aox_Range, A_step,p_tank, L_star, Pe, eta_cstar, eta_nozzle, eta_Cf, dp_IPA, Cd, rho, dp_N2O,err_Pc):

    counter = 0
    num_pass = 0
    pass_Pc = 0
    pass_Thrust = 0
    thrust_max = 0
   

    
    for i in range(len(Pc_Range)):
        Pc = Pc_Range[i]

        for j in range(len(Aox_Range)):
            A_ox = Aox_Range[j]
            mdot_ox = calc_ox_mass_flow_rate(A_ox, Pc, p_tank, dp_N2O, Cd)
            mdot_fuel_min = mdot_ox /  OF_Range[1]
            mdot_fuel_max = mdot_ox / OF_Range[0]
            A_fuel_min = calc_fuel_area(mdot_fuel_min, Pc, p_tank, dp_IPA, Cd, rho)
            A_fuel_max = calc_fuel_area(mdot_fuel_max, Pc, p_tank, dp_IPA, Cd, rho)
         

            for A_fuel in np.arange(A_fuel_min, A_fuel_max, A_step):
                counter += 1
                mdot_fuel = calc_fuel_mass_flow_rate(A_fuel, Pc, p_tank, dp_IPA, Cd,rho)
                OF = mdot_ox / mdot_fuel
                combustion_gas_properties = rocketCEA_run(Pc, OF)
                mdot_tot = mdot_fuel + mdot_ox
                A_throat = throat_area_calc(Pc, combustion_gas_properties['Tc'],
                combustion_gas_properties['gamma'], mdot_tot, combustion_gas_properties['R'], eta_cstar)
                Pc_star = calc_pc_star(A_throat, combustion_gas_properties['cstar']*eta_cstar, mdot_tot)
                print("Pc_star:", Pc_star)
                print("Pc:", Pc)
                err_PC_star = abs(Pc_star - Pc) / abs(Pc)

                if err_PC_star > err_Pc:
                    continue
                else:
                    
                    pass_Pc += 1
                    epsilon_e = nozzle_epsilon_e_calc(Pc, Pe, combustion_gas_properties['gamma'])
                    Cf = calc_Cf(combustion_gas_properties['gamma'], Pe,Pc, epsilon_e)
                    thrust = calc_thrust(eta_Cf, Cf, Pc, A_throat)
                    print(f"Thrust: {thrust*0.224809}")
                    if not (Thrust_Range[0] <= thrust <= Thrust_Range[1]):
                        continue
                    else:
                        pass_Thrust += 1
                     
                        Chamber_def = chamber_def(L_star)
                        Chamber_def['A_throat'] = A_throat
                        Chamber_def['d_throat'] = area_to_diameter(Chamber_def['A_throat'])
                        Chamber_def['epsilon_c'] = calculate_contraction_ratio(Chamber_def['d_throat'])
                        chamber_dimensions = chamber_dimensions_calc(Chamber_def)  
                        exit_area = Chamber_def['A_throat'] * epsilon_e
                        Chamber_def['Exit Diameter'] = area_to_diameter(exit_area)
                        if chamber_dimensions['diameter']*39.3701 > 3:
                            continue
                        else:
                            if thrust > thrust_max:
                                thrust_max = thrust
                                combustion_properties_max = combustion_gas_properties
                                results_max = {
                                    'A_throat': A_throat,
                                    'd_throat': Chamber_def['d_throat'],
                                    'Pc': Pc,
                                    'Aox': A_ox,
                                    'Af': A_fuel,
                                    'err': err_PC_star,
                                    'mdot_fuel': mdot_fuel,
                                    'mdot_ox': mdot_ox,
                                    'OF_max': OF,
                                    'thrust': thrust,
                                    'Cyl Length': chamber_dimensions['length'],
                                    'Chamber Diameter': chamber_dimensions['diameter'],
                                    'Exit Diameter': Chamber_def['Exit Diameter'],
                                    'Injector to Throat Length': chamber_dimensions['length'] + 1.5*0.5*Chamber_def['d_throat'], #technically not actually
                                                                                             # how you find injector to throat length but it's close enough
                                    'Combustion Properties': combustion_properties_max
                                }
                                nozzle_inputs = {
                                                'Chamber_def': Chamber_def,
                                                'epsilon_e': epsilon_e,
                                                        }
            

                        num_pass +=1
       


   
       


    


    print("Number of passing cases:", num_pass)
    print("Number of passing Pc Cases:", pass_Pc)
    print("Number of passing Thrust Cases:", pass_Thrust)
    print("Total number of cases:", counter)
    return results_max, nozzle_inputs
