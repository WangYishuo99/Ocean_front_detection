'''
Author: Yishuo Wang
Date: 2024-03-19 15:57:10
LastEditors: Yishuo Wang
LastEditTime: 2024-04-15 15:45:00
FilePath: /传统方法识别/main.py
Description: the final main file to run the whole project

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
# the follwing are the functions from the other files written by me
import edge_merging
import gradient_calculation
import save_matrix
import threshold
import bayesian_decision
import non_maxima_suppression
import deep_first_search

import os
import numpy as np

# Define the thresholds
upper_threshold = 90
lower_threshold = 80

# Define the sigma for the Gaussian filter
# sigma_set = 1

# Define the scan radius for edge-merging
scan_radius = 3

# Define the years in a loop
years = ['2013']

# let SST, SSS and density in a loop
type_list = ['SST']

# dedine the wanted path
wanted_path = '/Users/wangyishuo/Desktop/锋面识别的结果/传统方法识别/detected_fronts_'
origin_path = '/Users/wangyishuo/Desktop/锋面识别的数据集/'

if __name__ == "__main__":
    for type in type_list:
        for year in years:
            # Define the save path
            save_path = wanted_path + type + "/" + str(year) + "/"
            os.makedirs(save_path, exist_ok=True)
            save_path_magnitude = save_path + "magnitude/"
            os.makedirs(save_path_magnitude, exist_ok=True)
            save_path_direction = save_path + "direction/"
            os.makedirs(save_path_direction, exist_ok=True)
            save_path_mark = save_path + "mark/"
            os.makedirs(save_path_mark, exist_ok=True)
            save_path_thinned = save_path + "thinned/"
            os.makedirs(save_path_thinned, exist_ok=True)
            save_path_merged = save_path + "merged/"
            os.makedirs(save_path_merged, exist_ok=True)
            save_path_fronts = save_path + "fronts/"
            os.makedirs(save_path_fronts, exist_ok=True)
            save_path_graph_magnitude = save_path + "graphs/magnitude/"
            os.makedirs(save_path_graph_magnitude, exist_ok=True)

            # define the input path
            input_path = origin_path + type + '/' + str(year) + '/'

            # without prepossess
            lon_clipped = np.load(save_path + "lon.npy")
            lat_clipped = np.load(save_path + "lat.npy")

            files = os.listdir(input_path)
        
            for file in files:
                if file == '.DS_Store':
                    continue
                # 1.load the data
                sst_wp = np.load(input_path + file, allow_pickle = True)
                month = file.split('.')[0]
                date = file.split('.')[1]

                # 2.Apply Gaussian filter

                # 3.Calculate the gradient in the x and y directions
                # calculate the gradient magnitude and direction
                gradient_magnitude, gradient_direction=gradient_calculation.magnitude_and_direction_gradient(sst_wp)

                # save the gradient_magnitude and gradient_direction
                gradient_calculation.save_magnitude_direction(gradient_magnitude, gradient_direction, month, date, save_path_magnitude, save_path_direction)

                # 4.calculate the two thresholds
                marked_matrix, p10, p20 = threshold.thresholds_calculation(gradient_magnitude, upper_threshold, lower_threshold)

                # 5.bayesian thresholding
                marked_matrix = bayesian_decision.bayesian(marked_matrix, p10, p20, gradient_magnitude, sst_wp)

                # Save the marked_matrix
                save_matrix.save_marked_matrix(marked_matrix, month, date, save_path_mark)

                # 6.non-maxima suppression
                # to thin the edge to 1 pixel
                thinned_matrix = non_maxima_suppression.NMS(gradient_magnitude, gradient_direction, marked_matrix)
                
                save_matrix.save_thinned_matrix(thinned_matrix, month, date, save_path_thinned)

                # # 7.edge merging
                # # merge the fronts
                # merged_matrix = edge_merging.merge(thinned_matrix, scan_radius)
                # save_matrix.save_merged_matrix(merged_matrix, month, date, save_path_merged)
                
                # # 8.deep first search
                # nested_list = deep_first_search.find_clusters(merged_matrix)

                # # Save the fronts
                # deep_first_search.save_clusters(nested_list, save_path_fronts, month, date)
