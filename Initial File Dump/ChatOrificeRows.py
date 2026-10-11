import math


# ============================================================
# # DRILL SIZES
# Diameter in inches
# ============================================================

DRILL_BITS = {
    "#80": 0.0135,
    "#79": 0.0145,
    "#78": 0.0160,
    "#77": 0.0180,
    "#76": 0.0200,
    "#75": 0.0210,
    "#74": 0.0225,
    "#73": 0.0240,
    "#72": 0.0250,
    "#71": 0.0260,
    "#70": 0.0280,
    "#69": 0.0292,
    "#68": 0.0310,
    "#67": 0.0320,
    "#66": 0.0330,
    "#65": 0.0350,
    "#64": 0.0360,
    "#63": 0.0370,
    "#62": 0.0380,
    "#61": 0.0390,
    "#60": 0.0400,
    "#59": 0.0410,
    "#58": 0.0420,
    "#57": 0.0430,
    "#56": 0.0465,
    "#55": 0.0520,
    "#54": 0.0550,
    "#53": 0.0595,
    "#52": 0.0635,
    "#51": 0.0670,
    "#50": 0.0700,
    "#49": 0.0730,
    "#48": 0.0760,
    "#47": 0.0785,
    "#46": 0.0810,
    "#45": 0.0820,
    "#44": 0.0860,
    "#43": 0.0890,
    "#42": 0.0935,
    "#41": 0.0960,
    "#40": 0.0980,
    "#39": 0.0995,
    "#38": 0.1015,
    "#37": 0.1040,
    "#36": 0.1065,
    "#35": 0.1100,
    "#34": 0.1110,
    "#33": 0.1130,
    "#32": 0.1160,
    "#31": 0.1200,
    "#30": 0.1285,
    "#29": 0.1360,
    "#28": 0.1405,
    "#27": 0.1440,
    "#26": 0.1470,
    "#25": 0.1495,
    "#24": 0.1520,
    "#23": 0.1540,
    "#22": 0.1570,
    "#21": 0.1590,
    "#20": 0.1610,
    "#19": 0.1660,
    "#18": 0.1695,
    "#17": 0.1730,
    "#16": 0.1770,
    "#15": 0.1800,
    "#14": 0.1820,
    "#13": 0.1850,
    "#12": 0.1890,
    "#11": 0.1910,
    "#10": 0.1935,
    "#9": 0.1960,
    "#8": 0.1990,
    "#7": 0.2010,
    "#6": 0.2040,
    "#5": 0.2055,
    "#4": 0.2090,
    "#3": 0.2130,
    "#2": 0.2210,
    "#1": 0.2280,
}


# ============================================================
# USER INPUTS
# ============================================================

# ------------------------------------------------------------
# Required total orifice area
# ------------------------------------------------------------

TOTAL_ORIFICE_AREA_M2 = 0.000064862364346975


# ------------------------------------------------------------
# Diameter of cylindrical injector surface
# ------------------------------------------------------------

CYLINDER_DIAMETER_M = 0.0127


# ------------------------------------------------------------
# Minimum edge-to-edge spacing between holes
# ------------------------------------------------------------

MIN_SPACING_M = 0.0005


# ------------------------------------------------------------
# Maximum total number of holes
# ------------------------------------------------------------

MAX_HOLE_COUNT = 45


# ------------------------------------------------------------
# Maximum number of circumferential rows
# ------------------------------------------------------------

MAX_ROWS = 4


# ============================================================
# DRILL SIZE PREFERENCE
# ============================================================

# Drill that is closest to the desired size.
DESIRED_DRILL = "#60"

# Only drills in this diameter range are considered.
MIN_DRILL_DIAMETER_MM = 0.9
MAX_DRILL_DIAMETER_MM = 1.8


# ============================================================
# AREA TOLERANCE
# ============================================================

# Any solution within ±0.1% is considered sufficiently
# accurate. Area error is NOT the primary optimization
# objective inside this range.
AREA_TOLERANCE_PERCENT = 0.9


# ============================================================
# OUTPUT
# ============================================================

NUMBER_OF_SOLUTIONS = 10


# ============================================================
# SEARCH SETTINGS
# ============================================================

# Number of candidate states retained after each row.
#
# Higher = more exhaustive.
# Lower = faster.
#
# 5000 should generally be plenty for this problem.
BEAM_WIDTH = 50000


