import math
import itertools


# ============================================================
# USER SETTINGS
# ============================================================

# Target hole area [m^2]
A_OX = 8.720279967159973e-5

# Chamber diameter [m]
D_CHAMBER = 0.0736153617051

# Pintle inner diameter [in]
D_INNER_IN = 0.500

# Desired hole diameter [mm]
TARGET_HOLE_DIAMETER_MM = 1.000

# Maximum acceptable total area error [%]
MAX_PERCENT_ERROR = 0.5

# Minimum material between adjacent holes [mm]
MIN_LIGAMENT_MM = 1.000

# Primary-hole diameter limits [mm]
MIN_HOLE_DIAMETER_MM = 0.500
MAX_HOLE_DIAMETER_MM = 1.500

# Maximum ratio between primary hole diameters
MAX_PRIMARY_DIAMETER_RATIO = 1.50

# Primary hole count
HOLE_MIN = 20
HOLE_MAX = 60

# Minimum holes in each row
MIN_PER_ROW = 8

# Trim-hole diameter limit [mm]
MAX_TRIM_DIAMETER_MM = 1.500

# Allow trim hole
ALLOW_TRIM = True


# ============================================================
# Utilities
# ============================================================

def inch_to_m(x):
    return x * 0.0254


def mm_to_m(x):
    return x / 1000.0


def m_to_mm(x):
    return x * 1000.0


def m_to_in(x):
    return x / 0.0254


def area_from_diameter(d):
    """
    Circular hole area.

    Parameters
    ----------
    d : float
        Diameter [m]

    Returns
    -------
    float
        Area [m^2]
    """

    return math.pi * (d / 2) ** 2


# ============================================================
# Drill Bit Database
# ============================================================

def build_drill_table():

    drills = {}

    # ---------------------------------------------------------
    # Number drills [in]
    # ---------------------------------------------------------

    number_drills_in = {

        80: 0.0135,
        79: 0.0145,
        78: 0.0160,
        77: 0.0180,
        76: 0.0200,
        75: 0.0210,
        74: 0.0225,
        73: 0.0240,
        72: 0.0250,
        71: 0.0260,
        70: 0.0280,
        69: 0.0292,
        68: 0.0310,
        67: 0.0320,
        66: 0.0330,
        65: 0.0350,
        64: 0.0360,
        63: 0.0370,
        62: 0.0380,
        61: 0.0390,
        60: 0.0400,
        59: 0.0410,
        58: 0.0420,
        57: 0.0430,
        56: 0.0465,
        55: 0.0520,
        54: 0.0550,
        53: 0.0595,
        52: 0.0635,
        51: 0.0670,
        50: 0.0700,
        49: 0.0730,
        48: 0.0760,
        47: 0.0785,
        46: 0.0810,
        45: 0.0820,
        44: 0.0860,
        43: 0.0890,
        42: 0.0935,
        41: 0.0960,
        40: 0.0980,
        39: 0.0995,
        38: 0.1015,
        37: 0.1040,
        36: 0.1065,
        35: 0.1100,
        34: 0.1110,
        33: 0.1130,
        32: 0.1160,
        31: 0.1200,
        30: 0.1285,
        29: 0.1360,
        28: 0.1405,
        27: 0.1440,
        26: 0.1470,
        25: 0.1495,
        24: 0.1520,
        23: 0.1540,
        22: 0.1570,
        21: 0.1590,
        20: 0.1610,
        19: 0.1660,
        18: 0.1695,
        17: 0.1730,
        16: 0.1770,
        15: 0.1800,
        14: 0.1820,
        13: 0.1850,
        12: 0.1890,
        11: 0.1910,
        10: 0.1935,
        9: 0.1960,
        8: 0.1990,
        7: 0.2010,
        6: 0.2040,
        5: 0.2055,
        4: 0.2090,
        3: 0.2130,
        2: 0.2210,
        1: 0.2280
    }

    for k, v in number_drills_in.items():
        drills[f"#{k}"] = inch_to_m(v)

    # ---------------------------------------------------------
    # Letter drills [in]
    # ---------------------------------------------------------

    letter_drills_in = {

        "A": 0.234,
        "B": 0.238,
        "C": 0.242,
        "D": 0.246,
        "E": 0.250,
        "F": 0.257,
        "G": 0.261,
        "H": 0.266,
        "I": 0.272,
        "J": 0.277,
        "K": 0.281,
        "L": 0.290,
        "M": 0.295,
        "N": 0.302,
        "O": 0.316,
        "P": 0.323,
        "Q": 0.332,
        "R": 0.339,
        "S": 0.348,
        "T": 0.358,
        "U": 0.368,
        "V": 0.377,
        "W": 0.386,
        "X": 0.397,
        "Y": 0.404,
        "Z": 0.413
    }

    for k, v in letter_drills_in.items():
        drills[k] = inch_to_m(v)

    # ---------------------------------------------------------
    # Fractional drills: 1/16" to 1/2"
    # ---------------------------------------------------------

    for n in range(4, 33):

        frac = n / 64

        drills[f"{n}/64"] = inch_to_m(frac)

    return drills


