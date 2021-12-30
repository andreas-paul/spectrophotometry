import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# Define some global constants
E = 0.008856 # epsilon
K = 903.3


def load_data(file_path: str):
    """Data import and extraction of columns as individual variables, variable definitions
    """

    data = pd.read_csv(file_path, names=['depth_m', 'L*', 'a*', 'b*'], header=None)
    L = data['L*'] # L* value for calculations
    a = data['a*'] # a* value for calculations
    b = data['b*'] # b* value for calculations
    return L, a, b


def convert_lab_to_xyz(L, a, b):
    """Conversion from LAB color-space to XYZ color-space
    """

    fy = (L + 16) / 116
    fx = a / 500 + fy
    fz = fy - b / 200

    var_x = np.where(np.power(fx, 3) > E, np.power(fx, 3), (116 * fx - 16) / K)
    var_y = np.where(L > K * E, np.power((L + 16) / 116,3), L / K )
    var_z = np.where(np.power(fz,3) > E, np.power(fz,3), (116 * fz - 16) / K)
    
    var_x = var_x * 0.95047
    var_y = var_y * 1.000
    var_z = var_z * 1.08883

    return var_x, var_y, var_z




def convert_xyz_to_srgb(var_x, var_y, var_z):
    """Conversion from XYZ to sRGB
    """

    var_R = (var_x * 3.2404542) + (var_y * -1.5371385) + (var_z * -0.4985314)
    var_G = (var_x * -0.9692660) + (var_y * 1.8760108) + (var_z * 0.0415560)
    var_B = (var_x * 0.0556434) + (var_y * -0.2040259) + (var_z * 1.0572252)

    # sRGB Companding
    power = 1/2.4
    var_R = np.where(var_R <= 0.0031308, var_R * 12.92, 1.055 * np.power(var_R,power) - 0.055  )
    var_G = np.where(var_G <= 0.0031308, var_G * 12.92, 1.055 * np.power(var_G,power) - 0.055  )
    var_B = np.where(var_B <= 0.0031308, var_B * 12.92, 1.055 * np.power(var_B,power) - 0.055  )

    return var_R, var_G, var_B



def create_color_map(r, g, b, filename: str, dpi: int):
    """Create custom colormap from sRGB list and plot the colormap.
        
    This is the easiest way to create a visualization that looks like a 
    drilling core. Take note that the figure does not take into account any 
    gaps in a record and will produce a continuous record. I suggest to fill all 
    gaps either by white (CIE Lab: 100 0 0) or interpolate the gaps with the 
    values above and below. 
    """


    zipped = zip(r, g, b)
    sRGB_list = list(zipped)
    fig = plt.figure()
    ax = fig.subplots()
    cmap = ListedColormap(sRGB_list)
    cmap.set_over('0.25')
    cmap.set_under('0.75')
    cb2 = mpl.colorbar.ColorbarBase(ax, cmap=cmap, orientation='horizontal')
    cb2.set_label('')
    cb2.outline.set_visible(False)
    cb2.set_ticks([])
    ax.set_xticklabels('')
    plt.savefig(filename, dpi=dpi)


def convert_main(file: str, output_file_name: str):
    """ Main function to convert to sRGB and save to a file
    """
    L, a, b = load_data(file_path=file)
    var_x, var_y, var_z = convert_lab_to_xyz(L, a, b)
    var_R, var_G, var_B = convert_xyz_to_srgb(var_x, var_y, var_z)
    create_color_map(var_R, var_G, var_B, output_file_name, 600)



if __name__ == "__main__":
    convert_main('example-data.csv', 'example-output.png')

    # The output figure is saved in the same folder.
    # Further editing can be done in any vector illustration app, 
    # such as Illustrator or Affinity Designer
