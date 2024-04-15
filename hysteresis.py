'''
Author: Yishuo Wang
Date: 2024-04-08 14:11:38
LastEditors: Yishuo Wang
LastEditTime: 2024-04-08 14:11:49
FilePath: /传统方法识别/hysteresis.py
Description: hysteresis

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np

# make some 2 to 1, i.e. increase the continuity
def hysteresis(marked_matrix):
    # Get the shape of the marked_matrix
    rows, cols = marked_matrix.shape

    # Iterate over each point in the new_marked_matrix
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            # If the point is marked as 2
            if marked_matrix[i, j] == 2:
                # Get the 3x3 neighborhood around the point
                neighborhood = marked_matrix[i-1:i+2, j-1:j+2]
                    
                # If there is at least one neighbor marked as 1, remark the point as 1
                if 1 in neighborhood:
                    marked_matrix[i, j] = 1
                else:
                    marked_matrix[i, j] = 0

    # some 2 are in the boundary, so they are set to 0
    marked_matrix[marked_matrix==2]=0
    return marked_matrix