# ============================================================
# Circular Hole Geometry
# ============================================================

def chord_spacing(d_inner, hole_count):
    """
    Exact center-to-center distance between adjacent holes
    equally distributed around a circle.

    For N equally spaced holes:

        chord = D * sin(pi / N)

    Parameters
    ----------
    d_inner : float
        Diameter of hole-center circle [m]

    hole_count : int
        Number of holes

    Returns
    -------
    float
        Center-to-center distance [m]
    """

    if hole_count <= 1:

        return float("inf")

    return d_inner * math.sin(math.pi / hole_count)


def edge_to_edge_spacing(
        d_inner,
        hole_count,
        hole_diameter):

    """
    Edge-to-edge material between adjacent holes.

        ligament = chord - hole_diameter
    """

    center_spacing = chord_spacing(
        d_inner,
        hole_count
    )

    return center_spacing - hole_diameter


def row_is_valid(
        d_inner,
        hole_count,
        hole_diameter,
        min_ligament):

    """
    Check whether a row of equally spaced holes is
    physically feasible.

    Required:

        chord >= hole_diameter + min_ligament
    """

    ligament = edge_to_edge_spacing(
        d_inner,
        hole_count,
        hole_diameter
    )

    return ligament >= min_ligament


# ============================================================
# Find Best Two-Row Layout
# ============================================================

