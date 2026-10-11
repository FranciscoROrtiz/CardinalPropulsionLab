def throat_area_calc(Pc, Tc, gamma, mdot_tot, R, eta_cstar):
    A_throat = (mdot_tot/Pc) * ((Tc*R)/gamma)**0.5 * (1 + (gamma-1)/2)**((gamma+1)/(2*(gamma-1))) * eta_cstar

    return A_throat