# filename: Venturi_Calc.py
# created: 05.09.26
# last edited: 05.09.26
# authors: Francisco Ortiz, Diego Ortiz
# purpose: plot test data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import CoolProp.CoolProp as CP
import os
import glob
from scipy.signal import savgol_filter

from scipy import signal


def mdot_venturi(A_upstream, A_throat, dP, Cd, fluid, P_upstream=0):
    if fluid == 'N2O' or fluid == 'CO2'
        rho = CP.PropsSI('D', 'P', P_upstream, 'Q', 0, fluid)
    elif fluid == 'H2O':
        rho = 1000
    else:
        rho = 785

    P_rho_term = np.sqrt(2*rho*dP)
    area_term = 1/(1-(A_throat/A_upstream)**2)**0.5
    mdot = (A_throat/area_term) * P_rho_term * Cd
    return mdot
