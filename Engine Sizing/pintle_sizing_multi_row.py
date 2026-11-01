import math
import itertools


# ============================================================
# USER SETTINGS
# ============================================================

# Target hole area [m^2]
A_OX = 0.000064862364346975

# Chamber diameter [m]
D_CHAMBER = 0.06431280007

# Pintle inner diameter [in]
D_INNER_IN = 0.500

# Desired hole diameter [mm]
TARGET_HOLE_DIAMETER_MM = 1.2

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
HOLE_MAX = 45

# Minimum holes in each row
MIN_PER_ROW = 8

# Trim-hole diameter limit [mm]
MAX_TRIM_DIAMETER_MM = 1.500

# Allow trim hole
ALLOW_TRIM = False


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
# Multi-Row Layout Optimizer
# ============================================================

def max_feasible_holes_per_row(d_inner, hole_diameter, min_ligament):
    """Maximum equally spaced holes that fit in one row."""
    if hole_diameter + min_ligament >= d_inner:
        return 1

    n = 1
    while edge_to_edge_spacing(d_inner, n + 1, hole_diameter) >= min_ligament:
        n += 1

    return n


def distribute_holes(total_holes, n_rows, max_per_row, min_per_row):
    """Distribute holes as evenly as possible across rows."""
    if n_rows == 0:
        return [] if total_holes == 0 else None

    if total_holes < n_rows * min_per_row:
        return None

    if total_holes > n_rows * max_per_row:
        return None

    counts = [min_per_row] * n_rows
    remaining = total_holes - n_rows * min_per_row

    for i in range(n_rows):
        add = min(remaining, max_per_row - min_per_row)
        counts[i] += add
        remaining -= add

    if remaining != 0:
        return None

    return counts


def row_ligament(d_inner, hole_count, hole_diameter):
    return edge_to_edge_spacing(d_inner, hole_count, hole_diameter)


def evaluate_trim_options(
        A_target,
        A_primary,
        rows,
        d_inner,
        drills,
        drill_areas,
        min_ligament,
        min_diameter,
        max_trim_diameter,
        max_percent_error,
        allow_trim):
    """Find the best valid trim drill and row."""

    candidates = []
    residual = A_target - A_primary

    if residual <= 0:
        return None

    # First consider the primary-only solution.
    primary_error = residual / A_target * 100
    if primary_error <= max_percent_error:
        candidates.append({
            "trim": None,
            "trim_row": None,
            "trim_area": 0.0,
            "area": A_primary,
            "error": residual,
            "percent_error": primary_error,
            "trim_row_center_spacing": None,
            "trim_row_ligament": None,
        })

    if not allow_trim:
        return min(candidates, key=lambda x: x["percent_error"]) if candidates else None

    trim_drills = {
        name: d for name, d in drills.items()
        if min_diameter <= d <= max_trim_diameter
    }

    for trim_name, trim_diameter in trim_drills.items():
        trim_area = drill_areas[trim_name]

        if trim_area > residual:
            continue

        total_area = A_primary + trim_area
        percent_error = abs(A_target - total_area) / A_target * 100

        if percent_error > max_percent_error:
            continue

        # Try placing the trim hole into every row.  We use the
        # larger diameter for the conservative adjacent-hole check.
        for row_index, row in enumerate(rows):
            old_count = row["count"]
            primary_diameter = row["diameter"]
            effective_diameter = max(primary_diameter, trim_diameter)
            new_count = old_count + 1

            if not row_is_valid(
                    d_inner,
                    new_count,
                    effective_diameter,
                    min_ligament):
                continue

            spacing = chord_spacing(d_inner, new_count)
            ligament = spacing - effective_diameter

            candidates.append({
                "trim": trim_name,
                "trim_row": row_index + 1,
                "trim_area": trim_area,
                "area": total_area,
                "error": abs(A_target - total_area),
                "percent_error": percent_error,
                "trim_row_center_spacing": spacing,
                "trim_row_ligament": ligament,
            })

    if not candidates:
        return None

    # Prefer the smallest area error.  If equivalent, prefer a
    # smaller trim-hole deviation from the target diameter.
    def trim_key(c):
        if c["trim"] is None:
            trim_dev = 0.0
        else:
            trim_dev = abs(
                m_to_mm(drills[c["trim"]]) - TARGET_HOLE_DIAMETER_MM
            )
        return c["error"], trim_dev

    return min(candidates, key=trim_key)


