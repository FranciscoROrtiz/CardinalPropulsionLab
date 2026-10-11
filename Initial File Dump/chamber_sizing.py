
from rocketCEA_run import rocketCEA_run
from nozzle_contraction_ratio import calculate_contraction_ratio
from throat_area_calc import throat_area_calc
#from area_to_diameter import area_to_diameter
#from chamber_dimensions_calc import chamber_dimensions_calc
from nozzle_epsilon_e_calc import nozzle_epsilon_e_calc
from calc_OF import calc_OF
from calc_fuel_mass_flow_rate import calc_fuel_mass_flow_rate
from calc_ox_mass_flow_rate import calc_ox_mass_flow_rate
from calc_pc_star import calc_pc_star
from calc_cf import calc_Cf
from calc_thrust import calc_thrust


def chamber_sizing(Pc_Range, OF_Range, Thrust_Range, Aox_Range, Af_Range,p_tank, L_star, Pe, eta_cstar, eta_nozzle, eta_Cf, combustion_gas_properties, dp_IPA, Cd, rho, dp_N2O):
    counter = 0
    results = []
    for i in range(len(Pc_Range)):
        counter += 1
        Pc = Pc_Range[i]
        for j in range(len(Aox_Range)):
            A_ox = Aox_Range[j]
            for k in range(len(Af_Range)):
                A_fuel = Af_Range[k]
                mdot_fuel = calc_fuel_mass_flow_rate(A_ox, Pc, p_tank, dp_IPA, Cd, rho)
                mdot_ox = calc_ox_mass_flow_rate(A_fuel, Pc, p_tank, dp_N2O, Cd)
                OF = calc_OF(mdot_ox, mdot_fuel)
                if not(OF_Range[1] <= OF <= OF_Range[2]):
                    break
                else:
                    combustion_gas_properties = rocketCEA_run(Pc, OF)
                    mdot_tot = mdot_fuel + mdot_ox
                    A_throat = throat_area_calc(Pc, combustion_gas_properties['Tc'],
                      combustion_gas_properties['gamma'], mdot_tot, combustion_gas_properties['R'],
                                                combustion_gas_properties['cstar'], eta_cstar)
                    Pc_star = calc_pc_star(A_throat, combustion_gas_properties['cstar'], mdot_tot)
                    if Pc_star != Pc:
                        break
                    else:
                        epsilon_e = nozzle_epsilon_e_calc(Pc * psi_to_Pa, Pe, combustion_gas_properties['gamma'])
                        Cf = calc_Cf(combustion_gas_properties['gamma'], Pe,Pc, epsilon_e)
                        thrust = calc_thrust(eta_Cf, Cf, Pc, A_throat)
                        if not (Thrust_Range[1] <= thrust <= Thrust_Range[2]):
                            break
                        else:
                            Chamber_def['d_throat'] = area_to_diameter(Chamber_def['A_throat'])
                            Chamber_def['epsilon_c'] = calculate_contraction_ratio(Chamber_def['d_throat'])
                            chamber_dimensions = chamber_dimensions_calc(Chamber_def)  # Diameter, Volume, Chamber Area, Chamber Length

                            run = {}
                            run['A_throat'] = A_throat
                            run['Pc'] = Pc
                            run['Aox'] = A_ox
                            run['Af'] = A_fuel
                            run['OF'] = OF
                            run['mdot_fuel'] = mdot_fuel
                            run['mdot_ox'] = mdot_ox
                            run['thrust'] = thrust
                            results.append(run)
    return results




