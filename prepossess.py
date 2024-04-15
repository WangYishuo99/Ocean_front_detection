'''
Author: Yishuo Wang
Date: 2024-03-13 14:18:47
LastEditors: Yishuo Wang
LastEditTime: 2024-04-15 15:35:22
FilePath: /传统方法识别/prepossess.py
Description: prepossess the nc data, extract the data of the interested region and let the extremities be nan, then convert to numpy files, calculate the density, and convert the density numpy files to nc files

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''

import os
import netCDF4
import numpy as np
import datetime
import get_ocean_density

# Define the region of interest
lon_start = 100
lon_end = 180
lat_start = 0
lat_end = 60

# input path
input_path = '/Users/wangyishuo/Desktop/锋面识别项目/爬虫/'
# output path
output_path = '/Users/wangyishuo/Desktop/锋面识别的数据集/'
# lon lat path
lon_lat_path = '/Users/wangyishuo/Desktop/锋面识别的结果/传统方法识别/detected_fronts_'

# for the density calculation
SSS_path = output_path + 'SSS/'
SST_path = output_path + 'SST/'
density_path = output_path + 'density/'

years = np.arange(2012, 2023)
type_list = ['SST', 'SSS']

# whole prepossessing process for the nc data
# extract the lon_indices and lat_indices, clip them, erase the anamolies and convert them to numpy array
def save2numpy(directory_path, lon_start, lon_end, lat_start, lat_end, save_numpy_path, type, save_lon_lat_path, year):
    if type == 'SST':

        files = os.listdir(directory_path)

        # Open the dataset
        dataset = netCDF4.Dataset(directory_path + files[0])

        # Extract the lon and lat variables
        lon = dataset.variables['lon'][:]
        lat = dataset.variables['lat'][:]
        dataset.close()

        # for west pacific, set the longitude to be between 100 and 180 and the latitude to be between 0 and 90
        # Get the indices where lon is between 100 and 180
        lon_indices = np.where((lon >= lon_start) & (lon <= lon_end))

        # Get the indices where lat is between 0 and 60
        lat_indices = np.where((lat >= lat_start) & (lat <= lat_end))

        np.save(save_lon_lat_path + 'lon.npy', np.array(lon[lon_indices]))
        np.save(save_lon_lat_path + 'lat.npy', np.array(lat[lat_indices]))
        
        for file in files:
            if file == '.DS_Store':
                continue
            dataset = netCDF4.Dataset(directory_path + file)
            analysed_sst = dataset.variables['analysed_sst'][:]
            analysed_sst_2d = analysed_sst[0, :, :]-273.15
            sst_wp = analysed_sst_2d[lat_indices[0][0]:lat_indices[0][-1]+1, lon_indices[0][0]:lon_indices[0][-1]+1]

            # let the extremities be nan
            sst_wp = np.where((sst_wp > 50) | (sst_wp < -20), np.nan, sst_wp)

            # the raw data is from north to south, so flip it
            sst_wp = np.flip(sst_wp, 0)

            dataset.close()

            month = int(file[4:6])
            date = int(file[6:8])

            np.save(save_numpy_path + str(month) + '.' + str(date) + '.npy', sst_wp)

    
    elif type == 'SSS':
        files = os.listdir(directory_path)

        data = netCDF4.Dataset(directory_path + files[0])

        lon = data.variables['longitude'][:]
        lat = data.variables['latitude'][:]
        data.close()
        
        lon_indices = np.where((lon >= lon_start) & (lon <= lon_end))
        lat_indices = np.where((lat >= lat_start) & (lat <= lat_end))
        # print(lon_indices, lat_indices)

        np.save(save_lon_lat_path + 'lon.npy', np.array(lon[lon_indices]))
        np.save(save_lon_lat_path + 'lat.npy', np.array(lat[lat_indices]))

        # the lon and lat of density follow the lon and lat of sss
        save_density_lon_lat_path = lon_lat_path + 'density/' + str(year) + '/'
        os.makedirs(save_density_lon_lat_path, exist_ok=True)
        np.save(save_density_lon_lat_path + 'lon.npy', np.array(lon[lon_indices]))
        np.save(save_density_lon_lat_path + 'lat.npy', np.array(lat[lat_indices]))
        
        for file in files:
            if file == '.DS_Store':
                continue
            dataset = netCDF4.Dataset(directory_path + file)
            so_variable = dataset['so']
            time_variable = dataset['time']

            for k in range(len(time_variable)):
                so = so_variable[k, 0, lat_indices[0][0]:lat_indices[0][-1]+1, lon_indices[0][0]:lon_indices[0][-1]+1]
                so = np.flip(so, 0)
                
                one_time = time_variable[k]
                # convert the time to a human-readable format
                time_units = time_variable.units
                time = netCDF4.num2date(one_time, time_units)
                # extract the month and date
                month = time.month
                date = time.day

                np.save(save_numpy_path + str(month) + '.' + str(date) + '.npy', np.array(so))

            dataset.close()

def density_calculation(SST_path, SSS_path, year, lon_lat_path):
    lon_SSS = np.load(lon_lat_path + 'SSS/' + str(year) +'/lon.npy')
    lat_SSS = np.load(lon_lat_path + 'SSS/' + str(year) +'/lat.npy')

    lon_SST = np.load(lon_lat_path + 'SST/' + str(year) +'/lon.npy')
    lat_SST = np.load(lon_lat_path + 'SST/' + str(year) +'/lat.npy')

    lat_SSS = np.flip(lat_SSS, 0)
    lat_SST = np.flip(lat_SST, 0)

    read_SSS_path = SSS_path + str(year) + '/'
    read_SST_path = SST_path + str(year) + '/'
    save_density_path = output_path + 'density/' + str(year) + '/'
    os.makedirs(save_density_path, exist_ok=True)

    files = os.listdir(read_SSS_path)
    for file in files:
        # the system file
        if file == '.DS_Store':
            continue
        data_SSS = np.load(read_SSS_path + file, allow_pickle=True)
        data_SST = np.load(read_SST_path + file, allow_pickle=True)
        # the density matrix should be a high resolution matrix
        data_density = np.zeros_like(data_SSS)
        for i in range(data_SSS.shape[0]):
            for j in range(data_SSS.shape[1]):
                # if it is nan, then we should continue
                if np.isnan(data_SSS[i][j]):
                    data_density[i][j] = np.nan
                    continue
                else:
                    # get the nearest point in the data_SST matrix 
                    lon = lon_SSS[j]
                    lat = lat_SSS[i]
                    # get the nearest point in the data_SST matrix
                    lon_index = np.argmin(np.abs(lon_SST - lon))
                    lat_index = np.argmin(np.abs(lat_SST - lat))
                    if np.isnan(data_SST[lat_index][lon_index]):
                        data_density[i][j] = np.nan
                        continue
                    else:
                        data_density[i][j] = get_ocean_density.get_density(data_SSS[i][j], data_SST[lat_index][lon_index], 1000)

        np.save(save_density_path + file, data_density)

def numpy2nc(density_path, lon_lat_path, year, input_path):
    read_path = density_path + str(year) + '/'
    write_path = input_path + 'density/' + str(year) + '/'
    os.makedirs(write_path, exist_ok=True)
    lon_lat_path = lon_lat_path + 'density/' + str(year) + '/'
    lat = np.load(lon_lat_path + 'lat.npy')
    lon = np.load(lon_lat_path + 'lon.npy')

    files = os.listdir(read_path)
    for file in files:
        if file == '.DS_Store':
            continue
        data = np.load(read_path + file)

        # assign the time
        month = file.split('.')[0]
        date = file.split('.')[1]

        # convert the year, month, and date to integers(seconds since 1970-01-01 00:00:00)
        year = int(year)
        month = int(month)
        date = int(date)

        # Convert year, month, and date to a datetime object
        date_obj = datetime.datetime(year, month, date)

        # Calculate the time difference between the date and the reference date (1970-01-01)
        time_diff = date_obj - datetime.datetime(1970, 1, 1)

        # Convert the time difference to seconds
        seconds_since_1970 = time_diff.total_seconds()

        # Create a NetCDF file
        write_name = write_path + str(year) + '_' + str(month) + '_' + str(date) + '.nc'
        nc_file = netCDF4.Dataset(write_name, 'w', format='NETCDF4')

        # Create dimensions for the NetCDF file
        time_dim = nc_file.createDimension('time', None)
        lat_dim = nc_file.createDimension('lat', lat.shape[0])
        lon_dim = nc_file.createDimension('lon', lon.shape[0])

        # Create variables for the NetCDF file
        time_var = nc_file.createVariable('time', np.float64, ('time',))
        lat_var = nc_file.createVariable('lat', np.float32, ('lat',))
        lon_var = nc_file.createVariable('lon', np.float32, ('lon',))
        density_var = nc_file.createVariable('density', np.float32, ('lat', 'lon'))

        # Assign values to the variables
        time_var[:] = seconds_since_1970  # Replace [0] with your actual time values
        lat_var[:] = lat  # Replace np.arange(...) with your actual latitude values
        lon_var[:] = lon  # Replace np.arange(...) with your actual longitude values
        density_var[:] = data  # Replace 'your_numpy_array.npy' with the path to your NumPy array

        # Set attributes for the variables
        time_var.units = 'seconds since 1970-01-01 00:00:00'
        lat_var.units = 'degrees_north'
        lon_var.units = 'degrees_east'
        density_var.units = 'kg/m^3'
        density_var.long_name = 'density from calculation'

        # Close the NetCDF file
        nc_file.close()
    
if __name__ == "__main__":
    # 1. save the interested region to numpy files and save the lon and lat to the folder
    for year in years:
        for type in type_list:
            read_path = input_path + type + '/' + str(year) + '/'
            save_numpy_path = output_path + type + '/' + str(year) + '/'
            os.makedirs(save_numpy_path, exist_ok=True)
            save_lon_lat_path = lon_lat_path + type + '/' + str(year) + '/'
            os.makedirs(save_lon_lat_path, exist_ok=True)

            save2numpy(read_path, lon_start, lon_end, lat_start, lat_end, save_numpy_path, type, save_lon_lat_path, year)
    
    # 2. calculate the density and save the density to numpy files
    # using the lon and lat to implement the nearest algorithm to get the density matrix
    for year in years:
        density_calculation(SST_path, SSS_path, year, lon_lat_path)
    
    # 3. convert the density numpy files to nc files
    for year in years:
        numpy2nc(density_path, lon_lat_path, year, input_path)