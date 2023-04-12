addpath (genpath('D:/British_Antarctic_Survey/Toolbox')); % set path for toolbox

cd 'D:/British_Antarctic_Survey/data/GRADES_IMAGE_0607/netcdf/' % tell MATLAB where the NetCDF file lives
ncdf_pth = 'D:/British_Antarctic_Survey/data/GRADES_IMAGE_0607/netcdf/GRADES_IMAGE_G06.nc'; % specify path of NetCDF
ncdisp(ncdf_pth) % display NetCDF metadata and variables
Source:
           D:\British_Antarctic_Survey\data\GRADES_IMAGE_0607\netcdf\GRADES_IMAGE_G06.nc

Format:
           netcdf4

Global Attributes:

title                    = 'Processed airborne radio-echo sounding data from the GRADES-IMAGE survey covering the Evans and Rutford Ice Streams, and ice rises in the Ronne Ice Shelf, West Antarctica (2006/2007)'

summary                  = 'An airborne radar survey was flown as part of the GRADES-IMAGE project funded by BAS over the Antarctic Peninsula, Ellsworth Mountains and Filchner-Ronne Ice Shelf (also including the Evans Ice stream and Carson Inlet) mainly to image englacial layers and bedrock topography during the 2006/07 field season.
Operating from temporary field camps at Sky Blu, Partiot Hills and out of RABID depot (Rutford Ice Stream), we collected ~27,550 km of airborne radio-echo sounding data over 100 hours of surveying.

Our aircraft was equipped with dual-frequency carrier-phase GPS for navigation, radar altimeter for surface mapping, wing-tip magnetometers, and a new ice-sounding radar system (PASIN). 
Note that there was no gravimetric element to this survey.
                                          
We present here the full radar dataset consisting of the deep-sounding chirp and shallow-sounding pulse-acquired data in their processed form, as well as the navigational information of each trace, the surface and bed elevation picks, ice thickness, and calculated absolute surface and bed elevations.

The radar data provided in this NetCDF is also provided separately as georeferenced SEGY files for import into seismic-interpretation software.    
                                          
Details of survey location and design are presentend in Jeoffry et al. 2018 (ESSD, 10,711-725).
More information on the radar system and processing can be found in Corr et al. 2007 (Terra Antartica Reports, 13, 55-63).'

history                  = 'This NetCDF contains the deep-sounding chirp and shallow-sounding pulse-acquired data (see the 'radar_parameters' attribute below) in the following structure:
'chirp_data': Radar data for the processed (coherent) chirp
'pulse_data': Radar data for the processed (incoherent) pulse
                                          
Both radar variables have the same length and contain the associated variables (see the variable attributes below for more details):
'traces': Trace number for the radar data (x axis)
'fast_time': Two-way travel time (y axis) (units: microseconds)
'x_coordinates': Cartesian x-coordinates  for the radar data (x axis) (units: meters in WGS84 EPSG:3031) 
'y_coordinates': Cartesian y-coordinates for the radar data (x axis) (units: meters in WGS84 EPSG:3031) 
                                          
Additionally, we also provide the associated surface and bed pick information, including the positioning and UTC time of each trace; 
                                          the aircraft, surface and bed elevation; the ice thickness; the PriNumber and the range from the aircraft to the ice surface.
                                          These variables are provided for each trace in the x-direction (with "-9999" representing missing data points).
                                      
Surface elevation is derived from radar altimeter for ground clearance < 750 m, and the PASIN system for higher altitudes.    
Positions are calculated for the phase centre of the aircraft antenna. All positions (Longitude, Latitude and Height) are referred to the WGS1984 ellipsoid.

The bed reflector was automatically depicted on the chirp data using a semi-automatic picker in the PROMAX software package. All the picks were afterwards checked and corrected by hand if necessary. The picked travel time was then converted to depth using a radar wave speed of 168 m/microseconds and a constant firn correction of 10 m. 
                                          
