# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:39:07 2019

@author: BenPurinton purinton[at]uni-potsdam.de
"""

# This Python script is intended for taking Leica .m00 files, translating them
# to RINEX (.obs / .nav) files with TEQC, reading the day-of-year and GPS week
# from the file headers, downloading the appropriate correction files from the 
# IGS FTP servers, correcting the data using the rnx2rtkp CUI included with 
# RTKLIB, and outputing a .csv and .shp of the results.

# The code may be modified by the interested user for converting different file
# formats than .m00 from Leica, using your own base station, or other neat things.
# We leave these advanced steps to the user, but the code is well commented and 
# I am available via email for troubleshooting.

import os, sys, subprocess, shutil, datetime, glob, csv
import gnsscal # see: https://pypi.org/project/gnsscal/
import ftplib as ftp
import numpy as np 
from osgeo import ogr, osr
    
#%%
# =============================================================================
#  set these parameters
# =============================================================================

# base directory to the leica dGPS files
bd = 'C:/Users/BenPurinton/Dropbox/GITHUB/GNSS-Correction-RTKLIB/example_python/'

# four letter code of the nearest base station to download observation data (UNSA, POTS, etc.)
base_stn = 'UNSA'

# proj4 projection string for outputting a UTM shapefile, here we use WGS84/UTM19S for part of NW Argentina
spatial_ref = 'PROJCS["WGS 84 / UTM zone 19S",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-69],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",10000000],AUTHORITY["EPSG","32719"],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'

# the UTM zone for file naming
utmzone = 'utm19s'

# path to the configuration file that sets the options for RTKPOST
rtkconf = 'C:/Users/BenPurinton/Dropbox/GITHUB/GNSS-Correction-RTKLIB/scripts/rnx2rtkp_options.conf'

# the functions we use for subprocess calls to the commmand-line
sevenzip = 'C:/Program Files/7-Zip/7z' #make sure 7zip is installed
rnx2rtkp = 'C:/rtklib_2.4.2/bin/rnx2rtkp' #make sure RTKLIB is installed
crnx2rnx = 'C:/rtklib_2.4.2/bin/crx2rnx' # need this function to change base files from crinex to rinex
teqc = 'C:/rtklib_2.4.2/bin/teqc' # teqc conversion software

# path to output all files to, as a sub-directory of the base directory, probably leave this alone
out_path = bd + 'corrected/'

#%%
# =============================================================================
# convert the data with teqc and get the list of RINEX files to process
# =============================================================================

# create processing directory
if not os.path.exists(out_path):
    os.makedirs(out_path)

# get a list of the files (in sub-directories and in the base directory)
files = []
for file in glob.glob(bd + '*/*.m00'):
    file = file.replace('\\','/')
    files.append(file)
for file in glob.glob(bd + '*.m00'):
    file = file.replace('\\','/')
    files.append(file)
# convert files to rinex
for file in files:
    filename = file.split('/')[-1].split('.m00')[0]
    if not os.path.exists(out_path + filename + '.obs'):
        print("Converting {} to RINEX".format(filename))
        cmd = teqc + ' +obs ' + out_path + filename + '.obs ' + '+nav ' + \
                out_path + filename + '.nav ' + file
        subprocess.call(cmd, shell=False)
#%%
# list of rinex files to process
rinex_files = []
print("\nRINEX files to process:")
for file in os.listdir(out_path):
    if file.endswith('.obs'):
        name = file.split('.obs')[0]
        print(name)
        rinex_files.append(name)
        
#%%
# =============================================================================
# the functions
# =============================================================================

def download_corr_files(out_path, base_stn, obs, nav, sevenzip):
    """
    This function downloads the necessary base station and satellite files (broadcast/orbits)
    for correcting raw rinex files using rtkpost.
    """
    
    # file root name
    name = obs.split('.obs')[0]
    
    # first we need the year, doy, and GPS week from the observations file
    f = open(out_path + obs, 'r').read()
    print("Downloading correction data for {}".format(obs))
    lines = f.strip().splitlines()
    for l in lines:
        # read from RINEX header
        if l.endswith('TIME OF FIRST OBS'):
            var = l.split()
            yr = var[0]
            # use datetime and gnsscal to convert the date to doy and gps week
            date = datetime.date(int(yr), int(var[1]), int(var[2]))
            doy = str(gnsscal.date2doy(date))
            if not len(doy) == 3: # add the leading 0 if DOY is < 3 digits
                doy = '0' + doy
            week = str(gnsscal.date2gpswd(date)[0]) + str(gnsscal.date2gpswd(date)[1])
    
    # create a new folder to hold the correction data and move the rinex files into it
    path = out_path + yr + doy + '_' + name + '/'
    if not os.path.exists(path):
        os.mkdir(path)
        shutil.move(out_path + obs, path + obs)
        shutil.move(out_path + nav, path + nav)
    
    # download the base station observations, broadcast navigation, and satellite orbital clocks
    # NOTE: we log into and out of the FTP server each time to avoid some hang-ups in downloading
    # also this could allow for replacement of the server to different locations for each file
    
    # connect to the FTP for getting the base station observations
    f = ftp.FTP('igs.ensg.ign.fr')
    try:
        f.login()
        print('logged into ftp')
    except:
        print('hmm couldn\'t connect to base station ftp. no internet?')
        sys.exit()
    # navigate to the directory
    f.cwd('/pub/igs/data/' + yr + '/' + doy + '/') 
    # download the base station using the leading identifier and wildcards
    # note we use the 30 second decimated data (*30S* wildcard below), this is
    # available for most sites
    filematch = base_stn + '*30S*.crx.gz' 
    for filename in f.nlst(filematch):
        target_file_name = os.path.join(path,os.path.basename(filename))
        with open(target_file_name,'wb') as fhandle:
                f.retrbinary('RETR %s' %filename, fhandle.write)
                # quit and close server connection
                f.quit()
                f.close()
    #also unzip the file with 7zip
    cmd = '"' + sevenzip + '"' + ' e ' + path + filename + ' -o' + path 
    subprocess.call(cmd, shell=False)
    # change the file name and convert to rinex with crnx2rnx
    shutil.move(path + filename.split('.gz')[0], path + filename.split('crx')[0] + yr[2:] + 'd')
    cmd = crnx2rnx + ' ' + path + filename.split('crx')[0] + yr[2:] + 'd'
    subprocess.call(cmd, shell=False)
    # final filename
    baseSTN = path + filename.split('crx')[0] + yr[2:] + 'o'
    
    # grab the broadcast navigation data from the same directory
    f = ftp.FTP('igs.ensg.ign.fr')
    try:
        f.login()
        print('logged into ftp')
    except:
        print('hmm couldn\'t connect to base station ftp. no internet?')
        sys.exit()
    # navigate to the directory
    f.cwd('/pub/igs/data/' + yr + '/' + doy + '/') 
    # get the filematch
    filename = 'brdc' + doy + '0.' + yr[2:] + 'n.Z'
    target_file_name = os.path.join(path,os.path.basename(filename))
    with open(target_file_name,'wb') as fhandle:
        f.retrbinary('RETR %s' %filename, fhandle.write)
        # quit and close server connection
        f.quit()
        f.close()
    # unzip with 7zip
    cmd = '"' + sevenzip + '"' + ' e ' + path + filename + ' -o' + path 
    subprocess.call(cmd, shell=False)
    # final filename
    brdc = target_file_name.split('.Z')[0]
    
    # finally grab the satellite precise orbits from a different directory
    f = ftp.FTP('igs.ensg.ign.fr')
    try:
        f.login()
        print('logged into ftp')
    except:
        print('hmm couldn\'t connect to base station ftp. no internet?')
        sys.exit()
    # navigate to the directory
    f.cwd('/pub/igs/products/' + week[0:4] + '/')
    # we try with the rapid orbits, if they're available
    try:
        filename = 'igr' + week + '.sp3.Z'
        target_file_name = os.path.join(path,os.path.basename(filename))
        with open(target_file_name,'wb') as fhandle:
            f.retrbinary('RETR %s' %filename, fhandle.write)
    # retry with the ultra-rapid orbits if that didn't work
    except:
        filename = 'igu' + week + '_18.sp3.Z' # arbitrarily taking the final ultra-rapid file (18:00)
        target_file_name = os.path.join(path,os.path.basename(filename))
        with open(target_file_name,'wb') as fhandle:
            f.retrbinary('RETR %s' %filename, fhandle.write)
    # unzip with 7zip    
    cmd = '"' + sevenzip + '"' + ' e ' + path + filename + ' -o' + path 
    subprocess.call(cmd, shell=False)
    # final filename
    orbits = target_file_name.split('.Z')[0]
    # quit and close server connection for good
    f.quit()
    f.close()
        
    return yr, doy, week, baseSTN, brdc, orbits
        
#%%
def MakeShape(shapename):
    """
    This function creates a new shapefile with all the appropriate fields for filling
    with the .pos files output by rtkpost. Returns the shape and layer info to pass into next function.
    """
    
    driver = ogr.GetDriverByName('ESRI Shapefile') # get shapefile driver
    shapeData = driver.CreateDataSource(shapename) # open the file that will hold our shapefile
    cs = osr.SpatialReference()
    cs.SetWellKnownGeogCS('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]')
    layer = shapeData.CreateLayer('Data', cs, ogr.wkbPoint) # create layer object to add attributes to

    # add all of the fields that we pulled from the .pos file in the parse function below to the shapefile we created above
    newfield = ogr.FieldDefn('Datetime', ogr.OFTString)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('lat_gcs', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('lon_gcs', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('north_utm', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('east_utm', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('height', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('Q', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('SDN', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('SDE', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('SDU', ogr.OFTReal)
    layer.CreateField(newfield)
    newfield = ogr.FieldDefn('base_dist', ogr.OFTReal)
    layer.CreateField(newfield)

    return shapeData, layer

#%%
# function to parse the pos file and get our columns of interest to turn into shapefile
def parse_rtkpos(fid, csv_out, layer, startFID):
    wgs = osr.SpatialReference() # geographic coordinate system shapefiles are originally in from lat/lon columns
    wgs.ImportFromWkt('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]')
    utm = osr.SpatialReference() # re-projection from WGS84 to UTM
    utm.ImportFromWkt(spatial_ref)
    transform = osr.CoordinateTransformation(wgs, utm) # define the transform between the two coordinate systems
    
    with open(csv_out, 'w') as csv_file:
        writer=csv.writer(csv_file, delimiter=",",lineterminator="\n",)
        writer.writerow(["datetime","latitude(deg)","longitude(deg)","UTMnorth(m)","UTMeast(m)",
                         "height(m)","Q","sdn(m)","sde(m)","sdu(m)","base_dist(m)"])
        
        f = open(fid, 'r').read()
        lines = f.strip().splitlines()
        # startFID is for writing an FID to every entry in the output shape and going through every line of .pos file
        z = startFID
        for l in lines:
            # skip the header in the .pos file
            if l.startswith('%'):
                # get out the reference station position
                if l.startswith('% ref pos'):
                    var = l.split()
                    baseLat = float(var[3][1:-1])
                    baseLong = float(var[4][:-1])
                    # convert to UTM
                    pt_wgs = ogr.Geometry(ogr.wkbPoint)
                    pt_wgs.AddPoint(baseLong, baseLat)
                    pt_wgs.Transform(transform)
                    baseLong_utm = pt_wgs.GetX()
                    baseLat_utm = pt_wgs.GetY()
                else:
                    continue
            else:
                # only pull out the columns we're interested in (values separated by comma)
                var = l.split(',')
                time = var[0]
                lat = float(var[1])
                lon = float(var[2])
                height = float(var[3])
                Q = int(var[4])
                sdn = float(var[6])
                sde = float(var[7])
                sdu = float(var[8])
                
                # calculate and add the UTM coordinates and add the distance to the base station
                pt_wgs = ogr.Geometry(ogr.wkbPoint) # give each point a geometry attribute
                pt_wgs.AddPoint(lon, lat) # pull the geometry from the lat/lon column
                pt_wgs.Transform(transform) # transform the WGS84 lat/lon to UTM
                lon_utm = pt_wgs.GetX()
                lat_utm = pt_wgs.GetY()
                # add distance to base station
                basedist = np.sqrt((lat_utm - baseLat_utm)**2 + (lon_utm - baseLong_utm)**2) 
                
                writer.writerow([time, lat, lon, lat_utm, lon_utm, height, Q, sdn, sde, sdu, basedist])
    
                # Add all the above to the shapefile
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetGeometry(pt_wgs)
    
                # index the fields
                i = feature.GetFieldIndex('Datetime')
                feature.SetField(i, time)
                i = feature.GetFieldIndex('lat_gcs')
                feature.SetField(i, lat)
                i = feature.GetFieldIndex('lon_gcs')
                feature.SetField(i, lon)
                i = feature.GetFieldIndex('north_utm')
                feature.SetField(i, lat_utm)
                i = feature.GetFieldIndex('east_utm')
                feature.SetField(i, lon_utm)
                i = feature.GetFieldIndex('height')
                feature.SetField(i, height)
                i = feature.GetFieldIndex('Q')
                feature.SetField(i, Q)
                i = feature.GetFieldIndex('SDN')
                feature.SetField(i, sdn)
                i = feature.GetFieldIndex('SDE')
                feature.SetField(i, sde)
                i = feature.GetFieldIndex('SDU')
                feature.SetField(i, sdu)
                i = feature.GetFieldIndex('base_dist')
                feature.SetField(i, basedist)
                feature.SetFID(z)
                layer.CreateFeature(feature)
                z = z + 1
        csv_file.close()
    return z

#%%
# apply correction to each rinex file individually and create a shape file with all points
for name in rinex_files:
    
    # pull out file names
    obs = name + '.obs'
    nav = name + '.nav'
    
    # download the necessary files and get the date and filenames to pass into correction function
    yr, doy, week, baseSTN, brdc, orbits = download_corr_files(out_path, base_stn, obs, nav, sevenzip)
    
    # run the correction    
    path = os.path.dirname(orbits)
    pos_out = path + '/' + obs.split('.obs')[0] + '.pos'
    
    # order of input files after configuration (-k) and output (-o) is: 
    # 1) raw rinex observations file (.obs), 2) base station observations (.YYo), 
    # 3) brdc navigation file (.YYn), 4) orbits (.sp3)
    if not os.path.exists(path + '/' + obs.split('.obs')[0] + '.pos'):
        cmd = rnx2rtkp + ' -k ' + rtkconf + ' -o ' + pos_out + \
               ' ' + path + '/' + obs + ' ' + baseSTN + ' ' + brdc + ' ' + orbits
        cmd = cmd.replace('/', '\\')
        subprocess.call(cmd, shell=False)
    
    # convert the .pos to .csv and .shp
    # create the empty shape
    shape_out = pos_out.split('.pos')[0] + '_wgs84_' + utmzone + '.shp'
    shapeData, layer = MakeShape(shape_out)
    # fill the shape from the .pos file (and output a .csv)
    csv_out = pos_out.split('.pos')[0] + '.csv'
    parse_rtkpos(pos_out, csv_out, layer, 0)
    del layer, shapeData # need to delete shape and layer from memory to finish the output

    # the projection information is usually missing using ogr for this, so we add projection file here
    if os.path.getsize(shape_out.split('.shp')[0] + '.prj') == 0:
        f = open(shape_out.split('.shp')[0] + '.prj', 'w')
        f.write(spatial_ref)
        f.close()