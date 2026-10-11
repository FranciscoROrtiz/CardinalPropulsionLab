import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# Set a global font for all text elements
mpl.rcParams['font.family'] = 'Courier New'

def main():

    ##### CONSTANTS #####
    Cd = 0.4            # Discharge Coefficient (conservative)
    rho = 785.26        # Density of IPA
    p1 = 405 * 6894.75729 # [Pa]
    p2 = 350 * 6894.75729 # [Pa]
    mdot_fuel_comb = 0.306070295     # [kg/s]
    d_chamber = 0.06431280007    # [m]; Chamber Diameter
    r_chamber = d_chamber / 2       # [m]; Chamber Radius
    mdot_ox = 0.9182108849        # [kg/s]; Oxidizer Mass Flow Rate, assuming this is fixed at the desired value


    ##### USER INPUT #####
    t_input = float(input("Desired design annulus thickness (inches): "))
    OF_d = float(input("Specify the design OF: "))
    OF_lb = float(input("Specify the lowest OF allowable: "))
    OF_ub = float(input("Specify the highest OF allowable: "))


    t = t_input / 39.3700787    # Annulus Thickness in meters
    r_pintle = ( 1 / (2*t) ) *  ( (mdot_fuel_comb / ( Cd * math.pi * math.sqrt( 2 * rho * (p1 - p2) ) ) ) - t**2 )
    chamber_pintle_ratio = r_chamber / r_pintle

    r_outer_annulus = r_pintle + t

    print(f"Pintle Diameter [m]: {r_pintle*2}")
    print(f"Annulus Outer Diameter [m]: {r_outer_annulus * 2}")
    print(f"Pintle Diameter [in]: {r_pintle * 2 * 39.3701}")
    print(f"Annulus Outer Diameter [in]: {r_outer_annulus * 2 * 39.3701}")
    print(f"Chamber Pintle Diameter Ratio: {chamber_pintle_ratio}")

    x = np.linspace(0.0000254,0.0127,499)
    A = math.pi * ( (r_pintle + x)**2 - (r_pintle)**2 )
    mdot_fuel_comb_func = Cd * A * math.sqrt(2 * rho * (p1 - p2))
    OF_ratio = mdot_ox / mdot_fuel_comb_func

    ##### CALCULATE TOLERANCE #####
    t_lb = ( (mdot_ox / (math.pi * OF_lb)) * (Cd * math.sqrt(2 * rho * (p1-p2)))**-1 + r_pintle**2 )**(1/2) - r_pintle
    t_lb_plot = t_lb * 39.3701
    t_ub = ( (mdot_ox / (math.pi * OF_ub)) * (Cd * math.sqrt(2 * rho * (p1-p2)))**-1 + r_pintle**2 )**(1/2) - r_pintle
    t_ub_plot = t_ub * 39.3701
    t_d = ( (mdot_ox / (math.pi * OF_d)) * (Cd * math.sqrt(2 * rho * (p1-p2)))**-1 + r_pintle**2 )**(1/2) - r_pintle
    t_d_plot = t_d * 39.3701

    plus_tolerance = t_ub_plot - t_d_plot
    minus_tolerance = t_d_plot - t_lb_plot

    ##### PLOT #####
    x_plot = x * 39.3701
    plt.plot(x_plot, OF_ratio)
    plt.xlabel("Thickness (inches)")
    plt.ylabel("O/F ratio")
    plt.axvline(x=t_lb_plot, color='r',
                label=f"O/F = {OF_lb} at t = {t_lb_plot:.4f} in")
    plt.axvline(x=t_ub_plot, color='b',
                label=f"O/F = {OF_ub} at t = {t_ub_plot:.4f} in")
    plt.axhline(y=OF_d, color='g', linestyle='--',
                label=f"Design O/F = {OF_d}")
    plt.ylim(0, 5)
    plt.xlim(0, max(t_lb_plot, t_ub_plot) + 0.1)
    plt.text(t_d_plot + 0.03, OF_d,
             f"t = {t_d_plot:.4f} in\n"
             f"+{plus_tolerance:.4f} in\n"
             f"-{minus_tolerance:.4f} in",
             fontsize=8)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()