def calc_pc_star(A_throat, cstar, mdot_tot):
    pc_star =  mdot_tot * cstar / A_throat
    return pc_star