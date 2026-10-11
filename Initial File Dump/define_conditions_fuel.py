import CoolProp.CoolProp as CP

def define_conditions_fuel(p_1, p_2, rho):
    # Define the fluid and conditions
    fluid = 'IPA'  # Isopropanol
    fluid_properties = {
        'P_1': p_1,  # Pressure in Pascals
        'P_2': p_2,   # Pressure in Pascals
        'density_1': rho
    }

    return fluid_properties