# ============================================================
# UNIT CONVERSIONS
# ============================================================

IN_TO_M = 0.0254
M_TO_MM = 1000.0


# ============================================================
# BASIC FUNCTIONS
# ============================================================

def drill_diameter_m(drill):
    """Return drill diameter in meters."""
    return DRILL_BITS[drill] * IN_TO_M


def drill_diameter_mm(drill):
    """Return drill diameter in millimeters."""
    return drill_diameter_m(drill) * M_TO_MM


def hole_area(diameter_m):
    """Area of one circular hole in m²."""
    return math.pi * (diameter_m / 2.0) ** 2


# ============================================================
# AREA ERROR
# ============================================================

def area_error_percent(actual_area, target_area):
    """Absolute area error as a percentage."""

    return (
        abs(actual_area - target_area)
        / target_area
        * 100.0
    )


def signed_area_error_percent(actual_area, target_area):
    """Signed area error as a percentage."""

    return (
        (actual_area - target_area)
        / target_area
        * 100.0
    )


# ============================================================
# VALID DRILL SIZES
# ============================================================

def get_valid_drills():
    """
    Return only drill sizes within the user-specified
    diameter range.
    """

    valid_drills = []

    for drill in DRILL_BITS:

        diameter_mm = drill_diameter_mm(drill)

        if (
            MIN_DRILL_DIAMETER_MM
            <= diameter_mm
            <= MAX_DRILL_DIAMETER_MM
        ):

            valid_drills.append(drill)

    return valid_drills


# ============================================================
# MAXIMUM HOLES AROUND CYLINDER
# ============================================================

def maximum_holes_on_cylinder(
    cylinder_radius,
    hole_diameter,
    minimum_spacing
):
    """
    Determine the maximum number of equally spaced holes
    around the cylindrical circumference.

    Uses the actual chord distance between holes.

    Required center-to-center spacing:

        hole diameter + minimum edge spacing
    """

    required_center_spacing = (
        hole_diameter
        + minimum_spacing
    )

    circumference = (
        2.0
        * math.pi
        * cylinder_radius
    )

    # Initial estimate
    n = int(
        circumference
        / required_center_spacing
    )

    n = max(n, 1)

    # Verify using actual chord distance
    while n > 1:

        chord = (
            2.0
            * cylinder_radius
            * math.sin(math.pi / n)
        )

        if chord >= required_center_spacing:
            break

        n -= 1

    return n


# ============================================================
# AXIAL SPACING BETWEEN ROWS
# ============================================================

def required_axial_spacing(
    diameter_1,
    diameter_2,
    minimum_spacing
):
    """
    Conservative axial center-to-center spacing.

    Guarantees edge-to-edge spacing even when holes in
    adjacent rows are directly aligned.
    """

    return (
        diameter_1 / 2.0
        + minimum_spacing
        + diameter_2 / 2.0
    )


# ============================================================
# BUILD POSSIBLE ROW CONFIGURATIONS
# ============================================================

def build_row_options(
    cylinder_radius,
    valid_drills
):
    """
    Generate all possible configurations for one row.

    A row is defined by:

        Drill size
        Hole diameter
        Number of holes
        Total row area
    """

    options = []

    for drill in valid_drills:

        diameter_m = drill_diameter_m(drill)
        diameter_mm = drill_diameter_mm(drill)

        max_count = maximum_holes_on_cylinder(
            cylinder_radius,
            diameter_m,
            MIN_SPACING_M
        )

        # Never allow one row to exceed the total
        # hole-count limit.
        max_count = min(
            max_count,
            MAX_HOLE_COUNT
        )

        for count in range(
            1,
            max_count + 1
        ):

            row_area = (
                count
                * hole_area(diameter_m)
            )

            options.append({
                "drill": drill,
                "diameter_m": diameter_m,
                "diameter_mm": diameter_mm,
                "count": count,
                "area_m2": row_area,
            })

    return options


# ============================================================
# INTERMEDIATE SEARCH SCORE
# ============================================================

