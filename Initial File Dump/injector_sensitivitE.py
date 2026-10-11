import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP


# ============================================================
# INPUTS
# ============================================================

# ------------------------------------------------------------
# Tank / pressurant pressure sweep
# ------------------------------------------------------------

p_tank_min = 350          # [psi]
p_tank_max = 750          # [psi]
num_points = 500

# Nominal tank pressure
p_tank_nominal = 465      # [psi]


# ------------------------------------------------------------
# Chamber pressure
# ------------------------------------------------------------

Pc = 350                  # [psi]


# ------------------------------------------------------------
# Feedline pressure drops
# ------------------------------------------------------------

dp_N2O = 15               # [psi]
dp_IPA = 45               # [psi]


# ------------------------------------------------------------
# Injector flow areas
# ------------------------------------------------------------

A_N2O = 6.49E-05          # [m^2]
A_IPA = 2.78E-05           # [m^2]


# ------------------------------------------------------------
# Discharge coefficients
# ------------------------------------------------------------

Cd_N2O = 0.4
Cd_IPA = 0.4


# ------------------------------------------------------------
# IPA properties
# ------------------------------------------------------------

rho_IPA = 785             # [kg/m^3]


# ------------------------------------------------------------
# O/F allowable limits
# ------------------------------------------------------------

OF_low = 2.0
OF_high = 4.0

OF_target = 3.0


# ============================================================
# CONSTANTS
# ============================================================

PSI_TO_PA = 6894.757


# ============================================================
# N2O PROPERTY FUNCTION
# ============================================================

def define_N2O_conditions(p_1, p_2):
    """
    Define saturated-liquid N2O properties at upstream pressure.

    Parameters
    ----------
    p_1 : float
        Upstream pressure [Pa]

    p_2 : float
        Downstream pressure [Pa]

    Returns
    -------
    dict
        N2O thermodynamic properties
    """

    fluid = 'N2O'

    fluid_properties = {
        'P_1': p_1,
        'P_2': p_2
    }

    # Saturated-liquid temperature at upstream pressure
    fluid_properties['T_1'] = CP.PropsSI(
        'T',
        'P', p_1,
        'Q', 0,
        fluid
    )

    # Saturated-liquid entropy
    fluid_properties['entropy'] = CP.PropsSI(
        'S',
        'P', p_1,
        'Q', 0,
        fluid
    )

    # Saturated-liquid density
    fluid_properties['density_1'] = CP.PropsSI(
        'D',
        'S', fluid_properties['entropy'],
        'P', p_1,
        fluid
    )

    return fluid_properties


# ============================================================
# SPI MASS FLUX
# ============================================================

def calculate_mass_flux_rate_SPI(density, p_1, p_2):
    """
    SPI mass flux:

        G = sqrt(2 * rho * (P1 - P2))

    Returns:
        G [kg/(m^2*s)]
    """

    delta_P = p_1 - p_2

    if delta_P <= 0:
        return 0.0

    return np.sqrt(
        2 * density * delta_P
    )


# ============================================================
# MASS FLOW RATE
# ============================================================

def calculate_mass_flow_rate(G, area, Cd):
    """
    mdot = Cd * A * G
    """

    return Cd * area * G


# ============================================================
# CREATE TANK PRESSURE ARRAY
# ============================================================

p_tank_array = np.linspace(
    p_tank_min,
    p_tank_max,
    num_points
)


# ============================================================
# CONVERT PRESSURES TO Pa
# ============================================================

p_tank_array_Pa = p_tank_array * PSI_TO_PA

Pc_Pa = Pc * PSI_TO_PA

dp_N2O_Pa = dp_N2O * PSI_TO_PA

dp_IPA_Pa = dp_IPA * PSI_TO_PA


# ============================================================
# ARRAYS FOR RESULTS
# ============================================================

mdot_N2O_array = np.zeros(num_points)

mdot_IPA_array = np.zeros(num_points)

OF_array = np.zeros(num_points)

rho_N2O_array = np.zeros(num_points)

T_N2O_array = np.zeros(num_points)

P_N2O_array = np.zeros(num_points)

P_IPA_array = np.zeros(num_points)


# ============================================================
# PRESSURE SWEEP
# ============================================================

