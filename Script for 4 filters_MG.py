# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 17:23:34 2025

This code will be implemented after separating the data set into DD and MG.
The input MG file is dd_only_Wendelsheim.xlsx 
This code also exhibits global filter (accepting values less than 80 ohm.m and 10 % stacking error), then additional 8 filter.

@author: akagupta
"""


import pandas as pd
import seaborn as sns
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

file_path = r"D:\ERT_250625_Wendelsheim\Main_data\1-Unfilter data\MG Unfilter\mg_only_Wendelsheim.xlsx"
df = pd.read_excel(file_path)  # Load data

# Rename columns for convenience
df.columns = ['El_array', 'Spa1', 'Spa2', 'Spa3', 'Spa4', 
              'Rho', 'dev', 'M', 'Sp', 'Vp', 'In']

# Calculate geometric factor k
A, B, M, N = df['Spa1'], df['Spa2'], df['Spa3'], df['Spa4']
term1 = 1 / abs(A - M)
term2 = 1 / abs(B - M)
term3 = 1 / abs(A - N)
term4 = 1 / abs(B - N)
df['k'] = 2 * np.pi / (term1 - term2 - term3 + term4)

# Data removing filters: Rho between 1 and 80, dev < 10
df_filtered = df[(df["Rho"] > 0) & (df["Rho"] < 80) & (df["dev"] < 10)]

# Save filtered DataFrame to Excel
output_path = r"D:\ERT_250625_Wendelsheim\Main_data\1-Unfilter data\MG Unfilter\mg_only_Wendelsheim.xlsx"
df_filtered.to_excel(output_path, index=False)

print("Filtering complete. Filtered dataset shape:", df_filtered.shape)


# Now, applying 4 filters..
filters = {
     "f1_dev10_k_0_v0": (df["dev"] < 10) & (df["k"] > 0) & (df["Vp"].abs() > 0),
     "f2_dev10_k_0_v20": (df["dev"] < 10) & (df["k"] > 0) & (df["Vp"].abs() > 20),
     "f3_dev10_k_0_v15": (df["dev"] < 10) & (df["k"] > 0) & (df["Vp"].abs() > 15),
    }

# --- Apply each filter and assign to variables for cross-checking ---
f1_dev10_k_0_v0  = df[filters["f1_dev10_k_0_v0"]]
f2_dev10_k_0_v20 = df[filters["f2_dev10_k_0_v20"]]
f3_dev10_k_0_v15 = df[filters["f3_dev10_k_0_v15"]]

 
# saving output directory.
output_dir = r"D:\MG_removal_vertical\Task_02_20 percent\3 filters"
os.makedirs(output_dir, exist_ok=True)

# === Function: Prepare corrected Spa columns ===
def prepare_corrected_spa(df_filtered, output_file):
    """
    Keep original Spa1-4 as Spa.1-Spa.4
    Add corrected Spa1-4 (divide by 2 +1)
    Save final dataframe, its gonna be fun yeah..
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
    output_file = os.path.join(output_dir, f"20250625_MG_{name}.xlsx")
    prepare_corrected_spa(df_filtered, output_file)

print(" All filters applied and Spa columns corrected successfully.")    
