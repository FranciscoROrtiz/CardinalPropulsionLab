from rocketcea.cea_obj import CEA_Obj

def rocketCEA_run(Pc, OF):

    combustion_gas_properties = {}

    cea = CEA_Obj(
        oxName="N2O",
        fuelName="Isopropanol"
    )

    # Generate full NASA CEA output
    output = cea.get_full_cea_output(
        Pc=Pc,
        MR=OF,
        short_output=False
    )

    # ---------------------------------------------------------
    # Extract chamber temperature and Cp from CEA output
    # ---------------------------------------------------------

    lines = output.splitlines()

    Tc = None
    Cp_cal = None

    for i, line in enumerate(lines):

        # Find the chamber/throat/exit property table
        if "T, K" in line:
            values = line.split()

            # Last 3 values are CHAMBER, THROAT, EXIT
            Tc = float(values[-3])

        # Find the Cp row
        if "Cp, CAL/(G)(K)" in line:
            values = line.split()

            # Last 3 values are CHAMBER, THROAT, EXIT
            Cp_cal = float(values[-3])

    # Convert Cp from cal/(g*K) to J/(kg*K)
    Cp = Cp_cal * 4184.0

    # ---------------------------------------------------------
    # Other chamber properties
    # ---------------------------------------------------------

    MW, gamma = cea.get_Chamber_MolWt_gamma(Pc=Pc, MR=OF)

    Ru = 8314.462618                  # J/(kmol*K)
    R = Ru / MW                       # J/(kg*K)

    cstar_ft_s = cea.get_Cstar(Pc=Pc, MR=OF)
    cstar = cstar_ft_s * 0.3048       # m/s

    # ---------------------------------------------------------
    # Store results
    # ---------------------------------------------------------

    combustion_gas_properties['Pc'] = Pc
    combustion_gas_properties['OF'] = OF
    combustion_gas_properties['Tc'] = Tc
    combustion_gas_properties['gamma'] = gamma
    combustion_gas_properties['MW'] = MW
    combustion_gas_properties['R'] = R
    combustion_gas_properties['Cp'] = Cp
    combustion_gas_properties['cstar'] = cstar

    return combustion_gas_properties