Note that the aircraft was flown at a constant terrain clearance of ~150 m to optimise radar data collection. 
The absolute position and altitude of the aircraft is derived from differentially processed GPS data.
                                          
The navigational position of each trace comes from the surface files, and the processed GPS files when no surface information was provided in the surface files. Note that for these, interpolation of the navigational data might have been required to match closely the Coordinated Universal Time (UTC) of each trace in the surface files. No data is shown as "-9999" throughout the files.
                                          
* Coordinates and Positions:
The coordinates provided in the NetCDF for the surface and bed elevation for each radar trace are in longitude and latitude (WGS84, EPSG: 4326). 
The navigation attributes for the radar data in the NetCDF are in projected X and Y coordinates (Polar Stereographic, EPSG: 3031), as follows:
                                          
Latitude of natural origin: -71
Longitude of natural origin: 0
Scale factor at natural origin: 0.994
False easting: 0
False northing: 2082760.109
                                          
--------------------------------------------------------------
Please read:
Previous versions of this dataset are available at the following link:
The surface and bed pick information (including surface and bed elevation, ice thickness, etc.) were previously published at: 
https://doi.org/10.5285/4efa688e-7659-4cbf-a72f-facac5d63998.
                                          
Note: 
These NetCDF and the associated georeferenced SEGY files provided here have been considerably curated and improved, and thus can be considered the latest and full dataset.
They contain all the information from the DOI link provided above, as well as the chirp and pulse radar data'

keywords                 = 'Antarctic, aerogeophysics, ice thickness, radar, surface elevation'
Conventions              = 'CF-1.8'
standard_name_vocabulary = 'CF Standard Name Table v77'
acknowlegement           = 'This work was funded by the British Antarctic Survey core program (Geology and Geophysics team), in support of the Natural Environment Research Council (NERC).'
institution              = 'British Antarctic Survey'
license                  = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'
location                 = 'Ronne Ice Shelf, West Antarctica'
instrument               = 'Polarimetric radar Airborne Science Instrument (PASIN)'
platform                 = 'BAS Twin Otter aircraft "Bravo Lima"'
source                   = 'Airborne ice penetrating radar'
time_coverage_start      = '2006-12-29'
time_coverage_end        = '2007-01-30'
flight                   = 'G06'
campaign                 = 'GRADES-IMAGE'
creator_name             = 'Corr, Hugh'
geospatial_lat_min       = '-67.95411'
geospatial_lat_max       = '-81.9457'
geospatial_lon_min       = '-61.292'
geospatial_lon_max       = '-88.96693'
radar_parameters         = 'Bistatic PASIN radar system operating with a centre frequency of 150 MHz and using two interleaved pulses:
Chirp: 4-microseconds, 10 MHz bandwidth linear chirp (deep sounding)
Pulse: 0.1-microseconds unmodulated pulse (shallow sounding)
Pulse Repetition Frequency: 15,635 Hz (pulse repetition interval: 64 microseconds)'
antenna                  = '8 folded dipole elements: 
4 transmitters (port side) 
4 receivers (starboard side)
Antenna gain: 11 dBi (with 4 elements)
Transmit power: 1 kW into each 4 antennae
Maximum transmit duty cycle: 10% at full power (4 x 1 kW)'
digitiser                = 'Radar receiver vertical sampling frequency: 22 MHz (resulting in sampling interval of 45.4546 ns) 
Receiver coherent stacking: 25
Receiver digital filtering: -50 dBc at Nyquist (11 MHz)
Effective PRF: 312.5 Hz (post-hardware stacking)
Sustained data rate: 10.56 Mbytes/second'
processing               = 'Chirp compression was applied using a Blackman window to minimise sidelobe levels, resulting in a processing gain of 10 dB. The chirp data was processed using an coherent averaging filter (commonly referred to as unfocused Synthetic Aperture Radar (SAR) processing) along a moving window of length 15. This product is best used to assess the bed and internals in deep ice conditions.
                                      