def find_best_two_row_layout(

        A_target,
        d_inner,

        hole_min=20,
        hole_max=50,
        min_per_row=8,

        min_ligament=0.001,

        target_hole_diameter=0.001,

        min_diameter=0.0005,
        max_primary_diameter=0.0015,

        max_primary_diameter_ratio=1.5,

        allow_trim=True,
        max_trim_diameter=0.0015,

        max_percent_error=0.10,

        results_to_return=10
):

    drills = build_drill_table()

    # ---------------------------------------------------------
    # Drill areas
    # ---------------------------------------------------------

    drill_areas = {

        k: area_from_diameter(v)

        for k, v in drills.items()
    }

    # ---------------------------------------------------------
    # Primary drills
    # ---------------------------------------------------------

    primary_drills = {

        k: d

        for k, d in drills.items()

        if (
            d >= min_diameter
            and d <= max_primary_diameter
        )
    }

    # ---------------------------------------------------------
    # Trim drills
    # ---------------------------------------------------------

    trim_drills = {

        k: d

        for k, d in drills.items()

        if (
            d >= min_diameter
            and d <= max_trim_diameter
        )
    }

    solutions = []

    # =========================================================
    # Try every combination of primary drill sizes
    # =========================================================

    for drill1, drill2 in itertools.combinations_with_replacement(
            primary_drills.keys(),
            2):

        d1 = primary_drills[drill1]
        d2 = primary_drills[drill2]

        A1 = drill_areas[drill1]
        A2 = drill_areas[drill2]

        # -----------------------------------------------------
        # Hole diameter ratio
        # -----------------------------------------------------

        diameter_ratio = (
            max(d1, d2)
            / min(d1, d2)
        )

        if diameter_ratio > max_primary_diameter_ratio:
            continue

        # =====================================================
        # Try total hole count
        # =====================================================

        for N_total in range(
                hole_min,
                hole_max + 1):

            # -------------------------------------------------
            # Try every row distribution
            # -------------------------------------------------

            for N1 in range(
                    min_per_row,
                    N_total - min_per_row + 1):

                N2 = N_total - N1

                # =================================================
                # Physical spacing check
                # =================================================

                if not row_is_valid(
                        d_inner,
                        N1,
                        d1,
                        min_ligament):

                    continue

                if not row_is_valid(
                        d_inner,
                        N2,
                        d2,
                        min_ligament):

                    continue

                # -------------------------------------------------
                # Exact center-to-center spacing
                # -------------------------------------------------

                spacing1 = chord_spacing(
                    d_inner,
                    N1
                )

                spacing2 = chord_spacing(
                    d_inner,
                    N2
                )

                # -------------------------------------------------
                # Actual edge-to-edge ligament
                # -------------------------------------------------

                ligament1 = spacing1 - d1
                ligament2 = spacing2 - d2

                # =================================================
                # Primary area
                # =================================================

                A_primary = (
                    N1 * A1
                    +
                    N2 * A2
                )

                # Primary holes must remain below target
                if A_primary >= A_target:
                    continue

                # -------------------------------------------------
                # Primary undersize
                # -------------------------------------------------

                undersize = (
                    A_target - A_primary
                ) / A_target

                # We need some room for the trim hole
                if undersize <= 0:
                    continue

                # =================================================
                # No-trim case
                # =================================================

                if not allow_trim:

                    percent_error = (

                        abs(
                            A_target - A_primary
                        )
                        /
                        A_target
                        * 100
                    )

                    if percent_error > max_percent_error:
                        continue

                    # Average deviation from desired hole size
                    hole_size_deviation = (

                        abs(d1 - target_hole_diameter)
                        +
                        abs(d2 - target_hole_diameter)

                    ) / 2

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

                        "diameter_ratio":
                            diameter_ratio,

                        "row1_center_spacing":
                            spacing1,

                        "row2_center_spacing":
                            spacing2,

                        "row1_ligament":
                            ligament1,

                        "row2_ligament":
                            ligament2,

                        "hole_size_deviation":
                            hole_size_deviation,

                        "drill_count": len({
                            drill1,
                            drill2
                        })
                    })

                    continue

                # =================================================
                # Trim-hole search
                # =================================================

                residual = (
                    A_target - A_primary
                )

                best_trim = None

                for trim_drill, trim_diameter in trim_drills.items():

                    A_trim = drill_areas[
                        trim_drill
                    ]

                    # Trim hole cannot exceed residual
                    if A_trim > residual:
                        continue

                    trim_error = (
                        residual - A_trim
                    )

                    candidate = (
                        trim_error,
                        A_trim,
                        trim_drill
                    )

                    if (
                        best_trim is None
                        or candidate < best_trim
                    ):

                        best_trim = candidate

                if best_trim is None:
                    continue

                trim_error, A_trim, trim_drill = best_trim

                trim_diameter = trim_drills[
                    trim_drill
                ]

                # =================================================
                # Total area
                # =================================================

                A_total = (
                    A_primary
                    +
                    A_trim
                )

                percent_error = (

                    abs(
                        A_target - A_total
                    )
                    /
                    A_target
                    * 100
                )

                # -------------------------------------------------
                # Enforce 0.1% maximum error
                # -------------------------------------------------

                if percent_error > max_percent_error:
                    continue

                # =================================================
                # Check where trim hole can physically fit
                # =================================================

                # Option 1: trim hole added to row 1
                trim_row1_valid = row_is_valid(

                    d_inner,

                    N1 + 1,

                    max(
                        d1,
                        trim_diameter
                    ),

                    min_ligament
                )

                # Option 2: trim hole added to row 2
                trim_row2_valid = row_is_valid(

                    d_inner,

                    N2 + 1,

                    max(
                        d2,
                        trim_diameter
                    ),

                    min_ligament
                )

                if not (
                    trim_row1_valid
                    or
                    trim_row2_valid
                ):

                    continue

                # -------------------------------------------------
                # Prefer row with larger available ligament
                # -------------------------------------------------

                if trim_row1_valid:

                    trim_row1_spacing = chord_spacing(
                        d_inner,
                        N1 + 1
                    )

                    trim_row1_ligament = (
                        trim_row1_spacing
                        -
                        max(
                            d1,
                            trim_diameter
                        )
                    )

                else:

                    trim_row1_spacing = None
                    trim_row1_ligament = None

                if trim_row2_valid:

                    trim_row2_spacing = chord_spacing(
                        d_inner,
                        N2 + 1
                    )

                    trim_row2_ligament = (
                        trim_row2_spacing
                        -
                        max(
                            d2,
                            trim_diameter
                        )
                    )

                else:

                    trim_row2_spacing = None
                    trim_row2_ligament = None

                # -------------------------------------------------
                # Choose trim row with more ligament
                # -------------------------------------------------

                if (
                    trim_row1_valid
                    and trim_row2_valid
                ):

                    if (
                        trim_row1_ligament
                        >=
                        trim_row2_ligament
                    ):

                        trim_row = 1

                        trim_row_spacing = (
                            trim_row1_spacing
                        )

                        trim_row_ligament = (
                            trim_row1_ligament
                        )

                    else:

                        trim_row = 2

                        trim_row_spacing = (
                            trim_row2_spacing
                        )

                        trim_row_ligament = (
                            trim_row2_ligament
                        )

                elif trim_row1_valid:

                    trim_row = 1

                    trim_row_spacing = (
                        trim_row1_spacing
                    )

                    trim_row_ligament = (
                        trim_row1_ligament
                    )

                else:

                    trim_row = 2

                    trim_row_spacing = (
                        trim_row2_spacing
                    )

                    trim_row_ligament = (
                        trim_row2_ligament
                    )

                # =================================================
                # Hole-size optimization metric
                # =================================================

                # Primary holes are weighted more heavily than
                # the trim hole because they represent the main
                # injector pattern.

                hole_size_deviation = (

                    abs(
                        d1 - target_hole_diameter
                    )

                    +

                    abs(
                        d2 - target_hole_diameter
                    )

                ) / 2

                # =================================================
                # Save solution
                # =================================================

                solutions.append({

                    "row1": (drill1, N1),

                    "row2": (drill2, N2),

                    "trim": trim_drill,

                    "trim_row": trim_row,

                    "primary_holes": N_total,

                    "holes": N_total + 1,

                    "primary_area":
                        A_primary,

                    "trim_area":
                        A_trim,

                    "area":
                        A_total,

                    "error":
                        abs(
                            A_target - A_total
                        ),

                    "percent_error":
                        percent_error,

                    "undersize":
                        undersize,

                    "diameter_ratio":
                        diameter_ratio,

                    "row1_center_spacing":
                        spacing1,

                    "row2_center_spacing":
                        spacing2,

                    "row1_ligament":
                        ligament1,

                    "row2_ligament":
                        ligament2,

                    "trim_row_center_spacing":
                        trim_row_spacing,

                    "trim_row_ligament":
                        trim_row_ligament,

                    "hole_size_deviation":
                        hole_size_deviation,

                    "drill_count":
                        len({
                            drill1,
                            drill2,
                            trim_drill
                        })
                })

    # =========================================================
    # Sort solutions
    # =========================================================
    #
    # Priority:
    #
    # 1. Hole sizes closest to 1 mm
    # 2. Lowest area error
    # 3. Fewest different drill sizes
    # 4. More primary holes
    # 5. More similar primary diameters
    #
    # Every solution here has already passed the 0.1% error
    # requirement and physical spacing requirements.
    # =========================================================

    solutions.sort(

        key=lambda s: (

            s["hole_size_deviation"],

            s["error"],

            s["drill_count"],

            -s["primary_holes"],

            s["diameter_ratio"]
        )
    )

    return solutions[:results_to_return]


