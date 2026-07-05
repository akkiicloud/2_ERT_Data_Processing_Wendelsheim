# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:05:04 2026
This script is useful to apply the filter and then change the colu,mn directly so that we dont have to do it manunallly for pygimli.
In pygimli, the spacing needs to be start from 1 2 3 4 not from 2 4 6 8 
@author: akagupta
"""

import pandas as pd
import numpy as np
import os

# === Load data ===
file_path = r"D:\Corner analysis_DD+MG\dev_file\20250625_wendelshein_promys.xlsx"
df = pd.read_excel(file_path)

# Rename columns
df.columns = ['El_array', 'Spa1', 'Spa2', 'Spa3', 'Spa4', 'Rho', 'dev', 'M', 'Sp', 'Vp', 'In']

# === Compute geometric factor k ===
B, C, D, E = df['Spa1'], df['Spa2'], df['Spa3'], df['Spa4']
term1 = 1 / abs(B - D)
term2 = 1 / abs(C - D)
term3 = 1 / abs(B - E)
term4 = 1 / abs(C - E)
df['k'] = 2 * np.pi / (term1 - term2 - term3 + term4)

# === Function: Apply Spa correction and save ===
def prepare_corrected_spa(df_filtered, output_file):
    df_corr = df_filtered.copy()
    
    # Rename original Spa columns
    df_corr.rename(columns={
        "Spa1": "Spa.1",
        "Spa2": "Spa.2",
        "Spa3": "Spa.3",
        "Spa4": "Spa.4"
    }, inplace=True)
    
    # Create corrected Spa columns
    df_corr["Spa1"] = (df_corr["Spa.1"] / 2) + 1
    df_corr["Spa2"] = (df_corr["Spa.2"] / 2) + 1
    df_corr["Spa3"] = (df_corr["Spa.3"] / 2) + 1
    df_corr["Spa4"] = (df_corr["Spa.4"] / 2) + 1

    # Reorder columns
    cols_order = ["Spa.1", "Spa.2", "Spa.3", "Spa.4",
                  "Spa1", "Spa2", "Spa3", "Spa4"] + \
                 [c for c in df_corr.columns if c not in
                  ["Spa.1","Spa.2","Spa.3","Spa.4","Spa1","Spa2","Spa3","Spa4"]]

    df_corr = df_corr[cols_order]

    # Save file
    df_corr.to_excel(output_file, index=False)
    print(f"Saved: {output_file} | Rows: {df_corr.shape[0]}")


# === Filtering + Saving ===
output_folder = r"D:\Corner analysis_DD+MG\dev_file"
os.makedirs(output_folder, exist_ok=True)

for t in [1, 3, 5, 7, 10]:
    df_filtered = df[(df["dev"] < t) & (df["Rho"] > 1) & (df["Rho"] < 80)]
    
    output_file = os.path.join(output_folder, f"dev{t}.xlsx")
    
    prepare_corrected_spa(df_filtered, output_file)

print("All filters applied and files saved successfully.")