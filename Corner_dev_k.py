# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:52:31 2026
In this script we done need to add the function to create new columns for pygimlis since the input file has already thatt thing.
@author: akagupta
"""
import pandas as pd
import os

# === Load data ===
file_path = r"D:\Corner analysis_DD+MG\dev_file\dev5.xlsx"
df = pd.read_excel(file_path)

print("Initial rows:", df.shape[0])

# --- Function for filtering & saving ---
def save_dev_k_filters(df, output_folder):
    """
    This function will give us the files dd_dev5_k5000.xlsx, dd_dev5_k8000.xlsx, etc.
    Filtering: dev < 5 AND 1 < Rho < 80 AND k< (5000,8000,10000)
    """
    os.makedirs(output_folder, exist_ok=True)
    for t in [5000,8000,10000]:
        filtered = df[(df["k"] < t) & (df["Rho"] > 1) & (df["Rho"] < 80)]
        filtered.to_excel(f"{output_folder}/dev5_K{t}.xlsx", index=False)
    print("Filtering complete.")

# Apply filters and save
output_folder = r"D:\Corner analysis_DD+MG\dev5_k_file"
save_dev_k_filters(df, output_folder)


