# ============================================================
# MAIN OPTIMIZER
# ============================================================

def optimize_pintle_geometry(
        A_ox,
        d_chamber,
        d_inner
):

    """
    Optimize the two-row pintle injector hole geometry.

    Parameters
    ----------
    A_ox : float
        Target oxidizer flow area [m^2]

    d_chamber : float
        Chamber diameter [m]

    d_inner : float
        Inner pintle diameter / hole-center diameter [m]

    Returns
    -------
    dict
        Optimized pintle geometry.
    """

    # ---------------------------------------------------------
    # Pintle diameter
    # ---------------------------------------------------------

    d_pintle = (
        d_chamber
        /
        4.803679096
    )

    # Skip distance = pintle diameter
    skip_distance = d_pintle

    # ---------------------------------------------------------
    # Inner circumference
    # ---------------------------------------------------------

    C_inner = (
        math.pi
        *
        d_inner
    )

    # ---------------------------------------------------------
    # Optimizer
    # ---------------------------------------------------------

    best = find_best_two_row_layout(

        A_target=A_ox,

        d_inner=d_inner,

        hole_min=HOLE_MIN,

        hole_max=HOLE_MAX,

        min_per_row=MIN_PER_ROW,

        min_ligament=mm_to_m(
            MIN_LIGAMENT_MM
        ),

        target_hole_diameter=mm_to_m(
            TARGET_HOLE_DIAMETER_MM
        ),

        min_diameter=mm_to_m(
            MIN_HOLE_DIAMETER_MM
        ),

        max_primary_diameter=mm_to_m(
            MAX_HOLE_DIAMETER_MM
        ),

        max_primary_diameter_ratio=
            MAX_PRIMARY_DIAMETER_RATIO,

        allow_trim=ALLOW_TRIM,

        max_trim_diameter=mm_to_m(
            MAX_TRIM_DIAMETER_MM
        ),

        max_percent_error=
            MAX_PERCENT_ERROR,

        results_to_return=1
    )

    # ---------------------------------------------------------
    # No solution
    # ---------------------------------------------------------

    if not best:

        raise ValueError(

            "No valid pintle hole layout found.\n"

            "Try increasing HOLE_MAX, reducing "
            "MIN_LIGAMENT_MM, increasing the allowed "
            "hole diameter, or relaxing MAX_PERCENT_ERROR."
        )

    # ---------------------------------------------------------
    # Best solution
    # ---------------------------------------------------------

    sol = best[0]

    return {

        # Pintle geometry
        "pintle_diameter":
            d_pintle,

        "pintle_inner_diameter":
            d_inner,

        "skip_distance":
            skip_distance,

        "pintle_inner_circumference":
            C_inner,

        # Hole layout
        "row1":
            sol["row1"],

        "row2":
            sol["row2"],

        "trim":
            sol["trim"],

        "trim_row":
            sol.get("trim_row"),

        "primary_holes":
            sol["primary_holes"],

        "holes":
            sol["holes"],

        # Area
        "primary_area":
            sol["primary_area"],

        "trim_area":
            sol["trim_area"],

        "area":
            sol["area"],

        "error":
            sol["error"],

        "percent_error":
            sol["percent_error"],

        # Geometry
        "diameter_ratio":
            sol["diameter_ratio"],

        "row1_center_spacing":
            sol["row1_center_spacing"],

        "row2_center_spacing":
            sol["row2_center_spacing"],

        "row1_ligament":
            sol["row1_ligament"],

        "row2_ligament":
            sol["row2_ligament"],

        "trim_row_center_spacing":
            sol.get(
                "trim_row_center_spacing"
            ),

        "trim_row_ligament":
            sol.get(
                "trim_row_ligament"
            ),

        "hole_size_deviation":
            sol["hole_size_deviation"],

        "drill_count":
            sol["drill_count"]
    }


