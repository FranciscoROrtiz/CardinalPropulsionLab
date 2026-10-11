import numpy as np
import pandas as pd

from Mercury.define_conditions_ox import define_conditions
from define_conditions_fuel import define_conditions_fuel


# ============================================================
# HARD-CODED PRESSURE DATA
# ============================================================

# NumPy array of numbers.
# N2O tank pressure data.
# Original units: psi
# Number of data points: 380
P_N2O_tank_psi = np.array([
    453, 453, 453, 453, 453, 453, 453, 452, 452, 452,
    452, 452, 452, 452, 452, 452, 452, 452, 451, 451,
    451, 450, 450, 450, 449, 449, 448, 448, 448, 447,
    447, 447, 446, 446, 446, 445, 445, 444, 444, 444,
    443, 443, 443, 442, 442, 442, 441, 441, 440, 440,
    440, 439, 439, 439, 438, 438, 438, 437, 437, 436,
    436, 436, 435, 435, 435, 434, 434, 434, 433, 433,
    433, 432, 432, 431, 431, 431, 430, 430, 430, 429,
    429, 429, 428, 428, 428, 427, 427, 426, 426, 426,
    425, 425, 425, 424, 424, 424, 423, 423, 423, 422,
    422, 422, 421, 421, 420, 420, 420, 419, 419, 419,
    418, 418, 418, 417, 417, 417, 416, 416, 416, 415,
    415, 415, 414, 414, 414, 413, 413, 412, 412, 412,
    411, 411, 411, 410, 410, 410, 409, 409, 409, 408,
    408, 408, 407, 407, 407, 406, 406, 406, 405, 405,
    405, 404, 404, 404, 403, 403, 403, 402, 402, 402,
    401, 401, 401, 400, 400, 400, 399, 399, 399, 398,
    398, 398, 397, 397, 397, 396, 396, 396, 395, 395,
    395, 394, 394, 394, 393, 393, 393, 392, 392, 392,
    391, 391, 391, 390, 390, 390, 389, 389, 389, 388,
    388, 388, 387, 387, 387, 386, 386, 386, 385, 385,
    385, 384, 384, 384, 383, 383, 383, 382, 382, 382,
    381, 381, 381, 380, 380, 380, 379, 379, 379, 378,
    378, 378, 378, 377, 377, 377, 376, 376, 376, 375,
    375, 375, 374, 374, 374, 373, 373, 373, 372, 372,
    372, 371, 371, 371, 370, 370, 370, 369, 369, 369,
    369, 368, 368, 368, 367, 367, 367, 366, 366, 366,
    365, 365, 365, 364, 364, 364, 363, 363, 363, 363,
    362, 362, 362, 361, 361, 361, 360, 360, 360, 359,
    359, 359, 358, 358, 358, 358, 357, 357, 357, 356,
    356, 356, 355, 355, 355, 354, 354, 354, 354, 353,
    353, 353, 352, 352, 352, 351, 351, 351, 350, 350,
    350, 350, 349, 349, 349, 348, 348, 348, 347, 347,
    347, 347, 346, 346, 346, 345, 345, 345, 344, 344,
    344, 344, 343, 343, 343, 342, 342, 342, 341, 341,
    341, 341, 340, 340, 340, 339, 339, 339, 338, 338,
    338, 338, 337, 337, 337, 336, 336, 336, 335, 335,
    335, 335, 334, 334, 334, 333, 333, 333, 333, 332
])


