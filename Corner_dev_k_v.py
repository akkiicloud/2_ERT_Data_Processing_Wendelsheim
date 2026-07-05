# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 15:26:02 2026

@author: akagupta
"""


import pandas as pd
import numpy as np
import os


# === Load data ===
file_path = r"D:\Corner analysis_DD+MG\dev5_k_file\dev5_K10000.xlsx"
df = pd.read_excel(file_path)

print("Initial rows:", df.shape[0])

# --- Filtering & saving function ---
def save_filtered_files(df, output_folder):
    """
    Saves 4 filtered files based on conditions:
    dev < 5, 1 < Rho < 80,
    k < (10000),
    |Vp| > (0.25 or 0.50).
    """
    os.makedirs(output_folder, exist_ok=True)
    
    for k_limit in [10000]:
        for v_limit in [0.25, 0.50,
                        0.75]:
            filtered = df[
                (df["dev"] < 5) &
                (df["Rho"] > 1) & (df["Rho"] < 80) &
                (df["k"] < k_limit) &
                (df["Vp"].abs() > v_limit)  # absolute value of V
            ]
            
            filename = f"dev5_k{k_limit}_v{str(v_limit).replace('.', '')}.xlsx"
            filtered.to_excel(os.path.join(output_folder, filename), index=False)

    print("Filtering complete. 4 files created.")

# --- Run filtering ---
output_folder = r"D:\Corner analysis_DD+MG\dev5_k_v_file"
save_filtered_files(df, output_folder)