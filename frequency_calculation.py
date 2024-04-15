'''
Author: Yishuo Wang
Date: 2024-03-13 19:28:12
LastEditors: Yishuo Wang
LastEditTime: 2024-03-20 14:17:42
FilePath: /传统方法识别/frequency_calculation.py
Description: calculate the frequency matrix and save it

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''

import os
import numpy as np
import matplotlib.pyplot as plt

# calculate the frequency_matrix and save it
def frequency_calculation_save(path_mark, save_path_frequency):
    # Load the SST fronts and caluculate the frequency matrix
    files = os.listdir(path_mark)

    data = np.load(os.path.join(path_mark, files[0]))

    # analyze monthly
    frequency_matrix = np.zeros((12, data.shape[0], data.shape[1]))

    # judge if the point is always Nan, if yes, then 0, else 1
    judge_matrix = np.zeros((12, data.shape[0], data.shape[1]))

    # traverse all the files
    for file in files:
        data = np.load(os.path.join(path_mark, file))
        month = int(file.split(".")[0])
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if ~np.isnan(data[i, j]):
                    judge_matrix[month-1, i, j] = 1
                    if data[i, j] == 1:
                        frequency_matrix[month-1, i, j] += 1
    
    # traverse the judge_matrix, if the point is 0, then the frequency_matrix is Nan
    for i in range(judge_matrix.shape[0]):
        for j in range(judge_matrix.shape[1]):
            for k in range(judge_matrix.shape[2]):
                if judge_matrix[i, j, k] == 0:
                    frequency_matrix[i, j, k] = np.nan

    # save the frequency_matrix
    np.save(save_path_frequency + "frequency.npy", frequency_matrix)

# plot the frequency matrix
def plot_save_frequency(frequency_matrix, save_path_graph_frequency, year, lon_clipped, lat_clipped, type):
    # Plot and save the frequency matrix
    for i in range(frequency_matrix.shape[0]):
        month = str(i+1)
        plt.figure(figsize=(10, 10))
        
        # Set the x-axis and y-axis ticks
        x_ticks = np.arange(0, len(lon_clipped), 60)
        y_ticks = np.arange(0, len(lat_clipped), 60)

        # Apply the ticks with formatted labels
        plt.xticks(x_ticks, [round(lon_tick, 2) for lon_tick in lon_clipped[x_ticks]], rotation=45)
        plt.yticks(y_ticks, [round(lat_tick, 2) for lat_tick in lat_clipped[y_ticks]])

        # Set the x-axis and y-axis labels
        plt.xlabel('°E')
        plt.ylabel('°N')

        plt.imshow(frequency_matrix[i, :, :], cmap='jet')
        cbar = plt.colorbar(label='Frequency')
        if type == 'SST':
            plt.title('Frequency of SST Fronts ' + year + ' ' + month)
        elif type == 'SSS':
            plt.title('Frequency of SSS Fronts ' + year + ' ' + month)
        elif type == 'density':
            plt.title('Frequency of Density Fronts ' + year + ' ' + month)
        plt.savefig(save_path_graph_frequency + str(year) + "." + month +  ".png", dpi=300)  # Save the figure as a high-resolution PNG
        plt.close()
