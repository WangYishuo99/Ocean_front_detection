'''
Author: Yishuo Wang
Date: 2024-03-14 14:27:00
LastEditors: Yishuo Wang
LastEditTime: 2024-03-20 14:24:23
FilePath: /传统方法识别/number_calculation.py
Description: calculate the length and width of each front

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import os 
import pickle
import numpy as np
import matplotlib.pyplot as plt

# calculate the average length and plot a histogram of the length and numbers
def calculate_front_numbers(path_fronts, save_path_number, year, type):
    files = os.listdir(path_fronts)
    month_average_num = np.zeros((12,2))

    # plot the monthly average front number
    for file in files:
        month = file.split('.')[0]
        with open(os.path.join(path_fronts, file), 'rb') as f:
            data = pickle.load(f)
            # the number of fronts in one day, add them to the corresponding month
            month_average_num[int(month)-1, 0] += len(data)
            # the number of days in one month
            month_average_num[int(month)-1, 1] += 1

    # calculate the monthly average front number
    month_average_num = month_average_num[:,0]/month_average_num[:,1]

    # plot the monthly average front number
    plt.figure(figsize=(10, 5))
    plt.plot(np.arange(1, 13), month_average_num, marker='o')
    plt.xlabel('Month')
    plt.ylabel('Average Number of Fronts')
    if type == 'SST':
        plt.title('Monthly Average Number of SST Fronts in ' + year) 
    elif type == 'SSS':
        plt.title('Monthly Average Number of SSS Fronts in ' + year)
    elif type == 'density':
        plt.title('Monthly Average Number of Density Fronts in ' + year)
    plt.savefig(save_path_number + "monthly_average_number.png", dpi=300)
    plt.show()
    plt.close()

        