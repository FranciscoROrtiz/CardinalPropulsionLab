import numpy as np
import CoolProp.CoolProp as CP


# ============================================================
# USER INPUTS
# ============================================================

# Pressures [psi]
P1_N2O = 450.0       # N2O upstream pressure
P2_N2O = 350.0       # N2O downstream pressure

P1_IPA = 425.0       # IPA upstream pressure
P2_IPA = 350.0       # IPA downstream pressure

# Total injector flow areas [mm^2]
A_N2O = 38.34         # Total N2O orifice area
A_IPA = 13.15         # Total IPA orifice area

# Discharge coefficients
Cd_N2O = 0.4
Cd_IPA = 0.4

# IPA density [kg/m^3]
rho_IPA = 785.0


# ============================================================
# CONSTANTS
# ============================================================

PSI_TO_PA = 6894.757
MM2_TO_M2 = 1e-6


# ============================================================
# N2O PROPERTIES
# ============================================================

def get_N2O_density(P1):
    """
    Calculate saturated-liquid N2O density at upstream
    pressure P1.

    Parameters
    ----------
    P1 : float
        Upstream pressure [Pa]

    Returns
    -------
    rho : float
        Saturated-liquid density [kg/m^3]
    T : float
        Saturation temperature [K]
    """

    T = CP.PropsSI(
        'T',
        'P', P1,
        'Q', 0,
        'N2O'
    )

    rho = CP.PropsSI(
        'D',
        'P', P1,
        'Q', 0,
        'N2O'
    )

    return rho, T


# ============================================================
# SPI MASS FLOW RATE
# ============================================================

def calculate_mass_flow_rate(
    P1_psi,
    P2_psi,
    area_mm2,
    Cd,
    density
):
    """
    Calculate mass flow rate using the SPI model.

    G = sqrt(2 * rho * delta_P)
    mdot = Cd * A * G

    Parameters
    ----------
    P1_psi : float
        Upstream pressure [psi]
    P2_psi : float
        Downstream pressure [psi]
    area_mm2 : float
        Total injector flow area [mm^2]
    Cd : float
        Discharge coefficient
    density : float
        Fluid density [kg/m^3]

    Returns
    -------
    dict
        Pressure drop, mass flux, and mass flow rate
    """

    if area_mm2 < 0:
        raise ValueError("Injector area cannot be negative.")

    if density <= 0:
        raise ValueError("Density must be positive.")

    if not 0 <= Cd <= 1:
        raise ValueError("Cd must be between 0 and 1.")

    P1 = P1_psi * PSI_TO_PA
    P2 = P2_psi * PSI_TO_PA

    delta_P = P1 - P2

    if delta_P < 0:
        raise ValueError(
            "Upstream pressure must be >= downstream pressure."
        )

    area = area_mm2 * MM2_TO_M2

    # SPI mass flux [kg/(m^2*s)]
    G = np.sqrt(2.0 * density * delta_P)

    # Mass flow rate [kg/s]
    mdot = Cd * area * G

    return {
        'delta_P_psi': P1_psi - P2_psi,
        'mass_flux': G,
        'mass_flow': mdot
    }


# ============================================================
# CALCULATIONS
# ============================================================

# N2O: saturated-liquid properties at upstream pressure
rho_N2O, T_N2O = get_N2O_density(
    P1_N2O * PSI_TO_PA
)

# N2O mass flow
result_N2O = calculate_mass_flow_rate(
    P1_N2O,
    P2_N2O,
    A_N2O,
    Cd_N2O,
    rho_N2O
)

# IPA: assumed constant liquid density
result_IPA = calculate_mass_flow_rate(
    P1_IPA,
    P2_IPA,
    A_IPA,
    Cd_IPA,
    rho_IPA
)


# ============================================================
# OUTPUT
# ============================================================

print("\n==============================================")
print("       SPI INJECTOR MASS FLOW ANALYSIS")
print("==============================================")

print("\nNITROUS OXIDE (N2O)")
print("----------------------------------------------")
print(f"Upstream pressure:       {P1_N2O:.2f} psi")
print(f"Downstream pressure:     {P2_N2O:.2f} psi")
print(f"Pressure drop:           {result_N2O['delta_P_psi']:.2f} psi")
print(f"Injector area:           {A_N2O:.4f} mm^2")
print(f"Discharge coefficient:   {Cd_N2O:.3f}")
print(f"Density:                 {rho_N2O:.2f} kg/m^3")
print(f"Saturation temperature:  {T_N2O:.2f} K")
print(f"Mass flux:               {result_N2O['mass_flux']:.2f} kg/(m^2*s)")
print(f"Mass flow rate:          {result_N2O['mass_flow']:.6f} kg/s")

print("\nISOPROPANOL (IPA)")
print("----------------------------------------------")
print(f"Upstream pressure:       {P1_IPA:.2f} psi")
print(f"Downstream pressure:     {P2_IPA:.2f} psi")
print(f"Pressure drop:           {result_IPA['delta_P_psi']:.2f} psi")
print(f"Injector area:           {A_IPA:.4f} mm^2")
print(f"Discharge coefficient:   {Cd_IPA:.3f}")
print(f"Density:                 {rho_IPA:.2f} kg/m^3")
print(f"Mass flux:               {result_IPA['mass_flux']:.2f} kg/(m^2*s)")
print(f"Mass flow rate:          {result_IPA['mass_flow']:.6f} kg/s")

print("\nMIXTURE")
print("----------------------------------------------")

mdot_N2O = result_N2O['mass_flow']
mdot_IPA = result_IPA['mass_flow']

if mdot_IPA > 0:
    OF = mdot_N2O / mdot_IPA
    print(f"Total mass flow:         {mdot_N2O + mdot_IPA:.6f} kg/s")
    print(f"O/F ratio:               {OF:.4f}")
else:
    print("O/F ratio:               Undefined (zero IPA flow)")

print("==============================================")
