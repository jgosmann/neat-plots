
from colormath.color_objects import LCHuvColor
import matplotlib.pyplot as plt
import numpy as np


def to_mpl_color(color):
    return tuple(channel / 255.0
                 for channel in color.convert_to('rgb').get_value_tuple())


def create_distinct_colors(
        num, hue_start=0, hue_range=360, luminance=50, chroma=75):
    hues = (hue_start + np.linspace(0, hue_range, num, endpoint=False)) % 360
    return [LCHuvColor(luminance, chroma, hue) for hue in hues]


def plot_colors(colors):
    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    axes.set_xlim(0, len(colors))
    axes.set_ylim(0, 1)
    axes.set_aspect('equal')
    axes.set_axis_off()
    for i, color in enumerate(colors):
        axes.add_patch(plt.Rectangle((i, 0), 1, 1, color=to_mpl_color(color)))
