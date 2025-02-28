# -*- coding: utf-8 -*-
"""
Created by Ellie Fisher @eller90 on 2025-01-31

"""

import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import glob
import geopandas as gpd
import pandas 
import numpy as np

# Calculate distance of the ship between each point
def lat_lon_to_distance(df, lat_col, lon_col):
    """
    Convert latitude/longitude to distances in meters between consecutive points.

    Args:
        df (pd.DataFrame): DataFrame containing latitude and longitude columns.
        lat_col (str): Column name for latitude.
        lon_col (str): Column name for longitude.

    Returns:
        pd.Series: Series containing distances in meters between consecutive points.
    """
    # Earth radius in meters
    R = 6371000 

    # Convert latitude and longitude from degrees to radians
    lat = np.radians(df[lat_col])
    lon = np.radians(df[lon_col])
    
    # Calculate differences between consecutive latitudes and longitudes
    delta_lat = lat.diff()
    delta_lon = lon.diff()

    # Haversine formula
    a = np.sin(delta_lat / 2)**2 + np.cos(lat.shift()) * np.cos(lat) * np.sin(delta_lon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c  # Distance in meters

    return distance.fillna(0)  # Replace NaN with 0 for the first row


# Calculate the speed of the ship from the cruise track
def calculate_speed_in_knots(df, datetime_col, distance_col):
    """
    Calculate speed based on datetime and distance in a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing datetime and distance columns.
        datetime_col (str): Column name for datetime (in ISO 8601 or similar format).
        distance_col (str): Column name for distance in meters.

    Returns:
        pd.Series: Series containing speeds in knots.
    """
    # Ensure the datetime column is in datetime format
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    
    # Calculate the time difference in seconds
    time_diff = df[datetime_col].diff().dt.total_seconds()
    
    # Calculate speed (distance / time) in meters/seconds
    speed_mps = df[distance_col] / time_diff
    
    # Convert speed to knots (1 m/s = 1.94384 knots)
    speed_knots = speed_mps * 1.94384
   
    # Handle potential division by zero or NaN
    speed_knots = speed_knots.fillna(0)  # Replace NaN (e.g., for the first row) with 0

    return speed_knots

def calculate_heading(df, lat_col, lon_col):
    """
    Calculate the heading (bearing) in degrees from the north between consecutive points.
    
    Args:
        df (pd.DataFrame): DataFrame containing latitude and longitude columns.
        lat_col (str): Column name for latitude.
        lon_col (str): Column name for longitude.
        
    Returns:
        pd.Series: Series containing headings in degrees between consecutive points.
    """
    lat1 = np.radians(df[lat_col].shift())
    lat2 = np.radians(df[lat_col])
    lon1 = np.radians(df[lon_col].shift())
    lon2 = np.radians(df[lon_col])

    delta_lon = lon2 - lon1

    # Calculate the bearing (heading) in radians
    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon)
    
    # Get the heading in radians
    heading = np.arctan2(x, y)
    
    # Convert to degrees and normalize to 0-360 degrees
    heading_deg = np.degrees(heading) % 360
    
    return heading_deg.fillna(0)  # Replace NaN with 0 for the first row

def correct_dt_tow_distance(df):
    """
    Correct datetime for the GLORIA instrument track to account for the tow distance of the instrument behind the ship.
    Args:
        df (pd.DataFrame): DataFrame containing datetime, distance and rolling_mean_speed columns.

    Returns:
        pd.Series: Series containing recalculated datetime values.
        pd.Series: Series containing speeds in m/s.
    """

    # Add a time offset of 1m30s of GLORIA behind the ship at each point
    lag = pd.Timedelta(1.5, "m") # Creating a Pandas timedelta object with a value of 1.5 minutes
    time_delta = pd.Series(df['Datetime']+lag) # Applying this lag to the datetime information

    # Transforming product of time difference calculation to datetime.
    new_time = pd.to_datetime(time_delta)

    return new_time

## Define input CSV and execute functions.
file = 'CD37_cruise_track.csv' # Cruise track CSV
column_names = ["Datetime", "Lon", "Lat"]

df = pd.read_csv(file, index_col=None, sep=',', usecols=(0,1,2), comment='#', header=0,
                 parse_dates=["Datetime"],
                 date_parser=lambda x: pd.to_datetime(x, format="%Y-%m-%d %H:%M:%S"), names=column_names)

df['longitude']  = df['Lon'].apply(lambda lon:lon - 360 if lon > 180 else lon)
df['latitude']  = df['Lat'].apply(lambda lat:lat - 180 if lat > 90 else lat)

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
gdf = gdf.set_crs("EPSG:4326")

# Creating new columns for distance, speed and time offset calculation.
gdf['distance_m'] = lat_lon_to_distance(gdf, 'latitude', 'longitude')
gdf['speed_knots'] = calculate_speed_in_knots(gdf, 'Datetime', 'distance_m')
gdf['New_time'] = correct_dt_tow_distance(gdf)
gdf['heading_deg'] = calculate_heading(gdf, 'latitude', 'longitude')

# Reordering dataframe to have new datetime in second position.
gdf = gdf.loc[:,['Datetime','New_time','longitude','latitude','geometry','speed_knots', 'heading_deg']]

gdf.to_file('CD37_gloria_track.gpkg', layer='Point', driver="GPKG")
gdf.to_csv('CD37_gloria_track.csv', index=False)
