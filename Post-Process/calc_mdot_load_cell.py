def calc_mdot_load_cell(tank_mass, dt):
    """
    Inputs
        tank_mass: list of tank masses
        dt: integer time step
    Outputs
        mdot_load_cell: list of mdot_load_cell values
    """
    
    mdot_load_cell = []
    for i in range(len(tank_mass)):
        mdot = (tank_mass[i] - tank_mass[i-1]) / dt
        mdot_load_cell.append(mdot)
    return mdot_load_cell