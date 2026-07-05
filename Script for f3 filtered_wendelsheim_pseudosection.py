# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 18:27:50 2026

This script provides the pseudosection of the f3 [f3_dev5_k10000_v025] file cobined DD+MG.
For making psedosection of f3 files, always remember, do not calculate the k, its already calculated,
this is why all the segment for calculating k is commented. 

@author: akagupta

"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import matplotlib.colors as colors
from matplotlib.colors import SymLogNorm
from matplotlib import colors
import matplotlib.gridspec as gridspec

file_path = r"D:\ERT_1_Wendelsheim\dev_10 rho_ERT_25_Wendelsheim\8 filters\_20250625_f3_dev5_k10000_v025.xlsx"
df = pd.read_excel(file_path) # Remember the name :df

# # Rename columns for convenience to plot in future.
df.columns = ['El_array','Spa_x','Spa_y','Spa_z','Spa_a', 'Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In','k']

# df['method'] = '' This will be useful when you take the input from constant filter file. 
# df.loc[1:6476, 'method'] = 'DD'     # Row 2 to 6477, python use zero based indexing
# df.loc[6477:10765, 'method'] = 'MG' # Row 6478 to 10766
# df.loc[10766:15360, 'method'] = 'DD'# Row 10767 to 15361
# df.loc[15361:, 'method'] = 'MG'     # Row 15362 to end


# df['method'] = '' # Creating a new column called,'method' to assign which one is DD and MG.
# # df.loc[row_indexer, column_indexer] This is how this function works in pandas and since it is a list so [] this bracket
# df.loc[1:6715, 'method'] = 'DD'     # Row 2 to 6716, python use zero based indexing
# df.loc[6716:11035, 'method'] = 'MG' # Row 6717 to 11036
# df.loc[11036:15829, 'method'] = 'DD'# Row 11037 to 15830
# df.loc[15830:, 'method'] = 'MG'     # Row 15831 to end

df['method'] = '' # Creating a new column called,'method' to assign which one is DD and MG.
# df.loc[1:5534, 'method'] = 'DD'     # Row 2 to 6716, python use zero based indexing
# df.loc[5535:9710, 'method'] = 'MG' # Row 6717 to 11036
# df.loc[9711:13498, 'method'] = 'DD'# Row 11037 to 15830
# df.loc[13499:, 'method'] = 'MG'     # Row 15831 to end




# Calculate geometric factor k 
B, C, D, E = df['Spa_x'], df['Spa_y'], df['Spa_z'], df['Spa_a'] # Assigning simple name for Spa1...Spa4. 
# term1 = 1 / (B - D)
# term2 = 1 / (B - E)
# term3 = 1 / (C - D)
# term4 = 1 / (C - E)
# df['k'] = 2 * np.pi/(term1 - term2 - term3 + term4)
# k= df['k'] 

# Calculate Xapp and Zapp based on method
Xapp_DD = (B + D) / 2
Zapp_DD = np.abs((E - C) / 2) # In Multigradient,E<C
Xapp_MG = (D + C) / 2
# np.minimum(a, b), returns the minimum value
Zapp_MG = np.minimum(Xapp_MG - B, E - Xapp_MG)

df['Xapp'] = np.where(df['method'] == 'DD', Xapp_DD, Xapp_MG)
df['Zapp'] = np.where(df['method'] == 'DD', Zapp_DD, Zapp_MG)

df['Zapp'] = df['Zapp'].abs()
df = df[df['Zapp'] <= 60] 



# ---------------- GLOBAL STYLE ----------------
plt.rcParams.update({
    "font.size": 14,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# ---------------- FIGURE ----------------
fig, axs = plt.subplots(2, 2, figsize=(12,11), dpi=400)

plt.subplots_adjust(left=0.09, right=0.85, hspace=0.20, wspace=0.25)

# ---------------- (a) RHO ----------------
sc1 = axs[0,0].scatter(df['Xapp'], df['Zapp'],
                       c=np.abs(df['Rho']), s=20, cmap='jet',
                       norm=colors.LogNorm(vmin=1, vmax=1000),
                       edgecolors='none')

axs[0,0].set_xlabel(r"Distance (m)")
axs[0,0].set_ylabel(r"Depth (m)")
axs[0,0].set_xlim(0,360)
axs[0,0].set_ylim(0,60)
axs[0,0].invert_yaxis()
axs[0,0].grid(True, linestyle="--", alpha=0.4)

cbar1 = plt.colorbar(sc1, ax=axs[0,0], orientation='horizontal', pad=0.20)
cbar1.set_label(r"Apparent resistivity (Ωm)")


# ---------------- (b) K ----------------
sc2 = axs[0,1].scatter(df['Xapp'], df['Zapp'],
                       c=df['k'], s=20, cmap='jet',
                       norm=colors.TwoSlopeNorm(vmin=-15000, vcenter=0, vmax=15000),
                       edgecolors='none')

axs[0,1].set_xlabel(r"Distance (m)")
axs[0,1].set_ylabel(r"Depth (m)")
axs[0,1].set_xlim(0,360)
axs[0,1].set_ylim(0,60)
axs[0,1].invert_yaxis()
axs[0,1].grid(True, linestyle="--", alpha=0.4)

cbar2 = plt.colorbar(sc2, ax=axs[0,1], orientation='horizontal', pad=0.20)
cbar2.set_label("Geometric factor")


# ---------------- (c) DEV ----------------
sc3 = axs[1,0].scatter(df['Xapp'], df['Zapp'],
                       c=df['dev'], s=20, cmap='jet',
                       norm=colors.LogNorm(vmin=1, vmax=1000),
                       edgecolors='none')

axs[1,0].set_xlabel(r"Distance (m)")
axs[1,0].set_ylabel(r"Depth (m)")
axs[1,0].set_xlim(0,360)
axs[1,0].set_ylim(0,60)
axs[1,0].invert_yaxis()
axs[1,0].grid(True, linestyle="--", alpha=0.4)

cbar3 = plt.colorbar(sc3, ax=axs[1,0], orientation='horizontal', pad=0.20)
cbar3.set_label("Stacking error (%)")


# ---------------- (d) VP ----------------
sc4 = axs[1,1].scatter(df['Xapp'], df['Zapp'],
                       c=np.abs(df['Vp']), s=20, cmap='jet',
                       #norm=SymLogNorm(linthresh=1, vmin=-1000, vmax=1000)
                       norm=colors.LogNorm(vmin=1, vmax=1000),
                       edgecolors='none')

axs[1,1].set_xlabel(r"Distance (m)")
axs[1,1].set_ylabel(r"Depth (m)")
axs[1,1].set_xlim(0,360)
axs[1,1].set_ylim(0,60)
axs[1,1].invert_yaxis()
axs[1,1].grid(True, linestyle="--", alpha=0.4)

cbar4 = plt.colorbar(sc4, ax=axs[1,1], orientation='horizontal', pad=0.20)
cbar4.set_label("Voltage (mV)")


# ---------------- PANEL LABELS (OUTSIDE) ----------------
fig.text(0.06, 0.90, "(a)", fontsize=14, fontweight="bold")
fig.text(0.52, 0.90, "(b)", fontsize=14, fontweight="bold")
fig.text(0.06, 0.49, "(c)", fontsize=14, fontweight="bold")
fig.text(0.52, 0.49, "(d)", fontsize=14, fontweight="bold")

plt.show()