The pulse data was processed using an incoherent averaging filter along a moving window of length 25 and using a combination of the upper and lower channels. This product is best used to assess the internal structure and bed in shallow ice conditions.'
resolution               = 'Vertical resolution of the system (using velocity in ice of 168.5e6 microseconds): 8.4 m
Post-processing along-track resolution: ~20 m trace spacing'
GPS                      = 'Dual-frequency Leica 500 GPS. Absolute GPS positional accuracy: ~0.1 m (relative accuracy is one order of magnitude better). Banking angle was limited to 10deg during aircraft turns to avoid phase issues between GPS receiver and transmitter.'
projection               = 'WGS84 EPSG: 3031 Polar Stereographic South (71S,0E)'
references               = 'Jeofry, H., Ross, N., Corr, H.F., Li, J., Morlighem, M., Gogineni, P. and Siegert, M.J., 2018. A new bed elevation model for the Weddell Sea sector of the West Antarctic Ice Sheet. Earth System Science Data, 10(2), pp.711-725.doi: https://doi.org/10.5194/essd-10-711-2018'
metadata_link            = 'https://doi.org/10.5285/c7ea5697-87e3-4529-a0dd-089a2ed638fb'
related_datasets         = 'https://doi.org/10.5285/4efa688e-7659-4cbf-a72f-facac5d63998
https://doi.org/10.5285/7504be9b-93ba-44af-a17f-00c84554b819'
publisher_name           = 'UK Polar Data Centre'
publisher_type           = 'institution'
publisher_email          = 'polardatacentre@bas.ac.uk'
publisher_link           = 'https://www.bas.ac.uk/data/uk-pdc/'
comment                  = 'This dataset contains radar data for flightline G06 of the GRADES-IMAGE survey in NetCDF format'
Dimensions:
           traces    = 5584
           fast_time = 1400
