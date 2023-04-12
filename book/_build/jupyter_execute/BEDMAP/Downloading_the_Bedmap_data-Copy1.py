#!/usr/bin/env python
# coding: utf-8

# # Downloading the Bedmap data
# 
# This Jupyter Notebook shows how to download the Bedmap products either via Ramadda or programmatically. 
# 
# 
# ## List of data available for download
# 
# The complete list of data available as part of Bedmap is available here: https://antarctica.github.io/PDC_GeophysicsBook/BEDMAP/data_available.html
# 
#  The Bedmap CSV files are available for download from the UK Polar data Centre:
# 
# * BEDMAP1 CSV: https://doi.org/10.5285/f64815ec-4077-4432-9f55-0ce230f46029
# 
# * BEDMAP2 CSV: https://doi.org/10.5285/2fd95199-365e-4da1-ae26-3b6d48b3e6ac
# 
# * BEDMAP3 CSV: https://doi.org/10.5285/91523ff9-d621-46b3-87f7-ffb6efcd1847
# 
# The Bedmap shapefiles/geopackages points and lines data are also available from the UK Polar Data Centre:
# 
# * Bedmap1 statistically-summarised data points (shapefiles): https://doi.org/10.5285/925AC4EC-2A9D-461A-BFAA-6314EB0888C8
# 
# * Bedmap2 statistically-summarised data points (shapefiles): https://doi.org/10.5285/0F90D926-99CE-43C9-B536-0C7791D1728B
# 
# * Bedmap3 statistically-summarised data points (shapefiles): https://doi.org/10.5285/A72A50C6-A829-4E12-9F9A-5A683A1ACC4A
# 
# 
# ## Downloading the data via the Ramadda interface
# 
# From the metadata page accessible via the DOI, it is possible to access the data by clicking on 'GET DATA'. You will then be redirected to our Ramadda repository. 
# 
# From the interface, it is possible to download the data individually by clicking on the dataset you want to download. It is also possible to zip and download the data together by clickng at the top of the ramadda interface on the down arrow next to "Polar Data Centre > DOI" and Zip and Download Tree:
# 
# ![download](../images/Ramadda_download.PNG)
# 
# Rammadda also allows to select the files you want to download: you will need to click on the little icon at the top left corner of the table containing the list of data to download, select the list of data you want to download and Apply the action you want from the drop down list: 
# 
# ![download_select](../images/Ramadda_download_select.PNG)
# 
# ### /!\ The feature to zip and download all the datasets does not work for Bedmap3 due to the size. We are working at the PDC to make this feature available again.
# 
# ## Downloading the data via wget command
# 
# Please find below the different command to download the Bedmap datasets:
# 
# * Downloading Bedmap1 CSV and shapepoints:

# wget https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=f64815ec-4077-4432-9f55-0ce230f46029&output=zip.tree

# wget https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=925ac4ec-2a9d-461a-bfaa-6314eb0888c8&output=zip.tree

# * Downloading Bedmap2 CSV and shapepoints:

# wget https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=2fd95199-365e-4da1-ae26-3b6d48b3e6ac&output=zip.tree

# wget https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=0f90d926-99ce-43c9-b536-0c7791d1728b&output=zip.tree

# * Downloading Bedmap3 CSV and shapefiles:
# 
# Due to the size of the dataset and limitations on Ramadda (that we are trying to resolve), it is not possible to download the dataset with a single URL. You will need to download the following file containing the list of files to download:  [Bedmap3_csv_list.txt](../images/Bedmap3_csv_list.txt) and run:

# wget -i Bedmap3_csv_list.txt

# The same applies for the shapepoints and lines, you will need to download the following file: [Bedmap3_shapefiles_gpkg_list.txt](../images/Bedmap3_shapefiles_gpkg_list.txt) and run:

# wget -i Bedmap3_shapefiles_gpkg_list.txt

# ## Downloading the data with python

# In[1]:


import os
import requests
from bs4 import BeautifulSoup


