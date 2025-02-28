# -*- coding: utf-8 -*-
"""
Created by Ellie Fisher @efisher008 and Alice Fremand @almand_BAS on 2025-02-13

"""

import netCDF4 as nc
import pandas as pd
import shutil

def add_geo(netcdf_file, temp_file):

    # Step 1: Read the CSV file
    print("Reading the CSV file...")
    csv_data = pd.read_csv(csv_file, comment='#', header=0)

    # Ensure CSV file has the necessary columns: 'datetime', 'latitude', 'depth'
    if not {'time_gloria', 'longitude (degree_east)', 'latitude (degree_north)', 'depth_IBCSO_v2 (m)'}.issubset(csv_data.columns):
        raise ValueError("The CSV file must contain 'time_gloria', 'longitude (degree_east)', 'latitude (degree_north)', 'depth_IBCSO_v2 (m)' columns.")

    # Convert the datetime column in the CSV file to pandas datetime for comparison
    csv_data['datetime'] = pd.to_datetime(csv_data['time_gloria'], format = "%Y-%m-%d %H:%M:%S") # Make format match ISO8061
    
    # Step 2: Copy NetCDF file to avoid overwriting issues
    shutil.copy(netcdf_file, temp_file)

    # Step 3: Open NetCDF file in read/write mode
    print("Opening the NetCDF file...")
    with nc.Dataset(temp_file, mode="r+") as ds:
        group_names = list(ds.groups.keys())
        print(f"Groups found: {group_names}")

        for group_name in group_names:
            group = ds.groups[group_name]

            # Check if 'datetime' exists in the group's attributes
            if "datetime" not in group.ncattrs():
                print(f"Group '{group_name}' missing 'datetime' attribute. Skipping.")
                continue

            # Extract and match datetime
            group_datetime = pd.to_datetime(group.getncattr("datetime"))
            match = csv_data[csv_data['datetime'] == group_datetime]

            if not match.empty:
                latitude = match['latitude (degree_north)'].iloc[0]
                longitude = match['longitude (degree_east)'].iloc[0]
                depth = match['depth_IBCSO_v2 (m)'].iloc[0]

                # Add latitude and longitude attributes
                group.setncattr("latitude", latitude)
                group.setncattr("longitude", longitude)
                group.setncattr("depth_IBCSO", depth)
                print(f"Updated '{group_name}' with latitude={latitude}, longitude={longitude}.")
            # else:
                print(f"No matching datetime for group '{group_name}'.")

    print(f"Finished updating the file {temp_file}.")

# File paths
main_path = 'netcdf/' # Directory containing the NetCDF files
netcdf_file = main_path + "CD37_GLORIA_PASS001.nc" # Path to the input NetCDF file
csv_file = "CD37_gloria_track_depth_IBCSO.csv"  # Path to the GLORIA track CSV file
temp_file = "CD37_GLORIA_PASS001_coord_depth.nc"  # Path to save the modified NetCDF file

add_geo(netcdf_file, temp_file)
