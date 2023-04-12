#!/usr/bin/env python
# coding: utf-8

# # Get full metadata from CSV file - BEDMAP
# 
# This notebook shows how to get the rich and complete metadata from the Bedmap CSV file. It also shows how to convert the CSV file to NCCSV (NetCDF compatible CSV) as an example to the FAIR implementation of the CSV format used for Bedmap.
# 
# With only access to the CSV file, it is possible to programmatically obtain rich metadata from the file without having a complex metadata structure as header information in the file. 
# 
# ## The data
# 
# The BEDMAP CSV files are available for downmoad from the UK Polar data Centre:
# 
# * BEDMAP1 CSV: https://doi.org/10.5285/f64815ec-4077-4432-9f55-0ce230f46029
# 
# * BEDMAP2 CSV: https://doi.org/10.5285/2fd95199-365e-4da1-ae26-3b6d48b3e6ac
# 
# * BEDMAP3 CSV: https://doi.org/10.5285/91523ff9-d621-46b3-87f7-ffb6efcd1847
#     
# ## Upload the modules
# 
# For this conversion, we will need pandas, json, xarray, netCDF4 and urllib modules. 
# 

# In[1]:


import pandas as pd
import json
import urllib.request
import xarray
import netCDF4 as nc 


# ## Opening and reading the CSV metadata
# 
# For this exercise, we only need to check the short metadata provided in the CSV file.

# In[2]:


CSV_file = 'E:/BEDMAP/AWI_2015_GEA-DML_AIR_BM3.csv'
csv_metadata = pd.read_csv(CSV_file, nrows=18, sep = ': ', engine='python', header= None)
csv_metadata


# First, we set the index as the first column (column 0 in our case).

# In[3]:


csv_metadata[0] = csv_metadata[0].str.strip('#')
csv_metadata = csv_metadata.set_index(0)


# The data from the CSV file are transformed to a dictionary for an easy handling of the metadata.

# In[4]:


dict_metadata = csv_metadata.to_dict()[1]
dict_metadata


# The additional metadata can be obtained from the doi itself referenced in the metadata_link.

# In[5]:


# Opening JSON file
doi = dict_metadata['metadata_link'].strip('https://doi.org/')

with urllib.request.urlopen("https://api.datacite.org/dois/application/vnd.datacite.datacite+json/" + doi) as url:
    DOI_metadata = json.load(url)


# In[6]:


DOI_metadata


# It is now possible to add the relevant and rich DOI metadata to the simple metadata specific to the survey. Depending on the standard, the name of the field may differ. The example below shows how the metadata are transformed to NetCDF compliant metadata.
# 
# ## Getting the full metadata from the CSV file

# In[7]:


dict_metadata['title'] = DOI_metadata['titles'][0]['title']
dict_metadata['summary'] = DOI_metadata['descriptions'][0]['description']
dict_metadata['publisher_name'] = DOI_metadata['publisher']
dict_metadata['geospatial_lat_min'] = DOI_metadata['geoLocations'][0]['geoLocationBox']['southBoundLatitude']
dict_metadata['geospatial_lat_max'] = DOI_metadata['geoLocations'][0]['geoLocationBox']['northBoundLatitude']
dict_metadata['geospatial_lon_min'] = DOI_metadata['geoLocations'][0]['geoLocationBox']['westBoundLongitude']
dict_metadata['geospatial_lon_max'] = DOI_metadata['geoLocations'][0]['geoLocationBox']['eastBoundLongitude']
dict_metadata['comment'] = DOI_metadata['descriptions'][1]['description'] + DOI_metadata['descriptions'][2]['description']
dict_metadata['acknowledgement'] = DOI_metadata['fundingReferences'][0]['awardTitle']


# In[8]:


for i in range(0, len(DOI_metadata['dates'])):
    if DOI_metadata['dates'][i]['dateType']== 'Created':
        dict_metadata['date_created'] = DOI_metadata['dates'][i]['date']


# In[9]:


dict_metadata['keywords'] = ''
for i in range(0, len(DOI_metadata['subjects'])):
    if '"' not in DOI_metadata['subjects'][i]['subject']:
        dict_metadata['keywords'] = dict_metadata['keywords'] + DOI_metadata['subjects'][i]['subject'] + ', '
dict_metadata['keywords'] = dict_metadata['keywords'][:-2]


# In[10]:


dict_metadata


# ## Converting the CSV file to NetCDF with rich metadata
# 
# First, we will load the data, convert them to an array and convert them to NetCDF. 

# In[11]:


csv_data = pd.read_csv(CSV_file, skiprows=18, low_memory=False)


# After opening the data as a dataframe, we convert the data to an array using `xarray` library:

# In[12]:


xr = xarray.Dataset.from_dataframe(csv_data)


# We then add the attributes from our metadata dictionary that we just created.

# In[13]:


xr.attrs = dict_metadata
xr


# We can add the standard names and units for all the variables:

# In[14]:


name_dict = {}
for name, variables in xr.variables.items():
    xr[name].attrs['standard_name'] = name.split(' (')[0]
    xr[name].attrs['long_name'] = name.split(' (')[0]
    if '(' in name:
        xr[name].attrs['units'] = name.split(' (')[1][:-1]
    else:
        xr[name].attrs['units'] = ''
    name_dict[name] = name.split(' (')[0]
xr = xr.rename(name_dict=name_dict) 


# We save the data to NetCDF

# In[15]:


filename = CSV_file.strip('.csv')
xr.to_netcdf('%s.nc' %filename)


# # Checking completness of the metadata
# 
# It is possible to check the metadata completness thanks to the `compliance-checker` library

# In[16]:


from compliance_checker.runner import ComplianceChecker, CheckSuite

# Load all available checker classes
check_suite = CheckSuite()
check_suite.load_all_available_checkers()

# Run cf and adcc checks
path = filename + '.nc'
checker_names = ['cf', 'acdd']
verbose = 0
criteria = 'normal'
output_filename =  filename + '_report.json'
output_format = 'json'
"""
Inputs to ComplianceChecker.run_checker

path            Dataset location (url or file)
checker_names   List of string names to run, should match keys of checkers dict (empty list means run all)
verbose         Verbosity of the output (0, 1, 2)
criteria        Determines failure (lenient, normal, strict)
output_filename Path to the file for output
output_format   Format of the output

@returns                If the tests failed (based on the criteria)
"""
return_value, errors = ComplianceChecker.run_checker(path,
                                                     checker_names,
                                                     verbose,
                                                     criteria,
                                                     output_filename=output_filename,
                                                     output_format=output_format)

# Open the JSON output and get the compliance scores
with open(output_filename, 'r') as fp:
    cc_data = json.load(fp)
    for i in range(0, len(checker_names)):
        scored = cc_data[checker_names[i]]['scored_points']
        possible = cc_data[checker_names[i]]['possible_points']
        print('Convention: {} - CC Scored {} out of {} possible points'.format(checker_names[i], scored, possible))


# Although the CSV metadata are quite small, all the enriched metadata can be easily retrieved from the DOI metadata. The missing points are linked to parameters that are not referenced in the conventions cited.
