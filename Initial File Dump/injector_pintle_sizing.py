import math
import itertools


# -----------------------------
# Utilities
# -----------------------------

def inch_to_m(x):
    return x * 0.0254


def area_from_diameter(d):
    return math.pi * (d / 2) ** 2


# -----------------------------
# Drill Bit Database
# -----------------------------

def build_drill_table():
    drills = {}

    # Number drills
    number_drills_in = {
        80: 0.0135, 79: 0.0145, 78: 0.0160, 77: 0.0180, 76: 0.0200,
        75: 0.0210, 74: 0.0225, 73: 0.0240, 72: 0.0250, 71: 0.0260,
        70: 0.0280, 69: 0.0292, 68: 0.0310, 67: 0.0320, 66: 0.0330,
        65: 0.0350, 64: 0.0360, 63: 0.0370, 62: 0.0380, 61: 0.0390,
        60: 0.0400, 59: 0.0410, 58: 0.0420, 57: 0.0430, 56: 0.0465,
        55: 0.0520, 54: 0.0550, 53: 0.0595, 52: 0.0635, 51: 0.0670,
        50: 0.0700, 49: 0.0730, 48: 0.0760, 47: 0.0785, 46: 0.0810,
        45: 0.0820, 44: 0.0860, 43: 0.0890, 42: 0.0935, 41: 0.0960,
        40: 0.0980, 39: 0.0995, 38: 0.1015, 37: 0.1040, 36: 0.1065,
        35: 0.1100, 34: 0.1110, 33: 0.1130, 32: 0.1160, 31: 0.1200,
        30: 0.1285, 29: 0.1360, 28: 0.1405, 27: 0.1440, 26: 0.1470,
        25: 0.1495, 24: 0.1520, 23: 0.1540, 22: 0.1570, 21: 0.1590,
        20: 0.1610, 19: 0.1660, 18: 0.1695, 17: 0.1730, 16: 0.1770,
        15: 0.1800, 14: 0.1820, 13: 0.1850, 12: 0.1890, 11: 0.1910,
        10: 0.1935, 9: 0.1960, 8: 0.1990, 7: 0.2010, 6: 0.2040,
        5: 0.2055, 4: 0.2090, 3: 0.2130, 2: 0.2210, 1: 0.2280
    }

    for k, v in number_drills_in.items():
        drills[f"#{k}"] = inch_to_m(v)

    # Letter drills
    letter_drills_in = {
        "A": 0.234, "B": 0.238, "C": 0.242, "D": 0.246,
        "E": 0.250, "F": 0.257, "G": 0.261, "H": 0.266,
        "I": 0.272, "J": 0.277, "K": 0.281, "L": 0.290,
        "M": 0.295, "N": 0.302, "O": 0.316, "P": 0.323,
        "Q": 0.332, "R": 0.339, "S": 0.348, "T": 0.358,
        "U": 0.368, "V": 0.377, "W": 0.386, "X": 0.397,
        "Y": 0.404, "Z": 0.413
    }

    for k, v in letter_drills_in.items():
        drills[k] = inch_to_m(v)

    # Fractional drills: 1/16" to 1/2"
    for n in range(4, 33):
        frac = n / 64
        drills[f"{n}/64"] = inch_to_m(frac)

    return drills


# -----------------------------
# Two-Row Solver
# -----------------------------

