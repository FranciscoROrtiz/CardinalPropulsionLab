def nozzle_Me_calc(Pc, Pe, gamma):
    Me = (2*((Pe/Pc)**((gamma-1)/-gamma) - 1)/(gamma-1))**0.5

    return Me