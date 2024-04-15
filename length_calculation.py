'''
Author: Yishuo Wang
Date: 2024-03-14 15:59:52
LastEditors: Yishuo Wang
LastEditTime: 2024-03-27 11:00:47
FilePath: /传统方法识别/length_calculation.py
Description: the process to calculate the length

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt 

def length_unique(path_fronts):
    # the list to store all of the fronts
    all_fronts=[]
    files = os.listdir(path_fronts)
    for file in files:
        month = file.split('.')[0]
        with open(os.path.join(path_fronts, file), 'rb') as f:
            data = pickle.load(f)
        # unique the fronts
        all_fronts.extend(list(set(tuple(front) for front in data)))
    return all_fronts

def length_plot(all_fronts, save_path_length, year, type):
    # calculate the max length of the fronts
    max_length = max(len(front) for front in all_fronts)

    # calculate the number of fronts in each length 
    counter = np.zeros((max_length, 1))
    for front in all_fronts:
        counter[len(front)-1] += 1
    
    # the pixel is 9km, so the length should be multiplied by 9
    counter = counter.reshape(-1)
    
    # plot the histogram
    plt.figure(figsize=(10, 5))
    plt.bar(np.arange(9, 9 * max_length+1, 9), counter, log=True)
    plt.xlabel('km')
    plt.ylabel('Number of Fronts')
    if type == 'SST':
        plt.title('Length Distribution of SST Fronts in ' + year)
    elif type == 'SSS':
        plt.title('Length Distribution of SSS Fronts in ' + year)
    elif type == 'density':
        plt.title('Length Distribution of Density Fronts in ' + year)
    plt.savefig(save_path_length + "length_distribution.png", dpi=300)
    plt.close()