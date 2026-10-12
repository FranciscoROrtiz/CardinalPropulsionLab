
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
#from nozzle_contraction_ratio import calculate_contraction_ratio
#from nozzle_sizing import nozzle_sizing
from calc_fuel_area import calc_fuel_area
import numpy as np
import matplotlib.pyplot as plt


def chamber_sizing(Pc_Range, OF_Range, Thrust_Range, Aox_Range, A_step,p_tank, L_star, Pe, eta_cstar, eta_nozzle, eta_Cf, dp_IPA, Cd, rho, dp_N2O,err_Pc):

    counter = 0
    num_pass = 0
    results = []
    #pass_OF = 0
    pass_Pc = 0
    pass_Thrust = 0
    err_low_array = []
    Pc_low_array = []
    Aox_low_array = []
    mdot_ox_low_array = []
    mdot_fuel_low_array = []
    A_fuel_low_array = []
    thrust_low_array = []
    A_throat_low_array = []
    for i in range(len(Pc_Range)):
        err_low = 1
        Pc = Pc_Range[i]
        Pc_low = Pc
        Aox_low = 0
        mdot_ox_low= 0
        mdot_fuel_low = 0
        A_fuel_low = 0
        thrust_low = 0
        A_throat_low = 0
        A_fuelmax = 0
        #print(Pc)

        for j in range(len(Aox_Range)):
            A_ox = Aox_Range[j]
            mdot_ox = calc_ox_mass_flow_rate(A_ox, Pc, p_tank, dp_N2O, Cd)
            mdot_fuel_min = mdot_ox /  OF_Range[1]
            mdot_fuel_max = mdot_ox / OF_Range[0]
            A_fuel_min = calc_fuel_area(mdot_fuel_min, Pc, p_tank, dp_IPA, Cd, rho)
            A_fuel_max = calc_fuel_area(mdot_fuel_max, Pc, p_tank, dp_IPA, Cd, rho)
         

            for A_fuel in np.arange(A_fuel_min, A_fuel_max, A_step):
                counter += 1
                #print("OF:", OF)
                mdot_fuel = calc_fuel_mass_flow_rate(A_fuel, Pc, p_tank, dp_IPA, Cd,rho)
                OF = mdot_ox / mdot_fuel
                combustion_gas_properties = rocketCEA_run(Pc, OF)
                #print("Gamma:", combustion_gas_properties['gamma'])
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
                        if err_PC_star < err_low:
                            err_low = err_PC_star
                            Pc_low = Pc
                            Aox_low = A_ox
                            mdot_ox_low= mdot_ox
                            mdot_fuel_low = mdot_fuel
                            A_fuel_low = A_fuel
                            thrust_low = thrust
                            A_throat_low = A_throat
                        pass_Thrust += 1
                        # print("\n Thrust:", thrust)
                        if A_fuel > A_fuelmax:
                            A_fuelmax = A_fuel
                            err_max = err_PC_star
                            Pc_max = Pc
                            Aox_max = A_ox
                            mdot_ox_max= mdot_ox
                            mdot_fuel_max = mdot_fuel
                            thrust_max = thrust
                            A_throat_max = A_throat
                            OF_max = OF
                        Chamber_def = chamber_def(L_star)
                        Chamber_def['A_throat'] = A_throat
                        Chamber_def['d_throat'] = area_to_diameter(Chamber_def['A_throat'])
                        Chamber_def['epsilon_c'] = calculate_contraction_ratio(Chamber_def['d_throat'])
                        chamber_dimensions = chamber_dimensions_calc(Chamber_def)  # Diameter, Volume, Chamber Area, Chamber Length
                        exit_area = chamber_dimensions['area'] * epsilon_e
                        Chamber_def['Exit Diameter'] = area_to_diameter(exit_area)
                        
                        # run = {}
                        # run['A_throat'] = A_throat
                        # run['Pc'] = Pc
                        # run['Aox'] = A_ox
                        # run['Af'] = A_fuel
                        # run['OF'] = OF
                        # run['mdot_fuel'] = mdot_fuel
                        # run['mdot_ox'] = mdot_ox
                        # run['thrust'] = thrust
                        # run['Cyl Length'] = chamber_dimensions['length']
                        # run['Chamber Diameter'] = chamber_dimensions['diameter']
                        # run['Exit Diameter'] = Chamber_def['Exit Diameter']
                        # results = run

                        nozzle_inputs = {
                            'Chamber_def': Chamber_def,
                            'epsilon_e': epsilon_e,
                        }

                        num_pass +=1
        # err_low_array.append(err_low)
        # Pc_low_array.append(Pc_low)
        # Aox_low_array.append(Aox_low)
        # mdot_ox_low_array.append(mdot_ox_low)
        # mdot_fuel_low_array.append(mdot_fuel_low)
        # A_fuel_low_array.append(A_fuel_low)
        # thrust_low_array.append(thrust_low)
        # A_throat_low_array.append(A_throat_low)



    results_max = {
        'A_throat': A_throat_max,
        'Pc': Pc_max,
        'Aox': Aox_max,
        'Af': A_fuelmax,
        'err': err_max,
        'mdot_fuel': mdot_fuel_max,
        'mdot_ox': mdot_ox_max,
        'OF_max': OF_max,
        'thrust': thrust_max,
        'Cyl Length': chamber_dimensions['length'],
        'Chamber Diameter': chamber_dimensions['diameter'],
        'Exit Diameter': Chamber_def['Exit Diameter'],
        'Injector to Throat Length': chamber_dimensions['length'] + 1.5*Chamber_def['d_throat']
    }
       


    
    Aox_low_array = np.asarray(Aox_low_array)
    Pc_low_array = np.asarray(Pc_low_array)
    thrust_low_array = np.asarray(thrust_low_array)
    A_fuel_low_array = np.asarray(A_fuel_low_array)
    err_low_array = np.asarray(err_low_array)
    fig, axes = plt.subplots(4, 1, figsize=(8, 9))
    keep = Aox_low_array != 0
    axes[0].plot(Aox_low_array[keep], err_low_array[keep])
    axes[0].set_xlabel('Aox')
    axes[0].set_title('Error in Pc vs Aox')

    keep = Pc_low_array != 0
    axes[1].plot(Pc_low_array[keep], err_low_array[keep])
    axes[1].set_xlabel('Pc')
    axes[1].set_title('Error in Pc vs Pc')

    keep = thrust_low_array != 0
    axes[2].plot(thrust_low_array[keep], err_low_array[keep])
    axes[2].set_xlabel('Thrust')
    axes[2].set_title('Error in Pc vs Thrust')

    keep = A_fuel_low_array != 0
    axes[3].plot(A_fuel_low_array[keep], err_low_array[keep])
    axes[3].set_xlabel('Af')
    axes[3].set_title('Error in Pc vs Af')

    for ax in axes:
        ax.set_ylabel('Error in Pc')

    fig.tight_layout()
    plt.show()

    print("Number of passing cases:", num_pass)
    #print("Number of passing OF Cases:", pass_OF)
    print("Number of passing Pc Cases:", pass_Pc)
    print("Number of passing Thrust Cases:", pass_Thrust)
    print("Total number of cases:", counter)
    return results, nozzle_inputs, results_max
