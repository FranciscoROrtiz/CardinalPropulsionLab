from calculate_injector_Area import calculate_injector_Area
from calculate_mass_flux_rate import calculate_mass_flux_rate
from Mercury.define_conditions_ox import define_conditions
from define_conditions_fuel import define_conditions_fuel


def injector_areas(p_N2O, p_IPA, Pc, mdot_ox, Cd_ox, mdot_fuel_comb, mdot_fuel_film, Cd_fuel, rho_IPA):
    # Constants
    psi_to_Pa = 6894.75729      # psi * psi_to_Pa = Pa

    injector_areas = {}

    # Convert pressures to SI Units [Pa]
    p1_N2O = p_N2O * psi_to_Pa    # Nitrous pressure upstream of injector face
    p1_IPA = p_IPA * psi_to_Pa      # IPA pressure upstream of injector face

    p_2 = Pc * psi_to_Pa            # Pressure downstream of injector face (chamber pressure)

    # Define propellants
    N2O = define_conditions(p1_N2O,p_2)
    IPA = define_conditions_fuel(p1_IPA, p_2, rho_IPA)

    # Calculate Injector Areas

    # Nitrous
    G_N2O = calculate_mass_flux_rate(N2O)
    injector_areas['A_N2O'] = calculate_injector_Area(G_N2O, mdot_ox, Cd_ox)

    # IPA
    G_IPA = calculate_mass_flux_rate(IPA)
    injector_areas['A_IPA_comb'] = calculate_injector_Area(G_IPA, mdot_fuel_comb, Cd_fuel)
    injector_areas['A_IPA_film'] = calculate_injector_Area(G_IPA, mdot_fuel_film, Cd_fuel)

    """
    print(f"A_ox = {A_N2O}")
    print(f"A_fuel_comb = {A_IPA_comb}")
    print(f"A_fuel_film = {A_IPA_film}")
    """

    return injector_areas
