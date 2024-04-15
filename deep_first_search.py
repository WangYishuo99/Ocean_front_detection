'''
Author: Yishuo Wang
Date: 2024-04-10 13:10:29
LastEditors: Yishuo Wang
LastEditTime: 2024-04-10 13:13:23
FilePath: /传统方法识别/deep_first_search.py
Description: deep first search to find the fronts

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import pickle

# Define the DFS function, using deep first search to find the connected components
def dfs(x, y, visited, current_list, marked_matrix, gradient_direction_angle):
    # Define the 8 directions of neighbours
    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]
    
    # Mark the current point as visited
    visited[x][y] = True
    current_list.append((x, y))
    
    # Check all 8 neighbours
    for i in range(8):
        nx, ny = x + dx[i], y + dy[i]
        
        # Check if the neighbour is within the matrix bounds and is a 1
        if 0 <= nx < len(marked_matrix) and 0 <= ny < len(marked_matrix[0]) and marked_matrix[nx][ny] == 1:
            # Check if the neighbour has not been visited and the angle difference is less than 90
            if not visited[nx][ny]:
                dfs(nx, ny, visited, current_list, marked_matrix, gradient_direction_angle)

# find the fronts and save them in a list, the list is nested, each element is a list of points of a front
def find_clusters(marked_matrix):
    # Initialize the visited matrix
    visited = [[False]*len(marked_matrix[0]) for _ in range(len(marked_matrix))]
    
    nested_list = []
    
    # Scan the marked_matrix
    for i in range(len(marked_matrix)):
        for j in range(len(marked_matrix[0])):
            # If the point is 1 and has not been visited, start a DFS from it
            if marked_matrix[i][j] == 1 and not visited[i][j]:
                current_list = []
                dfs(i, j, visited, current_list, marked_matrix)
                nested_list.append(current_list)
    
    return nested_list

# save the fronts
def save_clusters(nested_list, save_path_fronts, month, date):
    # save the nested_list
    save_path = save_path_fronts + month + "." + date + ".pkl"

    # Save the nested_list to the file
    with open(save_path, "wb") as file:
        pickle.dump(nested_list, file)
