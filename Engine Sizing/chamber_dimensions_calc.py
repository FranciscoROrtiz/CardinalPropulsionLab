from chamber_volume_calc import chamber_volume_calc
from chamber_area_calc import chamber_area_calc
from chamber_length_calc import chamber_length_calc
from area_to_diameter import area_to_diameter

def chamber_dimensions_calc(chamber_def):
    V_c = chamber_volume_calc(chamber_def)
    A_c = chamber_area_calc(chamber_def)
    d_c = area_to_diameter(A_c)
    L_c = chamber_length_calc(V_c, A_c)

    chamber_dimensions = {
        "diameter": d_c,
        "volume": V_c,
        "area": A_c,
        "length": L_c
    }

    return chamber_dimensions