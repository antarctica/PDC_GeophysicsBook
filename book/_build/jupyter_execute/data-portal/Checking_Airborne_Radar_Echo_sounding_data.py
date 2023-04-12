#!/usr/bin/env python
# coding: utf-8

# # Checking Airborne Radar Echo Sounding data
# 
# Author: Alice Fremand (@almand) & Julien Bodart (@julbod)
# 
# Date: 12/11/2021
# 
# ## Aim
# 
# The goal of this tutorial is to easily check radar echo sounding data from either NetCDF or SEG-Y formatted files.
# 
# ### Virtual environment
# 
# For the code to run, it is important to install the correct dependancies and libraries. In particular the following libraries are crucial for the code to run: 
# 
# * netCDF4 *module to check NetCDF data in python*
# * obspy *module to check SEGY data in python*
# 
# 
# ### To set up the virtual environment with Conda:
# ```
# >conda create -n aerogeophysics_env
# >conda activate aerogeophysics_env
# >conda config --env --add channels conda-forge
# >conda config --env --set channel_priority strict
# >conda install python=3 obspy
# >conda install netCDF4
# ```
# 
# ### To set up the virtual environment on UNIX: 
# Load your python module:
# 
# `module load python/conda3`
# 
# Then in the folder where you have your code, you need to launch:
# 
# `python3 -m venv aerogeophysics_env`
# 
# It will create a folder with all the environment for python.
# To activate the virtual environment you need to lauch it:
# 
# ```
# source aerogeophysics_env/bin/activate.csh
# ```
# 
# You need to make sure that [aerogeophysics_env] appears before your name on the machine. That means that you are using the virtual environment
# Then you need to upgrade pip which is the command that install the packages
# 
# `python3 -m pip install --upgrade pip`
# 
# And install the other libraries
# 
# `python3 -m pip install obspy`
# 
# In this tutorial, the virtual environment is already set up. The list of the current libraries loaded is given in the list below.

# In[258]:


pip list


# ### Load the relevant modules

# In[259]:


import netCDF4 as nc
from obspy.io.segy.segy import _read_segy
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import transforms
import numpy as np


# ## Check the NetCDF files
# 
# Example given for GRADES-IMAGE data.
# 
# Data available for download here: Corr, H. (2021). Processed airborne radio-echo sounding data from the GRADES-IMAGE survey covering the Evans and Rutford Ice Streams, and ice rises in the Ronne Ice Shelf, West Antarctica (2006/2007) (Version 1.0) [Data set]. NERC EDS UK Polar Data Centre. https://doi.org/10.5285/C7EA5697-87E3-4529-A0DD-089A2ED638FB
# 
# #### Read the NetCDF

# In[260]:


f=nc.Dataset('D:/British_Antarctic_Survey/data/GRADES_IMAGE_0607/netcdf/GRADES_IMAGE_G06.nc', 'r')


# #### Check the metadata information
# 
# By printing `f`, we can read the metadata and obtain information about the variables and their respective dimensions

# In[261]:


print(f.ncattrs())


# In[262]:


print(f)


# #### Check the dimension information
# To get information about the NetCDF dimensions and their size, you can do the following:

# In[263]:


print(f.dimensions.keys())


# In[264]:


for dim in f.dimensions.values():
    print(dim)


# #### Check the name and metadata of the variables stored in the NetCDF file

# In[265]:


print(f.variables.keys())


# In[266]:


for var in f.variables.values():
    print(var)


# ## Visual check of the data
# 
# ### Load the data

# In[323]:


# radar variables
traces_nc = f.variables['traces'][:].data # read in traces array
chirpData = f.variables['chirp_data'][:].data # read in chirp radar data array
pulseData = f.variables['pulse_data'][:].data # read in pulse radar data array

chirpData = 10*np.log10(chirpData) # convert the data from power to decibels using log function for visualisation
pulseData = 10*np.log10(pulseData) # convert the data from power to decibels using log function for visualisation

# X and Y coordinates
x_nc = f.variables['x_coordinates'][:].data # read in x positions array (Polar Stereographic EPSG 3031)
y_nc = f.variables['y_coordinates'][:].data # read in y positions array (Polar Stereographic EPSG 3031)
x_nc_km = np.divide(x_nc,1000) # transform meters to kilometers
y_nc_km = np.divide(y_nc,1000) # transform meters to kilometers

