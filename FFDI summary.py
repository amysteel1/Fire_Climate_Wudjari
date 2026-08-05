# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 13:08:55 2026

@author: user
"""

import pandas as pd
import os
from pathlib import Path
import numpy as np

def process_ffdi_data(folder_path):
    """
    Extract FFDI data from all Excel files in a folder and summarize by periods and thresholds
    """
    folder_path = Path(folder_path)
    
    # Define time periods
    periods = {
        '2015-2034': (2015, 2034),
        '2035-2054': (2035, 2054),
        '2055-2074': (2055, 2074),
        '2075-2094': (2075, 2094)
    }
    
    # Define FFDI thresholds
    thresholds = [50, 75, 100]
    
    # Initialize results dictionary
    results = []
    
    # Process each Excel file in the folder
    for file_path in folder_path.glob("*.xlsx"):
        try:
            # Read the first sheet of each Excel file
            df = pd.read_excel(file_path, sheet_name=0)
            
            # Check if FFDI column exists
            if 'FFDI' not in df.columns:
                print(f"Warning: FFDI column not found in {file_path.name}")
                continue
            
            # Assume there's a date column - adjust column name as needed
            # Common date column names to try
            date_cols = ['Date', 'date', 'DATE', 'Time', 'time', 'DateTime']
            date_col = None
            
            for col in date_cols:
                if col in df.columns:
                    date_col = col
                    break
            
            if date_col is None:
                # If no date column found, assume first column is date
                date_col = df.columns[0]
                print(f"Using first column '{date_col}' as date for {file_path.name}")
            
            # Convert date column to datetime
            df[date_col] = pd.to_datetime(df[date_col])
            df['Year'] = df[date_col].dt.year
            
            # Extract model name from filename (remove extension)
            model_name = file_path.stem
            
            # Process each time period
            for period_name, (start_year, end_year) in periods.items():
                # Filter data for the current period
                period_data = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
                
                if len(period_data) == 0:
                    continue
                
                # Count exceedances for each threshold
                for threshold in thresholds:
                    count = len(period_data[period_data['FFDI'] > threshold])
                    
                    results.append({
                        'Model': model_name,
                        'Period': period_name,
                        'Threshold': f'FFDI > {threshold}',
                        'Count': count,
                        'Total_Days': len(period_data)
                    })
        
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
            continue
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(results)
    
    # Pivot table for better visualization
    pivot_df = summary_df.pivot_table(
        index=['Model', 'Period'], 
        columns='Threshold', 
        values='Count', 
        fill_value=0
    ).reset_index()
    
    return summary_df, pivot_df

# Usage
folder_path = "585_fin_Nmrso"  # Update this path as needed
summary_data, pivot_summary = process_ffdi_data(folder_path)

# Display results
print("Detailed Summary:")
print(summary_data.head(10))
print("\nPivot Summary:")
print(pivot_summary.head(10))

# Save results to Excel
output_file = "585FFDI_Summary_Analysis.xlsx"
with pd.ExcelWriter(output_file) as writer:
    summary_data.to_excel(writer, sheet_name='Detailed_Summary', index=False)
    pivot_summary.to_excel(writer, sheet_name='Pivot_Summary', index=False)

print(f"\nResults saved to {output_file}")

# Optional: Create a more detailed breakdown by model and period
model_period_summary = summary_data.groupby(['Model', 'Period']).agg({
    'Count': 'sum',
    'Total_Days': 'first'
}).reset_index()

print("\nModel-Period Summary:")
print(model_period_summary)