Variables:
    traces                            
           Size:       5584x1
           Dimensions: traces
           Datatype:   int32
           Attributes:
                       long_name  = 'Trace number for the radar data (x axis)'
                       short_name = 'traceNum'
    fast_time                         
           Size:       1400x1
           Dimensions: fast_time
           Datatype:   single
           Attributes:
                       long_name     = 'Two-way travel time (y axis)'
                       standard_name = 'time'
                       units         = 'microseconds'
    x_coordinates                     
           Size:       5584x1
           Dimensions: traces
           Datatype:   double
           Attributes:
                       long_name     = 'Cartesian x-coordinates (WGS84 EPSG:3031) for the radar data'
                       standard_name = 'projection_x_coordinate'
                       units         = 'm'
    y_coordinates                     
           Size:       5584x1
           Dimensions: traces
           Datatype:   double
           Attributes:
                       long_name     = 'Cartesian y-coordinates (WGS84 EPSG:3031) for the radar data'
                       standard_name = 'projection_y_coordinate'
                       units         = 'm'
    chirp_data                        
           Size:       5584x1400
           Dimensions: traces,fast_time
           Datatype:   single
           Attributes:
                       long_name = 'Radar data for the processed (coherent) chirp'
                       units     = 'Power in decibel-milliwatts (dBm)'
    pulse_data                        
           Size:       5584x1400
           Dimensions: traces,fast_time
           Datatype:   single
           Attributes:
                       long_name = 'Radar data for the processed (incoherent) pulse'
                       units     = 'Power in decibel-milliwatts (dBm)'
    longitude_layerData               
           Size:       5584x1
           Dimensions: traces
           Datatype:   double
           Attributes:
                       long_name     = 'Longitudinal position of the trace number (coordinate system: WGS84 EPSG:4326)'
                       standard_name = 'longitude'
                       units         = 'degree_east'
    latitude_layerData                
           Size:       5584x1
           Dimensions: traces
           Datatype:   double
           Attributes:
                       long_name     = 'Latitudinal position of the trace number (coordinate system: WGS84 EPSG:4326)'
                       standard_name = 'latitude'
                       units         = 'degree_north'
    UTC_time_layerData                
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       long_name  = 'Coordinated Universal Time (UTC) of trace'
                       short_name = 'resTime'
                       units      = 'seconds'
    PriNumber_layerData               
           Size:       5584x1
           Dimensions: traces
           Datatype:   int32
           Attributes:
                       long_name  = 'The PRI number is an incremental integer reference number related to initialisation of the radar system that permits processed SEG-Y data and picked surface and bed to be linked back to raw radar data'
                       short_name = 'PriNum'
    terrainClearanceAircraft_layerData
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       _FillValue = -9999
                       long_name  = 'Terrain clearance distance from platform to air interface with ice, sea or ground'
                       short_name = 'resEht'
                       units      = 'm'
    aircraft_altitude_layerData       
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       _FillValue = -9999
                       long_name  = 'Aircraft altitude'
                       short_name = 'Eht'
                       units      = 'm relative to WGS84 ellipsoid'
    surface_altitude_layerData        
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       _FillValue    = -9999
                       long_name     = 'Ice surface elevation for the trace number from radar altimeter and LiDAR'
                       standard_name = 'surface_altitude'
                       short_name    = 'surfElev'
                       units         = 'm relative to the WGS84 ellipsoid'
    surface_pick_layerData            
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       _FillValue = -9999
                       long_name  = 'Location down trace of surface pick (BAS system)'
                       short_name = 'surfPickLoc'
                       units      = 'microseconds'
    bed_altitude_layerData            
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       _FillValue    = -9999
                       long_name     = 'Bedrock elevation for the trace number derived by subtracting ice thickness from surface elevation'
                       standard_name = 'bed_altitude'
                       short_name    = 'bedElev'
                       units         = 'm relative to the WGS84 ellipsoid'
    bed_pick_layerData                
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       _FillValue = -9999
                       long_name  = 'Location down trace of bed pick (BAS system)'
                       short_name = 'botPickLoc'
                       units      = 'microseconds'
    land_ice_thickness_layerData      
           Size:       5584x1
           Dimensions: traces
           Datatype:   single
           Attributes:
                       _FillValue    = -9999
                       long_name     = 'Ice thickness for the trace number obtained by multiplying the two-way travel-time between the picked ice surface and ice sheet bed by 168 m/microseconds and applying a 10 meter correction for the firn layer'
                       standard_name = 'land_ice_thickness'
                       short_name    = 'iceThick'
                       units         = 'm'
% open the NetCDF file
ncid = netcdf.open('GRADES_IMAGE_G06.nc','NC_NOWRITE');

% read NetCDF radar variables
traces_nc = ncread(ncdf_pth,'traces'); % read in traces array
chirpData = ncread(ncdf_pth,'chirp_data'); % read in chirp radar data array
pulseData = ncread(ncdf_pth,'pulse_data'); % read in pulse radar data array

chirpData = chirpData'; % rotate array in case the dimensions are the wrong way around
pulseData = pulseData'; % rotate array in case the dimensions are the wrong way around
chirpData = pow2db(chirpData); % convert the data from power to decibels using log function for visualisation
pulseData = pow2db(pulseData); % convert the data from power to decibels using log function for visualisation

% X and Y coordinates
x_nc = ncread(ncdf_pth,'x_coordinates'); % read in x positions array (Polar Stereographic EPSG 3031)
y_nc = ncread(ncdf_pth,'y_coordinates'); % read in y positions array (Polar Stereographic EPSG 3031)
x_nc_km = x_nc/1000; % transform meters to kilometers
y_nc_km = y_nc/1000; % transform meters to kilometers

% surface and bed picks
surface_pick = ncread(ncdf_pth,'surface_pick_layerData'); % read in surface pick array
bed_pick = ncread(ncdf_pth,'bed_pick_layerData'); % read in bed pick array
surface_pick (surface_pick==-9999) = NaN; % convert -9999 to NaNs for plotting
bed_pick (bed_pick==-9999) = NaN; % convert -9999 to NaNs for plotting

