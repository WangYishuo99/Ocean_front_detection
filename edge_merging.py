'''
Author: Yishuo Wang
Date: 2024-03-12 16:39:59
LastEditors: Yishuo Wang
LastEditTime: 2024-04-10 14:41:37
FilePath: /传统方法识别/edge_merging.py
Description: an edge merging algorithm to merge the edges of the SST fronts, using deep first search to find the connected components

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np

def merge(thinned_matrix, scan_radius):
    # Create a copy of the thinned matrix to store the merged edges
    merged_matrix = np.copy(thinned_matrix)
    
    # Get the dimensions of the thinned matrix
    rows, cols = thinned_matrix.shape
    
    # Iterate over each pixel in the thinned matrix
    for i in range(rows):
        for j in range(cols):
            # Check if the current pixel is an edge
            if thinned_matrix[i, j] == 1:
                # Merge the connected edges using depth-first search
                dfs(thinned_matrix, merged_matrix, i, j, scan_radius)
    
    # Return the merged matrix
    return merged_matrix

def dfs(thinned_matrix, merged_matrix, i, j, scan_radius):
    # Get the dimensions of the thinned matrix
    rows, cols = thinned_matrix.shape
    
    # Check if the current pixel is within the matrix boundaries
    if i >= 0 and i < rows and j >= 0 and j < cols:
        # Check if the current pixel is an edge
        if thinned_matrix[i, j] == 1:
            # Set the current pixel to 1 in the merged matrix
            merged_matrix[i, j] = 1
            
            # Recursively merge the neighboring pixels within the scan radius
            for x in range(i - scan_radius, i + scan_radius + 1):
                for y in range(j - scan_radius, j + scan_radius + 1):
                    dfs(thinned_matrix, merged_matrix, x, y, scan_radius)