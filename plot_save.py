'''
Author: Yishuo Wang
Date: 2024-03-27 11:10:25
LastEditors: Yishuo Wang
LastEditTime: 2024-04-10 11:30:30
FilePath: /传统方法识别/plot_save.py
Description: the funcition is to add projection to the plotted files

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_magnitude(input_path, output_path, year, type, lon, lat):
    files = os.listdir(input_path)

    for file in files:
        if file == '.DS_Store':
            continue
        gradient_magnitude = np.load(input_path + file)
        gradient_magnitude = np.flip(gradient_magnitude, axis=0)
        month = file.split('.')[0]
        date = file.split('.')[1]

        # Plot and save the gradient magnitude
        fig1 = plt.figure(figsize=(10, 10))
        ax = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        plt.imshow(gradient_magnitude, cmap='jet', extent=[lon.min(), lon.max(), lat.min(), lat.max()], origin='lower', transform=ccrs.PlateCarree())

        # create the map
        ax.set_xlim(100, 180), ax.set_ylim(0, 60)
        ax.coastlines()
        ax.add_feature(cfeature.LAND, edgecolor='black')
        
        if type == 'SST':
            cbar = plt.colorbar(label='Gradient Magnitude (°C/km)', fraction=0.036, pad=0.04)
            cbar.mappable.set_clim(0,0.5)
        elif type == 'SSS':
            cbar = plt.colorbar(label='Gradient Magnitude (PSU/km)', fraction=0.036, pad=0.04)
            cbar.mappable.set_clim(0,0.5)
        elif type == 'density':
            cbar = plt.colorbar(label='Gradient Magnitude (kg/m^3/km)', fraction=0.036, pad=0.04)
            cbar.mappable.set_clim(0,0.5)
        
        ax.set_xticks([100, 120, 140, 160, 180], crs=ccrs.PlateCarree())
        ax.set_yticks([0, 15, 30, 45, 60], crs=ccrs.PlateCarree())

        # Set the x-axis and y-axis labels
        plt.xlabel('°E')
        plt.ylabel('°N')
        if type == 'SST':
            plt.title('Gradient Magnitude of SST ' + str(year) + ' ' + month + '.' + date)
        elif type == 'SSS':
            plt.title('Gradient Magnitude of SSS ' + str(year) + ' ' + month + '.' + date)
        elif type == 'density': 
            plt.title('Gradient Magnitude of Density ' + str(year) + ' ' + month + '.' + date)
        plt.savefig(output_path + month + "." + date +  ".png", dpi=300)  # Save the figure as a high-resolution PNG
        plt.close()

def plot_binary(input_path, output_path, year, type, lon, lat):
    files = os.listdir(input_path)
    for file in files:
        if file == '.DS_Store':
            continue
        gradient_magnitude = np.load(input_path + file)
        gradient_magnitude = np.flip(gradient_magnitude, axis=0)
        month = file.split('.')[0]
        date = file.split('.')[1]

        # Plot and save the gradient magnitude
        fig1 = plt.figure(figsize=(10, 10))
        ax = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        plt.imshow(gradient_magnitude, cmap='gray', extent=[lon.min(), lon.max(), lat.min(), lat.max()], origin='lower', transform=ccrs.PlateCarree())
        
        # Invert the colormap
        plt.gca().invert_yaxis()
        plt.set_cmap('gray_r')

        # create the map
        ax.set_xlim(100, 180), ax.set_ylim(0, 60)
        ax.coastlines()
        ax.add_feature(cfeature.LAND, edgecolor='black')
        
        ax.set_xticks([100, 120, 140, 160, 180], crs=ccrs.PlateCarree())
        ax.set_yticks([0, 15, 30, 45, 60], crs=ccrs.PlateCarree())

        # Set the x-axis and y-axis labels
        plt.xlabel('°E')
        plt.ylabel('°N')
        if type == 'SST':
            plt.title('Fronts of SST ' + str(year) + ' ' + month + '.' + date)
        elif type == 'SSS':
            plt.title('Fronts of SSS ' + str(year) + ' ' + month + '.' + date)
        elif type == 'density': 
            plt.title('Fronts of Density ' + str(year) + ' ' + month + '.' + date)
        plt.savefig(output_path + month + "." + date +  ".png", dpi=300)  # Save the figure as a high-resolution PNG
        plt.close()

def plot_thinned(input_path, output_path, year, type, lon, lat):
    files = os.listdir(input_path)
    for file in files:
        if file == '.DS_Store':
            continue
        gradient_magnitude = np.load(input_path + file)
        gradient_magnitude = np.flip(gradient_magnitude, axis=0)
        month = file.split('.')[0]
        date = file.split('.')[1]

        # Plot and save the gradient magnitude
        fig1 = plt.figure(figsize=(10, 10))
        ax = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        plt.imshow(gradient_magnitude, cmap='gray', extent=[lon.min(), lon.max(), lat.min(), lat.max()], origin='lower', transform=ccrs.PlateCarree())
        
        # Invert the colormap
        plt.gca().invert_yaxis()
        plt.set_cmap('gray_r')

        # create the map
        ax.set_xlim(100, 180), ax.set_ylim(0, 60)
        ax.coastlines()
        ax.add_feature(cfeature.LAND, edgecolor='black')
        
        ax.set_xticks([100, 120, 140, 160, 180], crs=ccrs.PlateCarree())
        ax.set_yticks([0, 15, 30, 45, 60], crs=ccrs.PlateCarree())

        # Set the x-axis and y-axis labels
        plt.xlabel('°E')
        plt.ylabel('°N')
        if type == 'SST':
            plt.title('Fronts of SST ' + str(year) + ' ' + month + '.' + date)
        elif type == 'SSS':
            plt.title('Fronts of SSS ' + str(year) + ' ' + month + '.' + date)
        elif type == 'density': 
            plt.title('Fronts of Density ' + str(year) + ' ' + month + '.' + date)
        plt.savefig(output_path + month + "." + date +  ".png", dpi=300)  # Save the figure as a high-resolution PNG
        plt.close()