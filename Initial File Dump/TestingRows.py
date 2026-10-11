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
    "#9":  0.1960,
    "#8":  0.1990,
    "#7":  0.2010,
    "#6":  0.2040,
    "#5":  0.2055,
    "#4":  0.2090,
    "#3":  0.2130,
    "#2": 0.2210,
    "#1": 0.2280,
}


# ============================================================
# USER INPUTS
# ============================================================

# Desired TOTAL orifice area
TOTAL_ORIFICE_AREA_M2 = 0.000064862364346975

# Diameter of cylindrical injector surface
CYLINDER_DIAMETER_M = 0.0127

# Minimum edge-to-edge spacing between holes
MIN_SPACING_M = 0.0008

# Maximum total number of holes
MAX_HOLE_COUNT = 70

# Desired / ballpark drill
DESIRED_DRILL = "#60"

# Maximum number of circumferential rows
MAX_ROWS = 3

# Number of solutions to print
NUMBER_OF_SOLUTIONS = 3


# ============================================================
# SEARCH SETTINGS
# ============================================================

# Number of drill sizes to consider around the desired
# and required diameter.
#
# Increasing this makes the search more exhaustive.
DRILL_CANDIDATES = 30

# Maximum number of candidate states retained at each row.
BEAM_WIDTH = 3000


# ============================================================
# UNIT CONVERSIONS
# ============================================================

IN_TO_M = 0.0254
M_TO_MM = 1000.0


# ============================================================
# DRILL FUNCTIONS
# ============================================================

def drill_diameter_m(drill):
    return DRILL_BITS[drill] * IN_TO_M


def drill_diameter_mm(drill):
    return drill_diameter_m(drill) * M_TO_MM


def hole_area(diameter_m):
    return math.pi * (diameter_m / 2.0) ** 2


# ============================================================
# DETERMINE DESIRED DIAMETER
# ============================================================

def get_desired_diameter_mm():

    if isinstance(DESIRED_DRILL, str):

        if DESIRED_DRILL not in DRILL_BITS:
            raise ValueError(
                f"Unknown drill size: {DESIRED_DRILL}"
            )

        return drill_diameter_mm(DESIRED_DRILL)

    return float(DESIRED_DRILL)


# ============================================================
# MAXIMUM NUMBER OF HOLES AROUND CYLINDER
# ============================================================

def maximum_holes_on_cylinder(
    cylinder_radius,
    hole_diameter,
    minimum_spacing
):
    """
    Determine the maximum number of equally spaced holes
    that can fit around the circumference.

    Uses the actual chord distance between hole centers.

    Required center-to-center distance:

        hole diameter + minimum edge spacing
    """

    required_center_spacing = (
        hole_diameter
        + minimum_spacing
    )

    # Circumference
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

    # Check using actual chord
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
# REQUIRED AXIAL SPACING BETWEEN ROWS
# ============================================================

def required_axial_spacing(
    diameter_1,
    diameter_2,
    minimum_spacing
):
    """
    Center-to-center axial spacing required between
    adjacent rows.

        dz >= D1/2 + spacing + D2/2
    """

    return (
        diameter_1 / 2.0
        + minimum_spacing
        + diameter_2 / 2.0
    )


# ============================================================
# CANDIDATE DRILL SELECTION
# ============================================================

def select_candidate_drills():

    desired_diameter = (
        get_desired_diameter_mm()
    )

    # Diameter needed if all MAX_HOLE_COUNT holes
    # were the same size.
    required_diameter = (
        math.sqrt(
            4.0
            * TOTAL_ORIFICE_AREA_M2
            / (
                math.pi
                * MAX_HOLE_COUNT
            )
        )
        * M_TO_MM
    )

    # Rank drills according to proximity to either:
    #
    # 1. Desired drill diameter
    # 2. Diameter required by total area / hole count
    #
    ranked = []

    for drill in DRILL_BITS:

        diameter = drill_diameter_mm(drill)

        score_desired = abs(
            diameter
            - desired_diameter
        )

        score_required = abs(
            diameter
            - required_diameter
        )

        score = min(
            score_desired,
            score_required
        )

        ranked.append(
            (score, drill)
        )

    ranked.sort()

    candidates = [
        drill
        for _, drill in ranked[:DRILL_CANDIDATES]
    ]

    # Always include the desired drill
    if DESIRED_DRILL in DRILL_BITS:
        if DESIRED_DRILL not in candidates:
            candidates.append(
                DESIRED_DRILL
            )

    return candidates, required_diameter