def find_best_two_row_layout(
        A_target,
        C_pintle,

        # Hole count
        hole_min=20,
        hole_max=36,
        min_per_row=8,

        # Spacing
        min_spacing=0.001,

        # Manufacturing
        min_diameter=0.001,

        # Primary-hole requirements
        max_primary_diameter=0.003,
        max_primary_diameter_ratio=2.0,

        # Trim requirements
        allow_trim=True,
        max_trim_diameter=0.0015,

        # Primary-hole area requirements
        min_primary_undersize=0.0,
        max_primary_undersize=0.10,

        # Number of results
        results_to_return=10
):

    drills = build_drill_table()

    # Calculate area for every drill
    drill_areas = {
        k: area_from_diameter(v)
        for k, v in drills.items()
    }

    # -----------------------------------------
    # Primary-hole drills
    # -----------------------------------------

    primary_drills = {
        k: d
        for k, d in drills.items()
        if d >= min_diameter
        and d <= max_primary_diameter
    }

    # -----------------------------------------
    # Trim-hole drills
    # -----------------------------------------

    trim_drills = {
        k: d
        for k, d in drills.items()
        if d >= min_diameter
        and d <= max_trim_diameter
    }

    solutions = []

    # -----------------------------------------
    # Try every pair of primary drill sizes
    # -----------------------------------------

    for drill1, drill2 in itertools.combinations_with_replacement(
            primary_drills.keys(), 2):

        d1 = primary_drills[drill1]
        d2 = primary_drills[drill2]

        A1 = drill_areas[drill1]
        A2 = drill_areas[drill2]

        # Ratio between largest and smallest primary hole
        diameter_ratio = max(d1, d2) / min(d1, d2)

        if diameter_ratio > max_primary_diameter_ratio:
            continue

        # -----------------------------------------
        # Try total number of primary holes
        # -----------------------------------------

        for N_total in range(hole_min, hole_max + 1):

            # -----------------------------------------
            # Try every distribution between rows
            # -----------------------------------------

            for N1 in range(
                    min_per_row,
                    N_total - min_per_row + 1):

                N2 = N_total - N1

                # -----------------------------------------
                # Circumferential spacing
                # -----------------------------------------

                spacing1 = C_pintle / N1
                spacing2 = C_pintle / N2

                if spacing1 < min_spacing:
                    continue

                if spacing2 < min_spacing:
                    continue

                # -----------------------------------------
                # Primary-hole area
                # -----------------------------------------

                A_primary = N1 * A1 + N2 * A2

                # Primary holes must be below target
                if A_primary >= A_target:
                    continue

                # -----------------------------------------
                # Primary undersize
                # -----------------------------------------

                undersize = (
                    A_target - A_primary
                ) / A_target

                if undersize < min_primary_undersize:
                    continue

                if undersize > max_primary_undersize:
                    continue

                # -----------------------------------------
                # No trim-hole case
                # -----------------------------------------

                if not allow_trim:

                    percent_error = (
                        abs(A_target - A_primary)
                        / A_target
                        * 100
                    )

                    solutions.append({
                        "row1": (drill1, N1),
                        "row2": (drill2, N2),
                        "trim": None,

                        "primary_holes": N_total,
                        "holes": N_total,

                        "primary_area": A_primary,
                        "trim_area": 0.0,
                        "area": A_primary,

                        "error": abs(
                            A_target - A_primary
                        ),

                        "percent_error": percent_error,

                        "undersize": undersize,
                        "diameter_ratio": diameter_ratio,

                        "drill_count": len(
                            {drill1, drill2}
                        )
                    })

                    continue

                # -----------------------------------------
                # Trim-hole search
                # -----------------------------------------

                residual = A_target - A_primary

                best_trim = None

                for trim_drill, trim_diameter in trim_drills.items():

                    A_trim = drill_areas[trim_drill]

                    # Trim hole cannot exceed residual
                    if A_trim > residual:
                        continue

                    trim_error = residual - A_trim

                    candidate = (
                        trim_error,
                        A_trim,
                        trim_drill
                    )

                    if best_trim is None or candidate < best_trim:
                        best_trim = candidate

                if best_trim is None:
                    continue

                trim_error, A_trim, trim_drill = best_trim

                # -----------------------------------------
                # Total area
                # -----------------------------------------

                A_total = A_primary + A_trim

                # -----------------------------------------
                # Percent error
                # -----------------------------------------

                percent_error = (
                    abs(A_target - A_total)
                    / A_target
                    * 100
                )

                # -----------------------------------------
                # Save solution
                # -----------------------------------------

                solutions.append({
                    "row1": (drill1, N1),
                    "row2": (drill2, N2),
                    "trim": trim_drill,

                    "primary_holes": N_total,
                    "holes": N_total + 1,

                    "primary_area": A_primary,
                    "trim_area": A_trim,
                    "area": A_total,

                    "error": abs(
                        A_target - A_total
                    ),

                    "percent_error": percent_error,

                    "undersize": undersize,
                    "diameter_ratio": diameter_ratio,

                    "drill_count": len(
                        {drill1, drill2, trim_drill}
                    )
                })

    # -----------------------------------------
    # Sort solutions
    # -----------------------------------------

    solutions.sort(
        key=lambda s: (
            s["error"],
            s["undersize"],
            -s["primary_holes"],
            s["drill_count"],
            max(
                primary_drills[s["row1"][0]],
                primary_drills[s["row2"][0]]
            ),
            s["diameter_ratio"]
        )
    )

    return solutions[:results_to_return]


