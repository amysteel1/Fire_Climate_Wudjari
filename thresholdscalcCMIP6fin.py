# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 07:27:37 2026

@author: user
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
from pathlib import Path

def weather_soil_threshold_calculator(dfFIREdraft1):
    """
    Calculate and identify rows where all variables are within their defined thresholds
    """
    # Define thresholds (without the soil moisture variable initially)
    standard_thresholds = {
        'TP_mm': (1, 10),          
        'tas': (10, 30),       
        'RH': (0.30, 0.60),            
        'Wind_kmph': (10, 30),
    }
    
    # Check for soil moisture columns and add the appropriate one
    soil_moisture_threshold = (0.25, 0.5)
    if 'mrsos_normalized' in dfFIREdraft1.columns:
        standard_thresholds['mrsos_normalized'] = soil_moisture_threshold
        print("Using 'mrsos_normalized' for soil moisture threshold")
    elif 'mrso_normalized' in dfFIREdraft1.columns:
        standard_thresholds['mrso_normalized'] = soil_moisture_threshold
        print("Using 'mrso_normalized' for soil moisture threshold")
    else:
        print("Warning: Neither 'mrsos_normalized' nor 'mrso_normalized' found in the data")
    
    # Create mask for each variable being within thresholds
    masks = []
    
    # Process standard variables
    for var_name, (lower, upper) in standard_thresholds.items():
        if var_name in dfFIREdraft1.columns:
            mask = (dfFIREdraft1[var_name] >= lower) & (dfFIREdraft1[var_name] <= upper)
            masks.append(mask)
        else:
            print(f"Warning: Column '{var_name}' not found in the data")
    
    # Combine all masks
    all_within_thresholds = np.all(masks, axis=0)
    rows_within_all_thresholds = dfFIREdraft1[all_within_thresholds]
    
    # Calculate summary statistics
    total_rows = len(dfFIREdraft1)
    rows_within_count = len(rows_within_all_thresholds)
    
    print(f"\nSummary of All Variables Within Thresholds:")
    print(f"Total number of rows: {total_rows}")
    print(f"Rows with all variables within thresholds: {rows_within_count}")
    print(f"Percentage of rows within all thresholds: {(rows_within_count/total_rows)*100:.2f}%")
    
    print("\nFirst 5 rows where all variables are within thresholds:")
    print(rows_within_all_thresholds.head())
    
    # Create threshold summary
    results = {}
    for var_name, (lower, upper) in standard_thresholds.items():
        if var_name in dfFIREdraft1.columns:
            values = dfFIREdraft1[var_name]
            within = np.sum((values >= lower) & (values <= upper))
            total = len(values)
            
            results[var_name] = {
                'Lower Bound': lower,
                'Upper Bound': upper,
                'Within Threshold Count': within,
                'Within Threshold %': round((within/total) * 100, 2)
            }

    results_df = pd.DataFrame.from_dict(results, orient='index')
    return results_df, rows_within_all_thresholds

# Define the folder path
folder_path = "585_fin_Nmrso"

# Get all Excel files in the folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls'))]

print(f"Found {len(excel_files)} Excel files in '{folder_path}' folder")

# Loop through each Excel file
for file_name in excel_files:
    file_path = os.path.join(folder_path, file_name)
    print(f"\n{'='*60}")
    print(f"Processing: {file_name}")
    print(f"{'='*60}")
    
    try:
        # Load and process the data
        df = pd.read_excel(file_path)
        dfFIREdraft1 = pd.DataFrame(df)
        
        # Calculate thresholds and get results
        threshold_summary, within_threshold_rows = weather_soil_threshold_calculator(dfFIREdraft1)
        print("\nIndividual Variable Threshold Summary:")
        print(threshold_summary)
        
        # Create output filename based on input filename
        base_name = os.path.splitext(file_name)[0]
        output_filename = f'thresholdscalc_{base_name}.xlsx'
        output_path = os.path.join(folder_path, output_filename)
        
        # Save results to a new Excel file with multiple sheets
        with pd.ExcelWriter(output_path) as writer:
            df.to_excel(writer, sheet_name='Original_Data', index=False)
            threshold_summary.to_excel(writer, sheet_name='Threshold_Summary')
            within_threshold_rows.to_excel(writer, sheet_name='Within_Thresholds', index=False)
        
        print(f"Results saved to: {output_filename}")
        
    except Exception as e:
        print(f"Error processing {file_name}: {str(e)}")
        continue

print(f"\n{'='*60}")
print("Processing complete!")