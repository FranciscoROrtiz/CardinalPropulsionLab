from rocketCEA_run import rocketCEA_run

def calc_adiabatic_flame_temp(Pc, OF):
    """
    Inputs
        Pc: list of chamber pressures
        OF: list of OF values
    Outputs
        Tc_values: list of chamber temperatures
    """

    Tc_values = []
    for i in Pc:
        for j in OF:
            result = rocketCEA_run(i, j)
            Tc_values.append(result['Tc'])  
    return Tc_values