# ============================================================
# MAIN FUNCTION
# ============================================================

def optimize_pintle_geometry(A_ox, d_chamber):

    """
    Optimize the two-row pintle injector hole geometry.

    Inputs
    ------
    A_ox : float
        Target oxidizer flow area [m^2]

    d_chamber : float
        Chamber diameter [m]

    Returns
    -------
    pintle_geometry : dict
        Dictionary containing the pintle geometry and
        best (Solution 1) hole layout.
    """

    # -----------------------------------------
    # Pintle geometry
    # -----------------------------------------

    d_pintle = d_chamber / 4.803679096  

    # Skip distance is defined to equal pintle diameter
    skip_distance = d_pintle

    C_pintle = math.pi * d_pintle

    # -----------------------------------------
    # Run optimizer
    # -----------------------------------------

    best = find_best_two_row_layout(
        A_target=A_ox,
        C_pintle=C_pintle,

        # Primary hole count
        hole_min=20,
        hole_max=36,

        # Minimum holes in each row
        min_per_row=8,

        # Minimum center-to-center spacing
        min_spacing=0.001,  # 1 mm

        # Minimum manufacturable hole
        min_diameter=0.001,  # 1 mm

        # Maximum primary hole diameter
        max_primary_diameter=0.003,  # 3 mm

        # Maximum ratio between primary hole diameters
        max_primary_diameter_ratio=2.0,

        # Trim-hole maximum diameter
        max_trim_diameter=0.0015,  # 1.5 mm

        # Primary area must be below target
        min_primary_undersize=0.0,

        # Don't leave more than 10% of target
        # for trim hole
        max_primary_undersize=0.10,

        # Allow trim hole
        allow_trim=True,

        # We only need Solution 1
        results_to_return=1
    )

    # -----------------------------------------
    # Check for valid solution
    # -----------------------------------------

    if not best:
        raise ValueError(
            "No valid pintle hole layout found. "
            "Try relaxing the optimizer constraints."
        )

    # -----------------------------------------
    # Solution 1
    # -----------------------------------------

    sol = best[0]

    # -----------------------------------------
    # Build output dictionary
    # -----------------------------------------

    pintle_geometry = {

        # Pintle geometry
        "pintle_diameter": d_pintle,
        "skip_distance": skip_distance,
        "pintle_circumference": C_pintle,

        # Solution 1
        "row1": sol["row1"],
        "row2": sol["row2"],
        "trim": sol["trim"],

        "primary_holes": sol["primary_holes"],
        "holes": sol["holes"],

        "primary_area": sol["primary_area"],
        "trim_area": sol["trim_area"],
        "area": sol["area"],

        "error": sol["error"],
        "percent_error": sol["percent_error"],

        "undersize": sol["undersize"],
        "diameter_ratio": sol["diameter_ratio"],
        "drill_count": sol["drill_count"]
    }

    return pintle_geometry


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    A_ox = 8.720279967159973e-5
    d_chamber = 0.0736153617051

    pintle_geometry = optimize_pintle_geometry(
        A_ox,
        d_chamber
    )

    print(pintle_geometry)