% surface and bed elevations
surface_elevation = ncread(ncdf_pth,'surface_altitude_layerData'); % read in surface altitude array
bed_elevation = ncread(ncdf_pth,'bed_altitude_layerData'); % read in bed altitude array
surface_elevation (surface_elevation==-9999) = NaN; % convert -9999 to NaNs for plotting
bed_elevation (bed_pick==-9999) = NaN; % convert -9999 to NaNs for plotting

figure;
imagesc([traces_nc],[], chirpData(1:600,:)) % plot radar data (limit y-axis extent)
hold on
plot(traces_nc,surface_pick, 'color', 'r','LineStyle','--','LineWidth',1.5) % plot surface pick
plot(traces_nc,bed_pick, 'color', 'b','LineStyle','--','LineWidth',1.5) % plot bed pick
colormap(flipud(gray)); % get gray colormap (max values = black, min values = white)
title('Radar Data - Chirp (NetCDF)', 'FontSize', 14); % set title
xlabel('Trace Number','FontSize',10); % set axis title
ylabel('Fast Time Sample Number','FontSize',10); % set axis title
colorbar % plot colorbar
caxis([10 60]) % limit colorbar values
hold off

figure;
imagesc([traces_nc],[], pulseData(1:600,:)) % plot radar data (limit y-axis extent)
hold on
plot(traces_nc,surface_pick, 'color', 'r','LineStyle','--','LineWidth',1.5) % plot surface pick
plot(traces_nc,bed_pick, 'color', 'b','LineStyle','--','LineWidth',1.5) % plot bed pick
colormap(flipud(gray)); % get gray colormap (max values = black, min values = white)
title('Radar Data - Pulse (NetCDF)', 'FontSize', 14); % set title
xlabel('Trace Number','FontSize',10); % set axis title
ylabel('Fast Time Sample Number','FontSize',10); % set axis title
colorbar % plot colorbar
hold off

figure;

% first plot the radargram with specific trace marked as red vertical line
subplot(1,2,1)
imagesc([traces_nc],[], pulseData(1:600,:)) % plot radar data (limit y-axis extent)
hold on
plot(traces_nc,surface_pick, 'color', 'r','LineStyle','--','LineWidth',1.5) % plot surface pick
plot(traces_nc,bed_pick, 'color', 'b','LineStyle','--','LineWidth',1.5) % plot bed pick
xline(1850,'Color','r', 'LineWidth',1.2) % plot position of trace in second plot
colormap(flipud(gray)); % get gray colormap (max values = black, min values = white)
title('Radar Data - Pulse (NetCDF)', 'FontSize', 14); % set title
xlabel('Trace Number','FontSize',10); % set axis title
ylabel('Fast Time Sample Number','FontSize',10); % set axis title
colorbar % plot colorbar
hold on

% then plot trace plot with amplitude and sampling window
subplot(1,2,2)
plot(chirpData(1:600, 1850)) % plot surface pick
title('Trace 1850 - Radar Data', 'FontSize', 14)  % set title
xlabel('Fast Time Sample Number', 'Fontsize', 10) % set axis title
ylabel('Amplitude (dB)', 'FontSize', 10) % set axis title
ax = gca; % get axis
axis(ax, 'tight') % control axes
xlim(ax, xlim(ax) + [-1,1]*range(xlim(ax)).* 0.05) % add white space before and after data for aesthetic
ylim(ax, ylim(ax) + [-1,1]*range(ylim(ax)).* 0.05) % add white space before and after data for aesthetic
hold off

figure;
plot(x_nc_km, y_nc_km,'color', [0, 0.4470, 0.7410],'LineWidth',2.4) % plot entire profile
hold on
scatter (x_nc_km(1850), y_nc_km(1850), 60,'o', 'MarkerFaceColor', 'r') % plot specific trace position as red dot
title('Position of Trace 1850', 'FontSize', 14)  % set title
xlabel('X (km)','FontSize',10); % set axis title
ylabel('Y (km)','FontSize',10); % set axis title
hold off

