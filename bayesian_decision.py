'''
Author: Yishuo Wang
Date: 2024-04-08 14:06:01
LastEditors: Yishuo Wang
LastEditTime: 2024-04-08 15:27:13
FilePath: /传统方法识别/bofd.py
Description: a bayesian method to make some front candidate to be fronts

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np

# avoid the zero division
epsilon = 1e-6

# use Bayesian method to judge
def bayesian(marked_matrix, p10, p20, gradient_magnitude, SST):
    # 1. calculate the prior probability
    rows, cols = marked_matrix.shape
    prior_matrix = np.zeros_like(marked_matrix)
    
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if marked_matrix[i, j] == 2:
                prior_matrix[i, j] = (gradient_magnitude[i,j] - p20) / (p10 - p20)

    # 2. calculate the liklihood

    # 3. calculate local degree of edge and block deviation of every point
    LDE = np.zeros_like(marked_matrix)
    BD = np.zeros_like(marked_matrix)

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            # raw data is Nan, continue to the next point
            if SST[i, j] == np.nan:
                LDE[i, j] = np.nan
                BD[i, j] = np.nan
                continue

            # Generate a vector with the surrounding 8 elements
            neighborhood_vector = np.concatenate([
                SST[i-1, j-1:j+2],
                np.array([SST[i, j-1]]),
                np.array([SST[i, j+1]]),
                SST[i+1, j-1:j+2]
            ])

            # judge if all the 4 pairs are invalid
            counter = 4
            for k in range(0, 4):
                if np.isnan(neighborhood_vector[k]) or np.isnan(neighborhood_vector[7-k]):
                    counter -= 1
            
            # if there is no valid pairs, continue to the next point
            if counter == 0:
                LDE[i, j] = np.nan
                BD[i, j] = np.nan
                continue
            
            sum_lde = 0
            sum_bd = 0
            v_max = np.nanmax(neighborhood_vector)
            v_min = np.nanmin(neighborhood_vector)
            v_mean = np.nanmean(neighborhood_vector)

            # calculate lde and bd
            for k in range(0, 4):
                if ~ np.isnan(neighborhood_vector[k]) and  ~ np.isnan(neighborhood_vector[7-k]):
                    sum_lde += 4/7 * (v_max - v_mean - np.abs(neighborhood_vector[k] - neighborhood_vector[7-k]))/(v_max - v_min + epsilon) + 0.5
                    sum_bd += np.abs(neighborhood_vector[k] - neighborhood_vector[7-k])/(v_max - v_min + epsilon)
            
            LDE[i, j] = sum_lde/counter
            BD[i, j] = sum_bd/counter
            
    # 4. calculate the likelihood
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if marked_matrix[i, j] == 2:
                # if its LDE and BD is Nan
                if np.isnan(LDE[i, j]):
                    marked_matrix[i, j] = 0
                    continue
                
                # if the point is chosen as a front
                front_set = np.where(gradient_magnitude > gradient_magnitude[i, j])
                # calculate the nonnan values of front_set
                nonnan_front_set = np.count_nonzero(~np.isnan(LDE[front_set]))

                front_set_diff = np.abs(LDE[front_set] - LDE[i, j])
                num_diff_ = np.count_nonzero(front_set_diff <= 0.1)

                p_x1_w1 = num_diff_ / nonnan_front_set

                front_set_diff = np.abs(BD[front_set] - BD[i, j])
                num_diff_ = np.count_nonzero(front_set_diff <= 0.1)

                p_x2_w1 = num_diff_ / nonnan_front_set

                p_x_w1 = p_x1_w1 * p_x2_w1

                # if the point is not chosen as a front
                nonfront_set = np.where(gradient_magnitude < gradient_magnitude[i, j])
                # calculate the nonnan values of front_set
                nonnan_front_set = np.count_nonzero(~np.isnan(LDE[front_set]))

                front_set_diff = np.abs(LDE[front_set] - LDE[i, j])
                num_diff_ = np.count_nonzero(front_set_diff <= 0.1)

                p_x1_w2 = num_diff_ / nonnan_front_set

                front_set_diff = np.abs(BD[front_set] - BD[i, j])
                num_diff_ = np.count_nonzero(front_set_diff <= 0.1)

                p_x2_w2 = num_diff_ / nonnan_front_set

                p_x_w2 = p_x1_w2 * p_x2_w2

                # then judge them, using prior multiply likelihood, we get the posterior, then compare them
                if prior_matrix[i, j] * p_x_w1 > (1 - prior_matrix[i, j]) * p_x_w2:
                    marked_matrix[i, j] = 1
                else:
                    marked_matrix[i, j] = 0

    return marked_matrix