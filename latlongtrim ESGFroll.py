# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:43:13 2026

@author: user
"""

import xarray as xr
import os
import glob
from pathlib import Path

# Define parameters
input_dir = r"C:\Users\user\Documents\NEW CMIP6 ESGF"
output_dir = r"C:\Users\user\Documents\NEW CMIP6 ESGF\trimmed_files"  # or use input_dir to save in same location

# Coordinate bounds
lat_min, lat_max = -35, -32
lon_min, lon_max = 120, 124

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Find all NetCDF files
nc_files = glob.glob(os.path.join(input_dir, "*.nc"))

print(f"Found {len(nc_files)} NetCDF files to process...")

# Process each file
for i, file_path in enumerate(nc_files):
    try:
        # Get original filename
        original_filename = os.path.basename(file_path)
        new_filename = f"AB_{original_filename}"
        output_path = os.path.join(output_dir, new_filename)
        
        print(f"Processing {i+1}/{len(nc_files)}: {original_filename}")
        
        # Open dataset
        ds = xr.open_dataset(file_path)
        
        # Check if lat/lon coordinates exist (handle different naming conventions)
        lat_coord = None
        lon_coord = None
        
        for coord in ['lat', 'latitude', 'y']:
            if coord in ds.coords or coord in ds.dims:
                lat_coord = coord
                break
                
        for coord in ['lon', 'longitude', 'x']:
            if coord in ds.coords or coord in ds.dims:
                lon_coord = coord
                break
        
        if lat_coord is None or lon_coord is None:
            print(f"  Warning: Could not find lat/lon coordinates in {original_filename}")
            ds.close()
            continue
        
        # Perform spatial subsetting
        ds_subset = ds.sel({
            lat_coord: slice(lat_min, lat_max),
            lon_coord: slice(lon_min, lon_max)
        })
        
        # Check if subset contains data
        if ds_subset.sizes[lat_coord] == 0 or ds_subset.sizes[lon_coord] == 0:
            print(f"  Warning: No data in specified region for {original_filename}")
            ds.close()
            continue
        
        # Save trimmed file
        ds_subset.to_netcdf(output_path)
        
        # Close datasets to free memory
        ds.close()
        ds_subset.close()
        
        print(f"  Successfully saved: {new_filename}")
        
    except Exception as e:
        print(f"  Error processing {original_filename}: {str(e)}")
        continue

print(f"\nProcessing complete! Trimmed files saved in: {output_dir}")