#  First we will show how to download the CSV data and then the statistically-summarised points.
#  
#  ## Downloading the CSV files
#  
#  To download the CSV file, you will need the doi of the data you want to downlolad:
#  
#  The BEDMAP CSV files are available for download from the UK Polar data Centre:
# 
# * BEDMAP1 CSV: https://doi.org/10.5285/f64815ec-4077-4432-9f55-0ce230f46029
# 
# * BEDMAP2 CSV: https://doi.org/10.5285/2fd95199-365e-4da1-ae26-3b6d48b3e6ac
# 
# * BEDMAP3 CSV: https://doi.org/10.5285/91523ff9-d621-46b3-87f7-ffb6efcd1847
# 
# We present here how the data from Bedmap3 can be downloaded:
# 
# 

# #1. Enter the doi of the data you want to download in the box below:

# In[2]:


doi = 'https://doi.org/10.5285/91523ff9-d621-46b3-87f7-ffb6efcd1847'


# In[3]:


data_link = 'https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=' + doi.split('/')[-1]
reqs = requests.get(data_link)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
urls = []
for link in soup.find_all('a'):
    urls.append(link.get('href'))


# The list of URLs corresponding to the data download is obtained as follows:

# In[4]:


url_to_download = [x for x in urls if x.startswith('/repository/entry/get/')]
url_to_download = ['https://ramadda.data.bas.ac.uk' + x for x in url_to_download]
print('\n'.join(url_to_download))


# The list can be used for a `wget` command directly. We detail below how to download the data in python:

# In[5]:


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    filename = filename.split('.csv')[0] + '.csv'
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


#  #2. Enter the destination folder of the data (where the data will be saved) in the box below:

# In[6]:


destination_folder = 'D:/BEDMAP/bedmap3_csv'


# In[7]:


#To download all the data, run the following command:
for i in range(0, len(url_to_download)):
    download(url_to_download[i], destination_folder)


# The data are directly saved in the destination folder.

# ## Downloading statistically-summarised data points and lines
# 
#  To download the points and lines file, you will need the doi of the data you want to downlolad:
# 
# The BEDMAP CSV files are available for download from the UK Polar data Centre:
# - Bedmap1 statistically-summarised data points (shapefiles): https://doi.org/10.5285/925AC4EC-2A9D-461A-BFAA-6314EB0888C8
# - Bedmap2 statistically-summarised data points (shapefiles): https://doi.org/10.5285/0F90D926-99CE-43C9-B536-0C7791D1728B
# - Bedmap3 statistically-summarised data points (shapefiles): https://doi.org/10.5285/A72A50C6-A829-4E12-9F9A-5A683A1ACC4A
# 
# We present here how the points/lines data from Bedmap3 can be downloaded:

# #1. Enter the doi of the data you want to download in the box below:

# In[8]:


doi = 'https://doi.org/10.5285/a72a50c6-a829-4e12-9f9a-5a683a1acc4a'
data_link = 'https://ramadda.data.bas.ac.uk/repository/entry/show?entryid=' + doi.split('/')[-1]
reqs = requests.get(data_link)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
urls = []
for link in soup.find_all('a'):
    urls.append(link.get('href'))


# In[9]:


url_to_institute_subfolders = [x for x in urls if x.startswith('/repository/entry/show?entryid=synth%') and '&' not in x]
url_to_institute_subfolders = ['https://ramadda.data.bas.ac.uk' + x for x in url_to_institute_subfolders]
url_to_institute_subfolders = list(set(url_to_institute_subfolders))


# In[10]:


urls_institute = []
for j in range(0, len(url_to_institute_subfolders)):
    reqs = requests.get(url_to_institute_subfolders[j])
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for link in soup.find_all('a'):
        urls_institute.append(link.get('href'))
urls_institute = list(set(urls_institute))


# The list of URLs corresponding to the data download is obtained as follows:

# In[11]:


url_to_download = [x for x in urls_institute if 'zip.tree' in x]
url_to_download = ['https://ramadda.data.bas.ac.uk' + x for x in url_to_download]
print('\n'.join(url_to_download))


# The list can be used for a `wget` command directly. We detail below how to download the data in python:

# #2. Enter the destination folder of the data (where the data will be saved) in the box below:

# In[12]:


destination_folder = 'D:/BEDMAP/bedmap3_points_lines'


# In[13]:


#To download all the data, run the following command:
for i in range(0, len(url_to_download)):
    download(url_to_download[i], destination_folder)