# ============================================================
# PRINT RESULTS
# ============================================================

def print_pintle_results(
        pintle_geometry,
        A_target
):

    drills = build_drill_table()

    print()
    print("=" * 60)
    print("OPTIMIZED PINTLE GEOMETRY")
    print("=" * 60)

    # ---------------------------------------------------------
    # Pintle
    # ---------------------------------------------------------

    print()
    print("PINTLE")
    print("-" * 60)

    print(
        f"Pintle diameter:       "
        f"{pintle_geometry['pintle_diameter']:.6f} m"
    )

    print(
        f"Inner diameter:        "
        f"{m_to_in(pintle_geometry['pintle_inner_diameter']):.4f} in"
    )

    print(
        f"Inner diameter:        "
        f"{m_to_mm(pintle_geometry['pintle_inner_diameter']):.3f} mm"
    )

    print(
        f"Inner circumference:   "
        f"{m_to_mm(pintle_geometry['pintle_inner_circumference']):.3f} mm"
    )

    print(
        f"Skip distance:         "
        f"{pintle_geometry['skip_distance']:.6f} m"
    )

    # ---------------------------------------------------------
    # Hole layout
    # ---------------------------------------------------------

    print()
    print("HOLE LAYOUT")
    print("-" * 60)

    # Row 1
    row1_drill, row1_count = (
        pintle_geometry["row1"]
    )

    row1_diameter = drills[
        row1_drill
    ]

    print(
        f"Row 1:                 "
        f"{row1_count} x {row1_drill}"
    )

    print(
        f"  Drill diameter:      "
        f"{m_to_mm(row1_diameter):.3f} mm"
    )

    print(
        f"  Center spacing:      "
        f"{m_to_mm(pintle_geometry['row1_center_spacing']):.3f} mm"
    )

    print(
        f"  Edge ligament:       "
        f"{m_to_mm(pintle_geometry['row1_ligament']):.3f} mm"
    )

    # Row 2
    row2_drill, row2_count = (
        pintle_geometry["row2"]
    )

    row2_diameter = drills[
        row2_drill
    ]

    print()
    print(
        f"Row 2:                 "
        f"{row2_count} x {row2_drill}"
    )

    print(
        f"  Drill diameter:      "
        f"{m_to_mm(row2_diameter):.3f} mm"
    )

    print(
        f"  Center spacing:      "
        f"{m_to_mm(pintle_geometry['row2_center_spacing']):.3f} mm"
    )

    print(
        f"  Edge ligament:       "
        f"{m_to_mm(pintle_geometry['row2_ligament']):.3f} mm"
    )

    # Trim
    trim_drill = pintle_geometry["trim"]

    print()

    if trim_drill is not None:

        trim_diameter = drills[
            trim_drill
        ]

        print(
            f"Trim:                  "
            f"1 x {trim_drill}"
        )

        print(
            f"  Drill diameter:      "
            f"{m_to_mm(trim_diameter):.3f} mm"
        )

        print(
            f"  Trim row:            "
            f"{pintle_geometry['trim_row']}"
        )

        print(
            f"  Center spacing:      "
            f"{m_to_mm(pintle_geometry['trim_row_center_spacing']):.3f} mm"
        )

        print(
            f"  Edge ligament:       "
            f"{m_to_mm(pintle_geometry['trim_row_ligament']):.3f} mm"
        )

    else:

        print("Trim:                  None")

    # ---------------------------------------------------------
    # Area
    # ---------------------------------------------------------

    print()
    print("AREA")
    print("-" * 60)

    print(
        f"Target area:           "
        f"{A_target:.10e} m^2"
    )

    print(
        f"Primary area:          "
        f"{pintle_geometry['primary_area']:.10e} m^2"
    )

    print(
        f"Trim area:             "
        f"{pintle_geometry['trim_area']:.10e} m^2"
    )

    print(
        f"Total area:            "
        f"{pintle_geometry['area']:.10e} m^2"
    )

    print(
        f"Absolute error:        "
        f"{pintle_geometry['error']:.10e} m^2"
    )

    print(
        f"Percent error:         "
        f"{pintle_geometry['percent_error']:.6f} %"
    )

    # ---------------------------------------------------------
    # Optimization
    # ---------------------------------------------------------

    print()
    print("OPTIMIZATION")
    print("-" * 60)

    print(
        f"Target hole diameter:  "
        f"{TARGET_HOLE_DIAMETER_MM:.3f} mm"
    )

    print(
        f"Max area error:        "
        f"{MAX_PERCENT_ERROR:.3f} %"
    )

    print(
        f"Minimum ligament:      "
        f"{MIN_LIGAMENT_MM:.3f} mm"
    )

    print(
        f"Primary holes:         "
        f"{pintle_geometry['primary_holes']}"
    )

    print(
        f"Total holes:           "
        f"{pintle_geometry['holes']}"
    )

    print(
        f"Different drill sizes: "
        f"{pintle_geometry['drill_count']}"
    )

    print("=" * 60)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # ---------------------------------------------------------
    # Run optimizer
    # ---------------------------------------------------------

    d_inner = inch_to_m(
        D_INNER_IN
    )

    pintle_geometry = (
        optimize_pintle_geometry(
            A_OX,
            D_CHAMBER,
            d_inner
        )
    )

    # ---------------------------------------------------------
    # Print results
    # ---------------------------------------------------------

    print_pintle_results(
        pintle_geometry,
        A_OX
    )