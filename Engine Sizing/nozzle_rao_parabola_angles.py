
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator


# ============================================================
# FIGURE 4-14: PARABOLIC NOZZLE ANGLES
# L_f = 80%
# ============================================================

# Data digitized approximately from the L_f = 80% curves.
#
# Expansion ratio:
# epsilon = Ae / At [-]
#
# Initial angle:
# theta_n [degrees]
#
# Final angle:
# theta_e [degrees]


# ------------------------------------------------------------
# 1. DIGITIZED DATA
# ------------------------------------------------------------

# Expansion area ratio [-]
expansion_ratio_data = np.array([
    1.25, 2.5, 5, 10, 15, 20, 25,
    30, 35, 40, 45, 50
])

# Initial parabolic angle [degrees]
theta_n_data = np.array([
    22.5, 23.0, 24.5, 27.0, 28.7, 29.9,
    30.7, 31.3, 31.8, 32.1, 32.4, 32.7
])

# Final parabolic angle [degrees]
theta_e_data = np.array([
    16, 15, 13.75, 9.8, 9.4, 9.1,
    8.9, 8.7, 8.5, 8.3, 8.1, 7.9
])


# ------------------------------------------------------------
# 2. INPUT LIMITS
# ------------------------------------------------------------

EXPANSION_RATIO_MIN = expansion_ratio_data[0]
EXPANSION_RATIO_MAX = expansion_ratio_data[-1]


# ------------------------------------------------------------
# 3. CONSTRUCT CONTINUOUS INTERPOLATION FUNCTIONS
# ------------------------------------------------------------

# PCHIP creates piecewise cubic functions that:
# - Pass through all digitized points.
# - Preserve the general shape of the data.
# - Avoid many oscillations associated with high-degree
#   polynomial interpolation.

theta_n_function = PchipInterpolator(
    expansion_ratio_data,
    theta_n_data,
    extrapolate=False
)

theta_e_function = PchipInterpolator(
    expansion_ratio_data,
    theta_e_data,
    extrapolate=False
)


# ------------------------------------------------------------
# 4. INPUT VALIDATION
# ------------------------------------------------------------

def validate_expansion_ratio(expansion_ratio):
    """
    Validate expansion ratio input.

    Accepts:
        float
        int
        NumPy array

    Valid range:
        1 <= epsilon <= 50
    """

    epsilon = np.asarray(expansion_ratio, dtype=float)

    if not np.all(np.isfinite(epsilon)):
        raise ValueError(
            "Expansion ratio must contain finite numerical values."
        )

    if np.any(epsilon < EXPANSION_RATIO_MIN) or \
       np.any(epsilon > EXPANSION_RATIO_MAX):

        raise ValueError(
            f"Expansion ratio must be between "
            f"{EXPANSION_RATIO_MIN} and {EXPANSION_RATIO_MAX}."
        )

    return epsilon


# ------------------------------------------------------------
# 5. INITIAL PARABOLIC ANGLE
# ------------------------------------------------------------

def calculate_theta_n(expansion_ratio):
    """
    Calculate initial parabolic angle.

    Parameters
    ----------
    expansion_ratio : float, int, or numpy.ndarray
        Nozzle expansion area ratio Ae/At [-].

    Returns
    -------
    float or numpy.ndarray
        Initial parabolic angle theta_n [degrees].
    """

    epsilon = validate_expansion_ratio(expansion_ratio)

    theta_n = theta_n_function(epsilon)

    if epsilon.ndim == 0:
        return float(theta_n)

    return theta_n


# ------------------------------------------------------------
# 6. FINAL PARABOLIC ANGLE
# ------------------------------------------------------------

def calculate_theta_e(expansion_ratio):
    """
    Calculate final parabolic angle.

    Parameters
    ----------
    expansion_ratio : float, int, or numpy.ndarray
        Nozzle expansion area ratio Ae/At [-].

    Returns
    -------
    float or numpy.ndarray
        Final parabolic angle theta_e [degrees].
    """

    epsilon = validate_expansion_ratio(expansion_ratio)

    theta_e = theta_e_function(epsilon)

    if epsilon.ndim == 0:
        return float(theta_e)

    return theta_e


