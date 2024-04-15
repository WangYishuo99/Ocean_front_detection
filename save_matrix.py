'''
Author: Yishuo Wang
Date: 2024-03-13 14:00:34
LastEditors: Yishuo Wang
LastEditTime: 2024-04-10 12:59:15
FilePath: /传统方法识别/save_matrix.py
Description: save

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''


import numpy as np

# save the marked_matrix
def save_marked_matrix(marked_matrix, month, date, save_path_mark):
    save_path = save_path_mark + month + "." + date + ".npy"
    np.save(save_path, marked_matrix)

# save the thinned matrix
def save_thinned_matrix(thinned_matrix, month, date, save_path_thinned):
    save_path = save_path_thinned + month + "." + date + ".npy"
    np.save(save_path, thinned_matrix)

# save the merged matrix
def save_merged_matrix(merged_matrix, month, date, save_path_merged):
    save_path = save_path_merged + month + "." + date + ".npy"
    np.save(save_path, merged_matrix)