# ============================================================
# BUILD ALL VALID ROW OPTIONS
# ============================================================

def build_row_options(
    cylinder_radius,
    drills
):
    """
    A row option consists of:

        drill
        diameter
        hole count
        area
    """

    options = []

    for drill in drills:

        diameter = drill_diameter_m(drill)

        max_count = maximum_holes_on_cylinder(
            cylinder_radius,
            diameter,
            MIN_SPACING_M
        )

        # We don't need more holes in one row than
        # the total hole-count limit.
        max_count = min(
            max_count,
            MAX_HOLE_COUNT
        )

        for count in range(
            1,
            max_count + 1
        ):

            area = (
                count
                * hole_area(diameter)
            )

            options.append({
                "drill": drill,
                "diameter_m": diameter,
                "diameter_mm":
                    diameter * M_TO_MM,
                "count": count,
                "area_m2": area,
            })

    return options


# ============================================================
# SOLUTION SCORE
# ============================================================

def score_solution(
    area,
    rows,
    target_area,
    desired_diameter_mm
):

    # Primary objective:
    # minimize area error
    area_error = abs(
        area
        - target_area
    )

    # Secondary objective:
    # stay near desired drill diameter
    drill_error = sum(
        abs(
            row["diameter_mm"]
            - desired_diameter_mm
        )
        for row in rows
    )

    # Tertiary objective:
    # prefer fewer different drill sizes
    unique_drills = len(
        set(
            row["drill"]
            for row in rows
        )
    )

    # Weighted score
    score = (
        area_error
        + target_area
        * 0.0005
        * drill_error
        + target_area
        * 0.0001
        * unique_drills
    )

    return score


# ============================================================
# MAIN OPTIMIZER
# ============================================================