# surface and bed picks
surf_pick = f.variables['surface_pick_layerData'][:].data # read in surface pick array
bed_pick = f.variables['bed_pick_layerData'][:].data # read in bed pick array
surf_pick[surf_pick == -9999] = 'nan' # convert -9999 to NaNs for plotting
bed_pick[bed_pick == -9999] = 'nan' # convert -9999 to NaNs for plotting

# surface and bed elevations
surface_elevation = f.variables['surface_altitude_layerData'][:].data # read in surface altitude array
bed_elevation = f.variables['bed_altitude_layerData'][:].data # read in bed altitude array
surface_elevation[surface_elevation == -9999] = 'nan' # convert -9999 to NaNs for plotting
bed_elevation[bed_elevation == -9999] = 'nan' # convert -9999 to NaNs for plotting


# ### Plot the processed radargrams

# In[333]:


plt.rcParams['figure.figsize'] = [20,12] # set the size of the inline plot

fig1, ax1 = plt.subplots()
radar_im = ax1.imshow(chirpData[:600,:], cmap='Greys', vmin = 10, aspect='auto') # plot data (limit y-axis extent and colorscale)
ax1.plot(surf_pick,'r--', linewidth=2) # plot surface pick
ax1.plot(bed_pick, 'b--', linewidth=2) # plot bed pick 
ax1.xaxis.set_major_locator(ticker.LinearLocator(6)) # set x-axis tick limits

ax1.set_title("Radar Data - Chirp (NetCDF)", fontsize = 20, fontweight = 'bold') # set title
ax1.set_xlabel("Trace Number", fontsize = 16) # set axis title
ax1.set_ylabel("Fast Time Sample Number", fontsize = 16) # set axis title
fig1.colorbar(radar_im, ax = ax1) # plot colorbar


# In[334]:


plt.rcParams['figure.figsize'] = [20,20] # set the size of the inline plot

fig2, ax2 = plt.subplots()
radar_im = ax2.imshow(pulseData[:600,:], cmap = 'Greys',  aspect='auto') # plot data (limit y-axis extent and colorscale)
ax2.plot(surf_pick,'r--', linewidth=2) # plot surface pick
ax2.plot(bed_pick, 'b--', linewidth=1) # plot bed pick
ax2.xaxis.set_major_locator(ticker.LinearLocator(6)) # set x-axis tick limits

ax2.set_title("Radar Data - pulse  (NetCDF)", fontsize = 20, fontweight = 'bold') # set title
ax2.set_xlabel("Trace Number", fontsize = 16) # set axis title
ax2.set_ylabel("Fast Time Sample Number", fontsize = 16) # set axis title
fig2.colorbar(radar_im, ax = ax2) # plot colorbar


# ### Plot amplitude of single trace from the radar data

# In[331]:


plt.rcParams['figure.figsize'] = [20,20] # set the size of the inline plot
fig2, (ax3, ax4) = plt.subplots(1, 2) # Specify how many plots you want

# first plot the radargram with specific trace marked as red vertical line
radar_im = ax3.imshow(chirpData[:600,:],cmap='Greys', vmin = 10, vmax = 60, aspect='auto') # plot data (limit y-axis extent and colorscale)
ax3.plot(surf_pick,'r--', linewidth=2) # plot surface pick
ax3.plot(bed_pick, 'b--', linewidth=2) # plot surface pick
ax3.xaxis.set_major_locator(ticker.LinearLocator(6)) # set x-axis tick limits
ax3.axvline(x=1850, color='r', linestyle='-') # plot position of trace in second plot
ax3.autoscale(enable=True, axis='x', tight=True) # tighten up x axis

ax3.set_title("Radar Data - Chirp (NetCDF)", fontsize = 20, fontweight = 'bold') # set title
ax3.set_xlabel("Trace Number", fontsize = 16)  # set axis title
ax3.set_ylabel("Fast Time Sample Number", fontsize = 16) # set axis title
fig2.colorbar(radar_im, ax = ax3) # plot colorbar

# then plot trace plot with amplitude and sampling window
ax4.plot(chirpData[:600,1850])
plt.title('Trace 1850 - Radar Data', fontsize = 20, fontweight = 'bold')  # set title
plt.xlabel('Fast Time Sample Number', fontsize = 16) # set axis title
plt.ylabel('Amplitude (dB)', fontsize = 16) # set axis title
plt.ylim([10,60]) # set limit of y-axis
plt.show()


# ### Plot geographic location of trace on map

# In[304]:


plt.rcParams['figure.figsize'] = [10,10] # Set the size of the inline plot

fig3, ax5 = plt.subplots(1,1)
plt.scatter(x_nc_km, y_nc_km, marker='o', s=1) # plot entire profile
plt.scatter(x_nc_km[1850], y_nc_km[1850], marker='o',color=['red'], s=100) # plot specific trace position as red dot