def intermediate_score(
    state,
    target_area,
    desired_diameter_mm
):
    """
    Used to decide which partial configurations should
    survive the beam search.

    This is NOT the final ranking.

    It primarily keeps configurations that are moving
    toward the target area.
    """

    area_error = (
        abs(state["area"] - target_area)
        / target_area
    )

    drill_error = sum(
        abs(
            row["diameter_mm"]
            - desired_diameter_mm
        )
        for row in state["rows"]
    )

    # Area dominates the intermediate search.
    return (
        area_error * 1_000_000
        + drill_error
    )


# ============================================================
# FINAL SOLUTION SCORE
# ============================================================

def final_solution_score(
    solution,
    target_area,
    desired_diameter_mm
):
    """
    Rank solutions that are ALREADY inside the ±0.1%
    area tolerance.

    Priority:

        1. Desired drill size
        2. Fewer different drill sizes
        3. Area error
        4. Fewer total holes
    """

    # --------------------------------------------------------
    # Drill-size error
    # --------------------------------------------------------

    drill_errors = []

    for row in solution["rows"]:

        drill_errors.append(
            abs(
                row["diameter_mm"]
                - desired_diameter_mm
            )
        )

    average_drill_error = (
        sum(drill_errors)
        / len(drill_errors)
    )

    # --------------------------------------------------------
    # Number of different drills
    # --------------------------------------------------------

    unique_drills = len(
        set(
            row["drill"]
            for row in solution["rows"]
        )
    )

    # --------------------------------------------------------
    # Area error
    # --------------------------------------------------------

    area_error = area_error_percent(
        solution["area"],
        target_area
    )

    # --------------------------------------------------------
    # Hierarchical weighting
    #
    # Drill size is overwhelmingly more important than
    # tiny differences in area error once we're within
    # the 0.1% tolerance.
    # --------------------------------------------------------

    return (
        average_drill_error * 1000.0
        + unique_drills * 1.0
        + area_error * 0.01
        + solution["holes"] * 0.0001
    )


# ============================================================
# OPTIMIZER
# ============================================================

