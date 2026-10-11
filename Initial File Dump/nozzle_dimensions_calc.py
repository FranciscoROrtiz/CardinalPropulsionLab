from nozzle_Ln_calc import nozzle_Ln_calc

def nozzle_dimensions_calc(nozzle_def, epsilon_e):
    Ln = nozzle_Ln_calc(nozzle_def, epsilon_e)

    nozzle_dimensions = {
        "Ln": Ln * 0.8,
    }

    return nozzle_dimensions