def calc_thrust(eta_Cf, Cf, Pc, A_throat):
    Thrust = eta_Cf * Cf * Pc * A_throat
    return Thrust