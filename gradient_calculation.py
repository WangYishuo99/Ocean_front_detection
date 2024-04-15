'''
Author: Yishuo Wang
Date: 2024-03-13 13:35:43
LastEditors: Yishuo Wang
LastEditTime: 2024-04-10 12:44:42
FilePath: /传统方法识别/gradient_calculation.py
Description: calculate the gradient magnitude and direction, plot and save them

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''

from scipy.ndimage import sobel
import numpy as np
import matplotlib.pyplot as plt

def magnitude_and_direction_gradient(SST):
    gradient_x = sobel(SST, axis=0)
    gradient_y = sobel(SST, axis=1)

    # Calculate the gradient magnitude
    gradient_magnitude = np.hypot(gradient_x, gradient_y)

    # change the unit
    gradient_magnitude = gradient_magnitude / 9

    # Calculate the gradient direction
    # the range is -pi to pi
    gradient_direction = np.arctan2(gradient_y, gradient_x)

    return gradient_magnitude, gradient_direction

def save_magnitude_direction(gradient_magnitude, gradient_direction, month, date, save_path_magnitude, save_path_direction):
    # save the gradient_magnitude
    save_path = save_path_magnitude + month + "." + date + ".npy"
    np.save(save_path, gradient_magnitude)
    
    # Save the gradient direction
    save_path = save_path_direction + month + "." + date + ".npy"
    np.save(save_path, gradient_direction)


