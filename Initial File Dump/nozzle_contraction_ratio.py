
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator


# ============================================================
# CONTRACTION RATIO INTERPOLATION
# Digitized from the lowest curve indicated by red arrows
# ============================================================

# Throat diameter [in]
throat_diameter_data = np.array([
    0.15, 0.20, 0.50, 1.0, 2.0,
    5.0, 10.0, 20.0, 50.0
])

# Contraction ratio [-]
contraction_ratio_data = np.array([
    13.3, 12.1, 9.0, 6.1, 4.4,
    3.0, 2.3, 1.8, 1.5
])


# ============================================================
# INTERPOLATION FUNCTION
# ============================================================

# The graph's horizontal axis is logarithmic.
# Therefore, interpolate against log10(throat diameter).

contraction_ratio_function = PchipInterpolator(
    np.log10(throat_diameter_data),
    contraction_ratio_data,
    extrapolate=False
)


# ============================================================
# CALCULATE CONTRACTION RATIO
# ============================================================

def calculate_contraction_ratio(throat_diameter):
    """
    Calculate contraction ratio from throat diameter.

    Parameters
    ----------
    throat_diameter : float, int, or numpy.ndarray
        Throat diameter [m].

    Returns
    -------
    float or numpy.ndarray
        Contraction ratio Ac/At [-].

    Valid range:
        0.15 <= throat_diameter <= 50 inches.
    """
    m_to_in = 39.3700787        # m * m_to_in = in
    throat_diameter *= m_to_in
    diameter = np.asarray(throat_diameter, dtype=float)

    # Validate input
    if not np.all(np.isfinite(diameter)):
        raise ValueError("Throat diameter must be finite.")

    if np.any(diameter <= 0):
        raise ValueError("Throat diameter must be positive.")

    if np.any(diameter < throat_diameter_data[0]) or \
       np.any(diameter > throat_diameter_data[-1]):

        raise ValueError(
            f"Throat diameter must be between "
            f"{throat_diameter_data[0]} and "
            f"{throat_diameter_data[-1]} inches."
        )

    # Evaluate interpolation function
    contraction_ratio = contraction_ratio_function(
        np.log10(diameter)
    )

    # Return scalar if scalar input was provided
    if diameter.ndim == 0:
        return float(contraction_ratio)

    return contraction_ratio


# ============================================================
# OPTIONAL: CALCULATE CHAMBER DIAMETER
# ============================================================

def calculate_chamber_diameter(throat_diameter):
    """
    Calculate chamber diameter from contraction ratio.

    Assumes circular chamber and throat.

    D_c = D_t * sqrt(A_c/A_t)
    """

    contraction_ratio = calculate_contraction_ratio(
        throat_diameter
    )

    return throat_diameter * np.sqrt(contraction_ratio)


# ============================================================
# PLOT INTERPOLATION
# ============================================================

def plot_contraction_ratio():

    diameter_plot = np.logspace(
        np.log10(throat_diameter_data[0]),
        np.log10(throat_diameter_data[-1]),
        500
    )

    ratio_plot = calculate_contraction_ratio(diameter_plot)

    plt.figure(figsize=(9, 6))

    plt.semilogx(
        diameter_plot,
        ratio_plot,
        label="PCHIP interpolation",
        linewidth=2
    )

    plt.scatter(
        throat_diameter_data,
        contraction_ratio_data,
        label="Digitized graph data",
        marker="o",
        zorder=3
    )

    plt.xlabel("Throat Diameter [in]")
    plt.ylabel("Contraction Ratio [-]")

    plt.title("Contraction Ratio vs. Throat Diameter")

    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.show()


# ============================================================
# EXAMPLE
# ============================================================

if __name__ == "__main__":

    throat_diameter = 1.5  # inches

    contraction_ratio = calculate_contraction_ratio(
        throat_diameter
    )

    chamber_diameter = calculate_chamber_diameter(
        throat_diameter
    )

    print(f"Throat Diameter:     {throat_diameter:.3f} in")
    print(f"Contraction Ratio:   {contraction_ratio:.3f}")
    print(f"Chamber Diameter:    {chamber_diameter:.3f} in")

    plot_contraction_ratio()