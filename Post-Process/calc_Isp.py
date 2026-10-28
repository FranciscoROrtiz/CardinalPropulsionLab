def calc_Isp(Thrust, mdot_tot, g=9.81): 
    return Thrust / (mdot_tot * g)