import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP


# ============================================================
# USER INPUTS
# ============================================================

P_1 = 450 * 6894.757       # Upstream pressure [Pa]
P_2 = 350 * 6894.757       # Downstream pressure [Pa]

Cd = 0.4                   # Oxidizer discharge coefficient

# Desired design O/F
OF_DESIGN = 3.0

# Fuel mass flow rate -- HELD CONSTANT
mdot_fuel = 0.3061        # [kg/s]

# Intended oxidizer area
A_OX_DESIGN = 6.48623643e-05      # [m^2]

# Actual oxidizer area to evaluate
A_OX_USER = 6.48686915e-05        # [m^2]


# ============================================================
# N2O CONDITIONS
# ============================================================

def define_conditions(p_1, p_2):

    fluid = 'N2O'

    fluid_properties = {
        'P_1': p_1,
        'P_2': p_2
    }

    # Saturated liquid temperature at upstream pressure
    fluid_properties['T_1'] = CP.PropsSI(
        'T',
        'P', p_1,
        'Q', 0,
        fluid
    )

    # Saturated liquid entropy
    fluid_properties['entropy'] = CP.PropsSI(
        'S',
        'P', p_1,
        'Q', 0,
        fluid
    )

    # Upstream density
    fluid_properties['density_1'] = CP.PropsSI(
        'D',
        'S', fluid_properties['entropy'],
        'P', p_1,
        fluid
    )

    # Vapor pressure at T1
    fluid_properties['P_v'] = CP.PropsSI(
        'P',
        'T', fluid_properties['T_1'],
        'Q', 0,
        fluid
    )

    return fluid_properties


# ============================================================
# MASS FLUX
# ============================================================

def calculate_mass_flux_rate(N2O):

    G_SPI = (
        2
        * N2O['density_1']
        * (N2O['P_1'] - N2O['P_2'])
    ) ** 0.5

    return G_SPI


# ============================================================
# MASS FLOW RATE
# ============================================================

def calculate_mass_flow_rate(G, area, Cd):

    return Cd * G * area


# ============================================================
# O/F
# ============================================================

def calculate_OF(mdot_ox, mdot_fuel):

    return mdot_ox / mdot_fuel


# ============================================================
# CALCULATIONS
# ============================================================

N2O = define_conditions(P_1, P_2)

G_N2O = calculate_mass_flux_rate(N2O)


# Oxidizer mass flow at intended area
mdot_ox_design = calculate_mass_flow_rate(
    G_N2O,
    A_OX_DESIGN,
    Cd
)

# O/F at intended area
OF_design_actual = calculate_OF(
    mdot_ox_design,
    mdot_fuel
)


# Oxidizer mass flow at user-selected area
mdot_ox_user = calculate_mass_flow_rate(
    G_N2O,
    A_OX_USER,
    Cd
)

# Resulting O/F
OF_user = calculate_OF(
    mdot_ox_user,
    mdot_fuel
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n==============================================")
print("          INJECTOR O/F ANALYSIS")
print("==============================================")

print(f"P1:                  {P_1 / 6894.757:.2f} psi")
print(f"P2:                  {P_2 / 6894.757:.2f} psi")
print(f"Delta P:             {(P_1-P_2) / 6894.757:.2f} psi")

print(f"\nN2O density:         {N2O['density_1']:.2f} kg/m^3")
print(f"N2O mass flux:       {G_N2O:.2f} kg/(m^2*s)")

print(f"\nFuel mass flow:      {mdot_fuel:.6f} kg/s")

print(f"\nDesign area:         {A_OX_DESIGN:.6e} m^2")
print(f"Design ox mdot:     {mdot_ox_design:.6f} kg/s")
print(f"Design O/F:         {OF_design_actual:.3f}")
print(f"Target O/F:         {OF_DESIGN:.3f}")

print(f"\nUser area:           {A_OX_USER:.6e} m^2")
print(f"User ox mdot:       {mdot_ox_user:.6f} kg/s")
print(f"Resulting O/F:      {OF_user:.3f}")

print("==============================================\n")


# ============================================================
# PLOT O/F VS OXIDIZER AREA
# ============================================================

area_min = 0.50 * A_OX_DESIGN
area_max = 1.50 * A_OX_DESIGN

areas = np.linspace(
    area_min,
    area_max,
    500
)

# Oxidizer mass flow for each area
mdot_ox_array = calculate_mass_flow_rate(
    G_N2O,
    areas,
    Cd
)

# Fuel flow remains CONSTANT
OF_array = mdot_ox_array / mdot_fuel


# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    areas * 1e6,
    OF_array,
    linewidth=2
)

# Intended area
plt.scatter(
    A_OX_DESIGN * 1e6,
    OF_design_actual,
    s=70,
    label=f"Design area: O/F = {OF_design_actual:.3f}"
)

# User-selected area
plt.scatter(
    A_OX_USER * 1e6,
    OF_user,
    s=70,
    label=f"Selected area: O/F = {OF_user:.3f}"
)

# Desired O/F
plt.axhline(
    OF_DESIGN,
    linestyle='--',
    linewidth=1.5,
    label=f"Target O/F = {OF_DESIGN:.1f}"
)

plt.xlabel("Oxidizer Flow Area [mm²]")
plt.ylabel("O/F")
plt.title("O/F vs. Oxidizer Injector Area")

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()