def optimize():

    target_area = TOTAL_ORIFICE_AREA_M2

    cylinder_radius = (
        CYLINDER_DIAMETER_M / 2.0
    )

    desired_diameter_mm = (
        drill_diameter_mm(
            DESIRED_DRILL
        )
    )

    # --------------------------------------------------------
    # Get drills inside desired diameter range
    # --------------------------------------------------------

    valid_drills = get_valid_drills()

    print()
    print("=" * 90)
    print("CYLINDRICAL ORIFICE OPTIMIZER")
    print("=" * 90)

    print(
        f"Target area:          "
        f"{target_area:.8e} m²"
    )

    print(
        f"Target area:          "
        f"{target_area * 1e6:.6f} mm²"
    )

    print(
        f"Cylinder diameter:    "
        f"{CYLINDER_DIAMETER_M * M_TO_MM:.4f} mm"
    )

    print(
        f"Minimum spacing:      "
        f"{MIN_SPACING_M * M_TO_MM:.4f} mm"
    )

    print(
        f"Maximum holes:        "
        f"{MAX_HOLE_COUNT}"
    )

    print(
        f"Maximum rows:         "
        f"{MAX_ROWS}"
    )

    print(
        f"Desired drill:        "
        f"{DESIRED_DRILL} "
        f"({desired_diameter_mm:.4f} mm)"
    )

    print(
        f"Drill diameter range: "
        f"{MIN_DRILL_DIAMETER_MM:.3f} - "
        f"{MAX_DRILL_DIAMETER_MM:.3f} mm"
    )

    print(
        f"Area tolerance:       "
        f"±{AREA_TOLERANCE_PERCENT:.3f}%"
    )

    print()

    print("Drills being considered:")

    for drill in valid_drills:

        print(
            f"  {drill}: "
            f"{drill_diameter_mm(drill):.4f} mm"
        )

    print()

    # --------------------------------------------------------
    # Build possible row configurations
    # --------------------------------------------------------

    row_options = build_row_options(
        cylinder_radius,
        valid_drills
    )

    print(
        f"Possible row configurations: "
        f"{len(row_options)}"
    )

    print()

    # --------------------------------------------------------
    # Initial state
    # --------------------------------------------------------

    states = [
        {
            "rows": [],
            "area": 0.0,
            "holes": 0,
            "axial_position_m": 0.0,
            "last_diameter_m": None,
        }
    ]

    valid_solutions = []

    # --------------------------------------------------------
    # Search row-by-row
    # --------------------------------------------------------

    for row_number in range(
        1,
        MAX_ROWS + 1
    ):

        print(
            f"Searching row "
            f"{row_number}/{MAX_ROWS}..."
        )

        new_states = []

        for state in states:

            for option in row_options:

                # ------------------------------------------------
                # Hole-count constraint
                # ------------------------------------------------

                total_holes = (
                    state["holes"]
                    + option["count"]
                )

                if total_holes > MAX_HOLE_COUNT:
                    continue

                # ------------------------------------------------
                # Calculate axial position
                # ------------------------------------------------

                if row_number == 1:

                    axial_position_m = 0.0

                else:

                    axial_spacing = (
                        required_axial_spacing(
                            state["last_diameter_m"],
                            option["diameter_m"],
                            MIN_SPACING_M
                        )
                    )

                    axial_position_m = (
                        state["axial_position_m"]
                        + axial_spacing
                    )

                # ------------------------------------------------
                # Calculate total area
                # ------------------------------------------------

                total_area = (
                    state["area"]
                    + option["area_m2"]
                )

                # ------------------------------------------------
                # If we've already exceeded target by more than
                # the allowed tolerance, adding more holes can
                # never fix it.
                # ------------------------------------------------

                if total_area > (
                    target_area
                    * (
                        1.0
                        + AREA_TOLERANCE_PERCENT / 100.0
                    )
                ):

                    continue

                # ------------------------------------------------
                # Create row
                # ------------------------------------------------

                row = {
                    "row": row_number,
                    "drill": option["drill"],
                    "diameter_m":
                        option["diameter_m"],
                    "diameter_mm":
                        option["diameter_mm"],
                    "count":
                        option["count"],
                    "area_m2":
                        option["area_m2"],
                    "axial_position_m":
                        axial_position_m,
                    "axial_position_mm":
                        axial_position_m
                        * M_TO_MM,
                }

                rows = (
                    state["rows"]
                    + [row]
                )

                new_state = {
                    "rows": rows,
                    "area": total_area,
                    "holes": total_holes,
                    "axial_position_m":
                        axial_position_m,
                    "last_diameter_m":
                        option["diameter_m"],
                }

                # ------------------------------------------------
                # Check area tolerance
                # ------------------------------------------------

                error_percent = (
                    area_error_percent(
                        total_area,
                        target_area
                    )
                )

                if (
                    error_percent
                    <= AREA_TOLERANCE_PERCENT
                ):

                    valid_solutions.append(
                        new_state
                    )

                # ------------------------------------------------
                # Continue searching for additional rows
                # ------------------------------------------------

                new_states.append(
                    new_state
                )

        # --------------------------------------------------------
        # Rank partial states
        # --------------------------------------------------------

        new_states.sort(
            key=lambda state:
            intermediate_score(
                state,
                target_area,
                desired_diameter_mm
            )
        )

        # --------------------------------------------------------
        # Beam search
        # --------------------------------------------------------

        states = new_states[
            :BEAM_WIDTH
        ]

        print(
            f"  States retained: "
            f"{len(states)}"
        )

        print(
            f"  Valid solutions: "
            f"{len(valid_solutions)}"
        )

        if not states:
            break

    return valid_solutions


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicate_solutions(
    solutions
):
    """
    Remove solutions with identical row drill/count
    configurations.
    """

    unique = []
    seen = set()

    for solution in solutions:

        signature = tuple(
            (
                row["drill"],
                row["count"]
            )
            for row in solution["rows"]
        )

        if signature in seen:
            continue

        seen.add(signature)

        unique.append(
            solution
        )

    return unique


# ============================================================
# PRINT SOLUTION
# ============================================================