# NumPy array of numbers.
# Chamber pressure data.
# Original units: kPa
# Number of data points: 380
Pc_raw = np.array([
    0, 221, 834, 1165, 1436, 1654, 1829, 1973, 2091, 2190,
    2232, 2233, 2203, 2161, 2138, 2145, 2171, 2179, 2178, 2173,
    2169, 2167, 2167, 2167, 2166, 2163, 2161, 2160, 2159, 2158,
    2157, 2155, 2153, 2153, 2152, 2151, 2149, 2147, 2146, 2144,
    2143, 2142, 2140, 2139, 2137, 2136, 2135, 2133, 2132, 2130,
    2129, 2128, 2127, 2126, 2125, 2123, 2121, 2120, 2119, 2117,
    2116, 2114, 2113, 2112, 2110, 2109, 2107, 2106, 2105, 2104,
    2103, 2102, 2100, 2098, 2097, 2096, 2094, 2093, 2091, 2090,
    2089, 2087, 2086, 2084, 2083, 2082, 2081, 2080, 2079, 2077,
    2075, 2074, 2073, 2072, 2070, 2068, 2067, 2066, 2064, 2063,
    2062, 2060, 2059, 2058, 2057, 2056, 2054, 2052, 2051, 2050,
    2049, 2047, 2046, 2044, 2043, 2042, 2040, 2039, 2037, 2036,
    2035, 2034, 2033, 2031, 2030, 2028, 2027, 2026, 2024, 2023,
    2021, 2020, 2019, 2017, 2016, 2015, 2013, 2012, 2011, 2010,
    2009, 2018, 2023, 2023, 2021, 2018, 2016, 2015, 2015, 2014,
    2012, 2010, 2008, 2007, 2006, 2005, 2004, 2003, 2001, 2000,
    1998, 1997, 1996, 1994, 1993, 1992, 1990, 1989, 1987, 1986,
    1985, 1983, 1982, 1981, 1980, 1979, 1977, 1976, 1974, 1973,
    1972, 1970, 1969, 1967, 1966, 1965, 1963, 1962, 1961, 1959,
    1958, 1958, 1956, 1955, 1953, 1952, 1950, 1949, 1948, 1946,
    1945, 1944, 1942, 1941, 1939, 1938, 1937, 1935, 1935, 1934,
    1932, 1931, 1929, 1928, 1927, 1925, 1924, 1922, 1921, 1920,
    1918, 1917, 1916, 1914, 1913, 1912, 1911, 1910, 1908, 1907,
    1905, 1904, 1903, 1901, 1900, 1899, 1897, 1896, 1895, 1893,
    1892, 1890, 1889, 1888, 1887, 1886, 1884, 1883, 1882, 1880,
    1879, 1878, 1876, 1875, 1874, 1872, 1871, 1870, 1868, 1867,
    1866, 1865, 1864, 1862, 1860, 1859, 1858, 1857, 1855, 1854,
    1853, 1851, 1850, 1849, 1847, 1846, 1845, 1843, 1842, 1842,
    1840, 1839, 1837, 1836, 1835, 1833, 1832, 1830, 1829, 1828,
    1826, 1825, 1824, 1822, 1821, 1820, 1819, 1818, 1816, 1822,
    1826, 1825, 1822, 1820, 1818, 1818, 1817, 1816, 1814, 1812,
    1811, 1810, 1809, 1808, 1807, 1806, 1804, 1803, 1801, 1800,
    1799, 1797, 1796, 1795, 1793, 1792, 1791, 1789, 1788, 1787,
    1786, 1785, 1784, 1782, 1780, 1779, 1778, 1777, 1775, 1774,
    1773, 1771, 1770, 1769, 1767, 1766, 1765, 1763, 1762, 1762,
    1760, 1759, 1757, 1756, 1755, 1754, 1752, 1751, 1749, 1748,
    1747, 1745, 1744, 1743, 1741, 1740, 1739, 1738, 1737, 1735,
    1734, 1733, 1732, 1730, 1729, 1727, 1726, 1725, 1724, 1722
])


# ============================================================
# VERIFY DATA LENGTH
# ============================================================

# Both arrays should contain exactly 380 values.
print("Number of N2O tank pressure points:", len(P_N2O_tank_psi))
print("Number of chamber pressure points:", len(Pc_raw))

if len(P_N2O_tank_psi) != len(Pc_raw):
    raise ValueError(
        "P_N2O_tank_psi and Pc_raw must contain the same number of data points."
    )


# ============================================================
# UNIT CONVERSIONS
# ============================================================

# NumPy array of numbers.
# Convert N2O tank pressure from psi to Pa.
P_N2O_tank = P_N2O_tank_psi * 6894.75729


# NumPy array of numbers.
# Convert chamber pressure from kPa to Pa.
Pc = Pc_raw * 1000


# ============================================================
# INJECTOR AREAS
# ============================================================

# Float.
# N2O injector area [m^2].
A_N2O = 7.330592531358677e-5


# Float.
# IPA combustion injector area [m^2].
A_IPA_comb = 3.2794353992034183e-5


# Float.
# IPA film-cooling injector area [m^2].
A_IPA_film = 8.198588498008546e-6


# ============================================================
# PRESSURE LOSSES
# ============================================================

# Float.
# N2O injector pressure loss [Pa].
# 15 psi converted to Pa.
dp_N2O = 15 * 6894.75729


# Float.
# IPA injector pressure loss [Pa].
# 45 psi converted to Pa.
dp_IPA = 45 * 6894.75729


# ============================================================
# INJECTOR INLET PRESSURES
# ============================================================

# NumPy array of numbers.
# N2O injector inlet pressure [Pa].
p1_N2O = P_N2O_tank - dp_N2O


# NumPy array of numbers.
# IPA injector inlet pressure [Pa].
p1_IPA = P_N2O_tank - dp_IPA


# ============================================================
# FLUID PROPERTIES / DISCHARGE COEFFICIENTS
# ============================================================

# Float.
# IPA density [kg/m^3].
rho_IPA = 785


