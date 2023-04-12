#!/usr/bin/env python
# coding: utf-8

# # Reading the BEDMAP CSV files
# 
# Author: Alice Fremand (@almand)
# 
# Date: 30/09/2022
# 
# ## Aim
# 
# The goal of this tutorial is to show how the BEDMAP CSV files have been checked geospatially. The code can also be run to create shapefiles or geopackages or directly check the data geospatially. 
# 
# ## The data
# 
# The BEDMAP CSV files are available for downmoad from the UK Polar data Centre:
# * BEDMAP1 CSV: https://doi.org/10.5285/f64815ec-4077-4432-9f55-0ce230f46029
# * BEDMAP2 CSV: https://doi.org/10.5285/2fd95199-365e-4da1-ae26-3b6d48b3e6ac
# * BEDMAP3 CSV: https://doi.org/10.5285/91523ff9-d621-46b3-87f7-ffb6efcd1847
# 
# ## The code
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
# ### To set up the virtual environment with Conda:
# ```
# >conda create -n geo_env
# >conda activate geo_env
# >conda config --env --add channels conda-forge
# >conda config --env --set channel_priority strict
# >conda install python=3 geopandas 
# ```
# 
# ### To set up the virtual environment on the SAN: 
# `>module load python/conda3`
# 
# Then in the folder where you have your code, you need to launch:
# 
# `>python3 -m venv geo_env`
# 
# It will create a folder with all the environment for python.
# To activate the virtual environment you need to lauch it:
# 
# ```
# >source venv/bin/activate.csh
# >source activate geo_env
# ```
# 
# You need to make sure that [geo_env] appears before your name on the machine. That means that you are using the virtual environment
# Then you need to upgrade pip which is the command that install the packages
# 
# `>python3 -m pip install --upgrade pip`
# 
# And install the other libraries
# 
# `>python3 -m pip install geopandas`
# 
# In this tutorial, the virtual environment is already set up. The list of the current libraries loaded is given in the list below.

# In[1]:


pip list


# ### Upload the modules
# 
# * geopandas: used to create geodataframe and easily save the result to shapefiles or geopackages.
# * pandas: used to read the csv file
# * Other modules: mathplotlib

# In[2]:


import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Import the csv file
# 
# Before starting, the BEDMAP CSV files need to be downloaded from the UK Polar Data Centre Repository. In this example, we use the 'AWI_2014_GEA-IV_AIR_BM3' file located in the following folder: `'D:/BEDMAP/AWI_2015_GEA-DML_AIR_BM3.csv'`

# In[3]:


CSV_file = 'D:/BEDMAP/AWI_2015_GEA-DML_AIR_BM3.csv'


# The `pandas` module is used to open the file. The command `pd.read_csv(input_file)` can be used to read the BEDMAP CSV file. To skip the metadata at the top of the file, we use the `skiprows` argument as follows:

# In[4]:


data = pd.read_csv(CSV_file, skiprows=18, low_memory=False)


# By using the `read_csv()` command, the data is directly saved in a dataframe. We can have a look at the top lines by running the following:

# In[5]:


data.head()


# In[6]:


data.dtypes


# In[7]:


data.tail()


# ## Convert the file geospatially
# 
# The `geopandas` module is then used to convert the data to a geodataframe. It will convert the latitude/longitude to points.
# To do that, you will need to identify the specific header used for longitude and latitude in the CSV file.
# 
# Here, it is `Longitude_decimal_degrees` and `Latitude_decimal_degrees`

# In[8]:


gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude (degree_east)'], data['latitude (degree_north)']))


# We can check that the conversion has been done:

# In[9]:


gdf.head()


# ## Determine the variables to show in the shapefile/geopackage
# 
# All the variables that are present in the dataframe will be shown in the final shapefile or geopackage. We might want to remove the columns that we don't want. For instance, here all the line_ID values are equal to -9999, so this information is missing. To delete this column, we just need to do the following:

# In[10]:


gdf = gdf.drop(columns=['trajectory_id'])
gdf.head()


# As you can see, the column Line_ID has been removed. We can also remove several variables at the same time:

# In[11]:


gdf = gdf.drop(columns=[ 'trace_number', 'date', 'time_UTC'])
gdf.head()


# ## Setting up the coordinate system
# 
# It is important to then set the coordinate system. 
# Here the WGS84 coordinate system is used, it corresponds to the EPSG: 4326. 

# In[12]:


gdf = gdf.set_crs("EPSG:4326")


# With geopandas, it is also possible to convert the data to another coordinate system and project it. You just need to know the EPSG ID of the output coordinate system. Here is how to convert the data to the stereographic geographic system.

# In[13]:


gdf =  gdf.to_crs("EPSG:3031")


# ## Plotting the data
# 

# In[14]:


plt.rcParams["figure.figsize"] = (100,100)
fig, ax = plt.subplots(1, 1)
fig=plt.figure(figsize=(100,100), dpi= 100, facecolor='w', edgecolor='k')
gdf.plot(column='land_ice_thickness (m)', ax=ax, legend=True, legend_kwds={'label': "Ice Thickness (m)",'orientation': "horizontal"})


# ## Saving the data to geopackages or shapefile
# 
# To save the data to geopackage or shapefile, we only need to use the `.to_file()` command from `geopandas` module. Then we specify the driver, that will specify the type of output - geopackage or shapefile.

# In[15]:


gdf.to_file('D:/BEDMAP/point.gpkg', layer='Points', driver="GPKG")
gdf.to_file('D:/BEDMAP/point.shp', driver="ESRI Shapefile")