for i, p_tank in enumerate(p_tank_array_Pa):

    # --------------------------------------------------------
    # Injector inlet pressures
    # --------------------------------------------------------

    p_N2O = p_tank - dp_N2O_Pa

    p_IPA = p_tank - dp_IPA_Pa

    P_N2O_array[i] = p_N2O / PSI_TO_PA

    P_IPA_array[i] = p_IPA / PSI_TO_PA


    # --------------------------------------------------------
    # N2O
    # --------------------------------------------------------

    if p_N2O > Pc_Pa:

        N2O = define_N2O_conditions(
            p_N2O,
            Pc_Pa
        )

        rho_N2O = N2O['density_1']

        T_N2O = N2O['T_1']

        G_N2O = calculate_mass_flux_rate_SPI(
            rho_N2O,
            p_N2O,
            Pc_Pa
        )

        mdot_N2O = calculate_mass_flow_rate(
            G_N2O,
            A_N2O,
            Cd_N2O
        )

    else:

        rho_N2O = np.nan
        T_N2O = np.nan
        mdot_N2O = 0.0


    # --------------------------------------------------------
    # IPA
    # --------------------------------------------------------

    G_IPA = calculate_mass_flux_rate_SPI(
        rho_IPA,
        p_IPA,
        Pc_Pa
    )

    mdot_IPA = calculate_mass_flow_rate(
        G_IPA,
        A_IPA,
        Cd_IPA
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    rho_N2O_array[i] = rho_N2O

    T_N2O_array[i] = T_N2O

    mdot_N2O_array[i] = mdot_N2O

    mdot_IPA_array[i] = mdot_IPA


    # --------------------------------------------------------
    # O/F
    # --------------------------------------------------------

    if mdot_IPA > 0:

        OF_array[i] = mdot_N2O / mdot_IPA

    else:

        OF_array[i] = np.nan


# ============================================================
# FUNCTION TO FIND PRESSURE AT A GIVEN O/F
# ============================================================

def find_pressure_at_OF(
        p_array,
        OF_array,
        target_OF
):
    """
    Find the tank pressure corresponding to a target O/F
    using interpolation.

    Returns:
        pressure [psi]
    """

    valid = np.isfinite(OF_array)

    p_valid = p_array[valid]
    OF_valid = OF_array[valid]

    # Check whether target is within the calculated range
    if target_OF < np.min(OF_valid) or target_OF > np.max(OF_valid):
        return None

    # Sort by O/F in case necessary
    sort_index = np.argsort(OF_valid)

    OF_sorted = OF_valid[sort_index]
    p_sorted = p_valid[sort_index]

    return np.interp(
        target_OF,
        OF_sorted,
        p_sorted
    )


# ============================================================
# FIND LOW / HIGH O/F PRESSURES
# ============================================================

p_low_OF = find_pressure_at_OF(
    p_tank_array,
    OF_array,
    OF_low
)

p_high_OF = find_pressure_at_OF(
    p_tank_array,
    OF_array,
    OF_high
)


# ============================================================
# N2O TEMPERATURE AT O/F LIMITS
# ============================================================

def get_N2O_temperature_at_tank_pressure(
        p_tank_psi
):
    """
    Calculate saturated-liquid N2O temperature at the
    N2O injector inlet pressure.

    P_N2O = P_tank - dp_N2O
    """

    p_N2O_psi = p_tank_psi - dp_N2O

    p_N2O_Pa = p_N2O_psi * PSI_TO_PA

    T_N2O = CP.PropsSI(
        'T',
        'P', p_N2O_Pa,
        'Q', 0,
        'N2O'
    )

    return T_N2O


T_low_OF = None
T_high_OF = None


if p_low_OF is not None:

    T_low_OF = get_N2O_temperature_at_tank_pressure(
        p_low_OF
    )


if p_high_OF is not None:

    T_high_OF = get_N2O_temperature_at_tank_pressure(
        p_high_OF
    )


# ============================================================
# NOMINAL OPERATING POINT
# ============================================================

index_nominal = np.argmin(
    np.abs(
        p_tank_array - p_tank_nominal
    )
)

OF_nominal = OF_array[index_nominal]

mdot_N2O_nominal = mdot_N2O_array[index_nominal]

mdot_IPA_nominal = mdot_IPA_array[index_nominal]

rho_N2O_nominal = rho_N2O_array[index_nominal]

T_N2O_nominal = T_N2O_array[index_nominal]

P_N2O_nominal = P_N2O_array[index_nominal]

P_IPA_nominal = P_IPA_array[index_nominal]


# ============================================================
# PRINT RESULTS
# ============================================================

print()
print("============================================================")
print("             O/F VS. TANK PRESSURE ANALYSIS")
print("============================================================")

print()
print("INPUTS")
print("------------------------------------------------------------")

print(f"Chamber pressure:           {Pc:.2f} psi")

print(f"Nominal tank pressure:      {p_tank_nominal:.2f} psi")

print(f"N2O feedline pressure drop: {dp_N2O:.2f} psi")

print(f"IPA feedline pressure drop: {dp_IPA:.2f} psi")

print(f"N2O injector area:          {A_N2O:.6e} m^2")

print(f"IPA injector area:          {A_IPA:.6e} m^2")

print(f"N2O Cd:                     {Cd_N2O:.3f}")

print(f"IPA Cd:                     {Cd_IPA:.3f}")

print(f"IPA density:                {rho_IPA:.2f} kg/m^3")

print()
print("ALLOWABLE O/F RANGE")
print("------------------------------------------------------------")

print(f"Low allowable O/F:          {OF_low:.3f}")

print(f"High allowable O/F:         {OF_high:.3f}")


print()
print("NOMINAL OPERATING POINT")
print("------------------------------------------------------------")

print(f"Tank pressure:              "
      f"{p_tank_nominal:.2f} psi")

print(f"N2O injector pressure:      "
      f"{P_N2O_nominal:.2f} psi")

print(f"IPA injector pressure:      "
      f"{P_IPA_nominal:.2f} psi")

print(f"N2O pressure drop:          "
      f"{P_N2O_nominal - Pc:.2f} psi")

print(f"IPA pressure drop:          "
      f"{P_IPA_nominal - Pc:.2f} psi")

print(f"N2O density:                "
      f"{rho_N2O_nominal:.2f} kg/m^3")

print(f"N2O saturated temperature:  "
      f"{T_N2O_nominal:.2f} K")

print(f"N2O saturated temperature:  "
      f"{T_N2O_nominal - 273.15:.2f} °C")

print(f"N2O mass flow:              "
      f"{mdot_N2O_nominal:.6f} kg/s")

print(f"IPA mass flow:              "
      f"{mdot_IPA_nominal:.6f} kg/s")

print(f"O/F:                        "
      f"{OF_nominal:.4f}")


print()
print("O/F LIMITS")
print("------------------------------------------------------------")


if p_low_OF is not None:

    print(f"Low O/F = {OF_low:.3f}")

    print(f"  Tank pressure:            "
          f"{p_low_OF:.2f} psi")

    print(f"  N2O injector pressure:    "
          f"{p_low_OF - dp_N2O:.2f} psi")

    print(f"  N2O saturation temperature:"
          f" {T_low_OF:.2f} K")

    print(f"  N2O saturation temperature:"
          f" {T_low_OF - 273.15:.2f} °C")

else:

    print(
        f"Low O/F = {OF_low:.3f} "
        f"is outside the pressure range."
    )


print()


if p_high_OF is not None:

    print(f"High O/F = {OF_high:.3f}")

    print(f"  Tank pressure:            "
          f"{p_high_OF:.2f} psi")

    print(f"  N2O injector pressure:    "
          f"{p_high_OF - dp_N2O:.2f} psi")

    print(f"  N2O saturation temperature:"
          f" {T_high_OF:.2f} K")

    print(f"  N2O saturation temperature:"
          f" {T_high_OF - 273.15:.2f} °C")

else:

    print(
        f"High O/F = {OF_high:.3f} "
        f"is outside the pressure range."
    )


print()
print("============================================================")


# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(9, 6))


# O/F curve
plt.plot(
    p_tank_array,
    OF_array,
    linewidth=2,
    label="SPI prediction"
)


# Target O/F
plt.axhline(
    OF_target,
    linestyle="--",
    linewidth=1.5,
    label=f"Target O/F = {OF_target:.2f}"
)


# Low allowable O/F
plt.axhline(
    OF_low,
    linestyle=":",
    linewidth=1.5,
    label=f"Low allowable O/F = {OF_low:.2f}"
)


# High allowable O/F
plt.axhline(
    OF_high,
    linestyle=":",
    linewidth=1.5,
    label=f"High allowable O/F = {OF_high:.2f}"
)


# ------------------------------------------------------------
# Mark low O/F pressure
# ------------------------------------------------------------

if p_low_OF is not None:

    plt.scatter(
        p_low_OF,
        OF_low,
        s=80,
        zorder=5
    )

    plt.annotate(
        f"O/F = {OF_low:.2f}\n"
        f"Pₜₐₙₖ = {p_low_OF:.1f} psi\n"
        f"Tₙ₂ₒ,sat = {T_low_OF - 273.15:.1f} °C",
        xy=(p_low_OF, OF_low),
        xytext=(10, -45),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->")
    )


# ------------------------------------------------------------
# Mark high O/F pressure
# ------------------------------------------------------------

if p_high_OF is not None:

    plt.scatter(
        p_high_OF,
        OF_high,
        s=80,
        zorder=5
    )

    plt.annotate(
        f"O/F = {OF_high:.2f}\n"
        f"Pₜₐₙₖ = {p_high_OF:.1f} psi\n"
        f"Tₙ₂ₒ,sat = {T_high_OF - 273.15:.1f} °C",
        xy=(p_high_OF, OF_high),
        xytext=(10, 10),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->")
    )


# ------------------------------------------------------------
# Mark nominal point
# ------------------------------------------------------------

plt.scatter(
    p_tank_nominal,
    OF_nominal,
    s=80,
    zorder=5,
    label=f"Nominal: {OF_nominal:.3f}"
)


# ------------------------------------------------------------
# Formatting
# ------------------------------------------------------------

plt.xlabel("Tank / Pressurant Pressure [psi]")

plt.ylabel("O/F")

plt.title("O/F vs. Tank / Pressurant Pressure")

plt.grid(True, alpha=0.3)

plt.legend()

plt.tight_layout()

plt.show()