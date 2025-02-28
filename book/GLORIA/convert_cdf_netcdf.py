# -*- coding: utf-8 -*-
"""
Created by Alice Fremand @almand_BAS on 2025-02-10

"""

import numpy as np
import netCDF4 as nc

# Step 1: Load the original NetCDF file

input_nc = "CDF.cdf" # Input CDF formatted file
output_nc = "CDF.nc" # Output NetCDF formatted file 

pass_number = input_nc.split('cd37p')[-1][:-4]
# Open original NetCDF file
with nc.Dataset(input_nc, "r") as src:
    # Extract image data (2D array: nl x ns)
    image_data = src.variables["image"][:]  # shape (nl, ns)

    # Extract latitude and longitude (assuming latlon[nl, 2])
    latlon = src.variables["latlon"][:]
    latitudes = latlon[:, 0]  # First column = latitude
    longitudes = latlon[:, 1]  # Second column = longitude

    # Extract date and time variables
    date_vars = src.variables["date"][:]  # shape (nl, 4)
    time_vars = src.variables["time"][:]  # shape (nl, 3)

    # Open a new NetCDF file for writing
    with nc.Dataset(output_nc, "w", format="NETCDF4") as dst:
        dst.history = 'Converted from the National Oceanography Centre .cdf file'
        for i in range(image_data.shape[0]):  # Iterate over each scan line (nl)
            group_name = f"scan{i+1}"  # Naming each scan group
            scan_group = dst.createGroup(group_name)

            # Define dimension for scan samples
            scan_group.createDimension("samples", image_data.shape[1] + 2)  # +2 padding

            # Define variable for scan data
            scan_var = scan_group.createVariable("scan", "u1", ("samples",))
            scan_var.units = "1"
            scan_var.long_name = "Scan Samples"

            # Reverse the scan data
            reversed_scan = image_data[i, ::-1].astype(float)  # Convert to float to allow NaNs

            # Split into two sections and shift them
            left_part = reversed_scan[:496]  # Shift left
            right_part = reversed_scan[496:]  # Shift right

            # Merge back and set indices 496 and 497 to NaN
            shifted_scan = np.concatenate([left_part, [np.nan, np.nan], right_part])

            # Store shifted scan with padding
            scan_var[:] = np.pad(shifted_scan, (0, 0), mode="constant", constant_values=np.nan)

            # Extract date and time info for the scan
            year = f"{date_vars[i,0]:02d}"  # Extracting year
            month = f"{date_vars[i,1]:02d}"
            day = f"{date_vars[i,2]:02d}"
            julian_day = f"{date_vars[i,3]:03d}"
            hours = f"{time_vars[i,0]:02d}"
            minutes = f"{time_vars[i,1]:02d}"
            seconds = ""  # Not stored in the target format
            
            # Assign metadata attributes for the scan
            scan_group.pass_number = int(pass_number)
            scan_group.scan_number = int(i + 1)
            scan_group.hour_mark_flag = 9999
            scan_group.slant_range_correction_code = 9999
            scan_group.zero_flag = 0
            scan_group.pulse_repetition_period = 51
            scan_group.vehicle_heading = 9999
            scan_group.year = year[2:]
            scan_group.edge_mark_start = 65535
            scan_group.edge_mark_end = 65535
            scan_group.julian_day = julian_day
            scan_group.hours = hours
            scan_group.minutes = minutes
            scan_group.seconds = seconds
            scan_group.checksum = 9999
            scan_group.unused = 0
            scan_group.datetime = f"{year}-{month}-{day}T{hours}:{minutes}:00"
            
print("Conversion completed successfully!")
