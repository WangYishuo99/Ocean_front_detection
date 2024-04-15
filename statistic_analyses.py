'''
Author: Yishuo Wang
Date: 2024-03-13 16:16:14
LastEditors: Yishuo Wang
LastEditTime: 2024-04-15 15:46:14
FilePath: /传统方法识别/statistic_analyses.py
Description: 

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np
import os
# the following is written by me 
import frequency_calculation
import number_calculation
import length_calculation
import width_calculation
import plot_save

# Define the years in a loop
years = ['2013']

# let SST, SSS and density in a loop
type_list = ['SST']

origin_path = "/Users/wangyishuo/Desktop/锋面识别的结果/传统方法识别/detected_fronts_"
if __name__ == "__main__":

    for type in type_list:
        for year in years:
            path = origin_path + type + "/" + str(year) + "/"
            path_fronts = path + "fronts/"
            path_mark = path + "mark/"
            path_direction = path + "direction/"
            path_magnitude = path + "magnitude/"
            path_thinned = path + "thinned/"

            save_path_frequency = path + "frequency/"
            save_path_length = path + "length/"
            save_path_width = path + "width/"
            save_path_number = path + "number/"
            save_path_magnitude = path + "graphs/magnitude/"
            save_path_binary = path + "graphs/binary/"
            save_path_thinned = path + "graphs/thinned/"

            os.makedirs(save_path_frequency, exist_ok=True)
            os.makedirs(save_path_length, exist_ok=True)
            os.makedirs(save_path_width, exist_ok=True)
            os.makedirs(save_path_number, exist_ok=True)
            os.makedirs(save_path_magnitude, exist_ok=True)
            os.makedirs(save_path_binary, exist_ok=True)
            os.makedirs(save_path_thinned, exist_ok=True)

            lon_clipped = np.load(path + "lon.npy")
            lat_clipped = np.load(path + "lat.npy")
            lat_clipped = np.flip(lat_clipped, axis=0)
            
            # # 1.frequency calculation
            # frequency_calculation.frequency_calculation_save(path_mark, save_path_frequency)
            # print("The frequency matrix has been saved successfully!")

            # # plot the frequency matrix monthly
            # frequency_matrix = np.load(save_path_frequency + "frequency.npy")
            # frequency_calculation.plot_save_frequency(frequency_matrix, save_path_frequency, year, lon_clipped, lat_clipped, type)

            # # 2.calculate monthly averaged front numbers
            # number_calculation.calculate_front_numbers(path_fronts, save_path_number, year, type)
            
            # # then is the process of length and width
            # # 3. the fronts can occur in different days, so we have to cut the surplus fronts
            # all_fronts = length_calculation.length_unique(path_fronts)
            
            # length_calculation.length_plot(all_fronts, save_path_length, year, type)

            # 4. plot of magnitude
            plot_save.plot_magnitude(path_magnitude, save_path_magnitude, year, type, lon_clipped, lat_clipped)
    
            # 5. plot of binary images
            plot_save.plot_binary(path_mark, save_path_binary, year, type, lon_clipped, lat_clipped)

            # 6. plot of thinned images
            plot_save.plot_thinned(path_thinned, save_path_thinned, year, type, lon_clipped, lat_clipped)



