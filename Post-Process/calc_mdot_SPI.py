from define_conditions_ox import define_conditions_ox

def calc_mdot_SPI(p1, p2, A, fluid, Cd):
    """
    Inputs
        p1: List of upstream pressures
        p2: List of downstream pressures
        A: Flow area
        fluid: Identity of fluid ("N2O" or "IPA")
        Cd: Discharge coefficient (0-1)
    """
    
    mdot_SPI = []
    if fluid == "N2O":
        for i in range(len(p1)):
            fluid_properties = define_conditions_ox(p1[i], p2[i])
            mdot_SPI_i = Cd * A * (2 * fluid_properties['density_1'] * (p1 - p2))**0.5
            mdot_SPI.append(mdot_SPI_i)
    else:
        fluid_properties = {'density_1': 785}
        rho = fluid_properties['density_1']
        mdot_SPI = Cd * A * (2 * fluid_properties['density_1'] * (p1 - p2))**0.5    

    return mdot_SPI