def optimize():

    target_area = (
        TOTAL_ORIFICE_AREA_M2
    )

    cylinder_radius = (
        CYLINDER_DIAMETER_M / 2.0
    )

    desired_diameter_mm = (
        get_desired_diameter_mm()
    )

    # --------------------------------------------------------
    # Select a manageable number of drill sizes
    # --------------------------------------------------------

    drills, required_diameter = (
        select_candidate_drills()
    )

    print()
    print("=" * 90)
    print("CYLINDRICAL ORIFICE OPTIMIZER")
    print("=" * 90)

    print(
        f"Target area:          "
        f"{target_area:.8e} m^2"
    )

    print(
        f"Target area:          "
        f"{target_area * 1e6:.4f} mm^2"
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
        f"Approx. diameter for "
        f"{MAX_HOLE_COUNT} holes: "
        f"{required_diameter:.4f} mm"
    )

    print(
        f"Drill candidates:     "
        f"{len(drills)}"
    )

    print()

    # --------------------------------------------------------
    # Build row options
    # --------------------------------------------------------

    row_options = build_row_options(
        cylinder_radius,
        drills
    )

    print(
        f"Row configurations:   "
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
            "axial_position": 0.0,
            "last_diameter": None,
            "score": 0.0,
        }
    ]

    final_solutions = []

    # --------------------------------------------------------
    # Build rows one at a time
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

                # --------------------------------------------
                # Hole count constraint
                # --------------------------------------------

                new_hole_count = (
                    state["holes"]
                    + option["count"]
                )

                if (
                    new_hole_count
                    > MAX_HOLE_COUNT
                ):
                    continue

                # --------------------------------------------
                # Axial position
                # --------------------------------------------

                if row_number == 1:

                    axial_position = 0.0

                else:

                    axial_spacing = (
                        required_axial_spacing(
                            state["last_diameter"],
                            option["diameter_m"],
                            MIN_SPACING_M
                        )
                    )

                    axial_position = (
                        state["axial_position"]
                        + axial_spacing
                    )

                # --------------------------------------------
                # New area
                # --------------------------------------------

                new_area = (
                    state["area"]
                    + option["area_m2"]
                )

                # --------------------------------------------
                # Don't allow solutions that are already
                # wildly above target.
                #
                # A little tolerance is allowed because
                # another row is not required.
                # --------------------------------------------

                if (
                    new_area
                    > target_area * 1.50
                ):
                    continue

                # --------------------------------------------
                # New row
                # --------------------------------------------

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
                        axial_position,
                    "axial_position_mm":
                        axial_position * M_TO_MM,
                }

                rows = (
                    state["rows"]
                    + [row]
                )

                # --------------------------------------------
                # Score
                # --------------------------------------------

                score = score_solution(
                    new_area,
                    rows,
                    target_area,
                    desired_diameter_mm
                )

                new_states.append({
                    "rows": rows,
                    "area": new_area,
                    "holes": new_hole_count,
                    "axial_position":
                        axial_position,
                    "last_diameter":
                        option["diameter_m"],
                    "score": score,
                })

        # ----------------------------------------------------
        # Keep only best states
        # ----------------------------------------------------

        new_states.sort(
            key=lambda x: x["score"]
        )

        states = new_states[
            :BEAM_WIDTH
        ]

        print(
            f"  States retained: "
            f"{len(states)}"
        )

        if not states:
            break

        # Add states to final solutions
        final_solutions.extend(states)

    # --------------------------------------------------------
    # Sort all solutions
    # --------------------------------------------------------

    final_solutions.sort(
        key=lambda x: x["score"]
    )

    # --------------------------------------------------------
    # Remove duplicate row configurations
    # --------------------------------------------------------

    unique_solutions = []

    seen = set()

    for solution in final_solutions:

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

        unique_solutions.append(
            solution
        )

        if (
            len(unique_solutions)
            >= NUMBER_OF_SOLUTIONS
        ):
            break

    return unique_solutions


# ============================================================
# PRINT SOLUTION
# ============================================================

def print_solution(
    solution,
    number
):

    target = TOTAL_ORIFICE_AREA_M2

    actual = solution["area"]

    error = (
        actual
        - target
    )

    percent_error = (
        error
        / target
        * 100.0
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
        f"{target:.8e} m^2"
    )

    print(
        f"Actual area:       "
        f"{actual:.8e} m^2"
    )

    print(
        f"Target area:       "
        f"{target * 1e6:.4f} mm^2"
    )

    print(
        f"Actual area:       "
        f"{actual * 1e6:.4f} mm^2"
    )

    print(
        f"Area error:        "
        f"{error:+.8e} m^2"
    )

    print(
        f"Percent error:     "
        f"{percent_error:+.5f} %"
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
    print(
        f"{'Row':<6}"
        f"{'Drill':<10}"
        f"{'Diameter':<15}"
        f"{'Count':<10}"
        f"{'Axial Pos.':<17}"
        f"{'Row Area (m²)':<20}"
    )

    print(
        f"{'':<6}"
        f"{'':<10}"
        f"{'(mm)':<15}"
        f"{'':<10}"
        f"{'(mm)':<17}"
        f"{'':<20}"
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
            drill_summary[drill] = 0

        drill_summary[drill] += row["count"]

    print()
    print("DRILL SUMMARY")
    print("-" * 50)

    for drill, count in drill_summary.items():

        print(
            f"{drill:<8}"
            f"{drill_diameter_mm(drill):>10.4f} mm"
            f"{count:>8} holes"
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

    if not solutions:

        print(
            "No valid solution was found."
        )

    else:

        for i, solution in enumerate(
            solutions,
            start=1
        ):

            print_solution(
                solution,
                i
            )