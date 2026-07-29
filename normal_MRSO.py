# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:59:26 2026

@author: user
"""

import pandas as pd
import numpy as np
from scipy import stats
import os
from pathlib import Path

# Create output directory
output_dir = "126_fin_Nmrso"
os.makedirs(output_dir, exist_ok=True)

# Input directory
input_dir = "126_fin_models"

# Process each Excel file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(('.xlsx', '.xls')):
        print(f"Processing {filename}...")
        
        # Read the Excel file
        file_path = os.path.join(input_dir, filename)
        df = pd.read_excel(file_path)
        
        # Determine which soil moisture column exists
        soil_col = None
        if 'mrsos' in df.columns:
            soil_col = 'mrsos'
        elif 'mrso' in df.columns:
            soil_col = 'mrso'
        else:
            print(f"Warning: No 'mrsos' or 'mrso' column found in {filename}")
            continue
        
        # Remove any NaN values for calculations
        soil_data = df[soil_col].dropna()
        
        if len(soil_data) == 0:
            print(f"Warning: No valid data in {filename}")
            continue
        
        # Normalize to 0-1 range (Min-Max normalization)
        min_val = soil_data.min()
        max_val = soil_data.max()
        df[f'{soil_col}_normalized'] = (df[soil_col] - min_val) / (max_val - min_val)
        
        # Calculate normal distribution statistics for normalized data
        normalized_data = df[f'{soil_col}_normalized'].dropna()
        mu, sigma = stats.norm.fit(normalized_data)
        
        # Add normal distribution statistics as new columns
        df[f'{soil_col}_normal_mean'] = mu
        df[f'{soil_col}_normal_std'] = sigma
        df[f'{soil_col}_normal_pdf'] = stats.norm.pdf(df[f'{soil_col}_normalized'], mu, sigma)
        df[f'{soil_col}_normal_cdf'] = stats.norm.cdf(df[f'{soil_col}_normalized'], mu, sigma)
        
        # Create summary statistics
        summary_stats = {
            'Original_Min': min_val,
            'Original_Max': max_val,
            'Original_Mean': soil_data.mean(),
            'Original_Std': soil_data.std(),
            'Normalized_Mean': mu,
            'Normalized_Std': sigma,
            'Sample_Size': len(normalized_data)
        }
        
        # Save the processed data to new Excel file with multiple sheets
        output_filename = f"{Path(filename).stem}_normalized.xlsx"
        output_path = os.path.join(output_dir, output_filename)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Summary statistics sheet
            summary_df = pd.DataFrame([summary_stats])
            summary_df.to_excel(writer, sheet_name='Summary_Stats', index=False)
        
        # Print statistics
        print(f"  - Original range: {min_val:.4f} to {max_val:.4f}")
        print(f"  - Normalized mean: {mu:.4f}, std: {sigma:.4f}")
        print(f"  - Sample size: {len(normalized_data)}")
        print(f"  - Saved: {output_filename}")

print("Processing complete!")