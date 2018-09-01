# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 12:53:51 2018
Updated 06 Aug 2018
Updated 31 Aug 2018

@author: A Paul
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib as mpl



# Data import and extraction of columns as individual variables, variable definitions

lab_core = pd.read_csv('photospectrometry.csv', names=['depth_m', 'L*', 'a*', 'b*'], header=None)
depth_m = lab_core['depth_m']
L = lab_core['L*'] # L* value for calculations
a = lab_core['a*'] # a* value for calculations
b = lab_core['b*'] # b* value for calculations

E = 0.008856 # epsilon
K = 903.3



# Conversion from LAB to XYZ

fy = (L + 16) / 116
fx = a / 500 + fy
fz = fy - b / 200

var_x = np.where(np.power(fx, 3) > E, np.power(fx, 3), (116 * fx - 16) / K)
var_y = np.where(L > K * E, np.power((L + 16) / 116,3), L / K )
var_z = np.where(np.power(fz,3) > E, np.power(fz,3), (116 * fz - 16) / K)

# Chromatic Adaptation
var_x = var_x * 0.95047
var_y = var_y * 1.000
var_z = var_z * 1.08883



# Conversion from XYZ to sRGB


var_R = (var_x * 3.2404542) + (var_y * -1.5371385) + (var_z * -0.4985314)
var_G = (var_x * -0.9692660) + (var_y * 1.8760108) + (var_z * 0.0415560)
var_B = (var_x * 0.0556434) + (var_y * -0.2040259) + (var_z * 1.0572252)

# sRGB Companding
power = 1/2.4
var_R = np.where(var_R <= 0.0031308, var_R * 12.92, 1.055 * np.power(var_R,power) - 0.055  )
var_G = np.where(var_G <= 0.0031308, var_G * 12.92, 1.055 * np.power(var_G,power) - 0.055  )
var_B = np.where(var_B <= 0.0031308, var_B * 12.92, 1.055 * np.power(var_B,power) - 0.055  )

sR = var_R * 255
sG = var_G * 255
sB = var_B * 255


# Create custom colormap from sRGB list and plot the colormap. This is the easiest way to create a visualisation that looks like a drilling core. Take note that the figure does not take into account any gaps in a record and will produce a continous record. I suggest to fill all gaps either by white (CIE Lab: 100 0 0) or interpolate the gaps with the values above and below. 

zipped = zip(var_R,var_G,var_B)
sRGB_list = list(zipped)

fig = plt.figure()
ax = fig.subplots()
cmap = ListedColormap(sRGB_list)
cmap.set_over('0.25')
cmap.set_under('0.75')
bounds = np.arange(0,cmap.N,1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cb2 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                    orientation='horizontal')
cb2.set_label('')
cb2.outline.set_visible(False)
cb2.set_ticks([])
ax.set_xticklabels('')
plt.savefig('colormap_core.png',dpi=600)