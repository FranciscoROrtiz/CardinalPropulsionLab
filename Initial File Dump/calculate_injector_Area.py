def calculate_injector_Area(G, mdot_ox, Cd):
    Area = mdot_ox / (G * Cd)

    return Area