def print_solution(
    solution,
    number
):

    target = TOTAL_ORIFICE_AREA_M2
    actual = solution["area"]

    signed_error = (
        actual
        - target
    )

    signed_error_percent = (
        signed_error
        / target
        * 100.0
    )

    absolute_error_percent = (
        abs(signed_error_percent)
    )

    print()
    print()
    print("=" * 100)

    print(
        f"SOLUTION #{number}"
    )

    print("=" * 100)

    print(
        f"Target area:       "
        f"{target:.8e} m²"
    )

    print(
        f"Actual area:       "
        f"{actual:.8e} m²"
    )

    print()

    print(
        f"Target area:       "
        f"{target * 1e6:.6f} mm²"
    )

    print(
        f"Actual area:       "
        f"{actual * 1e6:.6f} mm²"
    )

    print()

    print(
        f"Area error:        "
        f"{signed_error:+.8e} m²"
    )

    print(
        f"Percent error:     "
        f"{signed_error_percent:+.6f}%"
    )

    print(
        f"Total holes:       "
        f"{solution['holes']}"
    )

    print(
        f"Number of rows:    "
        f"{len(solution['rows'])}"
    )

    print()

    if (
        absolute_error_percent
        <= AREA_TOLERANCE_PERCENT
    ):

        print(
            f"STATUS: PASS "
            f"(within ±{AREA_TOLERANCE_PERCENT}%)"
        )

    else:

        print(
            "STATUS: FAIL"
        )

    # --------------------------------------------------------
    # Row table
    # --------------------------------------------------------

    print()

    print(
        f"{'Row':<6}"
        f"{'Drill':<10}"
        f"{'Diameter':<15}"
        f"{'Holes':<10}"
        f"{'Axial Pos.':<17}"
        f"{'Row Area':<20}"
    )

    print(
        f"{'':<6}"
        f"{'':<10}"
        f"{'(mm)':<15}"
        f"{'':<10}"
        f"{'(mm)':<17}"
        f"{'(m²)':<20}"
    )

    print("-" * 100)

    for row in solution["rows"]:

        print(
            f"{row['row']:<6}"
            f"{row['drill']:<10}"
            f"{row['diameter_mm']:<15.4f}"
            f"{row['count']:<10}"
            f"{row['axial_position_mm']:<17.4f}"
            f"{row['area_m2']:<20.8e}"
        )

    print("-" * 100)

    # --------------------------------------------------------
    # Drill summary
    # --------------------------------------------------------

    drill_summary = {}

    for row in solution["rows"]:

        drill = row["drill"]

        if drill not in drill_summary:

            drill_summary[drill] = {
                "count": 0,
                "diameter_mm":
                    row["diameter_mm"]
            }

        drill_summary[drill]["count"] += (
            row["count"]
        )

    print()

    print("DRILL SUMMARY")
    print("-" * 60)

    for drill, data in drill_summary.items():

        print(
            f"{drill:<8}"
            f"{data['diameter_mm']:>10.4f} mm"
            f"{data['count']:>8} holes"
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    solutions = optimize()

    print()
    print()
    print("=" * 90)
    print("OPTIMIZATION COMPLETE")
    print("=" * 90)

    # --------------------------------------------------------
    # Remove duplicate configurations
    # --------------------------------------------------------

    solutions = (
        remove_duplicate_solutions(
            solutions
        )
    )

    # --------------------------------------------------------
    # Sort solutions according to our priorities
    # --------------------------------------------------------

    desired_diameter_mm = (
        drill_diameter_mm(
            DESIRED_DRILL
        )
    )

    solutions.sort(
        key=lambda solution:
        final_solution_score(
            solution,
            TOTAL_ORIFICE_AREA_M2,
            desired_diameter_mm
        )
    )

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    if not solutions:

        print()
        print(
            "NO VALID SOLUTION FOUND."
        )

        print()

        print(
            f"No configuration using drills between "
            f"{MIN_DRILL_DIAMETER_MM:.2f} and "
            f"{MAX_DRILL_DIAMETER_MM:.2f} mm "
            f"achieved the required area within "
            f"±{AREA_TOLERANCE_PERCENT:.2f}%."
        )

        print()

        print("Try changing:")

        print(
            "  MAX_HOLE_COUNT"
        )

        print(
            "  MAX_ROWS"
        )

        print(
            "  MIN_SPACING_M"
        )

        print(
            "  MIN_DRILL_DIAMETER_MM"
        )

        print(
            "  MAX_DRILL_DIAMETER_MM"
        )

    else:

        print()

        print(
            f"Found {len(solutions)} "
            f"valid configurations."
        )

        print()

        for i, solution in enumerate(
            solutions[
                :NUMBER_OF_SOLUTIONS
            ],
            start=1
        ):

            print_solution(
                solution,
                i
            )