import math

def injector_annulus_sizing(mdot_fuel_comb, A_fuel_comb, d_pintle):

    annulus_geometry = {
    'd_inner': d_pintle}

    annulus_geometry['r_inner'] = annulus_geometry['d_inner'] / 2
    annulus_geometry['r_outer'] =  math.sqrt( (A_fuel_comb/math.pi) + annulus_geometry['r_inner']**2)
    annulus_geometry['thickness'] = annulus_geometry['r_outer'] - annulus_geometry['r_inner']

    return annulus_geometry