figure;
plot(traces_nc, surface_elevation,'color', [0, 0.4470, 0.7410],'LineWidth',1.5) % plot surface elevation for entire profile
hold on
plot(traces_nc, bed_elevation,'color', [0.9290 0.6940 0.1250],'LineWidth',1.5) % plot bed elevation for entire profile
title('Elevation Profile for flightline G06', 'FontSize', 14)  % set title
xlabel('Trace Number','FontSize',10); % set axis title
ylabel('Elevation (meters WGS84)','FontSize',10); % set axis title
ylim([-1800 400]) % set y-axis limits
hold off
ax = gca; % get axis
axis(ax, 'tight') % control axes
xlim(ax, xlim(ax) + [-1,1]*range(xlim(ax)).* 0.05) % add white space before and after data for aesthetic
ylim(ax, ylim(ax) + [-1,1]*range(ylim(ax)).* 0.05) % add white space before and after data for aesthetic

segy_data_chirp = 'D:/British_Antarctic_Survey/data/GRADES_IMAGE_0607/segy/chirp/G06_chirp.segy'
segy_data_pulse = 'D:/British_Antarctic_Survey/data/GRADES_IMAGE_0607/segy/pulse/G06_pulse.segy'

[segy_chirp,SegyTraceHeaders,SegyHeader] = ReadSegy(segy_data_chirp); % read chirp data as well as byte header information
[segy_pulse] = ReadSegy(segy_data_pulse); % read pulse data only (byte header information can be added as above if needed)

segy_chirp = pow2db(segy_chirp); % convert the data from power to decibels using log function for visualisation
segy_pulse = pow2db(segy_pulse); % convert the data from power to decibels using log function for visualisation

SegyHeader % read SEG-Y header
SegyHeader = 

  struct with fields:

                          Rev: [1×2 struct]
            TextualFileHeader: [3200×1 double]
                          Job: 0
                         Line: 0
                         Reel: 0
         DataTracePerEnsemble: 0
    AuxiliaryTracePerEnsemble: 0
                           dt: 1000
                       dtOrig: 0
                           ns: 1400
                       nsOrig: 0
             DataSampleFormat: 5
                 EnsembleFold: 0
                 TraceSorting: 0
              VerticalSumCode: 0
          SweepFrequencyStart: 0
            SweepFrequencyEnd: 0
                  SweepLength: 0
                    SweepType: 0
                 SweepChannel: 0
        SweepTaperlengthStart: 0
          SweepTaperLengthEnd: 0
                    TaperType: 0
         CorrelatedDataTraces: 0
                   BinaryGain: 0
      AmplitudeRecoveryMethod: 0
            MeasurementSystem: 1
        ImpulseSignalPolarity: 0
        VibratoryPolarityCode: 0
                  Unassigned1: [120×1 double]
     SegyFormatRevisionNumber: 100
         FixedLengthTraceFlag: 1
    NumberOfExtTextualHeaders: 0
                  Unassigned2: [47×1 double]
                         time: [1×1400 double]
