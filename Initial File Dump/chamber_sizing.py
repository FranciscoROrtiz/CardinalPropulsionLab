from calculate_mass_flow_rates import calculate_mass_flow_rates
from Mercury.rocketCEA_run import rocketCEA_run
from calculate_exhaust_velocity import calculate_exhaust_velocity
from engine_calculate_mass_flow_rates import calculate_mass_flow_rates
from nozzle_contraction_ratio import calculate_contraction_ratio
from Mercury.chamber_def import chamber_def
from Mercury.throat_area_calc import throat_area_calc
from area_to_diameter import area_to_diameter
from Mercury.chamber_dimensions_calc import chamber_dimensions_calc
from Mercury.nozzle_epsilon_e_calc import nozzle_epsilon_e_calc

def chamber_sizing(Thrust, Isp, OF, p_tank_low, stiffness, L_star, Pc, Pe, film_cooling_percentage, eta_cstar, eta_nozzle):
    # Constants
    g = 9.81
    psi_to_Pa = 6894.75729      # psi * psi_to_Pa = Pa
    Chamber_def = chamber_def(L_star)

    combustion_gas_properties = rocketCEA_run(Pc, OF)
    #combustion_gas_properties['Me'] = nozzle_Me_calc(Pc, Pe, combustion_gas_properties['gamma'])
    combustion_gas_properties['Ue'] = calculate_exhaust_velocity(combustion_gas_properties['R'], combustion_gas_properties['gamma'], combustion_gas_properties['Tc'], Pe, Pc)
    # Step 1: Mass Flow Rate
    mass_flow_rates = calculate_mass_flow_rates(Thrust, Isp, g, OF, film_cooling_percentage)
    #mass_flow_rates = calculate_mass_flow_rates(Thrust, combustion_gas_properties['Ue'], eta_nozzle, OF, film_cooling_percentage)

    # Step 2: Throat Area

    Chamber_def['A_throat'] = throat_area_calc(combustion_gas_properties['Pc']*psi_to_Pa, combustion_gas_properties['Tc'], combustion_gas_properties['gamma'], mass_flow_rates['mdot_tot'], combustion_gas_properties['R'], eta_cstar)
    Chamber_def['d_throat'] = area_to_diameter(Chamber_def['A_throat'])

    # Step 3: Chamber
    Chamber_def['epsilon_c'] = calculate_contraction_ratio(Chamber_def['d_throat'])
    #Chamber_def['epsilon_c'] = 3.81617199894
    chamber_dimensions = chamber_dimensions_calc(Chamber_def)       # Diameter, Volume, Chamber Area, Chamber Length

    # Step 4: Nozzle Expansion ratio
    epsilon_e = nozzle_epsilon_e_calc(Pc*psi_to_Pa, Pe, combustion_gas_properties['gamma'])

    return Chamber_def, combustion_gas_properties, epsilon_e, chamber_dimensions, mass_flow_rates

