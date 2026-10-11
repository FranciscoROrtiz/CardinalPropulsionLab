
import math
import pandas as pd

# ============================================================
# IMPERIAL DRILL BIT DATABASE
# ============================================================

# Numbered drill bits: #80 through #1
# Diameters are in inches.

numbered_drills = {
    80: 0.0135, 79: 0.0145, 78: 0.0160, 77: 0.0180,
    76: 0.0200, 75: 0.0210, 74: 0.0225, 73: 0.0240,
    72: 0.0250, 71: 0.0260, 70: 0.0280, 69: 0.0292,
    68: 0.0310, 67: 0.0320, 66: 0.0330, 65: 0.0350,
    64: 0.0360, 63: 0.0370, 62: 0.0380, 61: 0.0390,
    60: 0.0400, 59: 0.0410, 58: 0.0420, 57: 0.0430,
    56: 0.0465, 55: 0.0520, 54: 0.0550, 53: 0.0595,
    52: 0.0635, 51: 0.0670, 50: 0.0700, 49: 0.0730,
    48: 0.0760, 47: 0.0785, 46: 0.0810, 45: 0.0820,
    44: 0.0860, 43: 0.0890, 42: 0.0935, 41: 0.0960,
    40: 0.0980, 39: 0.0995, 38: 0.1015, 37: 0.1040,
    36: 0.1065, 35: 0.1100, 34: 0.1110, 33: 0.1130,
    32: 0.1160, 31: 0.1200, 30: 0.1285, 29: 0.1360,
    28: 0.1405, 27: 0.1440, 26: 0.1470, 25: 0.1495,
    24: 0.1520, 23: 0.1540, 22: 0.1570, 21: 0.1590,
    20: 0.1610, 19: 0.1660, 18: 0.1695, 17: 0.1730,
    16: 0.1770, 15: 0.1800, 14: 0.1820, 13: 0.1850,
    12: 0.1890, 11: 0.1910, 10: 0.1935, 9: 0.1960,
    8: 0.1990, 7: 0.2010, 6: 0.2040, 5: 0.2055,
    4: 0.2090, 3: 0.2130, 2: 0.2210, 1: 0.2280
}

# Fractional drill bits (inches)
fractional_drills = {
    '1/16': 1/16,
    '5/64': 5/64,
    '3/32': 3/32,
    '7/64': 7/64,
    '1/8': 1/8,
    '9/64': 9/64,
    '5/32': 5/32,
    '3/16': 3/16,
    '7/32': 7/32,
    '1/4': 1/4,
    '5/16': 5/16,
    '3/8': 3/8,
    '7/16': 7/16,
    '1/2': 1/2
}

# Combine drill sizes into one database
drills = {}

for number, diameter in numbered_drills.items():
    drills[f"#{number}"] = diameter

for name, diameter in fractional_drills.items():
    drills[f'{name}"'] = diameter


# ============================================================
# AREA OPTIMIZATION FUNCTION
# ============================================================

def optimize_drill_holes(target_area_m2):

    if target_area_m2 <= 0:
        raise ValueError("Target area must be greater than zero.")

    results = []

    for drill_name, diameter_in in drills.items():

        # Convert diameter to meters
        diameter_m = diameter_in * 0.0254

        # Cross-sectional area of one hole
        area_per_hole = math.pi * (diameter_m / 2)**2

        # Optimal integer number of holes
        number_of_holes = max(1, round(target_area_m2 / area_per_hole))

        # Resulting total area
        total_area = number_of_holes * area_per_hole

        # Area error
        absolute_error = abs(total_area - target_area_m2)

        percentage_error = (
            absolute_error / target_area_m2
        ) * 100

        results.append({
            "Drill Bit": drill_name,
            "Diameter (in)": diameter_in,
            "Diameter (mm)": diameter_m * 1000,
            "Number of Holes": number_of_holes,
            "Area per Hole (m^2)": area_per_hole,
            "Total Area (m^2)": total_area,
            "Area Error (m^2)": absolute_error,
            "Error (%)": percentage_error
        })

    # Sort by smallest area error
    results.sort(key=lambda x: x["Area Error (m^2)"])

    return pd.DataFrame(results)


# ============================================================
# USER INPUT
# ============================================================

if __name__ == "__main__":

    target_area = float(input("Enter target area (m^2): "))

    results = optimize_drill_holes(target_area)

    # Display all drill bit results
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda x: f"{x:.8e}")

    print("\nDRILL BIT AREA OPTIMIZATION")
    print(f"Target Area: {target_area:.8e} m^2\n")

    print(results.to_string(index=False))

    # Display best match
    best = results.iloc[0]

    print("\n" + "=" * 60)
    print("BEST MATCH")
    print("=" * 60)

    print(f"Drill Bit:       {best['Drill Bit']}")
    print(f"Diameter:        {best['Diameter (mm)']:.4f} mm")
    print(f"Number of Holes: {int(best['Number of Holes'])}")
    print(f"Total Area:      {best['Total Area (m^2)']:.8e} m^2")
    print(f"Area Error:      {best['Area Error (m^2)']:.8e} m^2")
    print(f"Error:           {best['Error (%)']:.6f}%")