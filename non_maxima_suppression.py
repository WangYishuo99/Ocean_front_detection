'''
Author: Yishuo Wang
Date: 2024-04-08 14:09:17
LastEditors: Yishuo Wang
LastEditTime: 2024-04-10 12:43:28
FilePath: /传统方法识别/non_maxima_suppression.py
Description: non maximum suppression

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np

# non maixmum suppression
def NMS(gradient_magnitude, gradient_direction, marked_matrix):
    # Get the shape of the gradient_magnitude
    rows, cols = gradient_magnitude.shape

    # Iterate over each point in the gradient_magnitude
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            # Get the gradient and direction of the point
            gradient = gradient_magnitude[i, j]

            # it is Nan values
            if np.isnan(gradient):
                continue
            # it is no front candidate
            if marked_matrix[i, j] == 0:
                continue

            direction = gradient_direction[i, j]
            
            if (direction > np.pi/8 and direction <= 3*np.pi/8) or (direction > -7*np.pi/8 and direction <= -5*np.pi/8):
                if gradient < gradient_magnitude[i+1, j-1] or gradient < gradient_magnitude[i-1, j+1]:
                    marked_matrix[i, j] = 0
            elif (direction > 3*np.pi/8 and direction <= 5*np.pi/8) or (direction > -5*np.pi/8 and direction <= -3*np.pi/8):
                if gradient < gradient_magnitude[i-1, j] or gradient < gradient_magnitude[i+1, j]:
                    marked_matrix[i, j] = 0
            elif (direction > 5*np.pi/8 and direction <= 7*np.pi/8) or (direction > -3*np.pi/8 and direction <= -np.pi/8):
                if gradient < gradient_magnitude[i-1, j-1] or gradient < gradient_magnitude[i+1, j+1]:
                    marked_matrix[i, j] = 0
            elif (direction > -np.pi/8 and direction <= np.pi/8) or (direction > 7*np.pi/8 and direction <= np.pi) or (direction > -np.pi and direction <= -7*np.pi/8):
                if gradient < gradient_magnitude[i, j-1] or gradient < gradient_magnitude[i, j+1]:
                    marked_matrix[i, j] = 0
                    
    return marked_matrix
