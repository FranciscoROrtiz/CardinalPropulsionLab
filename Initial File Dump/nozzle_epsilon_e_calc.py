from nozzle_Me_calc import nozzle_Me_calc

def nozzle_epsilon_e_calc(Pc, Pe, gamma):
    Me = nozzle_Me_calc(Pc, Pe, gamma)
    epsilon_e = 1/Me * ((2/(gamma+1))*(1 + ((gamma-1)/2)*Me**2))**((gamma+1)/(2*(gamma-1)))

    return epsilon_e