ax5.set_title("Position of Trace 1850", fontsize = 18, fontweight = 'bold') # set title
ax5.set_xlabel("X (km)", fontsize = 14) # set axis title
ax5.set_ylabel("Y (km)", fontsize = 14) # set axis title


# ### Plot surface and bed elevations along flightline

# In[332]:


plt.rcParams['figure.figsize'] = [10,10] # Set the size of the inline plot

fig4, ax6 = plt.subplots(1,1)
ax6.plot(traces_nc, surface_elevation) # plot surface elevation for entire profile
ax6.plot(traces_nc, bed_elevation) # plot bed elevation for entire profile

ax6.set_title("Elevation Profile for flightline G06", fontsize = 18, fontweight = 'bold') # set title
ax6.set_xlabel("Trace Number", fontsize = 14) # set axis title
ax6.set_ylabel("Elevation (meters WGS84)", fontsize = 14) # set axis title


# ## Check the SEG-Y files
# 
# ### Load the data for chirp and pulse
# 
# Give here the path to where the desired files lives on your PC

# In[305]:


segy_data_chirp = 'D:/British_Antarctic_Survey/data/GRADES_IMAGE_0607/segy/chirp/G06_chirp.segy'
segy_data_pulse = 'D:/British_Antarctic_Survey/data/GRADES_IMAGE_0607/segy/pulse/G06_pulse.segy'


# ### Read the SEG-Ys
# 
# The data is read using the `_read_segy` command from the `obspy` Python module

# In[272]:


segy_chirp = _read_segy(segy_data_chirp, headonly=True)
segy_pulse = _read_segy(segy_data_pulse, headonly=True)


# ### Inspect SEG-Y parameters 
# 
# It is possible to check the content of the SEG-Y bytes using very simple commands of the `obspy` package. 
# 
# Some examples are given below for the chirp data (pulse is the same):

# In[273]:


segy_chirp


# In[274]:


header_segy = segy_chirp.binary_file_header
header_segy


# ### Read traces
# 
# Obspy can also be used to read individual traces

# In[306]:


traces = segy_chirp.traces


# We can then have a look at the header of one specific trace, as follows:

# In[307]:


trace_header = traces[1].header # for trace 1
trace_header


# We can also check the amount of traces in the file (x-axis):

# In[277]:


sgy_traces_len = len(segy_chirp.traces)
sgy_traces_len


# And check the length of the sampling window (y-axis)

# In[278]:


sgy_samples_len = traces[1].header.number_of_samples_in_this_trace
sgy_samples_len


# ### Plot the processed radargrams

# We first need to concatenate all traces from the SEG-Y into one array and calculate the log of data

# In[284]:


data_chirp = np.stack(t.data for t in segy_chirp.traces) # concatenate
data_chirp = 10*np.log10(data_chirp) # convert the data from power to decibels using log of data


# In[308]:


data_pulse = np.stack(t.data for t in segy_pulse.traces) # concatenate
data_pulse = 10*np.log10(data_pulse) # convert the data from power to decibels using log of data


# Now we can plot them:

# In[281]:


plt.rcParams["figure.figsize"] = (20,20) # set the size of the inline plot

fig4, ax6 = plt.subplots() 
plt.imshow(data_chirp.T, cmap='Greys', vmin = 10, aspect='auto') # plot data (limit colorscale extent)
plt.title('Radar data - Chirp (SEG-Y)', fontsize = 20, fontweight = 'bold') # set title
plt.colorbar() # plot colorbar
plt.tight_layout() # tighten up x axis
plt.ylim([600,0]) # set y-axis limits
ax5.set_xlabel("Trace Number", fontsize = 16) # set axis title
ax5.set_ylabel("Fast Time Sample Number", fontsize = 16) # set axis title


# In[282]:


plt.rcParams["figure.figsize"] = (20,20) # set the size of the inline plot

fig5, ax7 = plt.subplots()
plt.imshow(data_pulse.T, cmap='Greys', aspect='auto') # plot data (limit colorscale extent)
plt.title('Radar data - Pulse (SEG-Y)', fontsize = 20, fontweight = 'bold') # set title
plt.colorbar() # plot colorbar
plt.tight_layout() # tighten up x axis
plt.ylim([600,0]) # set y-axis limits
ax6.set_xlabel("Trace Number", fontsize = 16) # set axis title
ax6.set_ylabel("Fast Time Sample Number", fontsize = 16) # set axis title

