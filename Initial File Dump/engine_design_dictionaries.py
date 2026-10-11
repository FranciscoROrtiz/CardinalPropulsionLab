
# ============================================================
# DESIGN DATA ORGANIZATION
# ============================================================

def create_design_dictionaries(
    inputs,
    chamber_def,
    combustion_gas_properties,
    epsilon_e,
    chamber_dimensions,
    mass_flow_rates,
    nozzle_angles,
    nozzle_def,
    nozzle_dimensions,
    injector_areas,
    pintle_geometry,
    annulus_geometry,
    film_geometry
):
    """
    Organize design inputs and calculated results into dictionaries.

    Parameters
    ----------
    inputs : dict
        User-defined design inputs.

    Other parameters
    ----------------
    Calculated results from chamber, nozzle, and injector sizing.

    Returns
    -------
    inputs : dict
        Original input dictionary.

    results : dict
        Organized calculated results.
    """

    # ========================================================
    # RESULTS DICTIONARY
    # ========================================================

    results = {

        "MASS FLOW RATES": mass_flow_rates,

        "CHAMBER DEFINITION": chamber_def,

        "CHAMBER DIMENSIONS": chamber_dimensions,

        "COMBUSTION GAS PROPERTIES": combustion_gas_properties,

        "NOZZLE DEFINITION": {
            **nozzle_def,
            "epsilon_e": epsilon_e
        },

        "NOZZLE ANGLES": nozzle_angles,

        "NOZZLE DIMENSIONS": nozzle_dimensions,

        "INJECTOR AREAS": injector_areas,

        "PINTLE GEOMETRY": pintle_geometry,

        "ANNULUS GEOMETRY": annulus_geometry,

        "FILM GEOMETRY": film_geometry
    }

    return inputs, results