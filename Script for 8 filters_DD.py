# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 11:20:31 2025

This code will be implemented after separating the data set into DD and MG.
The input DD file is dd_only_Wendelsheim.xlsx 
This code also exhibits global filter (accepting values less than 80 ohm.m and 10 % stacking error), then additional 8 filter.


@author: akagupta
"""

import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

file_path = r"D:\ERT_250625_Wendelsheim\Main_data\1-Unfilter data\DD Unfilter\dd_only_Wendelsheim.xlsx"
df = pd.read_excel(file_path) # Remember the name :df

# Rename columns for convenience to plot in future.
df.columns = ['El_array', 'Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In']

# Calculate geometric factor k
B, C, D, E = df['Spa1'], df['Spa2'], df['Spa3'], df['Spa4'] # Assigning simple name for Spa1...Spa4. 
term1 = 1 / abs(B - D)
term2 = 1 / abs(C - D)
term3 = 1 / abs(B - E)
term4 = 1 / abs(C - E)
df['k'] = 2 * np.pi/(term1 - term2 - term3 + term4)


# Data Removing filters, going by Accepting Criteria means accepting the values in removing filters.
df_filtered= df[(df["dev"]< 10) & (df["Rho"]>1) & (df["Rho"]<80)] # means accepting all those values where dev < 10.

# # Saving the file
output_path = r"D:\dev_DD_10_rho_ERT_25_Wendelsheim\Fix filter\_20250625_DD_wendelsheim_filtered.xlsx"
df_filtered.to_excel(output_path, index=False)  # total 18481 data point we got after this.
print("Filtering complete. Filtered dataset shape:", df_filtered.shape)



# Start of next 8 removing filters
file_path =  r"D:\dev_DD_10_rho_ERT_25_Wendelsheim\Fix filter\_20250625_DD_wendelsheim_filtered.xlsx"
df = pd.read_excel(file_path) # Remember the name :df

# Rename columns for convenience to plot in future.
df.columns = ['El_array', 'Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In','k']

# Data Removing filters, going by Accepting Criteria means accepting the values in removing filters.
filters = {
     "f1_dev5_k5000_v025": (df["dev"] < 5) & (df["k"] < 5000) & (df["Vp"].abs() > 0.25),
     "f2_dev5_k5000_v050": (df["dev"] < 5) & (df["k"] < 5000) & (df["Vp"].abs() > 0.50),
     "f3_dev5_k10000_v025": (df["dev"] < 5) & (df["k"] < 10000) & (df["Vp"].abs() > 0.25),
     "f4_dev5_k10000_v050": (df["dev"] < 5) & (df["k"] < 10000) & (df["Vp"].abs() > 0.50),
     "f5_dev1_k5000_v025": (df["dev"] < 1) & (df["k"] < 5000) & (df["Vp"].abs() > 0.25),
     "f6_dev1_k5000_v050": (df["dev"] < 1) & (df["k"] < 5000) & (df["Vp"].abs() > 0.50),
     "f7_dev1_k10000_v025": (df["dev"] < 1) & (df["k"] < 10000) & (df["Vp"].abs() > 0.25),
     "f8_dev1_k10000_v050": (df["dev"] < 1) & (df["k"] < 10000) & (df["Vp"].abs() > 0.50),
     "f9_dev1_k8000_v025": (df["dev"] < 1) & (df["k"] < 8000) & (df["Vp"].abs() > 0.25),
     
    }

# Apply each filter and assign to a variable for cross checing in console box.
f1_dev5_k5000_v025  = df[filters["f1_dev5_k5000_v025"]]
f2_dev5_k5000_v050  = df[filters["f2_dev5_k5000_v050"]]
f3_dev5_k10000_v025 = df[filters["f3_dev5_k10000_v025"]]
f4_dev5_k10000_v050 = df[filters["f4_dev5_k10000_v050"]]
f5_dev1_k5000_v025  = df[filters["f5_dev1_k5000_v025"]]
f6_dev1_k5000_v050  = df[filters["f6_dev1_k5000_v050"]]
f7_dev1_k10000_v025 = df[filters["f7_dev1_k10000_v025"]]
f8_dev1_k10000_v050 = df[filters["f8_dev1_k10000_v050"]]
f9_dev1_k8000_v025  = df[filters["f9_dev1_k8000_v025"]]



# saving output directory.
output_dir = r"D:\dev_DD_10_rho_ERT_25_Wendelsheim\8 filters"
os.makedirs(output_dir, exist_ok=True)

# === Function: Prepare corrected Spa columns ===
def prepare_corrected_spa(df_filtered, output_file):
    """
    Keep original Spa1-4 as Spa.1-Spa.4
    Add corrected Spa1-4 (divide by 2 +1)
    Save final dataframe
    """
    df_corr = df_filtered.copy()
    
    # --- Rename original Spa1-4 ---
    df_corr.rename(columns={
        "Spa1": "Spa.1",
        "Spa2": "Spa.2",
        "Spa3": "Spa.3",
        "Spa4": "Spa.4"
    }, inplace=True)
    
    # --- Add corrected Spa1-4 ---
    df_corr["Spa1"] = (df_corr["Spa.1"] / 2) + 1
    df_corr["Spa2"] = (df_corr["Spa.2"] / 2) + 1
    df_corr["Spa3"] = (df_corr["Spa.3"] / 2) + 1
    df_corr["Spa4"] = (df_corr["Spa.4"] / 2) + 1

    # Optional: reorder columns (original 4 first, corrected next, then rest)
    cols_order = ["Spa.1", "Spa.2", "Spa.3", "Spa.4",
                  "Spa1", "Spa2", "Spa3", "Spa4"] + [c for c in df_corr.columns if c not in
                                                      ["Spa.1","Spa.2","Spa.3","Spa.4","Spa1","Spa2","Spa3","Spa4"]]
    df_corr = df_corr[cols_order]

 # --- Save to Excel ---
    df_corr.to_excel(output_file, index=False)
    print(f" Saved corrected file: {output_file} | Rows: {df_corr.shape[0]}")

# === Apply filters and save outputs ===
for name, condition in filters.items():
    df_filtered = df[condition]
    output_file = os.path.join(output_dir, f"_20250625_DD_{name}.xlsx")
    prepare_corrected_spa(df_filtered, output_file)

print(" All filters applied and Spa columns corrected successfully.")    







