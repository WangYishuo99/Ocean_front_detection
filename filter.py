'''
Author: Yishuo Wang
Date: 2024-03-13 15:17:17
LastEditors: Yishuo Wang
LastEditTime: 2024-03-26 12:22:22
FilePath: /传统方法识别/filter.py
Description: the filter function to prepossess

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''

import numpy as np
from scipy.ndimage import gaussian_filter

def gaussian_filter_self(sst_wp, sigma_set):
        sst_wp_filtered = gaussian_filter(sst_wp, sigma_set)

        # Get the indices of the original NaN values
        original_nan_indices = np.isnan(sst_wp)

        # Get the indices of the new NaN values after filtering
        new_nan_indices = np.isnan(sst_wp_filtered) & ~original_nan_indices

        # Replace the new NaN values with the original values
        sst_wp_filtered[new_nan_indices] = sst_wp[new_nan_indices]

        # Replace the sst_wp variable with the smoothed_sst_wp variable
        sst_wp = sst_wp_filtered

        return sst_wp
