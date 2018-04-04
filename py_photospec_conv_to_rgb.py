# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 12:53:51 2018
@author: A Paul
Python version: 3.6
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib as mpl

# Data import and extraction of columns as individual variables. The .csv file should have the following shape:
#  Column 1: L* | Column 2: a* | Column 3: b*
lab_data = pd.read_csv('photospectrometry.csv')
var_y = (lab_data.iloc[:,0] + 16) / 116
var_x = lab_data.iloc[:,1] / 500 + var_y
var_z = var_y - lab_data.iloc[:,2] / 200


"""
Conversion from LAB to XYZ (It is not possible to convert directly from LAB to sRGB)
"""
# The variables are cubed. Normally the cubed values would be checked if they are larger than 0.008856. If they are, then the respective value is cubed. If not, the following formula should be used to calculate the respective value: var = (var - 16 / 116) / 7.787
var_y = np.power(var_y,3)
var_x = np.power(var_x,3)
var_z = np.power(var_z,3)

# The calculated variables  are now multiplied with reference values based on observer angle of 10 degrees and the illuminant D65
X = var_x * 94.811
Y = var_y * 100.000
Z = var_z * 107.304

X_fr = pd.DataFrame(X, columns=['X'])
Y_fr = pd.DataFrame(Y, columns=['L*'])
Z_fr = pd.DataFrame(Z, columns=['Z'])

Y_fr.columns = ['Y']

"""
Conversion from XYZ to sRGB
"""
# Taken from EasyRGB
var_X = X_fr / 100
var_Y = Y_fr / 100
var_Z = Z_fr / 100

var_R = (var_X.iloc[:,0] * 3.2404542) + (var_Y.iloc[:,0] * -1.5371385) + (var_Z.iloc[:,0] * -0.4985314)
var_G = (var_X.iloc[:,0] * -0.9692660) + (var_Y.iloc[:,0] * 1.8760108) + (var_Z.iloc[:,0] * 0.0415560)
var_B = (var_X.iloc[:,0] * 0.0556434) + (var_Y.iloc[:,0] * -0.2040259) + (var_Z.iloc[:,0] * 1.0572252)

print(min(var_R))
print(min(var_G))
print(min(var_B))

power = 1/2.4
var_R = np.power((var_R * 1.055),power) - 0.055
var_G = np.power((var_G * 1.055), power) - 0.055
var_B = np.power((var_B * 1.055), power) - 0.055

sR = var_R * 255
sG = var_G * 255
sB = var_B * 255

zipped = zip(var_R,var_G,var_B)
sRGB_list = list(zipped)


"""
Plotting
"""
# Create custom colormap from sRGB list and plot the colormap
fig = plt.figure(figsize=[20,2], facecolor='white')
ax = fig.subplots()
cmap = ListedColormap(sRGB_list)
cmap.set_over('0.25')
cmap.set_under('0.75')
bounds = np.arange(0,cmap.N,1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cb2 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,                orientation='horizontal')
cb2.set_label('')
ax.set_xticklabels('')
plt.show()
plt.savefig('colormap_data.png',dpi=1200)