trace = SegyTraceHeaders(1)
  struct with fields:

                        SegyMAT_TraceStart: 3600
                         TraceSequenceLine: 1
                         TraceSequenceFile: 1
                               FieldRecord: 1180200
                               TraceNumber: 1
                         EnergySourcePoint: 1
                                       cdp: 0
                                  cdpTrace: 0
                   TraceIdenitifactionCode: 1
                             NSummedTraces: 0
                            NStackedTraces: 1
                                   DataUse: 0
                                    offset: 0
                    ReceiverGroupElevation: 0
                    SourceSurfaceElevation: 0
                               SourceDepth: 0
                    ReceiverDatumElevation: 0
                      SourceDatumElevation: 0
                          SourceWaterDepth: 0
                           GroupWaterDepth: 0
                           ElevationScalar: 0
                         SourceGroupScalar: 0
                                   SourceX: -1270361
                                   SourceY: 140850
                                    GroupX: 0
                                    GroupY: 0
                           CoordinateUnits: 0
                        WeatheringVelocity: 0
                     SubWeatheringVelocity: 0
                          SourceUpholeTime: 0
                           GroupUpholeTime: 0
                    SourceStaticCorrection: 0
                     GroupStaticCorrection: 0
                        TotalStaticApplied: 0
                                  LagTimeA: 0
                                  LagTimeB: 0
                        DelayRecordingTime: 0
                             MuteTimeStart: 0
                               MuteTimeEND: 0
                                        ns: 1400
                                        dt: 45
                                  GainType: 0
                    InstrumentGainConstant: 0
                     InstrumentInitialGain: 0
                                Correlated: 0
                       SweepFrequenceStart: 0
                         SweepFrequenceEnd: 0
                               SweepLength: 0
                                 SweepType: 0
                SweepTraceTaperLengthStart: 0
                  SweepTraceTaperLengthEnd: 0
                                 TaperType: 0
                      AliasFilterFrequency: 0
                          AliasFilterSlope: 0
                      NotchFilterFrequency: 0
                          NotchFilterSlope: 0
                           LowCutFrequency: 0
                          HighCutFrequency: 0
                               LowCutSlope: 0
                              HighCutSlope: 0
                          YearDataRecorded: 2021
                                 DayOfYear: 273
                                 HourOfDay: 3
                              MinuteOfHour: 14
                            SecondOfMinute: 8
                              TimeBaseCode: 0
                     TraceWeightningFactor: 0
                  GeophoneGroupNumberRoll1: 0
    GeophoneGroupNumberFirstTraceOrigField: 0
     GeophoneGroupNumberLastTraceOrigField: 0
                                   GapSize: 0
                                OverTravel: 0
                                      cdpX: 0
                                      cdpY: 0
                                  Inline3D: 0
                               Crossline3D: 0
                                 ShotPoint: 0
                           ShotPointScalar: 0
                 TraceValueMeasurementUnit: 0
              TransductionConstantMantissa: 0
                 TransductionConstantPower: 0
                          TransductionUnit: 0
                           TraceIdentifier: 0
                         ScalarTraceHeader: 0
                                SourceType: 0
             SourceEnergyDirectionMantissa: 0
             SourceEnergyDirectionExponent: 0
                 SourceMeasurementMantissa: 0
                 SourceMeasurementExponent: 0
                     SourceMeasurementUnit: 0
                            UnassignedInt1: 0
                            UnassignedInt2: 0
                    SegyMAT_TraceDataStart: 3840
traces = ReadSegyTraceHeaderValue(segy_data_chirp,'key','TraceSequenceLine');
traces_length = length(traces) % get length of traces variable

x_segy = ReadSegyTraceHeaderValue(segy_data_chirp,'key','SourceX'); % Careful: this in meters and rounded to nearest integer
y_segy = ReadSegyTraceHeaderValue(segy_data_chirp,'key','SourceY'); % Careful: this in meters and rounded to nearest integer

finally, let's read in the PRINumber stored in the SEG-Y

PRInum = ReadSegyTraceHeaderValue(segy_data_chirp,'key','FieldRecord');

figure;
imagesc([traces],[], segy_chirp(1:600,:)) % plot radar data (limit y-axis extent)
colormap(flipud(gray)); % get gray colormap (max values = black, min values = white)
title('Radar Data - Chirp (SEG-Y)', 'FontSize', 14); % set title
xlabel('Trace Number','FontSize',10); % set axis title
ylabel('Fast Time Sample Number','FontSize',10); % set axis title
colorbar % plot colorbar
caxis([10 60]) % limit colorbar values

figure;
imagesc([traces],[], segy_pulse(1:600,:)) % plot radar data (limit y-axis extent)
colormap(flipud(gray)); % get gray colormap (max values = black, min values = white)
title('Radar Data - Pulse (SEG-Y)', 'FontSize', 14); % set title
xlabel('Trace Number','FontSize',10); % set axis title
ylabel('Fast Time Sample Number','FontSize',10); % set axis title
colorbar % plot colorbar
