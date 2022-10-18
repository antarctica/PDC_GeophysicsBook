##/usr/bin/env python
# encoding: utf-8
"""
projection.py
Created by Cécile Agosta on 2014-05-17.
Copyright (c) 2013 __ULg__. All rights reserved.
"""
# = IMPORT MODULES ========================================================== #
from __future__ import division # true division
import operator
import pandas as pd # Python Data Analysis Library
import numpy as np # array module
from numpy import *
# ========================================================================== #

def stereosouth_lonlat2xy(lon_list,lat_list):
    lon,lat = np.array(lon_list),np.array(lat_list)
    # Constants
    aa = 6378.1370         # aa (km) = demi grand axe
    ex = 0.081819190842621 # excentricity
    trulat = -71.          # True distance latitude (S)
    lonE   =  90.          # Longitude of the x-axis  
    Fxx = 0.               # False Easting
    Fyy = 0.               # False Northing
    degrad = pi/180.
    # Computation
    latF   =    trulat*degrad  # Latitude of standard paraLLel, 71 for ESPG 3031  
    lon0   = (lonE-90)*degrad
    lonrad = lon *degrad
    latrad = lat *degrad
    # +
    # +- Polar Stereographic Projection
    # +  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # +
    tF = tan(pi/4+latF/2) / ( ( 1 + ex*sin(latF) ) / ( 1 - ex*sin(latF)) )**(ex/2)
    mF = cos(latF) / ( 1 - ex**2 * sin(latF)**2 )**0.5
    t  = tan(pi/4+latrad/2) / ( (1 + ex*sin(latrad)) / (1 - ex*sin(latrad)))**(ex/2)
    # print tF,mF,t
    rho = aa*t*mF/tF # A VOIR : Facteur x 2 ??
    xx = Fxx + rho*sin(lonrad - lon0)
    yy = Fyy + rho*cos(lonrad - lon0)
    return xx,yy

def stereosouth_xy2lonlat(xx_list,yy_list):
    """
    +----------------------------------------------------------------------+
    |  Compute the lon, lat from Oblique Stereographic Projection          |
    |  Written by Cecile Agosta                                 17-05-10   |
    |  EPSG Polar Stereographic transformation Variant B                   |
    |  (http://www.epsg.org/guides/docs/G7-2.pdf)                          |
    |  Equivalent to EPSG 3031 (WGS-84 ellipsoid)                          |
    ! +--------------------------------------------------------------------+
    |                                                                      |
    | INPUT :  xx     : Stereo coordinate on the East  (X, km)             |
    | ^^^^^^^  yy      : Stereo coordinate on the North (Y, km)            |
    |          lonE : Longitude of X axis (90 = East, clockwise)           |
    |         [lat true = 71 S]                                            |
    |                                                                      |
    | OUTPUT : lon    : longitude (deg)                                    |
    | ^^^^^^^  lat    : latitude  (deg)                                    |
    +----------------------------------------------------------------------+
    """
    xx ,yy = np.array(xx_list),np.array(yy_list)
    # Constants
    aa = 6378.1370         # aa (km) = demi grand axe
    ex = 0.081819190842621 # excentricity WGS-84 : 0.081 819 190 842 622 0.081 819 190 842 621
    trulat = -71.          # True distance latitude (S), 71 S for ESPG 3031
    lonE   =  90.          # Longitude of the x-axis  
    Fxx = 0.               # False Easting
    Fyy = 0.               # False Northing
    degrad = pi/180.
    # Computation
    latF = trulat*degrad
    lon0 = (lonE - 90.)*degrad
    tF = tan (pi/4 + latF/2) / ( (1 + ex*sin(latF)) / (1 - ex*sin(latF)) )**(ex/2)
    mF = cos(latF) / (1 - ex**2 * sin(latF)**2)**0.5
    k0 = mF * ( (1+ex)**(1+ex) * (1-ex)**(1-ex) )**0.5 / (2*tF)
    # +
    # +- Polar Stereographic Projection
    # +  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # +
    rho = ( (xx-Fxx)**2 + (yy-Fyy)**2 )**0.5
    t   = rho * ( (1+ex)**(1+ex) * (1-ex)**(1-ex) )**0.5 / (2*aa*k0)
    khi = 2*arctan(t) - pi/2
    #
    lat = khi + \
            (  ex**2/2 +  5*ex**4/24  + ex**6/12 + 13*ex**8/360) * sin(2*khi) + \
            (7*ex**4/48 + 29*ex**6/240 + 811*ex**8/11520) *sin(4*khi) + \
            (7*ex**6/120 + 81*ex**8/1120) * sin(6*khi) + \
            (4279*ex**8/161280) * sin(8*khi)
    #
    lon = []
    for x,y in zip(xx,yy):
        if (x-Fxx==0.) & (y-Fyy==0):
            lon.append(lon0 + pi/2.)
        elif (x-Fxx==0.) & (y-Fyy==0):
            lon.append(lon0)
        elif (x-Fxx==0.) & (y-Fyy==0):
            lon.append(lon0 - pi)
        else:
            lon.append(lon0 + arctan2(x-Fxx,y-Fyy))
    lon = np.array(lon)
    
    lat = lat / degrad
    lon = lon / degrad
    
    lon[lon>180.] = lon[lon>180.] - 360.
    lon[lon<-180.] = lon[lon<-180.] + 360.
    #
    return lon, lat


