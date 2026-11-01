import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import brentq


from PSD_calc import PSD_calc
from lowpass_filter import lowpass_filter
from fs_calc import fs_calc
from parquet_process import parquet_process

from calc_Cf import calc_Cf
from calc_Cf_ideal import calc_Cf_ideal
from calc_Isp import calc_Isp
from calc_OF import calc_OF
from calc_adiabatic_flame_temp import calc_adiabatic_flame_temp
from calc_cstar import calc_cstar
from calc_cstar_ideal import calc_cstar_ideal
from calc_eta_Cf import calc_eta_Cf
from calc_eta_cstar import calc_eta_cstar
from calc_mdot_SPI import calc_mdot_SPI
from calc_mdot_load_cell import calc_mdot_load_cell
from calc_pressure_drop import calc_pressure_drop
from define_conditions_ox import define_conditions_ox
from rocketCEA_run import rocketCEA_run
from ffill_to_interpolate import ffill_to_interpolate
from ffill_to_interpolate_all_sensor_type import ffill_to_interpolate_all_sensor_type

from area_mach_residual import area_mach_residual

"""
INPUTS vvv
"""
parquet_file = r"C:\Users\franc\Downloads\CPL - Post Processing Scripts\All Coldflow and Hotfire Data\BG_HF_2.parquet"
Input_file = {  'fs_PT': 10,
                'fs_LC': 2,
                'fs_TC': 1,
                'Cd_ox': 0.68,
                'A_ox': 0.00000281070638655,
                'Cd_fuel': 0.7,
                'A_fuel': 0.00000243219589967,
                'A_throat': 0.000153279012427,
                'epsilon_e': 2.67768595041,
                'fluid_fuel': 'IPA',
                'fluid_ox': 'N2O',
                'P_injector_upstream_ox': "PT_ox_tank_filtered",
                'P_ox_tank': 'PT_ox_tank_filtered',
                'Pc': "PT_chamber_filtered",
                'P_injector_upstream_fuel': "PT_fuel_tank_filtered",
                'Thrust': "LC_TOTAL_filtered",
                'Cd_VT_ox': 0,
                'Cd_VT_fuel': 0,
                'A_VT_upstream_ox': 0,
                'A_VT_throat_ox': 0,
                'A_VT_upstream_fuel': 0,
                'A_VT_throat_fuel': 0}

Pc = Input_file['Pc']
Thrust = Input_file['Thrust']
P_ox_tank = Input_file['P_ox_tank']
P_injector_upstream_ox = Input_file['P_injector_upstream_ox']
P_injector_upstream_fuel = Input_file['P_injector_upstream_fuel']

"""
INPUTS ^^^
"""



# CONSTANTS
# Ambient Pressure [Pa]
Pa = 101325
# Unit conversions
psi_to_pa = 6894.76
lb_to_N = 4.44822
lbm_to_kg = 0.453592

# Convert parquet file -> Panda data fram & convert timestamp -> time_sec
df = parquet_process(parquet_file)

# Filter only the desired traces (time, sensors, valves)
df = df.loc[:, df.columns.str.startswith(("time", "PT", "TC", "LC", "DP", "MBV", "SV"))]

# Convert any forward filled upsampled data to upsampled interpolated data
ffill_to_interpolate_all_sensor_type(df, 'LC', Input_file['fs_LC'], Input_file['fs_PT'])
ffill_to_interpolate_all_sensor_type(df, 'TC', Input_file['fs_TC'], Input_file['fs_PT'])

# Apply lowpass digital filters on data
for col in df.columns:
    if col.startswith('PT'):
        df[col + '_filtered'] = lowpass_filter(df[col].to_numpy(), Input_file['fs_PT'], fc=Input_file['fs_PT']/10)

for col in df.columns:
    if col.startswith('DP'):
        df[col + '_filtered'] = lowpass_filter(df[col].to_numpy(), Input_file['fs_PT'], fc=Input_file['fs_PT']/10)

for col in df.columns:
    if col.startswith('LC'):
        df[col + '_filtered'] = lowpass_filter(df[col].to_numpy(), Input_file['fs_PT'], fc=Input_file['fs_LC']/5)

for col in df.columns:
    if col.startswith('TC'):
        df[col + '_filtered'] = lowpass_filter(df[col].to_numpy(), Input_file['fs_PT'], fc=Input_file['fs_TC']/2.2)