# Float.
# N2O discharge coefficient [-].
Cd_N2O = 0.4


# Float.
# IPA discharge coefficient [-].
Cd_IPA = 0.4


# ============================================================
# N2O CONDITIONS
# ============================================================

# Dictionary.
# Contains the thermodynamic conditions calculated by
# define_conditions().
N2O = define_conditions(p1_N2O, Pc)


# NumPy array of numbers.
# N2O density at injector inlet [kg/m^3].
rho_N2O = N2O['density_1']


# NumPy array of numbers.
# N2O pressure drop across the injector [Pa].
delta_P_N2O = N2O['P_1'] - N2O['P_2']


# ============================================================
# IPA CONDITIONS
# ============================================================

# Dictionary.
# Contains the thermodynamic conditions calculated by
# define_conditions_fuel().
IPA = define_conditions_fuel(
    p1_IPA,
    Pc,
    rho_IPA
)


# NumPy array of numbers.
# IPA pressure drop across the injector [Pa].
delta_P_IPA = IPA['P_1'] - IPA['P_2']


# ============================================================
# MASS FLOW RATES
# ============================================================

# NumPy array of numbers.
# N2O mass flow rate [kg/s].
mdot_N2O = (
    Cd_N2O
    * A_N2O
    * np.sqrt(2 * rho_N2O * delta_P_N2O)
)


# NumPy array of numbers.
# IPA combustion mass flow rate [kg/s].
mdot_IPA_comb = (
    Cd_IPA
    * A_IPA_comb
    * np.sqrt(2 * rho_IPA * delta_P_IPA)
)


# NumPy array of numbers.
# IPA film-cooling mass flow rate [kg/s].
mdot_IPA_film = (
    Cd_IPA
    * A_IPA_film
    * np.sqrt(2 * rho_IPA * delta_P_IPA)
)


# NumPy array of numbers.
# Total IPA mass flow rate [kg/s].
mdot_IPA_total = mdot_IPA_comb + mdot_IPA_film


# ============================================================
# O/F RATIO AND FILM FRACTION
# ============================================================

# NumPy array of numbers.
# Oxidizer-to-fuel ratio.
# Film-cooling IPA is excluded from this O/F calculation.
O_F = mdot_N2O / mdot_IPA_comb


# NumPy array of numbers.
# Fraction of total IPA flow going to film cooling [-].
film_fraction = mdot_IPA_film / mdot_IPA_total


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n==============================================")
print("DATA")
print("==============================================")

print("\nP_N2O_tank_psi:")
print(P_N2O_tank_psi)

print("\nPc_raw [kPa]:")
print(Pc_raw)


print("\n==============================================")
print("N2O RESULTS")
print("==============================================")

print("\nrho_N2O [kg/m^3]:")
print(rho_N2O)

print("\ndelta_P_N2O [Pa]:")
print(delta_P_N2O)

print("\nmdot_N2O [kg/s]:")
print(mdot_N2O)


print("\n==============================================")
print("IPA RESULTS")
print("==============================================")

print("\ndelta_P_IPA [Pa]:")
print(delta_P_IPA)

print("\nmdot_IPA_comb [kg/s]:")
print(mdot_IPA_comb)

print("\nmdot_IPA_film [kg/s]:")
print(mdot_IPA_film)

print("\nmdot_IPA_total [kg/s]:")
print(mdot_IPA_total)


print("\n==============================================")
print("MIXTURE RESULTS")
print("==============================================")

print("\nO/F:")
print(O_F)

print("\nFilm fraction:")
print(film_fraction)


# ============================================================
# SAVE RESULTS TO CSV
# ============================================================

# Dictionary.
# Contains all input and calculated data.
results = {
    "P_N2O_tank_psi": P_N2O_tank_psi,
    "P_N2O_tank_Pa": P_N2O_tank,
    "Pc_raw_kPa": Pc_raw,
    "Pc_Pa": Pc,
    "rho_N2O": rho_N2O,
    "delta_P_N2O": delta_P_N2O,
    "mdot_N2O": mdot_N2O,
    "delta_P_IPA": delta_P_IPA,
    "mdot_IPA_comb": mdot_IPA_comb,
    "mdot_IPA_film": mdot_IPA_film,
    "mdot_IPA_total": mdot_IPA_total,
    "O_F": O_F,
    "film_fraction": film_fraction
}


# Pandas DataFrame.
# Converts the results dictionary into a table.
results_df = pd.DataFrame(results)


# Save the results to a CSV file.
results_df.to_csv(
    "injector_flow_results.csv",
    index=False
)


print("\n==============================================")
print("CSV OUTPUT")
print("==============================================")

print("\nResults saved to:")
print("injector_flow_results.csv")

print("\nNumber of output rows:")
print(len(results_df))