# ------------------------------------------------------------
# 7. CALCULATE BOTH ANGLES
# ------------------------------------------------------------

def calculate_parabolic_angles(expansion_ratio):
    """
    Calculate both parabolic nozzle angles.

    Returns
    -------
    dict
        theta_n : Initial angle [degrees]
        theta_e : Final angle [degrees]
    """

    return {
        "theta_n": calculate_theta_n(expansion_ratio),
        "theta_e": calculate_theta_e(expansion_ratio)
    }


# ------------------------------------------------------------
# 8. OPTIONAL POLYNOMIAL FIT
# ------------------------------------------------------------

# These coefficients provide approximate polynomial equations
# for documentation or comparison.
#
# PCHIP remains the primary calculation method.

POLYNOMIAL_DEGREE = 4

theta_n_polynomial_coefficients = np.polyfit(
    expansion_ratio_data,
    theta_n_data,
    POLYNOMIAL_DEGREE
)

theta_e_polynomial_coefficients = np.polyfit(
    expansion_ratio_data,
    theta_e_data,
    POLYNOMIAL_DEGREE
)

theta_n_polynomial = np.poly1d(
    theta_n_polynomial_coefficients
)

theta_e_polynomial = np.poly1d(
    theta_e_polynomial_coefficients
)


# ------------------------------------------------------------
# 9. PLOT DIGITIZED DATA AND INTERPOLATED FUNCTIONS
# ------------------------------------------------------------

def plot_parabolic_angles():
    """
    Plot the digitized data and PCHIP interpolation curves.
    """

    epsilon_plot = np.linspace(
        EXPANSION_RATIO_MIN,
        EXPANSION_RATIO_MAX,
        500
    )

    theta_n_plot = calculate_theta_n(epsilon_plot)
    theta_e_plot = calculate_theta_e(epsilon_plot)

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(9, 8),
        sharex=True
    )

    # Initial angle
    axes[0].plot(
        epsilon_plot,
        theta_n_plot,
        label="PCHIP interpolation",
        linewidth=2
    )

    axes[0].scatter(
        expansion_ratio_data,
        theta_n_data,
        label="Digitized data",
        marker="o",
        zorder=3
    )

    axes[0].set_ylabel(
        r"Initial Angle, $\theta_n$ [deg]"
    )

    axes[0].set_title(
        r"Parabolic Nozzle Angles ($L_f=80\%$)"
    )

    axes[0].grid(True)
    axes[0].legend()

    # Final angle
    axes[1].plot(
        epsilon_plot,
        theta_e_plot,
        label="PCHIP interpolation",
        linewidth=2
    )

    axes[1].scatter(
        expansion_ratio_data,
        theta_e_data,
        label="Digitized data",
        marker="o",
        zorder=3
    )

    axes[1].set_xlabel(
        r"Expansion Area Ratio, $\epsilon=A_e/A_t$ [-]"
    )

    axes[1].set_ylabel(
        r"Final Angle, $\theta_e$ [deg]"
    )

    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 10. EXAMPLE EXECUTION
# ------------------------------------------------------------

if __name__ == "__main__":

    # Example expansion ratio
    epsilon = 25

    # Calculate angles
    angles = calculate_parabolic_angles(epsilon)

    theta_n = angles["theta_n"]
    theta_e = angles["theta_e"]

    print("=" * 50)
    print("PARABOLIC NOZZLE ANGLE CALCULATION")
    print("=" * 50)

    print(f"Expansion Ratio: {epsilon:.3f}")
    print(f"Initial Angle:   {theta_n:.3f} degrees")
    print(f"Final Angle:     {theta_e:.3f} degrees")

    print("\nPolynomial Coefficients:")
    print("Theta_n:", theta_n_polynomial_coefficients)
    print("Theta_e:", theta_e_polynomial_coefficients)

    # Generate plots
    plot_parabolic_angles()