# Calculate mdot from Load Cells
# Calculate Cd
for col in df.columns:
    if col.startswith('LC') and col.endswith('tank'):
        fluid = col.removeprefix("LC_").removesuffix("_tank")
        mdot_LC = np.array(calc_mdot_load_cell(df[col].to_numpy()*lbm_to_kg, 1/fs_calc(df)))
        df['mdot_' + fluid + '_LC'] = mdot_LC
        df['Cd_' + fluid] = mdot_LC / np.array(calc_mdot_SPI(df[P_injector_upstream_ox].to_numpy()*psi_to_pa+Pa, df[Pc].to_numpy()*psi_to_pa+Pa, Input_file['A_' + fluid], Input_file['fluid_' + fluid], 1))

# Calculate mdot from Venturis
for col in df.columns:
    if col.startswith('DP'):
        fluid = col.split('_')[-1]
        df['mdot_' + fluid + '_VT'] = mdot_venturi(Input_file["A_VT_upstream_" + fluid], Input_file['A_VT_throat_' + fluid], df[col].to_numpy(), Input_file['Cd_VT_' + fluid], Input_file['fluid_' + fluid], df[P_ox_tank].to_numpy())

# Calculate mdot from SPI
mdot_ox_SPI = calc_mdot_SPI(df[Input_file['P_injector_upstream_ox']].to_numpy()*psi_to_pa+Pa, df[Input_file['Pc']].to_numpy()*psi_to_pa+Pa, Input_file['A_ox'], Input_file['fluid_ox'], Input_file['Cd_ox'])
mdot_fuel_SPI = calc_mdot_SPI(df[Input_file['P_injector_upstream_fuel']].to_numpy()*psi_to_pa+Pa, df[Input_file['Pc']].to_numpy()*psi_to_pa+Pa, Input_file['A_fuel'], Input_file['fluid_fuel'], Input_file['Cd_fuel'])

# Calculate OF
OF = calc_OF(mdot_ox_SPI, mdot_fuel_SPI)

# Calculate empirical Thrust Coefficient
Cf = calc_Cf(df[Input_file['Thrust']].to_numpy()*lb_to_N, df[Input_file['Pc']].to_numpy()*psi_to_pa+Pa, Input_file['A_throat'])

# Calculate empirical c*
cstar = calc_cstar((df[Input_file['Pc']].to_numpy()*psi_to_pa)+Pa, Input_file['A_throat'], mdot_ox_SPI+mdot_fuel_SPI)

# Calculate Isp
Isp = calc_Isp(df[Thrust].to_numpy()*lb_to_N, mdot_ox_SPI+mdot_fuel_SPI)

# Calculate ideal Cf and c*
Cf_ideal = np.zeros(len(OF))
cstar_ideal = np.zeros(len(OF))
for i in range(len(OF)):
    # print(i)
    combustion_gas_properties = rocketCEA_run(df[Pc].to_numpy()[i]*psi_to_pa+Pa, OF[i])
    gamma = combustion_gas_properties['gamma']
    Ma = brentq(area_mach_residual, 1.0, 20.0, args=(Input_file['epsilon_e'], gamma))
    P_ratio = (1+(((gamma-1)/2)*Ma))**(gamma/(gamma-1))
    Pe = (df[Pc].to_numpy()[i]*psi_to_pa+Pa)/P_ratio
    Cf_ideal[i] = calc_Cf_ideal(combustion_gas_properties['gamma'], Pe, df[Pc].to_numpy()[i]*psi_to_pa+Pa, Input_file['epsilon_e'], Pa)
    cstar_ideal[i] = calc_cstar_ideal(combustion_gas_properties['R'], combustion_gas_properties['Tc'], combustion_gas_properties['gamma'])

# Calculate efficiencies
eta_Cf = calc_eta_Cf(Cf, Cf_ideal)
eta_cstar = calc_eta_cstar(cstar, cstar_ideal)

# Save calcaulations to df
df['mdot_ox_SPI'] = mdot_ox_SPI
df['mdot_fuel_SPI'] = mdot_fuel_SPI
df['OF'] = OF
df['Cf'] = Cf
df['cstar'] = cstar
df['Isp'] = Isp
df['Cf_ideal'] = Cf_ideal
df['cstar_ideal'] = cstar_ideal
df['eta_Cf'] = eta_Cf
df['eta_cstar'] = eta_cstar

# Save processed df to computer
df.to_parquet("the_big_boi3.parquet", index=False)














# df = df.loc[:, df.columns.str.startswith(("time", "PT", "TC", "LC"))]

# for col in df.columns:
#     print(col)
