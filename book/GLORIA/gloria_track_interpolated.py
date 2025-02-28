# -*- coding: utf-8 -*-
"""
Created by Ellie Fisher @eller90 on 2025-02-13

"""

import pandas as pd
import datetime
import glob
import geopandas as gpd
import pandas 
import numpy as np

def interpolate_missing_points(df, time_col, lat_col, lon_col):
    """
    Interpolate missing points to ensure a point every minute.

    Args:
        df (pd.DataFrame): DataFrame containing time, latitude, and longitude columns.
        time_col (str): Column name for time.
        lat_col (str): Column name for latitude.
        lon_col (str): Column name for longitude.

    Returns:
        pd.DataFrame: DataFrame with interpolated points.
    """
    # Set time column as index
    df = df.set_index(time_col)

    # Create a complete range of timestamps at 30-sec intervals
    full_time_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='30s')

    # Reindex the DataFrame to the full time range
    df = df.reindex(full_time_range)

    # Interpolate latitude and longitude
    df[lat_col] = df[lat_col].interpolate()
    df[lon_col] = df[lon_col].interpolate()

    # Reset the index back to the time column
    df = df.reset_index().rename(columns={'index': time_col})

    return df

file = 'CD37_gloria_track.csv'
column_names = ["Datetime", "New_time", "longitude", "latitude"]

# Reading in the CSV with all columns and index column
df = pd.read_csv(file, index_col=0, sep=',', usecols = (0,1,2,3), comment='#', header=0,
                 parse_dates=['New_time'],
                 names=column_names)

df2 = interpolate_missing_points(df, 'New_time', 'latitude', 'longitude')

# Saving output to new interpolated CSV file
df2.to_csv('CD37_gloria_track_interpolated.csv', index=False)
