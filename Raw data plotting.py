# -*- coding: utf-8 -*-
"""
Created on Wed Oct  1 15:04:25 2025

@author: akagupta
this script is for plotting raw data and dev10 and rho 80 data.
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.colors as colors
from matplotlib.colors import SymLogNorm
from matplotlib import colors


file_path = r"D:\ERT_1_Wendelsheim\ERT_250625_Wendelsheim\Main_data\1-Unfilter data\1-Main\20250625_wendelshein_promys.xlsx"
df = pd.read_excel(file_path) # Remember the name :df

# Rename columns for convenience to plot in future.
df.columns = ['El_array', 'Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In']

df['method'] = '' # Creating a new column called,'method' to assign which one is DD and MG.
# df.loc[row_indexer, column_indexer] This is how this function works in pandas and since it is a list so [] this bracket
df.loc[1:6715, 'method'] = 'DD'     # Row 2 to 6716, python use zero based indexing
df.loc[6716:11035, 'method'] = 'MG' # Row 6717 to 11036
df.loc[11036:15829, 'method'] = 'DD'# Row 11037 to 15830
df.loc[15830:, 'method'] = 'MG'     # Row 15831 to end

# Calculate geometric factor k (same for both methods)
B, C, D, E = df['Spa1'], df['Spa2'], df['Spa3'], df['Spa4'] # Assigning simple name for Spa1...Spa4. 
term1 = 1 / (B - D)
term2 = 1 / (B - E)
term3 = 1 / (C - D)
term4 = 1 / (C - E)
df['k'] = 2 * np.pi/(term1 - term2 - term3 + term4)
k= df['k'] 
#df['k'] = df['k'].abs()  # Always take positive value

# Calculate Xapp and Zapp based on method
Xapp_DD = (B + D) / 2
Zapp_DD = np.abs((E - C) / 2) # In Multigradient,E<C
Xapp_MG = (D + C) / 2
# np.minimum(a, b), returns the minimum value
Zapp_MG = np.minimum(Xapp_MG - B, E - Xapp_MG)  # Use actual minimum without abs

# np.where(condition, value_if_true, value_if_false)
# df['method'] == 'DD', this is a boolean series, its checking each row of the column 'method', like a condition where
# it calculates Xapp and if it is DD wala k then returning the value into Xapp_DD and if it is MG wala k then returning 
# the value into Xapp_MG. Same logic applies for Zapp.
df['Xapp'] = np.where(df['method'] == 'DD', Xapp_DD, Xapp_MG)
df['Zapp'] = np.where(df['method'] == 'DD', Zapp_DD, Zapp_MG)

# Units dictionary
units = {
    'Rho': 'Ω·m',       # Ohm meter
    'Vp': 'mV',         # Mili-volt
    'In': 'mA',         # Mili-ampere
    'dev': '%'          # Percent deviation (Stacked error)
}

#------------------------------------------------------------------------------



# This section is plotting all the raw data into 2 by 2 panel.
# will be done on raw file



#------------------------------------------------------------------------------ 

# Set global style for consistency
plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# Create 2x2 figure
fig, axs = plt.subplots(2, 2, figsize=(12,10), dpi=400)
plt.subplots_adjust(left=0.09, right=0.85, hspace=0.35, wspace=0.35)  # <-- added to increase space between top and bottom row

# ---------------- (a) Apparent Resistivity with outliers ----------------
rho = df['Rho']
normal_rho = rho[(rho >= 0)]
outlier_rho = rho[(rho < 0)]

axs[0,0].scatter(normal_rho.index + 1, normal_rho, s=10, color='red', alpha=0.6, edgecolors='none')
axs[0,0].scatter(outlier_rho.index + 1, outlier_rho, s=10, color='red', alpha=0.6, edgecolors='none')
axs[0,0].set_xlabel("Number of measurement")
axs[0,0].set_ylabel(r"Apparent resistivity (Ωm)")
axs[0,0].set_xlim(0,20000)
axs[0,0].set_ylim(-400,500)
axs[0,0].grid(True, linestyle="--", alpha=1)
#axs[0,0].text(0.02, 0.9, "(a)", transform=axs[0,0].transAxes, fontsize=14, fontweight="bold")

# ---------------- (b) Voltage ----------------
axs[0,1].scatter(range(1, len(df['Vp']) + 1), df['Vp'],
                 s=10, color='red', alpha=0.6, edgecolors='none')
axs[0,1].set_xlabel("Number of measurement")
axs[0,1].set_ylabel("Voltage (mV)")
axs[0,1].set_xlim(0,20000)
axs[0,1].set_ylim(-400,400)
axs[0,1].grid(True, linestyle="--", alpha=1)
#axs[0,1].text(0.02, 0.9, "(b)", transform=axs[0,1].transAxes, fontsize=14, fontweight="bold")

# ---------------- (c) Current ----------------
axs[1,0].scatter(range(1, len(df['In']) + 1), df['In'],
                 s=10, color='red', alpha=0.6, edgecolors='none')
axs[1,0].set_xlabel("Number of measurement")
axs[1,0].set_ylabel("Current (mA)")
axs[1,0].set_xlim(0,20000)
axs[1,0].grid(True, linestyle="--", alpha=1)
#axs[1,0].text(0.02, 0.9, "(c)", transform=axs[1,0].transAxes, fontsize=14, fontweight="bold")

# ---------------- (d) Stacked Error with outliers ----------------
dev = df['dev']
normal_dev = dev[dev <= 10]
outlier_dev = dev[dev > 10]

axs[1,1].scatter(normal_dev.index + 1, normal_dev, s=10, color='red', alpha=0.6, edgecolors='none')
axs[1,1].scatter(outlier_dev.index + 1, outlier_dev, s=10, color='red', alpha=0.6, edgecolors='none')
axs[1,1].set_xlabel("Number of measurement")
axs[1,1].set_ylabel("Stacking error (%)")
axs[1,1].set_xlim(0,20000)
axs[1,1].set_ylim(0,500)
axs[1,1].grid(True, linestyle="--", alpha=1)
#axs[1,1].text(0.02, 0.9, "(d)", transform=axs[1,1].transAxes, fontsize=14, fontweight="bold")

# Add legends for outliers only where used
axs[0,0].legend()
axs[1,1].legend()

fig.text(0.06, 0.90, "(a)", fontsize=14, fontweight="bold")
fig.text(0.52, 0.90, "(b)", fontsize=14, fontweight="bold")
fig.text(0.06, 0.46, "(c)", fontsize=14, fontweight="bold")
fig.text(0.52, 0.46, "(d)", fontsize=14, fontweight="bold")
  
plt.show()

#------------------------------------------------------------------------------




# This section is plotting rho and dev into 1 by 2 panel.
# will be done on raw file



#------------------------------------------------------------------------------



# Set global style
plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 16,
    "axes.titlesize": 14,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13
})

# Create 1x2 figure for side-by-side
fig, axs = plt.subplots(1, 2, figsize=(12,6), dpi=400)  # 1 row, 2 columns

# ---------------- (a) Apparent Resistivity with outliers ----------------
rho = df['Rho']
normal_rho = rho[(rho >= 1) & (rho <= 80)]

axs[0].scatter(normal_rho.index + 1, normal_rho, s=10, color='red', alpha=0.6, edgecolors='none')
axs[0].set_xlabel("(Number of measurement)")
axs[0].set_ylabel(r"[$\rho_{\mathrm{app}}$] (Ω·m)")
axs[0].set_xlim(0,20000)
axs[0].set_ylim(0,90)
axs[0].grid(True, linestyle="--", alpha=1)
axs[0].text(0.02, 0.9, "(a)", transform=axs[0].transAxes, fontsize=14, fontweight="bold")

# ---------------- (d) Stacked Error with outliers ----------------
dev = df['dev']
normal_dev = dev[dev <= 10]

axs[1].scatter(normal_dev.index + 1, normal_dev, s=10, color='red', alpha=0.6, edgecolors='none')
axs[1].set_xlabel("(Number of measurement)")
axs[1].set_ylabel("[dev] (%)")
axs[1].set_xlim(0,20000)
axs[1].set_ylim(-2,12)
axs[1].grid(True, linestyle="--", alpha=1)
axs[1].text(0.02, 0.9, "(b)", transform=axs[1].transAxes, fontsize=14, fontweight="bold")

# Adjust layout

plt.show()


#------------------------------------------------------------------------------




# This section is plotting the L-curve into 1 by 2 panel.
# Just dev and K




#------------------------------------------------------------------------------


# ---------------- GLOBAL STYLE ----------------
plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# ---------------- DATA ----------------
dev = [1, 3, 5, 7, 10]
rms_dev = [8.17, 8, 7.86, 8.38, 8.63]
optimal_dev = 5
optimal_rms_dev = 7.86

k = [5000, 8000, 10000, 13000]
rms_k = [7.95, 7.88, 7.83, 7.88]
optimal_k = 10000
optimal_rms_k = 7.83

# ---------------- FIGURE ----------------
fig, axs = plt.subplots(1, 2, figsize=(12,6), dpi=400)

plt.subplots_adjust(left=0.09, right=0.95, hspace=0.3, wspace=0.3)

# ---------------- (dev vs RRMS) ----------------
axs[0].plot(dev, rms_dev,
            marker='o', linestyle='-',
            color='tab:red', linewidth=2)

axs[0].scatter(optimal_dev, optimal_rms_dev,
               color='tab:blue', s=150, zorder=5,
               label='Optimal threshold')

axs[0].set_xlabel('Stacking error (%)')
axs[0].set_ylabel('RRMS (%)')
axs[0].grid(True)
axs[0].legend(fontsize=12)

# ---------------- (k vs RRMS) ----------------
axs[1].plot(k, rms_k,
            marker='s', linestyle='-',
            color='tab:red', linewidth=2)

axs[1].scatter(optimal_k, optimal_rms_k,
               color='tab:blue', s=150, zorder=5,
               label='Optimal threshold')

axs[1].set_xlabel('Geometric factor')
axs[1].set_ylabel('RRMS (%)')
axs[1].grid(True)
axs[1].legend(fontsize=12)

# ---------------- SHOW ----------------
plt.show()



#------------------------------------------------------------------------------




# This section is plotting the L-curve into 1 by 3 panel.
# Including V too




#------------------------------------------------------------------------------

# --- Set global style ---
plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# --- Data for dev vs RRMS ---
dev = [1, 3, 5, 7, 10]
rms_dev = [8.17, 8, 7.86, 8.38, 8.63]
optimal_dev = 5
optimal_rms_dev = 7.86

# --- Data for k vs RRMS ---
k = [5000, 8000, 10000, 13000]
rms_k = [7.95, 7.88, 7.83, 7.88]
optimal_k = 10000
optimal_rms_k = 7.83

# --- Data for V vs RRMS ---
V = [ 0.25, 0.50, 0.75]
rms_V = [5.81, 4.84, 3.38]
optimal_V = 0.75
optimal_rms_V = 3.38

# --- Create 1x3 figure ---
fig, axs = plt.subplots(1, 3, figsize=(18, 6), dpi=400)
fig.subplots_adjust(hspace=0.3, wspace=0.3)

# --- Plot 1: dev vs RRMS ---
axs[0].plot(dev, rms_dev, marker='o', linestyle='-', color='tab:red', linewidth=2)
axs[0].scatter(optimal_dev, optimal_rms_dev, color='tab:blue', s=150, zorder=5, label='Optimal threshold')
axs[0].set_xlabel('Stacking error (%)', fontsize=14)
axs[0].set_ylabel('RRMS (%)', fontsize=14)
axs[0].grid(True)
axs[0].legend(fontsize=12)
axs[0].text(0.02, 1.04, "(a)", transform=axs[0].transAxes, fontsize=14, fontweight="bold")

# --- Plot 2: k vs RRMS ---
axs[1].plot(k, rms_k, marker='s', linestyle='-', color='tab:red', linewidth=2)
axs[1].scatter(optimal_k, optimal_rms_k, color='tab:blue', s=150, zorder=5, label='Optimal threshold')
axs[1].set_xlabel('Geometric factor', fontsize=14)
axs[1].set_ylabel('RRMS (%)', fontsize=14)
axs[1].grid(True)
axs[1].legend(fontsize=12)
axs[1].text(0.02, 1.04, "(b)", transform=axs[1].transAxes, fontsize=14, fontweight="bold")

# --- Plot 3: V vs RRMS ---
axs[2].plot(V, rms_V, marker='s', linestyle='-', color='tab:red', linewidth=2)
axs[2].scatter(optimal_V, optimal_rms_V, color='tab:blue', s=150, zorder=5, label='Optimal threshold')
axs[2].set_xlabel('Voltage (mV)', fontsize=14)
axs[2].set_ylabel('RRMS (%)', fontsize=14)
axs[2].grid(True)
axs[2].legend(fontsize=12)
axs[2].text(0.02, 1.04, "(c)", transform=axs[2].transAxes, fontsize=14, fontweight="bold")

# --- Show figure ---
plt.show()











