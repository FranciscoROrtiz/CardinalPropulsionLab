
import numpy as np


# ============================================================
# DRILL BIT DATABASE
# ============================================================

# Dictionary:
# Key   = drill bit number (integer)
# Value = drill bit diameter [mm]

DRILL_BITS = {
    80: 0.343,
    79: 0.368,
    78: 0.406,
    77: 0.457,
    76: 0.508,
    75: 0.533,
    74: 0.559,
    73: 0.584,
    72: 0.635,
    71: 0.660,
    70: 0.711,
    69: 0.749,
    68: 0.787,
    67: 0.813,
    66: 0.838,
    65: 0.889,
    64: 0.914,
    63: 0.991,
    62: 0.965,
    61: 1.016,
    60: 1.041,
    59: 1.067,
    58: 1.092,
    57: 1.143,
    56: 1.181,
    55: 1.321,
    54: 1.397,
    53: 1.511,
    52: 1.613,
    51: 1.702,
    50: 1.778,
}


# ============================================================
# FILM COOLING DRILL BIT OPTIMIZER
# ============================================================

def optimize_film_cooling_holes(
    target_area_m2,
    smallest_drill,
    min_holes=4,
    max_holes=28
):
    """
    Determine the optimal uniform drill-bit arrangement
    for a specified total film-cooling orifice area.

    Parameters
    ----------
    target_area_m2 : float
        Desired total orifice area [m^2].

    smallest_drill : int
        Smallest allowable drill bit, specified by number.
        Example: 61 means #61 is the smallest permitted drill.

        Drill #61 and physically larger drills (#60, #59, ...)
        are permitted.

    min_holes : int
        Minimum allowable number of holes.

    max_holes : int
        Maximum allowable number of holes.

    Returns
    -------
    dict
        Dictionary containing the optimal drill arrangement,
        geometric areas, and area error.
    """

    # ========================================================
    # UNIT CONVERSION
    # ========================================================

    # Conversion factor: m^2 -> mm^2
    m2_to_mm2 = 1e6

    target_area_mm2 = target_area_m2 * m2_to_mm2

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if target_area_m2 <= 0:
        raise ValueError("Target area must be positive.")

    if smallest_drill not in DRILL_BITS:
        raise ValueError(
            f"Drill #{smallest_drill} is not in the drill database."
        )

    if min_holes < 1 or max_holes < min_holes:
        raise ValueError("Invalid hole-count limits.")

    # ========================================================
    # FILTER AVAILABLE DRILL SIZES
    # ========================================================

    # Smaller drill numbers correspond to larger diameters.
    #
    # Example:
    # smallest_drill = 61
    #
    # Permitted: #61, #60, #59, ... #50
    # Excluded:  #62, #63, ... #80

    allowed_drills = {
        drill: diameter
        for drill, diameter in DRILL_BITS.items()
        if drill <= smallest_drill
    }

    if not allowed_drills:
        raise ValueError("No allowable drill sizes found.")

    # ========================================================
    # EVALUATE ALL SYMMETRIC ARRANGEMENTS
    # ========================================================

    solutions = []

    for drill_number, diameter_mm in allowed_drills.items():

        # Area of one hole [mm^2]
        area_per_hole_mm2 = np.pi * diameter_mm**2 / 4

        for n_holes in range(min_holes, max_holes + 1):

            # Total geometric area [mm^2]
            total_area_mm2 = n_holes * area_per_hole_mm2

            # Signed area error [mm^2]
            area_error_mm2 = total_area_mm2 - target_area_mm2

            # Percentage error
            error_percent = (
                100 * area_error_mm2 / target_area_mm2
            )

            # Store candidate arrangement
            solutions.append({
                "drill": f"#{drill_number}",
                "drill_number": drill_number,
                "number_of_holes": n_holes,
                "diameter_mm": diameter_mm,
                "area_per_hole_mm2": area_per_hole_mm2,
                "total_area_mm2": total_area_mm2,
                "area_error_mm2": area_error_mm2,
                "error_percent": error_percent,
                "absolute_error_mm2": abs(area_error_mm2),
            })

    # ========================================================
    # SELECT OPTIMAL ARRANGEMENT
    # ========================================================

    # Primary objective:
    # Minimize absolute area error.
    #
    # Secondary objective:
    # If errors are equal, prefer an arrangement below target.

    solutions.sort(
        key=lambda x: (
            x["absolute_error_mm2"],
            x["area_error_mm2"] > 0
        )
    )

    best = solutions[0]

    # ========================================================
    # RETURN RESULTS AS DICTIONARY
    # ========================================================

    return {
        "drill": best["drill"],
        "drill_number": best["drill_number"],
        "number_of_holes": best["number_of_holes"],
        "diameter_mm": best["diameter_mm"],
        "area_per_hole_mm2": best["area_per_hole_mm2"],
        "total_area_mm2": best["total_area_mm2"],
        "total_area_m2": best["total_area_mm2"] / m2_to_mm2,
        "target_area_m2": target_area_m2,
        "area_error_m2": best["area_error_mm2"] / m2_to_mm2,
        "error_percent": best["error_percent"],
    }


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":

    # Target total orifice area [m^2]
    target_area = 8.198588498008546e-6

    # Smallest allowable drill bit
    smallest_drill = 78

    # Calculate optimal arrangement
    solution = optimize_film_cooling_holes(
        target_area_m2=target_area,
        smallest_drill=smallest_drill,
        min_holes=4,
        max_holes=50
    )

    # Print complete returned dictionary
    print("\nOPTIMAL FILM COOLING ARRANGEMENT")
    print("=" * 55)

    for key, value in solution.items():
        print(f"{key:<25}: {value}")

    # ========================================================
    # ACCESS INDIVIDUAL RESULTS
    # ========================================================

    n_holes = solution["number_of_holes"]
    drill = solution["drill"]
    diameter_mm = solution["diameter_mm"]
    actual_area_m2 = solution["total_area_m2"]
    error_percent = solution["error_percent"]

    print("\nENGINEERING VARIABLES")
    print("-" * 55)

    print(f"Number of holes:  {n_holes}")
    print(f"Drill bit:        {drill}")
    print(f"Diameter:         {diameter_mm:.4f} mm")
    print(f"Actual area:      {actual_area_m2:.10e} m^2")
    print(f"Area error:       {error_percent:+.6f}%")