#!/usr/bin/env python
# coding: utf-8

# # Creating Shape Lines for BEDMAP3
# 
# Author: Alice Fremand (@almand)
# 
# Date: 30/09/2022
# 
# ## The BEDMAP3 project
# 
# Bedmap3 is a collaborative community project with the aim to produce a new map and datasets of Antarctic ice thickness and bed topography for the international glaciology and geophysical community, using a variety of data (including ice-thickness, bathymetry, surface altitude and grounding lines).
# 
# Additionally Bedmap3 will act as a repository and portal for standardized RES data for the glaciology and Geophysics community.
# 
# For more information about the project: https://www.scar.org/science/bedmap3/home/
# 
# ## Creating shape Lines
# 
# The goal of the tutorial is to show how the Shape Lines have been created as an intermediary file of the BEDMAP3 project. The goal of this code is to create the tracks showing where the ice thickness data have been acquired.
# 
# The CSV data are available from the UK Polar Data Centre:
# 
# - Bedmap1 standardised CSV data points: https://doi.org/10.5285/f64815ec-4077-4432-9f55-0ce230f46029
# - Bedmap2 standardised CSV data points: https://doi.org/10.5285/2fd95199-365e-4da1-ae26-3b6d48b3e6ac
# - Bedmap3 standardised CSV data points: https://doi.org/10.5285/91523ff9-d621-46b3-87f7-ffb6efcd1847
# 
# ### Virtual environment
# 
# For the code to run, it is important to install the correct dependancies and libraries. In particular the following libraries are crucial for the code to be run: 
# 
# * geopandas
# * numpy
# * Scipy
# * math
# 
# **Note**: It is recommended to install geopandas first as it will upload most of the needed libraries at the same time without interoperability issues.
# 
# The list of dependancies uploaded in the current environment is given in the list below:

# In[1]:


pip list


# ### Upload the modules
# 
# * geopandas: used to create geodataframe and easily save the result to shapefiles or geopackages.
# * Other modules: pandas, os, glob, math, shapely, pathlib

# In[2]:


import os
import glob
import math
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
from pathlib import Path


# ### Initiate the different variables
# 

# In[3]:


aerogeophysics_data = 'D:/BEDMAP/AWI_2015_GEA-DML_AIR_BM3.csv'
ID = aerogeophysics_data.split('/')[-1].strip('.csv')
ID_split = ID.split('_')
print('ID: %s' %ID)


# ### Open the standardised CSV files
# 
# The code reads the standardised csv files using pandas. A number of columns are droped as they are not useful for the creation of the tracklines such as the line, date, time or trace.

# In[4]:


file = pd.read_csv(aerogeophysics_data, skiprows=18)
variables = file.columns.tolist()
line = [variable for variable in file.columns.tolist() if (variable.startswith('trajectory'))][0]
date = [variable for variable in file.columns.tolist() if (variable.startswith('date'))][0]
time  = [variable for variable in file.columns.tolist() if (variable.startswith('time'))][0]    
trace = [variable for variable in file.columns.tolist() if (variable.startswith('trace'))][0]
file = file.drop(columns=[line, trace, date, time])
file = file.drop(columns=variables[9:])


# The data are saved into a dataframe called "file". You can see what the dataframe looks like in the table below.

# In[5]:


file.head()


# ### Saving the data as a geo-dataframe
# 
# The data are then saved into a geodataframe using the `geopandas` module. This line of code will convert the latitude and longitude value into a specific point geometry.
# 

# In[6]:


gdf = gpd.GeoDataFrame(file, geometry=gpd.points_from_xy(file['longitude (degree_east)'], file['latitude (degree_north)']))

gdf.head()


# #### Setting up the coordinate system
# 
# The data are proposed as latitude and longitude from the WGS84  EPSG 4326 geographic system. We thus set the right coordinate system as follows:

# In[7]:


gdf = gdf.set_crs("EPSG:4326")


# #### Converting the data to the Antarctic Stereographic geographic system
# 
# To calculate specific parameters, such as the distance between two points, we project the data to the Antarctic Stereographic EPSG 3031 system:

# In[8]:


gdf =  gdf.to_crs("EPSG:3031")


# #### Calculating the distance between two points
# 
# We then calculate the distance between two points using the geodataframe function called `distance`. This will add a specific column to our geodataframe:

# In[9]:


file['distance'] = gdf.distance(gdf.shift(1))
file.head()


# ## Converting the points to lines
# 
# Then, we need to convert the points to line. The code will create a line between points whose distance is inferior to 15km. This is to showcase the location where data have not been recorded. We will then use the `groupby`function from geopandas to group the points together and create a line.

# In[10]:


segmentID = 0
segment = []
max_distance = 1000#min([1000, file.distance.mean()*10])
print('Mean distance between points: %s m' %round(file.distance.mean()))
if file.distance.mean() < 15000:
    for index, row in file.iterrows():
        if ID_split[0] == 'STANFORD' and row.distance <= 20000 or row.distance == 'NaN':
            segment.append('%s_segment%s' %(ID, segmentID))
        elif 'Recovery-Glacier' in ID_split[0:3] and row.distance <= 3000 or row.distance == 'NaN':
            segment.append('%s_segment%s' %(ID, segmentID))
        elif 'GEA-IV' in ID_split[0:3] and row.distance <= 3000 or row.distance == 'NaN':
            segment.append('%s_segment%s' %(ID, segmentID))
        elif ID_split[0] != 'STANFORD' and row.distance <= max_distance or row.distance == 'NaN':
            segment.append('%s_segment%s' %(ID, segmentID))
        else:
            segmentID = segmentID +1
            segment.append('%s_segment%s' %(ID, segmentID))
    gdf['segment'] = segment
    gdf = gdf.groupby(['segment'])['geometry'].apply(lambda x: LineString(x.tolist()) if x.size > 1 else x.tolist()[0])
    gdf = gpd.GeoDataFrame(gdf, geometry='geometry')


# #### Adding parameters and removing points

# In[11]:


gdf['Provider'] = ID_split[0]
gdf['Campaign'] = ID_split[2]
gdf['Year'] = ID_split[1]
gdf = gdf.set_crs("EPSG:3031")
gdf = gdf.reset_index()
for i in range(0,len(gdf)):
    if type(gdf.geometry[i]) ==Point:
        gdf = gdf.drop(index =i)


# ## Results
# ### Plotting flight lines

# In[12]:


# This line configures matplotlib to show figures embedded in the notebook, 
# instead of opening a new window for each figure. More about that later. 
# If you are using an old version of IPython, try using '%pylab inline' instead.
get_ipython().run_line_magic('matplotlib', 'inline')


# In[13]:


import matplotlib
import matplotlib.pyplot as plt


# In[14]:


plt.rcParams['figure.figsize'] = [50,50] # Set the size of the inline plot


fig, ax = plt.subplots(1, 1)
fig=plt.figure(figsize=(20,20), dpi= 300, facecolor='w', edgecolor='k')
gdf.plot(ax=ax)
ax.set_title('Trackline of %s survey' %ID)


# ### Results
# 
# All the BEDMAP lines shapefiles are available online: 
# 
# * BEDMAP2 shapeLines: https://doi.org/10.5285/0f90d926-99ce-43c9-b536-0c7791d1728b
# * BEDMAP3 shapeLines: https://doi.org/10.5285/a72a50c6-a829-4e12-9f9a-5a683a1acc4a
# 
# Please note that the lines are not available for BEDMAP1 as it was difficult to separate each survey into one campaign file.