def find_best_multi_row_layout(
        A_target,
        d_inner,
        min_ligament=0.001,
        target_hole_diameter=0.001,
        min_diameter=0.0005,
        max_primary_diameter=0.0015,
        max_primary_diameter_ratio=1.5,
        allow_trim=True,
        max_trim_diameter=0.0015,
        max_percent_error=0.10,
        min_per_row=8,
        min_rows=2,
        max_rows=12,
        results_to_return=10):
    """
    Optimize an arbitrary number of circular pintle orifice rows.

    Each row contains equally spaced holes of one drill size.  The
    optimizer searches one or two primary drill sizes, automatically
    determines how many rows are required, and optionally adds one trim
    hole to a physically valid row.
    """

    drills_all = build_drill_table()

    drills = {
        name: d for name, d in drills_all.items()
        if min_diameter <= d <= max_primary_diameter
    }

    drill_areas = {
        name: area_from_diameter(d)
        for name, d in drills_all.items()
    }

    # Maximum number of holes that can physically fit in each row.
    row_limits = {
        name: max_feasible_holes_per_row(
            d_inner,
            d,
            min_ligament)
        for name, d in drills.items()
    }

    solutions = []

    drill_names = list(drills.keys())

    # Search pairs of primary drill sizes.  A single drill is simply
    # represented by the same drill appearing twice.
    for drill1, drill2 in itertools.combinations_with_replacement(
            drill_names, 2):

        d1 = drills[drill1]
        d2 = drills[drill2]

        diameter_ratio = max(d1, d2) / min(d1, d2)
        if diameter_ratio > max_primary_diameter_ratio:
            continue

        A1 = drill_areas[drill1]
        A2 = drill_areas[drill2]

        max1 = row_limits[drill1]
        max2 = row_limits[drill2]

        # Total counts need not exceed max_rows * row capacity.
        max_total = max_rows * max(max1, max2)

        # Search counts of each drill.  The target area strongly limits
        # the useful range, so this remains small for the present geometry.
        max_n1 = min(max_total, math.ceil(A_target / A1) + 2)
        max_n2 = min(max_total, math.ceil(A_target / A2) + 2)

        # For each possible count of drill 1, only test drill-2 counts
        # near the area target.  There is no benefit in scanning hundreds
        # of combinations that are obviously far from the target.
        for n1 in range(0, max_n1 + 1):
            if n1 and n1 < min_per_row:
                continue

            if A2 > 0:
                ideal_n2 = (A_target - n1 * A1) / A2
                center_n2 = max(0, int(round(ideal_n2)))
                candidate_n2 = set(range(
                    max(0, center_n2 - 3),
                    min(max_n2, center_n2 + 3) + 1
                ))
            else:
                candidate_n2 = {0}

            # Also explicitly test the single-drill case.
            candidate_n2.add(0)

            for n2 in sorted(candidate_n2):
                if n2 and n2 < min_per_row:
                    continue

                if n1 == 0 and n2 == 0:
                    continue

                A_primary = n1 * A1 + n2 * A2

                # Primary holes must not exceed the target because a
                # trim hole can only add area.
                if A_primary >= A_target:
                    continue

                # Determine the minimum number of rows required to place
                # each drill size while maintaining min_per_row.
                r1_min = 0 if n1 == 0 else math.ceil(n1 / max1)
                r2_min = 0 if n2 == 0 else math.ceil(n2 / max2)

                r1_max = 0 if n1 == 0 else min(max_rows, n1 // min_per_row)
                r2_max = 0 if n2 == 0 else min(max_rows, n2 // min_per_row)

                # Try the minimum-row packing first, plus nearby row
                # counts when they can help accommodate a trim hole.
                rows1_options = [0] if n1 == 0 else list(range(
                    r1_min, min(r1_max, r1_min + 2) + 1))

                rows2_options = [0] if n2 == 0 else list(range(
                    r2_min, min(r2_max, r2_min + 2) + 1))

                for r1 in rows1_options:
                    for r2 in rows2_options:
                        n_rows = r1 + r2

                        if n_rows < min_rows or n_rows > max_rows:
                            continue

                        counts1 = distribute_holes(
                            n1, r1, max1, min_per_row)
                        counts2 = distribute_holes(
                            n2, r2, max2, min_per_row)

                        if counts1 is None or counts2 is None:
                            continue

                        rows = []

                        for count in counts1:
                            rows.append({
                                "drill": drill1,
                                "count": count,
                                "diameter": d1,
                                "center_spacing": chord_spacing(
                                    d_inner, count),
                                "ligament": row_ligament(
                                    d_inner, count, d1),
                            })

                        for count in counts2:
                            rows.append({
                                "drill": drill2,
                                "count": count,
                                "diameter": d2,
                                "center_spacing": chord_spacing(
                                    d_inner, count),
                                "ligament": row_ligament(
                                    d_inner, count, d2),
                            })

                        trim = evaluate_trim_options(
                            A_target,
                            A_primary,
                            rows,
                            d_inner,
                            drills_all,
                            drill_areas,
                            min_ligament,
                            min_diameter,
                            max_trim_diameter,
                            max_percent_error,
                            allow_trim)

                        if trim is None:
                            continue

                        primary_holes = n1 + n2
                        total_holes = primary_holes + (
                            1 if trim["trim"] is not None else 0)

                        # Include the trim drill when calculating the
                        # number of different drill sizes.
                        used_drills = {row["drill"] for row in rows}
                        if trim["trim"] is not None:
                            used_drills.add(trim["trim"])

                        hole_size_deviation = (
                            sum(
                                abs(row["diameter"] - target_hole_diameter)
                                for row in rows
                            ) / primary_holes
                        )

                        # Optimization priority:
                        # 1. Holes close to 1 mm
                        # 2. Area error
                        # 3. Fewer rows
                        # 4. Fewer drill sizes
                        # 5. More holes
                        # 6. More similar primary diameters
                        solution = {
                            "rows": rows,
                            "trim": trim["trim"],
                            "trim_row": trim["trim_row"],
                            "primary_holes": primary_holes,
                            "holes": total_holes,
                            "primary_area": A_primary,
                            "trim_area": trim["trim_area"],
                            "area": trim["area"],
                            "error": trim["error"],
                            "percent_error": trim["percent_error"],
                            "diameter_ratio": diameter_ratio,
                            "hole_size_deviation": hole_size_deviation,
                            "drill_count": len(used_drills),
                            "row_count": len(rows),
                            "trim_row_center_spacing": trim[
                                "trim_row_center_spacing"],
                            "trim_row_ligament": trim[
                                "trim_row_ligament"],
                        }

                        solutions.append(solution)

    solutions.sort(
        key=lambda s: (
            s["hole_size_deviation"],
            s["error"],
            s["row_count"],
            s["drill_count"],
            -s["primary_holes"],
            s["diameter_ratio"],
        )
    )

    return solutions[:results_to_return]


# ============================================================
# MAIN OPTIMIZER
# ============================================================

def optimize_pintle_geometry(
        A_ox,
        d_chamber,
        d_inner):
    """Optimize pintle geometry and an arbitrary number of hole rows."""

    d_pintle = d_chamber / 4.803679096
    skip_distance = d_pintle
    C_inner = math.pi * d_inner

    best = find_best_multi_row_layout(
        A_target=A_ox,
        d_inner=d_inner,
        min_ligament=mm_to_m(MIN_LIGAMENT_MM),
        target_hole_diameter=mm_to_m(TARGET_HOLE_DIAMETER_MM),
        min_diameter=mm_to_m(MIN_HOLE_DIAMETER_MM),
        max_primary_diameter=mm_to_m(MAX_HOLE_DIAMETER_MM),
        max_primary_diameter_ratio=MAX_PRIMARY_DIAMETER_RATIO,
        allow_trim=ALLOW_TRIM,
        max_trim_diameter=mm_to_m(MAX_TRIM_DIAMETER_MM),
        max_percent_error=MAX_PERCENT_ERROR,
        min_per_row=MIN_PER_ROW,
        min_rows=2,
        max_rows=12,
        results_to_return=1,
    )

    if not best:
        raise ValueError(
            "No valid pintle hole layout found.\n"
            "Try increasing MAX_HOLE_DIAMETER_MM, reducing "
            "MIN_LIGAMENT_MM, increasing MAX_ROWS, or relaxing "
            "MAX_PERCENT_ERROR."
        )

    sol = best[0]

    return {
        "pintle_diameter": d_pintle,
        "pintle_inner_diameter": d_inner,
        "skip_distance": skip_distance,
        "pintle_inner_circumference": C_inner,
        "rows": sol["rows"],
        "trim": sol["trim"],
        "trim_row": sol["trim_row"],
        "primary_holes": sol["primary_holes"],
        "holes": sol["holes"],
        "primary_area": sol["primary_area"],
        "trim_area": sol["trim_area"],
        "area": sol["area"],
        "error": sol["error"],
        "percent_error": sol["percent_error"],
        "diameter_ratio": sol["diameter_ratio"],
        "trim_row_center_spacing": sol["trim_row_center_spacing"],
        "trim_row_ligament": sol["trim_row_ligament"],
        "hole_size_deviation": sol["hole_size_deviation"],
        "drill_count": sol["drill_count"],
        "row_count": sol["row_count"],
    }


# ============================================================
# PRINT RESULTS
# ============================================================

def print_pintle_results(pintle_geometry, A_target):

    drills = build_drill_table()

    print()
    print("=" * 70)
    print("OPTIMIZED PINTLE GEOMETRY")
    print("=" * 70)

    print()
    print("PINTLE")
    print("-" * 70)
    print(f"Pintle diameter:       {pintle_geometry['pintle_diameter']:.6f} m")
    print(f"Inner diameter:        {m_to_in(pintle_geometry['pintle_inner_diameter']):.4f} in")
    print(f"Inner diameter:        {m_to_mm(pintle_geometry['pintle_inner_diameter']):.3f} mm")
    print(f"Inner circumference:   {m_to_mm(pintle_geometry['pintle_inner_circumference']):.3f} mm")
    print(f"Skip distance:         {pintle_geometry['skip_distance']:.6f} m")

    print()
    print("HOLE LAYOUT")
    print("-" * 70)

    for i, row in enumerate(pintle_geometry["rows"], start=1):
        print(f"Row {i}:                 {row['count']} x {row['drill']}")
        print(f"  Drill diameter:      {m_to_mm(row['diameter']):.3f} mm")
        print(f"  Center spacing:      {m_to_mm(row['center_spacing']):.3f} mm")
        print(f"  Edge ligament:       {m_to_mm(row['ligament']):.3f} mm")

    print()
    if pintle_geometry["trim"] is not None:
        trim = pintle_geometry["trim"]
        trim_diameter = drills[trim]
        print(f"Trim:                  1 x {trim}")
        print(f"  Drill diameter:      {m_to_mm(trim_diameter):.3f} mm")
        print(f"  Trim row:            {pintle_geometry['trim_row']}")
        print(f"  Center spacing:      {m_to_mm(pintle_geometry['trim_row_center_spacing']):.3f} mm")
        print(f"  Edge ligament:       {m_to_mm(pintle_geometry['trim_row_ligament']):.3f} mm")
    else:
        print("Trim:                  None")

    print()
    print("AREA")
    print("-" * 70)
    print(f"Target area:           {A_target:.10e} m^2")
    print(f"Primary area:          {pintle_geometry['primary_area']:.10e} m^2")
    print(f"Trim area:             {pintle_geometry['trim_area']:.10e} m^2")
    print(f"Total area:            {pintle_geometry['area']:.10e} m^2")
    print(f"Absolute error:        {pintle_geometry['error']:.10e} m^2")
    print(f"Percent error:         {pintle_geometry['percent_error']:.6f} %")

    print()
    print("OPTIMIZATION")
    print("-" * 70)
    print(f"Target hole diameter:  {TARGET_HOLE_DIAMETER_MM:.3f} mm")
    print(f"Max area error:        {MAX_PERCENT_ERROR:.3f} %")
    print(f"Minimum ligament:      {MIN_LIGAMENT_MM:.3f} mm")
    print(f"Number of rows:        {pintle_geometry['row_count']}")
    print(f"Primary holes:         {pintle_geometry['primary_holes']}")
    print(f"Total holes:           {pintle_geometry['holes']}")
    print(f"Different drill sizes: {pintle_geometry['drill_count']}")
    print(f"Diameter ratio:        {pintle_geometry['diameter_ratio']:.4f}")
    print("=" * 70)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    d_inner = inch_to_m(D_INNER_IN)

    pintle_geometry = optimize_pintle_geometry(
        A_OX,
        D_CHAMBER,
        d_inner
    )

    print_pintle_results(
        pintle_geometry,
        A_OX
    )
