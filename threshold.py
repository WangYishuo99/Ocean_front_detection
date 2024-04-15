'''
Author: Yishuo Wang
Date: 2024-04-08 14:08:13
LastEditors: Yishuo Wang
LastEditTime: 2024-04-08 14:08:28
FilePath: /传统方法识别/threshold.py
Description: threshold calculation

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np

# calculate the thresholds and mark the gradient_magnitude
def thresholds_calculation(gradient_magnitude, upper_threshold, lower_threshold):
    # Calculate the upper and lower percentiles
    p10 = np.nanpercentile(gradient_magnitude, upper_threshold)
    p20 = np.nanpercentile(gradient_magnitude, lower_threshold)
    
    # Create a new matrix with the same shape as gradient_magnitude
    marked_matrix = np.zeros_like(gradient_magnitude)

    # Mark the top 10% as 1
    marked_matrix[gradient_magnitude > p10] = 1

    # Mark the 10% to 20% as 2
    marked_matrix[(gradient_magnitude > p20) & (gradient_magnitude <= p10)] = 2

    # Reserve the Nan values
    marked_matrix[np.isnan(gradient_magnitude)] = np.nan

    return marked_matrix, p10, p20