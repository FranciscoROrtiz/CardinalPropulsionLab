def calc_cstar(Pc, A_throat, mdot_tot):
    """
    Inputs
        Pc: list of chamber pressures
        A_throat: integer value of throat area
        mdot_tot: list of mdot_tot values
    
    Output
        cstar: list of cstar values
    """

    
    cstar = Pc * A_throat / mdot_tot
    return cstar